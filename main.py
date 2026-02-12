import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import shutil  # ファイル移動（切り取り）に使用

# ==========================================
# 1. 設定項目
# ==========================================
NOW = datetime.now()
STR_YEAR_MONTH = NOW.strftime('%Y%m')
STR_YEAR_SLASH_MONTH = NOW.strftime('%Y/%m')

ENCODING = 'UTF-8'
REPLACE_TARGET = 'BURNOUT'

# 処理対象の設定を1つに統合
# move_from: 救済元（ここからファイルを「移動」させる）
# base: 最終的な保存先（ここで一括置換処理を行う）
TARGET_CONFIGS = [
    {
        "name": "DATA1",
        "move_from": f"../error_bk/",
        "base": f"/DATA/{STR_YEAR_SLASH_MONTH}"
    },
]

# ==========================================
# 2. 実行関数
# ==========================================

def move_files_only(configs):
    """error_bk から通常フォルダへファイルを移動（元の場所からは消える）"""
    print("=== [STEP 1] ファイル移動（救済処理）開始 ===")
    for item in configs:
        src_dir = Path(item["move_from"])
        dst_dir = Path(item["base"])
        
        if not src_dir.exists():
            print(f"  [Skip] 救済元なし: {src_dir}")
            continue
            
        dst_dir.mkdir(parents=True, exist_ok=True)
        
        # 移動元から全CSVを取得
        files = list(src_dir.glob("*.csv"))
        if files:
            print(f"  {item['name']}: {len(files)} 件を移動中...")
            for f in files:
                try:
                    # shutil.move は移動先に同名ファイルがあるとエラーになる場合があるため
                    # 安全のために移動先のパスを明示
                    target_path = dst_dir / f.name
                    # 移動（移動元からは削除される）
                    shutil.move(str(f), str(target_path))
                except Exception as e:
                    print(f"    【移動失敗】 {f.name}: {e}")
        else:
            print(f"  {item['name']}: 移動対象なし")

def process_csv_conversion(configs):
    """base ディレクトリにある全ファイルを対象に置換処理"""
    print("\n=== [STEP 2] 置換処理（Pandas）開始 ===")
    for item in configs:
        target_dir = Path(item["base"])
        
        if not target_dir.exists():
            continue

        files = list(target_dir.glob("*.csv"))
        if not files:
            continue

        print(f"  カテゴリ: {item['name']} ({len(files)}件)")
        for file in files:
            try:
                # 読み込み
                df = pd.read_csv(file, encoding=ENCODING, low_memory=False)
                
                # 置換（BURNOUTをNaNへ）
                df_replaced = df.replace(REPLACE_TARGET, np.nan)
                
                # 上書き保存
                df_replaced.to_csv(file, index=False, encoding=ENCODING)
                print(f"    処理完了: {file.name}")
                
            except Exception as e:
                print(f"    【エラー】 {file.name}: {e}")

# ==========================================
# 3. メイン実行
# ==========================================
if __name__ == "__main__":
    # 1. まず「切り取り」移動を行い、error_bk を空にする
    move_files_only(TARGET_CONFIGS)

    # 2. 移動後のフォルダに対して一括置換を行う
    process_csv_conversion(TARGET_CONFIGS)

    print("\n" + "="*30)
    print(" 全ての処理が正常に終了しました ")
    print("="*30)
