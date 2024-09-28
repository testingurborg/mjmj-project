import re
import sys

def read_file(file_path):
    """ファイルを読み込む"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(file_path, content):
    """ファイルに書き込む"""
    with open(file_path, 'w', encoding='utf-8', newline='\r\n') as file:
        file.write(content)

def replace_index(match):
    """目次部分にリンクを追加する処理"""
    # 誤変換されてしまうものをスキップ
    if any(keyword in match.group(3) for keyword in [':', '。', 'マッチ・ポイント', '・ウィン・']):
        return match.group(0)

    index_id = match.group(1)
    dot = match.group(2) or ""  # ドットがある場合にはそれを保持
    return f'<p>\u3000<a class="r" href="#r{index_id}">{index_id}{dot}</a> {match.group(3)}</p>'

def replace_appendix_halfwidth(match):
    """半角の付録部分にリンクを追加する処理"""
    appendix_id = match.group(1).strip()
    return f'<h4><a id="r付録 {appendix_id}">付録 {appendix_id}</a> - {match.group(2)}</h4>'

def replace_appendix_fullwidth(match):
    """全角の付録部分にリンクを追加する処理"""
    appendix_id = match.group(1).strip()
    return f'<h4><a id="r付録{appendix_id}">付録{appendix_id}</a> ─ {match.group(2)}</h4>'

def replace_heading(match):
    """見出し部分にリンクを追加する処理"""
    heading_id = match.group(1).strip()
    dot = match.group(2) or ""  # ドットがある場合にはそれを保持
    return f'<h3><a id="r{heading_id}">{heading_id}{dot}</a> {match.group(3)}</h3>'

def process_content(content):
    """HTMLの内容を処理してリンクを挿入する"""
    # 目次部分を置換
    index_pattern = r'<p>\s*([\d]+(?:\.[\d]+)*)\s*(\.)?\s*(.+?)</p>'
    content = re.sub(index_pattern, replace_index, content)

    # 半角の付録部分を置換
    appendix_halfwidth_pattern = r'<p>\s*付録\s+([A-F])\s*-\s*(.+?)</p>'
    content = re.sub(appendix_halfwidth_pattern, lambda m: f'<p>\u3000<a class="r" href="#r付録 {m.group(1)}">付録 {m.group(1)}</a> - {m.group(2)}</p>', content)

    appendix_halfwidth_heading_pattern = r'<h4>\s*付録\s+([A-F])\s*-\s*(.+?)</h4>'
    content = re.sub(appendix_halfwidth_heading_pattern, replace_appendix_halfwidth, content)

    # 全角の付録部分を置換
    appendix_fullwidth_pattern = r'<p>\s*付録([Ａ-Ｆ])\s*─\s*(.+?)</p>'
    content = re.sub(appendix_fullwidth_pattern, lambda m: f'<p>\u3000<a class="r" href="#r付録{m.group(1)}">付録{m.group(1)}</a> ─ {m.group(2)}</p>', content)

    appendix_fullwidth_heading_pattern = r'<h4>\s*付録([Ａ-Ｆ])\s*─\s*(.+?)</h4>'
    content = re.sub(appendix_fullwidth_heading_pattern, replace_appendix_fullwidth, content)

    # 見出し部分を置換
    heading_pattern = r'<h3>\s*([\d]+(?:\.[\d]+)*)\s*(\.)?\s*(.+?)</h3>'
    content = re.sub(heading_pattern, replace_heading, content)

    return content

def add_index_links(input_html_path, output_html_path):
    """ファイル内容を全て読み込み、条件に当てはまる物にジャンプリンクを付与する"""
    content = read_file(input_html_path)
    updated_content = process_content(content)
    write_file(output_html_path, updated_content)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python add_index_links.py <input_html_path> <output_html_path>")
        sys.exit(1)

    input_html_path = sys.argv[1]
    output_html_path = sys.argv[2]

    add_index_links(input_html_path, output_html_path)