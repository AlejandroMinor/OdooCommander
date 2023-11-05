

class Color:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    ORANGE = '\033[38;5;208m'
    PURPLE = '\033[38;5;135m'
    LIGHT_BLUE = '\033[38;5;39m'
    DARK_RED = '\033[38;5;196m'

    

class Emoji:
    OK = "✅"
    WARNING = "⚠️"
    ERROR = "❌"
    INFO = "ℹ️"
    QUESTION = "❓"
    FLOPPY_DISK = "💾"
    DEBUG = "🐞"
    NOTICE = "📝"
    CRITICAL = "💥"
    SUCCESS = "🎉"


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

    @staticmethod
    def success(message):
        print(f"{Color.MAGENTA}{Emoji.SUCCESS}  {message}{Color.RESET}")
    
    @staticmethod
    def warning(message):
        print(f"{Color.ORANGE}{Emoji.WARNING}  {message}{Color.RESET}")

    @staticmethod
    def debug(message):
        print(f"{Color.PURPLE}{Emoji.DEBUG}  {message}{Color.RESET}")

    @staticmethod
    def notice(message):
        print(f"{Color.LIGHT_BLUE}{Emoji.NOTICE}  {message}{Color.RESET}")

    @staticmethod
    def critical(message):
        print(f"{Color.DARK_RED}{Emoji.CRITICAL}  {message}{Color.RESET}")


# Uso de las funciones
# Prueba todos los colores y emojis
# ColorfulMessages.alert("Alerta")
# ColorfulMessages.error("Error")
# ColorfulMessages.ok("Ok")
# ColorfulMessages.info("Información")
# ColorfulMessages.question("Pregunta")
# ColorfulMessages.green("Verde")
# ColorfulMessages.reset("Reset")
# ColorfulMessages.list_elements(["Elemento 1", "Elemento 2", "Elemento 3"])
# ColorfulMessages.separator()
# ColorfulMessages.success("Éxito")
# ColorfulMessages.warning("Advertencia")
# ColorfulMessages.debug("Debug")
# ColorfulMessages.notice("Noticia")
# ColorfulMessages.critical("Crítico")

