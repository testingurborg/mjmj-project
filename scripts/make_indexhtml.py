import os
import argparse
import datetime

def generate_styled_index_html(target_directory):
    """
    指定されたディレクトリ内の .txt および .html ファイルへのリンクと最終更新日を持つ、
    ファイル名でソートされた CSS スタイルの table を含む index.html ファイルを生成します。
    index.html が存在する場合は無視します。
    テーブルのカラム幅を調整します。

    Args:
        target_directory (str): index.html を作成するディレクトリのパス。
    """
    html_content = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ファイル一覧</title>
    <style>
        body {
            font-family: sans-serif;
            background-color: #f0f0f0;
            color: #333;
            margin: 20px;
        }
        h1 {
            color: #555;
            border-bottom: 2px solid #ccc;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
            background-color: #e0e0e0;
            box-shadow: 2px 2px 5px #888888;
        }
        th, td {
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #ccc;
        }
        th:nth-child(1) {
            width: 60%; /* ファイル名カラムの幅 */
        }
        th:nth-child(2) {
            width: 40%; /* 最終更新日カラムの幅 */
        }
        td:nth-child(1) {
            width: 60%;
        }
        td:nth-child(2) {
            width: 40%;
            font-size: 0.9em; /* 少し小さく表示 */
            color: #777;
        }
        th {
            background-color: #a9a9a9; /* DarkGray */
            color: #fff;
        }
        tr:hover {
            background-color: #d3d3d3; /* LightGray */
        }
        a {
            color: #337ab7;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <h1>ファイル一覧</h1>
    <table>
        <thead>
            <tr>
                <th>ファイル名</th>
                <th>最終更新日</th>
            </tr>
        </thead>
        <tbody>
"""
    file_info = []
    for filename in os.listdir(target_directory):
        if (filename.endswith(".txt") or filename.endswith(".html")) and filename != "index.html":
            filepath = os.path.join(target_directory, filename)
            modified_time_epoch = os.path.getmtime(filepath)
            modified_datetime = datetime.datetime.fromtimestamp(modified_time_epoch)
            modified_date_str = modified_datetime.strftime("%Y-%m-%d %H:%M:%S")
            file_info.append((filename, modified_date_str))

    # ファイル名でソート
    file_info.sort(key=lambda item: item[0])

    for filename, modified_date in file_info:
        relative_path = filename
        html_content += f"""
            <tr>
                <td><a href="{relative_path}">{filename}</a></td>
                <td>{modified_date}</td>
            </tr>
"""
    html_content += """
        </tbody>
    </table>
</body>
</html>
"""

    output_path = os.path.join(target_directory, "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="指定されたディレクトリにファイル一覧（ファイル名と最終更新日付き）の index.html を生成します（ファイル名でソート）。index.html は無視します。")
    parser.add_argument("target_directory", help="index.html を作成するディレクトリのパス")
    args = parser.parse_args()

    generate_styled_index_html(args.target_directory)
    print(f"ファイル名と最終更新日付きのスタイリング済み index.html ファイルが '{args.target_directory}' に生成されました（ファイル名でソート、index.html は無視）。")
	