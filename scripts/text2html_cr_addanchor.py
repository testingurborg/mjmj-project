import sys
import re
import html

def add_id_and_anchor_tags(content):
    lines = content.split('\n')
    separator_count = 0
    in_id_section = False
    in_anchor_section = False
    result = []

    for line in lines:
        if line.strip() == '<p>--------</p>':
            separator_count += 1
            if separator_count == 4:
                in_anchor_section = True
                in_id_section = True
            elif separator_count == 5:
                in_id_section = False

        if in_id_section:
            # IDタグを追加（末尾のピリオドを除去）
            line = re.sub(r'<p>([0-9a-zA-Z.]+)\.?', lambda m: f'<p><a id="{m.group(1).rstrip(".")}">{"".join(m.groups())}</a>', line)

        if in_anchor_section:
            # アンカータグを追加
            line = re.sub(r'rule ([0-9a-z.]+)', lambda m: f'<a href="#{m.group(1).rstrip(".")}">rule {m.group(1)}</a>', line)
        
        result.append(line)

    return '\n'.join(result)

def convert_text_to_html_with_tags(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f_in:
            lines = f_in.readlines()
        
        html_lines = [f"<p>{html.escape(line.strip())}</p>" for line in lines if line.strip()]
        html_content = '\n'.join(html_lines)
        
        # IDタグとアンカータグを追加
        html_content_with_tags = add_id_and_anchor_tags(html_content)
        
        full_html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>変換されたテキスト（IDタグとアンカータグ付き）</title>
</head>
<body>
{html_content_with_tags}
</body>
</html>"""
        
        with open(output_file, 'w', encoding='utf-8') as f_out:
            f_out.write(full_html)
        
        print(f"変換が完了しました。出力ファイル: {output_file}")
    except IOError as e:
        print(f"エラーが発生しました: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("使用法: python script.py 入力ファイル.txt 出力ファイル.html")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    convert_text_to_html_with_tags(input_file, output_file)
	