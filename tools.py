import asyncio
import subprocess
import os
from color_messagges import ColorfulMessages as cm, Color

class SystemNotify:
    @staticmethod
    def send_notify(message, title="Alert"):
        try:
            command = ['notify-send', '-u', 'normal', title, message]
            subprocess.Popen(command)
        except FileNotFoundError:
            cm.error("El comando 'notify-send' no está disponible en este sistema.")
        
        except PermissionError as e:
            cm.error(f"Error de permisos al enviar notificación: {e}")

        except Exception as e:
            cm.error("Error al enviar notificación: ", e)

    @staticmethod
    def send_important_notify(message, title="Alert"):
        try:
            #command = ['notify-send', '-u', 'critical', title, message]
            command = ['notify-send', '-u', 'critical', '-t', '15000', title, message]
            subprocess.Popen(command)
        except FileNotFoundError:
            print("El comando 'notify-send' no está disponible en este sistema.")
        
        except PermissionError as e:
            print(f"Error de permisos al enviar notificación: {e}")

        except Exception as e:
            print("Error al enviar notificación: ", e)

# Ejemplo de uso
# SystemNotify.send_notify("Este es un mensaje de prueba", "Notificación")
# SystemNotify.send_important_notify("Esto es importante", "Notificación Crítica")

class TelegramNotify:
    @staticmethod
    async def conector(bot_token, chat_id, message):
        from telegram import Bot
        bot=Bot(token=bot_token)
        await bot.send_message(chat_id, text=message)

    @staticmethod
    def send_telegram_message(bot_token, chat_id, message):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(TelegramNotify.conector(bot_token, chat_id, message))

# Ejemplo de uso
#message = "OdooCommander terminó de ejecutar la actualización de los módulos"
#TelegramNotify.send_telegram_message(bot_token,chat_id,message)

class CheckVersion:
    def check_for_update():
        try:
            project_path = os.path.dirname(os.path.realpath(__file__))
            print(project_path)
            os.chdir(project_path)
            subprocess.run(['git', 'fetch'], check=True)

            result = subprocess.run(['git', 'status', '-sb'], capture_output=True, text=True, check=True)

            if "[" in result.stdout:
                cm.notice("Nueva versión disponible.")
            
            else:
                cm.notice("Odoo Commander está actualizado.")

        except Exception as e:
            cm.error(f"Error al intentar revisar versión: {e}")
