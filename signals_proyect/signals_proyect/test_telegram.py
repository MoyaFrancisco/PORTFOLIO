import asyncio
from telegram import Bot
import yaml

# Leer token y chat_id de config.yaml
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

TOKEN = config['telegram_token']
CHAT_ID = config['telegram_chat_id']

async def main():
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text="Mensaje de prueba desde script Python", parse_mode='HTML')
    print("Mensaje enviado")

asyncio.run(main()) 