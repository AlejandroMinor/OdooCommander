from odooCommander import OdooCommanderActions
import unittest
from unittest.mock import patch

class TestOdooCommander(unittest.TestCase):

    def test_update_odoo_modules(self):
        oc = OdooCommanderActions()
        data_base_name = "Febrero_2024"
        with patch('odooCommander.Utils.yes_no_option', return_value=True):
            with patch('odooCommander.os.system') as mock_system:
                with patch('odooCommander.OdooCommanderActions.update_odoo_modules') as mock_update_odoo_modules:
                    oc.update_all_modules(data_base_name)
                    mock_system.assert_called_once_with("sudo systemctl restart odoo")
                    mock_update_odoo_modules.assert_called_once_with(data_base_name, 'all')

    # def test_update_all_modules_2(self):
    #     oc = OdooCommanderActions()
    #     data_base_name = "Febrero_2024"
    #     with patch('odooCommander.Utils.yes_no_option', return_value=False):
    #         oc.update_all_modules(data_base_name)
    #         assert oc.odooClient.update_all.called

    def test_update_module(self):
        oc = OdooCommanderActions()
        data_base_name = "Febrero_2024"
        module = "jt_investment"
        with patch('odooCommander.Utils.yes_no_option', return_value=True):
            with patch('odooCommander.OdooCommanderActions.update_odoo_modules') as mock_update_odoo_modules:
                oc.update_module(data_base_name, module)
                mock_update_odoo_modules.assert_called_once_with(data_base_name, module)
    
    # def test_update_all_modules_2(self):
    #     oc = OdooCommanderActions()
    #     data_base_name = "Febrero_2024"
    #     module = "base"
    #     with patch('odooCommander.Utils.yes_no_option', return_value=True):
    #         oc.update_module(data_base_name, module)
    #         assert oc.odooClient.update_module.called
                

    def test_update_translations(self):
        oc = OdooCommanderActions()
        data_base_name = "Febrero_2024"
        with patch('odooCommander.Utils.yes_no_option', return_value=True):
            with patch('odooCommander.OdooCommanderActions.update_translations')   as mock_update_translations:
                oc.update_translations(data_base_name)
                mock_update_translations.assert_called_once_with(data_base_name)

    # def test_update_translations_2(self):
    #     oc = OdooCommanderActions()
    #     data_base_name = "Febrero_2024"
    #     with patch('odooCommander.Utils.yes_no_option', return_value=True):
    #         oc.update_translations(data_base_name)
    #         assert oc.odooClient.update_translations.called

