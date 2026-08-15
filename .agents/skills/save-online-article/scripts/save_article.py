#!/usr/bin/env python3
"""保存在线文章（微信公众号 / 通用网页）到本地 Obsidian 笔记库。

用法:
    save_article.py <url> <target_dir> [--name 自定义文章名]

功能:
    1. 抓取页面（移动端 UA，兼容微信反爬校验页）
    2. 提取元信息：标题、作者/公众号、发布时间
    3. 提取正文 HTML（微信取 #js_content，通用网页用 readability）
    4. 下载正文内全部图片到 <目标目录>/<YYMM-文章名>/images/
    5. HTML 转 Markdown，图片替换为本地相对路径
    6. 生成 <YYMM-文章名>.md，开头列出原文标题/链接/作者/发布时间
    7. 打印结果摘要（含元信息、图片统计、问题提示）

注意:
    - 微信图片直链必须带完整 URL 参数（?wx_fmt=...&from=appmsg）并加 Referer，
      否则返回 400；页面本身需移动端 UA。
    - markdownify 转换表格时可能丢弃表格单元格内的内联图片，脚本会检测并报告，
      由调用方决定在 md 中补回。
    - 下载失败的图片在 md 中保留原链接，并在摘要中提示。
"""

import argparse
import datetime
import html as htmllib
import os
import re
import sys
import time

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

try:
    import readability
    HAS_READABILITY = True
except ImportError:
    HAS_READABILITY = False

# ---------- 常量 ----------
MOBILE_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
)
DESKTOP_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)
MIN_IMG_BYTES = 500
FORBIDDEN_CHARS = re.compile(r'[\\/:*?"<>|\r\n\t]+')
WS_RUN = re.compile(r'\s+')


def fetch(url: str) -> str:
    """抓取页面 HTML。先移动端 UA，失败再用桌面 UA。"""
    last_err = None
    for ua in (MOBILE_UA, DESKTOP_UA):
        try:
            r = requests.get(url, headers={"User-Agent": ua}, timeout=30)
            if r.status_code == 200 and len(r.text) > 500:
                return r.text
            last_err = f"HTTP {r.status_code}, {len(r.text)} bytes"
        except Exception as e:
            last_err = str(e)
    raise RuntimeError(f"页面抓取失败: {last_err}")


def unescape_entities(text: str) -> str:
    return htmllib.unescape(text)


def is_wechat(url: str) -> bool:
    return "mp.weixin.qq.com" in url


# ---------- 元信息提取 ----------

def find_first(pattern: str, html: str, group: int = 1) -> str | None:
    m = re.search(pattern, html)
    if m:
        return unescape_entities(m.group(group)).strip()
    return None


def extract_metadata(html: str, url: str, source: str) -> dict:
    if source == "wechat":
        title = (
            find_first(r"var msg_title = '([^']*)'", html)
            or find_first(r'<meta property="og:title" content="([^"]*)"', html)
            or find_first(r"<title>([^<]*)</title>", html)
        )
        author = (
            find_first(r"var nickname = '([^']*)'", html)
            or find_first(r'<meta property="og:article:author" content="([^"]*)"', html)
            or find_first(r"var author = '([^']*)'", html)
        )
        ts = find_first(r'var ct = "(\d+)"', html) or find_first(r"var ct = (\d+);", html)
        pub_time = (
            datetime.datetime.fromtimestamp(int(ts)).strftime("%Y-%m-%d %H:%M")
            if ts
            else None
        )
        desc = find_first(r'<meta property="og:description" content="([^"]*)"', html)
        return {"title": title, "author": author, "pub_time": pub_time, "desc": desc,
                "source": "微信公众号"}

    # 通用网页
    title = (
        find_first(r'<meta property="og:title" content="([^"]*)"', html)
        or find_first(r"<title>([^<]*)</title>", html)
    )
    author = (
        find_first(r'<meta property="og:article:author" content="([^"]*)"', html)
        or find_first(r'<meta name="author" content="([^"]*)"', html)
        or find_first(r'<meta property="author" content="([^"]*)"', html)
    )
    pub_time = None
    pub_raw = (
        find_first(r'<meta property="og:article:published_time" content="([^"]*)"', html)
        or find_first(r'<meta property="article:published_time" content="([^"]*)"', html)
        or find_first(r'<meta name="parsely-pub-date" content="([^"]*)"', html)
        or find_first(r'<time[^>]*datetime="([^"]*)"', html)
    )
    if pub_raw:
        for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
            try:
                dt = datetime.datetime.strptime(pub_raw.strip(), fmt)
                if dt.tzinfo:
                    dt = dt.replace(tzinfo=None)
                pub_time = dt.strftime("%Y-%m-%d %H:%M")
                break
            except ValueError:
                continue
    desc = find_first(r'<meta property="og:description" content="([^"]*)"', html)
    return {"title": title, "author": author, "pub_time": pub_time, "desc": desc,
            "source": "通用网页"}


# ---------- 正文提取 ----------

def extract_body_wechat(html: str) -> str | None:
    m = re.search(r'<div[^>]*id="js_content"[^>]*>(.*?)</div>\s*<script', html, re.S)
    if m:
        return m.group(1)
    m = re.search(r'<div[^>]*id="js_content"[^>]*>(.*)', html, re.S)
    return m.group(1) if m else None


def extract_body_general(html: str) -> str | None:
    if HAS_READABILITY:
        try:
            doc = readability.Document(html)
            return doc.summary(html_partial=True)
        except Exception:
            pass
    soup = BeautifulSoup(html, "html.parser")
    for sel in ["article", "#js_content", ".article-content", ".post-content", ".entry-content", ".article"]:
        el = soup.select_one(sel)
        if el and len(el.get_text(strip=True)) > 200:
            return str(el)
    return None


# ---------- 图片处理 ----------

def collect_images(body_html: str) -> list[tuple[str, str]]:
    """返回 [(本地文件名, 原始URL)]，按出现顺序，去重。"""
    seen = set()
    out = []
    for tag in re.findall(r"<img[^>]*>", body_html):
        m = re.search(r'data-src="([^"]*)"', tag) or re.search(r'src="([^"]*)"', tag)
        if not m:
            continue
        url = m.group(1).replace("&amp;", "&").strip()
        if url in seen or not url.startswith("http"):
            continue
        seen.add(url)
        out.append((url, url))
    return out


def ext_for(url: str) -> str:
    m = re.search(r"wx_fmt=([a-z]+)", url)
    if m:
        return m.group(1)
    path = url.split("?")[0].lower()
    if re.search(r"\.(jpe?g)$", path):
        return "jpg"
    if re.search(r"\.webp$", path):
        return "webp"
    if re.search(r"\.gif$", path):
        return "gif"
    if re.search(r"\.png$", path):
        return "png"
    return "png"


def download_images(imgs: list[tuple[str, str]], images_dir: str, url: str) -> list[tuple[str, str, int | str]]:
    """下载图片到 images_dir，返回 [(序号, 状态, 信息)]，并写一个映射文件供替换。"""
    os.makedirs(images_dir, exist_ok=True)
    results = []
    mapping = {}  # index -> local filename
    referer = url if "mp.weixin.qq.com" in url else None
    for i, (local_name, img_url) in enumerate(imgs):
        ext = ext_for(img_url)
        fname = f"img-{i:02d}.{ext}"
        fpath = os.path.join(images_dir, fname)
        headers = {"User-Agent": MOBILE_UA}
        if referer:
            headers["Referer"] = referer
        try:
            r = requests.get(img_url, headers=headers, timeout=60)
            if r.status_code == 200 and len(r.content) > MIN_IMG_BYTES:
                with open(fpath, "wb") as f:
                    f.write(r.content)
                mapping[i] = fname
                results.append((i, "ok", f"{fname} ({len(r.content)}B)"))
            else:
                results.append((i, "fail", f"HTTP {r.status_code} / {len(r.content)}B"))
        except Exception as e:
            results.append((i, "fail", str(e)))
        time.sleep(0.3)
    return results, mapping


def replace_img_srcs(body_html: str, mapping: dict[int, str], imgs: list[tuple[str, str]]) -> tuple[str, list[int]]:
    """把 <img> 的 data-src/src 替换为本地相对路径。返回 (新html, 被替换的序号)。"""
    replaced = []

    def repl(m):
        tag = m.group(0)
        m2 = re.search(r'data-src="([^"]*)"', tag) or re.search(r'src="([^"]*)"', tag)
        if not m2:
            return ""
        url = m2.group(1).replace("&amp;", "&").strip()
        # 找到该 url 在 imgs 中的序号
        for idx, (ln, u) in enumerate(imgs):
            if u == url and idx in mapping:
                replaced.append(idx)
                return f'<img src="images/{mapping[idx]}">'
        return tag  # 未下载成功的保留原样

    new_html = re.sub(r"<img[^>]*>", repl, body_html)
    return new_html, sorted(set(replaced))


# ---------- Markdown 转换与清理 ----------

def to_markdown(body_html: str) -> str:
    text = md(body_html, heading_style="ATX", bullets="-", strip=["script", "style"])
    text = text.replace("&amp;", "&")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def sanitize_name(title: str) -> str:
    """清理标题为安全的文件夹/文件名：去掉非法字符，—— 转为 -，压缩空白。"""
    name = title
    name = re.sub(r"\s*—+\s*", "-", name)          # —— 分隔符转 -
    name = re.sub(r"\s*-\s*", "-", name)           # 去掉 " - " 两侧空白
    name = FORBIDDEN_CHARS.sub("-", name)
    name = WS_RUN.sub("-", name)
    name = re.sub(r"-{2,}", "-", name).strip("-")
    return name or "未命名文章"


# ---------- 主流程 ----------

def build_header(meta: dict, url: str) -> str:
    lines = ["# " + (meta["title"] or "未命名文章"), ""]
    lines.append("> **原文标题**：" + (meta["title"] or "未知"))
    lines.append(">")
    lines.append(f"> **原文链接**：{url}")
    lines.append(">")
    lines.append("> **原文作者**：" + (meta["author"] or "未知"))
    lines.append(">")
    lines.append("> **发布时间**：" + (meta["pub_time"] or "未知"))
    if meta.get("desc"):
        lines.append(">")
        lines.append("> **原文简介**：" + meta["desc"])
    lines.append("")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="保存在线文章到本地 Obsidian 笔记库")
    ap.add_argument("url", help="文章链接")
    ap.add_argument("target_dir", help="目标目录（存放 YYMM-文章名 文件夹）")
    ap.add_argument("--name", help="自定义文章名（不传则用原标题）")
    args = ap.parse_args()

    source = "wechat" if is_wechat(args.url) else "general"
    print(f"[1/5] 抓取页面（来源: {source}）...")
    html_text = fetch(args.url)
    if source == "wechat" and "环境异常" in html_text:
        print("!! 微信返回环境验证页，请稍后重试或更换链接")
        return 1

    print("[2/5] 提取元信息与正文 ...")
    meta = extract_metadata(html_text, args.url, source)
    print(f"  标题: {meta['title']}")
    print(f"  作者: {meta['author'] or '未知'}")
    print(f"  发布时间: {meta['pub_time'] or '未知'}")

    body_html = extract_body_wechat(html_text) if source == "wechat" else extract_body_general(html_text)
    if not body_html or len(BeautifulSoup(body_html, "html.parser").get_text(strip=True)) < 100:
        print("!! 未提取到有效正文")
        return 1

    title = args.name or meta["title"] or "未命名文章"
    safe_name = sanitize_name(title)
    if meta["pub_time"]:
        yymm = meta["pub_time"][2:7].replace("-", "")
    else:
        yymm = datetime.date.today().strftime("%y%m")
    folder_name = f"{yymm}-{safe_name}"
    folder = os.path.join(args.target_dir, folder_name)
    images_dir = os.path.join(folder, "images")
    os.makedirs(images_dir, exist_ok=True)
    print(f"[3/5] 目标文件夹: {folder}")

    print("[4/5] 下载图片 ...")
    imgs = collect_images(body_html)
    results, mapping = download_images(imgs, images_dir, args.url)
    ok_count = sum(1 for _, st, _ in results if st == "ok")
    print(f"  图片: 共 {len(imgs)} 张，成功 {ok_count} 张")
    for i, st, info in results:
        if st == "fail":
            print(f"  !! 下载失败 img-{i:02d}: {info}（md 中将保留原链接）")

    new_body, replaced_idx = replace_img_srcs(body_html, mapping, imgs)
    # 未成功下载的图片在 md 中保留原链接 —— replace_img_srcs 已保留原 tag，
    # markdownify 会把保留的 <img src="https://..."> 输出为原链接

    print("[5/5] 转 Markdown 并写入文件 ...")
    markdown_body = to_markdown(new_body)
    header = build_header(meta, args.url)
    full_md = header + "\n" + markdown_body + "\n"

    md_path = os.path.join(folder, f"{folder_name}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(full_md)

    # 校验：md 引用的本地图片 vs 已下载文件
    refs = set(re.findall(r"!\[\]\(images/([^)]+)\)", full_md))
    downloaded = set(os.listdir(images_dir))
    missing_refs = refs - downloaded
    unreferenced = downloaded - refs

    print("\n===== 保存完成 =====")
    print(f"文件夹: {folder}")
    print(f"Markdown: {md_path}")
    print(f"图片: {ok_count}/{len(imgs)} 张已下载到 {images_dir}")
    if missing_refs:
        print(f"!! md 中引用了但未下载的图片: {sorted(missing_refs)}")
    if unreferenced:
        print(f"!! 已下载但未出现在 md 中的图片: {sorted(unreferenced)}（可能被表格转换丢弃，需人工补回）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
