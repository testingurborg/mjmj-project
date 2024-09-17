import difflib
import sys

def compare_files(file1_path, file2_path, output_html_path):
    # ファイルの内容を読み込む
    with open(file1_path, 'r', encoding='utf-8') as file1:
        file1_lines = file1.readlines()

    with open(file2_path, 'r', encoding='utf-8') as file2:
        file2_lines = file2.readlines()

    # ファイルの差分を取得する
    differ = difflib.HtmlDiff(wrapcolumn=60) # 英語
    # differ = difflib.HtmlDiff(wrapcolumn=40) # 日語
    # diff_content = differ.make_file(file1_lines, file2_lines)
    diff_content = differ.make_file(file1_lines, file2_lines, fromdesc=file1_path, todesc=file2_path, context=True, numlines=1)

    # HTMLファイルに差分を書き出す
    with open(output_html_path, 'w', encoding='utf-8') as output_file:
        output_file.write(diff_content)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <file1_path> <file2_path> <output_html_path>")
        sys.exit(1)

    file1_path = sys.argv[1]
    file2_path = sys.argv[2]
    output_html_path = sys.argv[3]

    compare_files(file1_path, file2_path, output_html_path)

