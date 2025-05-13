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
    
    # 出力先のMarkdownファイル名（対象ディレクトリの直下に作成）
    current_timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_markdown = os.path.join(directory, f"summarized_py_{current_timestamp}.md")
    
    # Markdownファイルに書き出し
    with open(output_markdown, "w", encoding="utf-8") as md:
        for py_file in py_files:
            # 指定ディレクトリからの相対パスをMarkdownの見出しレベル2として記述
            rel_path = os.path.relpath(py_file, directory)
            md.write(f"## {rel_path}\n\n")
            # コードブロック開始
            md.write("```python\n")
            # .pyファイルの内容を書き込む
            with open(py_file, "r", encoding="utf-8") as file:
                md.write(file.read())
            # コードブロックの終了
            md.write("\n```\n\n")
    
    print(f"{len(py_files)}個の.pyファイルの内容を '{output_markdown}' にまとめました。")

if __name__ == "__main__":
    main()
