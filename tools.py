import subprocess

class SystemTools:
    @staticmethod
    def send_notify(message, title="Alert"):
        command = ['notify-send', title, message]
        subprocess.Popen(command)
    @staticmethod
    def send_important_notify(message, title="Alert"):
        command = ['notify-send', '-u', 'critical', title, message]
        subprocess.Popen(command)

# Ejemplo de uso
# SystemTools.send_notify("Hola mundo", "Hola")
# SystemTools.send_important_notify("Hola mundo", "Hola")

