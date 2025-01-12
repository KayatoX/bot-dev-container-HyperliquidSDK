from dotenv import load_dotenv
from pathlib import Path
import os

def debug_env_file(path):
    try:
        with open(path, "r") as f:
            print("\nContents of .env file:")
            print(f.read())
    except FileNotFoundError:
        print(f"Error: .env file not found at {path}")

def main():
    # プロジェクトルートの .env ファイルを探索
    env_path = Path(__file__).resolve().parent.parent / ".env"  # src ディレクトリの親を探索
    print("Expected .env path:", env_path)

    # ファイルの存在を確認
    if not env_path.exists():
        print("Error: .env file not found at", env_path)
        return

    # .env ファイルを読み込む
    load_dotenv(dotenv_path=env_path)

    # 環境変数を確認
    print("ENVIRONMENT:", os.getenv("ENVIRONMENT"))
    print("TESTNET_SECRET_KEY:", os.getenv("TESTNET_SECRET_KEY"))
    print("TESTNET_ACCOUNT_ADDRESS:", os.getenv("TESTNET_ACCOUNT_ADDRESS"))
    print("TESTNET_API_URL:", os.getenv("TESTNET_API_URL"))

    # デバッグ用: .env ファイルの内容を出力
    debug_env_file(env_path)

if __name__ == "__main__":
    main()
