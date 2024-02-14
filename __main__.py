from odooCommander import OdooCommanderActions
from tools import CheckVersion as cv

if __name__ == "__main__":
    cv.check_for_update()
    commander_actions = OdooCommanderActions()
    commander_actions.menu()
