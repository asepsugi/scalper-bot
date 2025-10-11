import httpx

class TelegramNotifier:
    def __init__(self, bot_token, chat_id):
        if not bot_token or not chat_id or "YOUR" in bot_token:
            self.bot_token = None
            self.chat_id = None
            print("Peringatan: Token atau Chat ID Telegram tidak diatur. Notifikasi dinonaktifkan.")
        else:
            self.bot_token = bot_token
            self.chat_id = chat_id
            self.base_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

    async def send_message(self, text):
        if not self.bot_token:
            return

        payload = {
            'chat_id': self.chat_id,
            'text': text,
            'parse_mode': 'Markdown'
        }
        async with httpx.AsyncClient() as client:
            try:
                await client.post(self.base_url, json=payload)
            except Exception as e:
                print(f"Gagal mengirim notifikasi Telegram: {e}")