import os
import time
import json
from dotenv import dotenv_values, load_dotenv
from eth_account import Account
from eth_account.messages import encode_defunct
from hyperliquid.api import API
from pathlib import Path

# 環境変数のロード
def load_environment():
    # 明示的に .env ファイルのパスを指定
    env_path = "/workspaces/bot-dev-container-HyperliquidSDK/.env"  # 明示的なパス
    env_values = dotenv_values(env_path)
    print("Read .env values:")
    for key, value in env_values.items():
        print(f"{key}: {value}")

    environment = env_values.get("ENVIRONMENT")
    if not environment:
        raise ValueError("ENVIRONMENTが設定されていません。")

    secret_key = env_values.get(f"{environment}_SECRET_KEY")
    api_wallet_address = env_values.get(f"{environment}_ACCOUNT_ADDRESS")
    api_url = env_values.get(f"{environment}_API_URL")

    if not all([secret_key, api_wallet_address, api_url]):
        missing_vars = []
        if not secret_key:
            missing_vars.append("SECRET_KEY")
        if not api_wallet_address:
            missing_vars.append("ACCOUNT_ADDRESS")
        if not api_url:
            missing_vars.append("API_URL")
        raise ValueError(f"必要な環境変数が不足しています: {', '.join(missing_vars)}")

    return secret_key, api_wallet_address, api_url

# 注文を作成して送信する関数
def place_order(include_builder=False):
    try:
        # 環境変数を取得
        secret_key, api_wallet_address, api_url = load_environment()

        # APIインスタンス作成
        api = API(api_url)

        # Nonce生成
        nonce = int(time.time() * 1000)

        # 注文データ
        order_action = {
            "type": "order",
            "orders": [
                {
                    "a": 0,  # アセットID（例: BTCは0）
                    "b": True,  # 買い注文
                    "p": "30000",  # 価格
                    "s": "0.01",  # サイズ
                    "r": False,  # ポジション削減しない
                    "t": {"limit": {"tif": "Gtc"}}  # Good till canceled
                }
            ]
        }

        # builderFeeを追加（必要な場合のみ）
        if include_builder:
            order_action["builderFee"] = 0.01  # 数値形式

        order_data = {
            "action": order_action,
            "nonce": nonce,
            "vaultAddress": api_wallet_address
        }

        # メッセージのエンコード
        message = encode_defunct(text=json.dumps(order_data, separators=(",", ":")))

        # 署名の生成
        signed_message = Account.sign_message(message, private_key=secret_key)

        # 署名データの追加
        signature = {
            "r": hex(signed_message.r)[2:],
            "s": hex(signed_message.s)[2:],
            "v": signed_message.v
        }
        order_data["signature"] = signature

        # リクエストデータをデバッグ出力
        print("Order data being sent:", json.dumps(order_data, indent=2))

        # 注文リクエストを送信
        response = api.post("/exchange", order_data)
        print("注文が正常に実行されました:", json.dumps(response, indent=2))

    except Exception as e:
        print("エラーが発生しました:", str(e))

# 実行（builderFeeを含む/含まないを切り替えてテスト）
if __name__ == "__main__":
    place_order(include_builder=False)  # builderFeeなしでテスト
