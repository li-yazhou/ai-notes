#!/usr/bin/env python3
"""抓取 arXiv / 在线英文文章 → 提取正文结构（章节/段落/图表）+ 下载图片到本地。

用法:
  python3 extract_article.py <URL> <输出目录>

对 arXiv（abs 或 html 链接）用 LaTeXML HTML 解析（object SVG 图片、列表去重）；
对普通网页用 readability 提取正文。

输出:
  <输出目录>/extracted.md  英文正文（含章节标题/段落/图/表，图片已本地化引用 images/xxx）
  <输出目录>/images/        下载的图片
并在 stdout 打印元信息与统计，供翻译与校对。
"""
import sys
import os
import re
import json
import urllib.request
import urllib.error
import urllib.parse

from bs4 import BeautifulSoup

try:
    from readability import Document
except Exception:
    Document = None

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")

IMG_EXT = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.bmp'}


def log(*a):
    print(*a, flush=True)


def fetch(url, timeout=40):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(), r.geturl()


def download(url, dest):
    """下载单个文件；成功返回 True。"""
    try:
        data, _ = fetch(url)
        with open(dest, "wb") as f:
            f.write(data)
        return True
    except Exception as e:
        log(f"[下载失败] {url} -> {e}")
        return False


def is_arxiv(url):
    return "arxiv.org/abs/" in url or "arxiv.org/html/" in url


def arxiv_html_url(user_url):
    """把 arXiv abs/html 链接统一成 html 版本 URL（不带版本号→跟随到最新版）。"""
    m = re.search(r"arxiv\.org/(?:abs|html)/(\d{4}\.\d{4,5})(?:v\d+)?", user_url)
    if not m:
        return None
    aid = m.group(1)
    if "arxiv.org/html/" in user_url:
        # 保留用户给的版本号（若有）
        vm = re.search(r"arxiv\.org/html/(\d{4}\.\d{4,5}v\d+)", user_url)
        if vm:
            return f"https://arxiv.org/html/{vm.group(1)}"
        return f"https://arxiv.org/html/{aid}"
    return f"https://arxiv.org/html/{aid}"


# ---------------- arXiv: LaTeXML HTML 解析 ----------------

def clean_math(el):
    for m in el.find_all('math'):
        alt = m.get('alttext') or m.get_text(' ', strip=True)
        m.replace_with('$' + alt + '$' if alt else '')
    for m in el.find_all('span', class_='ltx_Math'):
        txt = m.get_text(' ', strip=True)
        m.replace_with('$' + txt + '$' if txt else '')


def inline(el):
    """元素 → 行内 markdown 文本（去掉 ref 上标、转 citation、内联代码/粗体）。"""
    if el is None:
        return ''
    clean_math(el)
    for sup in el.find_all('sup'):
        sup.decompose()
    for sub in el.find_all('cite'):
        t = sub.get_text(' ', strip=True)
        sub.replace_with('(' + t + ')')
    for a in el.find_all('a'):
        t = a.get_text(' ', strip=True)
        a.replace_with(t)
    for tt in el.find_all('tt'):
        t = tt.get_text(' ', strip=True)
        tt.replace_with('`' + t + '`')
    for em in el.find_all('em'):
        t = em.get_text(' ', strip=True)
        em.replace_with('*' + t + '*')
    for b in el.find_all('b'):
        t = b.get_text(' ', strip=True)
        b.replace_with('**' + t + '**')
    for span in el.find_all('span'):
        cls = span.get('class') or []
        if 'ltx_font_typewriter' in cls:
            t = span.get_text(' ', strip=True)
            span.replace_with('`' + t + '`')
        elif 'ltx_font_bold' in cls:
            t = span.get_text(' ', strip=True)
            span.replace_with('**' + t + '**')
    txt = el.get_text(' ', strip=True)
    return re.sub(r'\s+', ' ', txt).strip()


def parse_arxiv(html, html_url, outdir, imgs_dir):
    soup = BeautifulSoup(html, 'html.parser')
    # 移除参考文献/脚注块
    for el in soup.select('.ltx_bibliography, .ltx_bibblock, .ltx_bibitem, .ltx_biblist'):
        el.decompose()

    # object 的 data（如 "2210.03629v3/teaser-new.svg"）相对 https://arxiv.org/html/ 解析，
    # 与页面 URL 是否带版本号无关
    arxiv_html_base = "https://arxiv.org/html/"
    tokens = []
    seen_figs = set()

    for node in soup.find_all(['h2', 'h3', 'h4', 'figure', 'div', 'table']):
        cls = node.get('class') or []
        if node.name in ('h2', 'h3', 'h4') and any('ltx_title' in c for c in cls):
            txt = inline(node)
            if txt:
                lvl = {'h2': '##', 'h3': '###', 'h4': '####'}[node.name]
                tokens.append(f"\n{lvl} {txt}\n")
        elif node.name == 'figure' and 'ltx_figure' in cls:
            if id(node) in seen_figs:
                continue
            seen_figs.add(id(node))
            imgs = []
            for o in node.find_all('object', class_='ltx_graphics'):
                data = o.get('data') or ''
                name = os.path.basename(data)
                src = arxiv_html_base + data
                imgs.append((name, src))
            cap = node.find('figcaption')
            cap_txt = inline(cap)
            is_table = 'ltx_table' in (node.get('class') or [])
            # 下载图片
            for name, src in imgs:
                if not download(src, os.path.join(imgs_dir, name)):
                    imgs = [i for i in imgs if i[0] != name]
            if imgs or cap_txt:
                kind = "表" if is_table else "图"
                tokens.append(f"\n[{kind}] {cap_txt}\n")
                for name, _ in imgs:
                    tokens.append(f"![{name}](images/{name})\n")
        elif node.name == 'div' and 'ltx_para' in cls:
            if node.find_parent('figure') is not None:
                continue  # figure 内的段落（caption 已单独处理）
            txt = inline(node)
            if txt:
                tokens.append(f"\n{txt}\n")
        elif node.name == 'table' and 'ltx_tabular' in cls:
            if node.find_parent('figure') is None:
                # 独立表格（非 figure 包裹）
                rows = []
                for tr in node.find_all('tr'):
                    cells = [inline(td) for td in tr.find_all(['td', 'th'])]
                    rows.append(cells)
                tokens.append("\n[TABLE]\n")
                for r in rows:
                    tokens.append(" | ".join(r) + "\n")

    return "".join(tokens)


# ---------------- 普通网页：readability ----------------

def parse_web(html, url, outdir, imgs_dir):
    soup = BeautifulSoup(html, 'html.parser')
    # 标题/作者/日期
    title = ''
    t = soup.find('meta', attrs={'property': 'og:title'}) or \
        soup.find('meta', attrs={'name': 'twitter:title'}) or \
        soup.find('title')
    if t:
        title = (t.get('content') or t.get_text() or '').strip()

    body = ''
    if Document is not None:
        doc = Document(html)
        body_html = doc.summary(html_partial=True)
        body_soup = BeautifulSoup(body_html, 'html.parser')
        # 归一化相对 URL
        for img in body_soup.find_all('img'):
            src = img.get('src') or ''
            if src.startswith('/'):
                img['src'] = url.split('/', 3)[0] + '//' + url.split('/', 3)[2] + src
        body = str(body_soup)
    else:
        # 退而求其次：取 <article> 或 <main>，否则 <body>
        node = soup.find('article') or soup.find('main') or soup.body
        body = str(node) if node else ''

    bs = BeautifulSoup(body, 'html.parser')
    # 下载图片
    img_count = 0
    for img in bs.find_all('img'):
        src = img.get('src') or ''
        if not src:
            continue
        # 相对/根相对路径解析为绝对 URL
        src = urllib.parse.urljoin(url, src)
        m = re.search(r'\.([A-Za-z0-9]{3,4})(\?|$)', src)
        ext = m.group(1).lower() if m else 'png'
        if ext not in {e.lstrip('.') for e in IMG_EXT}:
            ext = 'png'
        name = f"img-{img_count:02d}.{ext}"
        if download(src, os.path.join(imgs_dir, name)):
            img['src'] = f"images/{name}"
            img_count += 1
        else:
            img.decompose()

    # 段落级 markdown（保留标题与代码块）
    out = []
    for el in bs.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'li', 'blockquote', 'pre', 'figure', 'img']):
        if el.name in ('h1', 'h2', 'h3', 'h4'):
            txt = el.get_text(' ', strip=True)
            if txt:
                out.append(f"\n{'#' * (int(el.name[1]) + 1)} {txt}\n")
        elif el.name == 'p':
            txt = el.get_text(' ', strip=True)
            if txt:
                out.append(f"\n{txt}\n")
        elif el.name == 'li':
            txt = el.get_text(' ', strip=True)
            if txt:
                out.append(f"- {txt}\n")
        elif el.name == 'blockquote':
            txt = el.get_text(' ', strip=True)
            if txt:
                out.append(f"\n> {txt}\n")
        elif el.name == 'pre':
            code = el.get_text('\n', strip=False)
            out.append(f"\n```\n{code}\n```\n")
        elif el.name == 'img' and el.get('src', '').startswith('images/'):
            out.append(f"\n![{el.get('alt','')}]({el['src']})\n")
    return title, "".join(out)


# ---------------- 主流程 ----------------

def main():
    if len(sys.argv) < 3:
        log("用法: python3 extract_article.py <URL> <输出目录>")
        sys.exit(2)
    url = sys.argv[1]
    outdir = sys.argv[2]
    imgs_dir = os.path.join(outdir, "images")
    os.makedirs(imgs_dir, exist_ok=True)

    if is_arxiv(url):
        html_url = arxiv_html_url(url)
        if not html_url:
            log("无法识别的 arXiv 链接")
            sys.exit(1)
        log(f"抓取 arXiv HTML: {html_url}")
        html, final_url = fetch(html_url)
        html = html.decode('utf-8', errors='replace')
        # 用重定向后的最终 URL 作为图片基准目录（无版本号链接会跳转到最新版）
        parse_arxiv(html, final_url, outdir, imgs_dir)
        # 元信息（标题/摘要）
        soup = BeautifulSoup(html, 'html.parser')
        h1 = soup.find('h1', class_='ltx_title_document')
        title = inline(h1) if h1 else ''
        content = parse_arxiv(html, html_url, outdir, imgs_dir)
        log(f"标题: {title}")
    else:
        log(f"抓取网页: {url}")
        html, _ = fetch(url)
        html = html.decode('utf-8', errors='replace')
        title, content = parse_web(html, url, outdir, imgs_dir)
        log(f"标题: {title}")

    with open(os.path.join(outdir, "extracted.md"), "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n来源: {url}\n\n{content}")

    imgs = sorted(os.listdir(imgs_dir)) if os.path.isdir(imgs_dir) else []
    log(f"图片数量: {len(imgs)} -> {imgs_dir}")
    log(f"提取正文: {outdir}/extracted.md")
    log("下一步：按段落翻译为中英对照（英文在前中文在后），默认只翻正文、不翻附录。")


if __name__ == "__main__":
    main()
