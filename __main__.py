import odooCommander
from tools import CheckVersion as cv

cv.check_for_update()
odooCommander.OddoCommander().menu()