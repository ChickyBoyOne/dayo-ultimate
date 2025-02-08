from telethon import TelegramClient

from telegram_secrets import API_HASH, API_ID

def main():
    client = TelegramClient("dayo-ultimate", API_ID, API_HASH)
    client.start()


if __name__ == "__main__":
    main()
