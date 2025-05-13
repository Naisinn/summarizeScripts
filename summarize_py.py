import os
import glob
import datetime

def main():
    # ユーザーに対象ディレクトリのパスを入力してもらう
    raw_input_path = input("対象ディレクトリのパスを入力してください: ").strip()
    directory = raw_input_path.strip('"').strip("'")
    
    if not os.path.isdir(directory):
        print("指定されたパスは存在しないか、ディレクトリではありません。")
        return

    # .py, .c, .h ファイルをそれぞれ再帰的に検索
    py_files = glob.glob(os.path.join(directory, "**", "*.py"), recursive=True)
    c_files  = glob.glob(os.path.join(directory, "**", "*.c"),  recursive=True)
    h_files  = glob.glob(os.path.join(directory, "**", "*.h"),  recursive=True)

    # ファイルタイプの選択 (py または c)
    if py_files and (c_files or h_files):
        file_type = input("サマリするファイルタイプを選択してください（py/c）：").strip().lower()
    elif py_files:
        file_type = "py"
    elif c_files or h_files:
        file_type = "c"
    else:
        print("対象の.py, .c, .hファイルが見つかりません。")
        return

    # 選択に応じてファイルリストとコード言語を設定
    if file_type == "py":
        files     = py_files
        ext       = "py"
        code_lang = "python"
    else:
        # .c と .h を両方まとめる
        files     = c_files + h_files
        ext       = "c_h"
        code_lang = "c"

    # 出力 Markdown ファイル名
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_md = os.path.join(directory, f"summarized_{ext}_{timestamp}.md")
    
    with open(output_md, "w", encoding="utf-8") as md:
        for path in files:
            rel = os.path.relpath(path, directory)
            md.write(f"## {rel}\n\n")
            md.write(f"```{code_lang}\n")
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                md.write(f.read())
            md.write("\n```\n\n")
    
    print(f"{len(files)}個のファイルの内容を '{output_md}' にまとめました。")

if __name__ == "__main__":
    main()
