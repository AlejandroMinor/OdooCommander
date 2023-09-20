from telegram import Bot
import asyncio
import subprocess

class SystemNotify:
    @staticmethod
    def send_notify(message, title="Alert"):
        command = ['notify-send', '-u', 'normal', title, message]
        subprocess.Popen(command)
    @staticmethod
    def send_important_notify(message, title="Alert"):
        command = ['notify-send', '-u', 'critical', title, message]
        subprocess.Popen(command)

# Ejemplo de uso
# SystemTools.send_notify("Hola mundo", "Hola")
# SystemTools.send_important_notify("Hola mundo", "Hola")

class TelegramNotify:
    @staticmethod
    async def conector(bot_token, chat_id, message):
        bot=Bot(token=bot_token)
        await bot.send_message(chat_id, text=message)

    @staticmethod
    def send_telegram_message(bot_token, chat_id, message):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(TelegramNotify.conector(bot_token, chat_id, message))

# Ejemplo de uso
#message = "OdooCommander terminó de ejecutar la actualización de los módulos"
#TelegramNotify.send_telegram_message(bot_token,chat_id,message)
