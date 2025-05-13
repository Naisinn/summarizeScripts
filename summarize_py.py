import os
import glob
import datetime

def main():
    # ユーザーに対象ディレクトリのパスを入力してもらう
    raw_input_path = input("対象ディレクトリのパスを入力してください: ").strip()
    # 前後に余計な " や ' が付いている場合はそれらを除去
    directory = raw_input_path.strip('"').strip("'")
    
    # 入力されたパスが実在するディレクトリであるかチェック
    if not os.path.isdir(directory):
        print("指定されたパスは存在しないか、ディレクトリではありません。")
        return

    # 対象ディレクトリ以下の全ての .py ファイルを取得（再帰的検索）
    py_files = glob.glob(os.path.join(directory, "**", "*.py"), recursive=True)
    # 対象ディレクトリ以下の全ての .c および .h ファイルを取得（再帰的検索）
    c_files = glob.glob(os.path.join(directory, "**", "*.c"), recursive=True)
    h_files = glob.glob(os.path.join(directory, "**", "*.h"), recursive=True)

    # ファイルタイプの選択
    if py_files and (c_files or h_files):
        file_type = input("サマリするファイルタイプを選択してください（py/c）：").strip().lower()
    elif py_files:
        file_type = "py"
    elif c_files or h_files:
        file_type = "c"
    else:
        print("対象の.py, .c, .hファイルが見つかりません。")
        return

    # 選択に応じてファイルリストと拡張子を設定
    if file_type == "py":
        files = py_files
        ext = "py"
        code_lang = "python"
    else:
        files = c_files + h_files
        ext = "c"
        code_lang = "c"

    # 出力先のMarkdownファイル名（対象ディレクトリの直下に作成）
    current_timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_markdown = os.path.join(directory, f"summarized_{ext}_{current_timestamp}.md")
    
    # Markdownファイルに書き出し
    with open(output_markdown, "w", encoding="utf-8") as md:
        for file_path in files:
            rel_path = os.path.relpath(file_path, directory)
            md.write(f"## {rel_path}\n\n")
            md.write(f"```{code_lang}\n")
            # errors="replace" を指定して、デコードエラーが出ても置換して読み込む
            with open(file_path, "r", encoding="utf-8", errors="replace") as file:
                md.write(file.read())
            md.write("\n```\n\n")
    
    print(f"{len(files)}個の.{ext}ファイルの内容を '{output_markdown}' にまとめました。")

if __name__ == "__main__":
    main()
