

class Color:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    

class Emoji:
    OK = "✅"
    WARNING = "⚠️"
    ERROR = "❌"
    INFO = "ℹ️"
    QUESTION = "❓"
    FLOPPY_DISK = "💾"


class ColorfulMessages:
    @staticmethod
    def alert(message):
        print(f"{Color.YELLOW}{Emoji.WARNING}  {message}{Color.RESET}")

    @staticmethod
    def error(message):
        print(f"{Color.RED}{Emoji.ERROR}  {message}{Color.RESET}")

    @staticmethod
    def ok(message):
        print(f"{Color.GREEN}{Emoji.OK}  {message}{Color.RESET}")

    @staticmethod
    def info(message):
        print(f"{Color.BLUE}{Emoji.INFO}  {message}{Color.RESET}")

    @staticmethod
    def question(message):
        print(f"{Color.CYAN}{Emoji.QUESTION}  {message}{Color.RESET}")
    @staticmethod
    def green(message=""):
        print(f"{Color.GREEN}{message}")

    @staticmethod
    def reset(message=""):
        print(f"{Color.RESET}{message}")

    @staticmethod
    def list_elements(list):
        for element in list:
            print(f"{Color.BLUE}{Emoji.FLOPPY_DISK}  {element}{Color.RESET}")

    @staticmethod
    def separator():
        print(f"{Color.RESET}{'=' * 80}{Color.RESET}")


# Uso de las funciones
# ColorfulMessages.alert("Este es un mensaje de alerta.")
# ColorfulMessages.error("Esto es un error.")
# ColorfulMessages.ok("¡Operación exitosa!")
# ColorfulMessages.info("Información importante.")
# ColorfulMessages.question("¿Estás seguro de continuar?")
