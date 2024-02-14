from odooCommander import OdooCommanderActions
import unittest
from unittest.mock import patch

class TestOdooCommander(unittest.TestCase):

    # def test_update_all_modules(self):
    #     oc = OdooCommanderActions()
    #     data_base_name = "Febrero_2024"
    #     oc.update_all_modules(data_base_name)
    #     assert oc.odooClient.update_all.called

    def test_update_odoo_modules(self):
        oc = OdooCommanderActions()
        data_base_name = "Febrero_2024"
        with patch('odooCommander.Utils.yes_no_option', return_value=True):
            with patch('odooCommander.os.system') as mock_system:
                with patch('odooCommander.OdooCommanderActions.update_odoo_modules') as mock_update_odoo_modules:
                    oc.update_all_modules(data_base_name)
                    mock_system.assert_called_once_with("sudo systemctl restart odoo")
                    mock_update_odoo_modules.assert_called_once_with(data_base_name, 'all')

    