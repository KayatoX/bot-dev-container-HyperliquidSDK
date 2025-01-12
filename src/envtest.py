from dotenv import dotenv_values

def debug_env_file():
    env_path = "/workspaces/bot-dev-container-HyperliquidSDK/.env"
    env_values = dotenv_values(env_path)
    print("Read .env values:")
    for key, value in env_values.items():
        print(f"{key}: {value}")

debug_env_file()
