import os
import glob

def main():
    # ユーザーに対象ディレクトリのパスを入力してもらう
    raw_input_path = input("対象ディレクトリのパスを入力してください: ").strip()
    # 前後に余計な " や ' が付いていた場合、それらを取り除く
    directory = raw_input_path.strip('"').strip("'")
    
    # 入力されたパスの存在を確認
    if not os.path.isdir(directory):
        print("指定されたパスは存在しないか、ディレクトリではありません。")
        return

    # 指定ディレクトリ直下の全ての .py ファイルを取得
    py_files = glob.glob(os.path.join(directory, "*.py"))
    
    # 出力先のMarkdownファイル名
    output_markdown = "summarized_py.md"
    
    # Markdownファイルに書き出し
    with open(output_markdown, "w", encoding="utf-8") as md:
        for py_file in py_files:
            # ファイル名をMarkdownの見出しとして記述
            md.write(f"## {os.path.basename(py_file)}\n\n")
            md.write("```python\n")
            # 各.pyファイルの内容を読み込んでMarkdownに書き込む
            with open(py_file, "r", encoding="utf-8") as file:
                md.write(file.read())
            md.write("\n```\n\n")
    
    print(f"{len(py_files)}個の.pyファイルの内容を '{output_markdown}' にまとめました。")

if __name__ == "__main__":
    main()
