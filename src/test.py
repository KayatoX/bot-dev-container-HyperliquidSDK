import os
import time
import json
from dotenv import load_dotenv
from eth_account import Account
from eth_account.messages import encode_defunct
from hyperliquid.api import API

# 環境変数のロード
def load_environment():
    load_dotenv()
    environment = os.getenv("ENVIRONMENT")
    if not environment:
        raise ValueError("ENVIRONMENTが設定されていません。")

    secret_key = os.getenv(f"{environment}_SECRET_KEY")
    api_wallet_address = os.getenv(f"{environment}_ACCOUNT_ADDRESS")
    api_url = os.getenv(f"{environment}_API_URL")

    if not all([secret_key, api_wallet_address, api_url]):
        raise ValueError("必要な環境変数が不足しています。")

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
    place_order(include_builder=False)  # builderFeeなしでテス