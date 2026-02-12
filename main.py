import pandas as pd
import numpy as np
from pathlib import Path

# ==========================================
# 1. パスの設定 (相対パス)
# ==========================================
# このプログラムがある場所を基準にする
BASE_DIR = Path(__file__).parent

SOURCE_NORMAL = BASE_DIR / "../data"      # 通常チェック元
SOURCE_ERROR  = BASE_DIR / "../dataerror"   # エラー救済元
DEST_DIR      = BASE_DIR / "../data"        # 出力先（共通）

# 設定
ENCODING = 'UTF-8'
REPLACE_TARGET = 'BURNOUT'

# ==========================================
# 2. 処理メイン関数
# ==========================================
def verify_process(src_dir, dest_dir, label):
    """
    src_dir 内のCSVを読み込み、BURNOUTを置換して dest_dir へ保存する
    """
    print(f"\n--- {label} 開始 ---")
    
    # 出力先フォルダがなければ作成
    dest_dir.mkdir(parents=True, exist_ok=True)

    # ソースフォルダ内のCSVを取得
    files = list(src_dir.glob("*.csv"))

    if not files:
        print(f"対象ファイルがありませんでした: {src_dir}")
        return

    for file_path in files:
        print(f"処理中: {file_path.name}")
        try:
            # 1. 読み込み
            df = pd.read_csv(file_path, encoding=ENCODING, low_memory=False)

            # 2. 置換 (BURNOUTがなければ何もしない)
            df_replaced = df.replace(REPLACE_TARGET, np.nan)

            # 3. 保存 (../data フォルダへ)
            save_path = dest_dir / file_path.name
            df_replaced.to_csv(save_path, index=False, encoding=ENCODING)
            
            print(f"成功: {save_path}")

            # 4. 「移動」させる場合（エラーフォルダから消す場合）は以下を有効化
            # if label == "エラー救済処理":
            #     file_path.unlink() 
            #     print(f"移動完了(元ファイルを削除しました): {file_path.name}")

        except Exception as e:
            print(f"【失敗】 {file_path.name}: {e}")

# ==========================================
# 3. 実行
# ==========================================
if __name__ == "__main__":
    # 実行1: 通常フォルダ(datae) -> data
    verify_process(SOURCE_NORMAL, DEST_DIR, "通常チェック処理")

    # 実行2: エラーフォルダ(dataerror) -> data
    verify_process(SOURCE_ERROR, DEST_DIR, "エラー救済処理")

    print("\n検証が完了しました。../data フォルダを確認してください。")
