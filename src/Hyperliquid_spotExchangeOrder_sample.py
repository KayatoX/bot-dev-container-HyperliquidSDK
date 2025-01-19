import os
from dotenv import load_dotenv
from eth_account import Account
from hyperliquid.exchange import Exchange
from hyperliquid.info import Info
from hyperliquid.utils.constants import TESTNET_API_URL, MAINNET_API_URL

# 環境変数を読み込み
load_dotenv(override=True)

ENVIRONMENT = os.getenv("ENVIRONMENT", "TESTNET").upper()
SECRET_KEY = os.getenv(f"{ENVIRONMENT}_SECRET_KEY")
ACCOUNT_ADDRESS = os.getenv(f"{ENVIRONMENT}_ACCOUNT_ADDRESS")
API_URL = os.getenv(f"{ENVIRONMENT}_API_URL")

def main():
    if not SECRET_KEY or not ACCOUNT_ADDRESS or not API_URL:
        raise ValueError(".envファイルに必要な環境変数が不足しています。")

    # アカウントと取引所の初期化
    account = Account.from_key(SECRET_KEY)
    info = Info(base_url=API_URL, skip_ws=True)
    exchange = Exchange(account, base_url=API_URL, account_address=ACCOUNT_ADDRESS)

    # ユーザーのスポット残高を表示
    spot_user_state = info.spot_user_state(ACCOUNT_ADDRESS)
    balances = spot_user_state.get("balances", [])
    if balances:
        print("スポット残高:")
        for balance in balances:
            print(balance)
    else:
        print("利用可能なスポット残高がありません。")
        print("DEBUG: spot_user_state:", spot_user_state)
        print("DEBUG: ACCOUNT_ADDRESS:", ACCOUNT_ADDRESS)

    # シンプルなスポット注文を出す (例: SCHIZO/USDC)
    COIN_PAIR = "SCHIZO/USDC"
    IS_BUY = True  # Trueは買い注文、Falseは売り注文
    SIZE = 0.2  # 売買数量
    LIMIT_PRICE = 60  # 単価
    ORDER_TYPE = {"limit": {"tif": "Gtc"}}  # Gtc (Good Till Canceled) の注文

    print("注文を送信中...")
    order_result = exchange.order(COIN_PAIR, IS_BUY, SIZE, LIMIT_PRICE, ORDER_TYPE)
    print("注文結果:", order_result)

    # 注文ステータスを確認
    if order_result["status"] == "ok":
        status = order_result["response"]["data"]["statuses"][0]
        if "resting" in status:
            oid = status["resting"]["oid"]
            order_status = info.query_order_by_oid(ACCOUNT_ADDRESS, oid)
            print("注文ステータス:", order_status)

if __name__ == "__main__":
    main()



