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

    # 各拡張子のファイルを検索
    py_files    = glob.glob(os.path.join(directory, "**", "*.py"), recursive=True)
    c_files     = glob.glob(os.path.join(directory, "**", "*.c"),  recursive=True)
    h_files     = glob.glob(os.path.join(directory, "**", "*.h"),  recursive=True)
    c_h_files   = c_files + h_files

    # どちらをまとめるか決定
    if py_files and c_h_files:
        print("以下のどちらのファイルをまとめますか？")
        print("1: Python (.py)   2: C/C++ (.c, .h)")
        choice = input("番号を入力してください (1 or 2): ").strip()
        if choice == "1":
            selected_files = py_files; prefix = "py"
        else:
            selected_files = c_h_files; prefix = "c"
    elif py_files:
        selected_files = py_files;  prefix = "py"
    elif c_h_files:
        selected_files = c_h_files; prefix = "c"
    else:
        print("対象の .py/.c/.h ファイルが見つかりません。")
        return

    # 出力ファイル名
    ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_md = os.path.join(directory, f"summarized_{prefix}_{ts}.md")

    # マークダウンに書き出し
    with open(output_md, "w", encoding="utf-8") as md:
        for fpath in selected_files:
            rel = os.path.relpath(fpath, directory)
            md.write(f"## {rel}\n\n```{ 'python' if prefix=='py' else 'c' }\n")
            with open(fpath, "r", encoding="utf-8") as rf:
                md.write(rf.read())
            md.write("\n```\n\n")

    print(f"{len(selected_files)} 個のファイルを '{output_md}' にまとめました。")

if __name__ == "__main__":
    main()
