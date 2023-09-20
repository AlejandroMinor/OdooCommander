from color_messagges import ColorfulMessages as cm, Color
import datetime
import os
import readline
import subprocess
from tools import SystemNotify as sn, TelegramNotify as tn

class OddoCommander :

    def __init__ (self):

        self.database_name = ''
        self.module = ''
        self.modules_path = ''
        self.use_telegram_bot = ''
        self.bot_token = ''
        self.bot_chat_id = ''
        self.data_bases_list=[]
        self.config_file_path = "data.txt"
        self.check_config_file_exists(self.config_file_path)      
        self.get_parameters_from_file(self.config_file_path)
        
    def show_title(self):
        cm.green("""
  __         _                
 /  )_/     / )  _  _  _   _/_ _ 
(__/(/()() (__()//)//)(//)(/(-/  
""")
        cm.reset()
        print("  💻  Base actual " + Color.GREEN +
              f"{self.database_name}" + Color.RESET 
              + " | Modulo actual" + Color.GREEN + f" {self.module} 💻")
        cm.reset()

    def menu (self):
        self.menu_options = {
            "q": self.close_program,
            "0": self.stop_odoo,
            "1": self.update_all_modules,
            "2": self.update_module,
            "3": self.update_translations,
            "4": self.restart_odoo,
            "5": self.show_logs,
            "6": self.change_expiration_date,
            "7": self.set_parameters,
            "8": self.terminal_mode,
            "9": self.run_unit_tests,
            "10": self.clear_screen
        }

        while True:
            self.show_title()
            print("""\
    0. Detener servicio de Odoo
    1. Actualizar la base
    2. Actualizar módulo(s)
    3. Actualizar traducciones
    4. Reiniciar Odoo
    5. Mostrar Logs
    6. Cambiar fecha de caducidad a base de datos
    7. Definir parametros [Base de datos y Modulo(s)]
    8. Odoo en modo terminal
    9. Ejecutar Pruebas Unitarias
    10. Limpiar Pantalla
    q. Salir
            """)

            selected_option = input("Acción a realizar: ")
            if selected_option in self.menu_options:
                self.menu_options[selected_option]()
            else:
                cm.error("Opción no válida. Intente nuevamente.")
                
    def close_program(self):
        cm.info("Hasta luego... no olvides revisar las nuevas versiones del programa")
        exit()

    def update_all_modules(self):
        if self.yes_no_option(f"Se detendra el servicio de Odoo y se actualizara toda la base {self.database_name} desea continuar ? "):
            command = "sudo systemctl restart odoo"
            cm.info("Deteniendo Odoo...")
            os.system(command)
            cm.info(" ✔️  Servicio detenido. Actualizando Modulos...")
            # Llamar al metodo update_odoo_modules y pasarle como parametro el nombre de la base y el modulo                    
            res = self.update_odoo_modules(self.database_name,'all')
            message = "El proceso de actualizacion de todos los modulos ha finalizado"                    
            self._result_process(res,message)
            cm.info("El servicio de Odoo se ha iniciado")
            cm.separator()        

    def update_module(self):
        if self.yes_no_option(f"Se actualizara la base {self.database_name} con {self.module} desea continuar ? "):
            # Llamar al metodo update_odoo_modules y pasarle como parametro el nombre de la base y el modulo
            res = self.update_odoo_modules(self.database_name,self.module)
            message = f"El proceso de actualizacion del modulo {self.module} ha finalizado"
            self._result_process(res,message)        
            
    def update_translations(self):
        if self.yes_no_option(f"Se actualizaran las traducciones {self.database_name} desea continuar ? "):
            # Llamar al metodo update_odoo_modules y pasarle como parametro el nombre de la base y el modulo                    
            self.update_traduction(self.database_name)
            cm.separator()
            cm.info("Reiniciar sistema para que los cambios surtan efecto")
            cm.separator()

    def restart_odoo(self):
        if self.yes_no_option("Se reiniciara Odoo desea continuar ? "):
            # Reinicia odoo con el comando systemctl
            restart_command = "sudo systemctl restart odoo"
            cm.info("Reiniciando Odoo...")
            os.system(restart_command)
            message = "El proceso de reinicio de Odoo ha finalizado"
            time = datetime.datetime.now()
            cm.separator()
            cm.ok(message)
            sn.send_notify(f"{message} (⏳ {time.hour}:{time.minute}:{time.second})", "OdooCommander")

    def show_logs(self):
        menu_logs_selected_option = ''
        while menu_logs_selected_option !=0 :
            self.show_title()
                    
            print("""\
    1. Mostrar log filtrado root (Nueva ventana)
    2. Mostrar log sin filtrado (Nueva ventana)
    0. Regresar...
                    """)
            menu_logs_selected_option = input("Acción a realizar: \n")

            if menu_logs_selected_option == "0":
                self.menu()

            if menu_logs_selected_option == "1":
                if self.yes_no_option("Se mostrara el log filtrado por root desea continuar ?"):
                    # Ejecuta el comando tail para mostrar el log filtrado por root en una nueva ventana por medio de grep
                    self.execute_command_new_terminal("echo 'Mostrando log de root:' && sudo tail -f /var/log/odoo/odoo-server.log | grep root")
            
            if menu_logs_selected_option == "2":
                if self.yes_no_option("Se mostrara el log sin filtrar desea continuar ?"):
                    # Ejecuta el comando tail para mostrar el log sin filtrar por grep en una nueva ventana
                    self.execute_command_new_terminal("echo 'Mostrando log sin filtrar:' && sudo tail -f /var/log/odoo/odoo-server.log")

    def change_expiration_date(self):
        if self.yes_no_option("Desea cambiar la fecha de caducidad de la base de datos ?"):
            # Obtener la fecha actual y sumarle 1 mes para actualizar la fecha de caducidad
            expiration_date = datetime.date.today() + datetime.timedelta(days=30)
            # Ejecutar el comando psql para actualizar la fecha de caducidad
            os.system(f"sudo -u odoo psql -d {self.database_name} -c \"UPDATE ir_config_parameter SET value = '{expiration_date}' WHERE key='database.expiration_date';\"")
            cm.ok(f"La fecha de caducidad de la base de datos {self.database_name} se actualizo a {expiration_date}")
            cm.info("Reiniciar sistema para que los cambios surtan efecto")           

    def set_parameters(self):
        parameters_menu = {
            '0': self.menu,
            '1': self.define_database_name,
            '2': self.define_module_name,
            '3': self.define_modules_path,
            '4': self.define_telegram_notifications
        }

        menu_parameters_selected_option = ''
        while True:
            self.show_title()
        
            print("""\
    1. Cambiar de base
    2. Cambiar modulo(s)
    3. Definir ruta de modulos de Odoo
    4. Configurar notificaciones de Telegram
    0. Regresar...
                    """)

            menu_parameters_selected_option = input("Acción a realizar: \n")
            if menu_parameters_selected_option in self.menu_options:
                parameters_menu[menu_parameters_selected_option]()
            else:
                cm.error("Opción no válida. Intente nuevamente.")


    def terminal_mode(self):
        if self.yes_no_option("Se ejecutara Odoo en modo terminal desea continuar ? "):
            self.execute_command_new_terminal(f"echo 'Iniciando odoo en modo terminal:' && sudo -u odoo odoo shell -c /etc/odoo/odoo.conf -d {self.database_name}")
                    
    def run_unit_tests(self):
        if self.yes_no_option("Se ejecutaran pruebas unitarias del modulo seleccionado desea continuar ? "):
            self.execute_command_new_terminal(f"echo 'Iniciando pruebas unitarias:' && sudo odoo --test-enable --stop-after-init -d '{self.database_name}' -i '{self.module}' -c /etc/odoo/odoo.conf")

    def clear_screen(self):
        os.system("clear")

    def update_odoo_modules (self,db_name,module):
        #Funcion que recibe dos parametros el nombre de la base de datos y el modulo a actualizar para completar el comando y ejecutarlo
        command = f"sudo -u odoo odoo -c /etc/odoo/odoo.conf -d {db_name} -u {module} -p 8069 --no-http --load-language=es_MX --stop-after-init"
        res = os.system(command)
        return res

    def update_traduction (self,db_name):
        #Funcion que recibe un parametro el nombre de la base de datos para completar el comando y ejecutarlo
        command = f"sudo -u odoo odoo -c /etc/odoo/odoo.conf -d {db_name} -p 8069 --no-http --load-language=es_MX --stop-after-init" 
        os.system(command)

    def yes_no_option (self,message):
        cm.green()
        option = input (f"{message} (S/N) \n")
        option = option.lower()
        cm.reset()
        if option == "s":
            return True
        else:
            return False

    def execute_command_new_terminal (self,command):
        # Funcion que recibe un parametro el comando a ejecutar y lo ejecuta en una nueva ventana
        subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', f"{command}; bash -c 'read -p \"Presiona enter para cerrar...\"'"])

    def completer(self, list, text, state):
        options = [name for name in list if name.startswith(text)]
        if state < len(options):
            return options[state]
        else:
            return None    
    
    def get_data_bases(self):
        # Ejecutar el comando psql para obtener el listado de bases de datos
        #command_psql = "psql -h localhost -U odoo -d postgres -1 -c '\l'" 
        command_psql = "psql -U odoo -l -t | cut -d'|' -f 1 | sed -e 's/ //g' -e '/^$/d'"
        process = subprocess.Popen(command_psql, stdout=subprocess.PIPE, shell=True)
        # Obtener la salida del comando
        output, error = process.communicate()
        
        # Limpiar lista para evitar que se dupliquen los elementos
        self.data_bases_list.clear()

        # Guardar cada linea en una lista y luego imprimirlo
        for line in output.decode("utf-8").splitlines():
            self.data_bases_list.append(f"{line}")
        cm.list_elements(self.data_bases_list)
    
    def tab_autocomplete(self, list):
        readline.set_completer(lambda text, state: self.completer(list, text, state))
        readline.parse_and_bind("tab: complete")

    def save_parameters(self):
        with open(self.config_file_path, 'w') as f:
            f.write(f"db,{self.database_name}\n")
            f.write(f"module,{self.module}\n")
            f.write(f"path,{self.modules_path}\n")
            f.write(f"use_telegram_bot,{self.use_telegram_bot}\n")
            f.write(f"bot_token,{self.bot_token}\n")
            f.write(f"bot_chat_id,{self.bot_chat_id}")
        cm.info("Parametros guardados correctamente")
            
    def get_models_list(self):
        if not os.path.exists(self.modules_path):
            cm.error("La ruta no existe")
            self.define_modules_path()
        model_list = [nombre for nombre in os.listdir(self.modules_path) if os.path.isdir(os.path.join(self.modules_path, nombre))]
        return model_list
    
    def verify_if_exist_in_list(self, list, message):
        bandera = False
        while bandera == False:
            element = input(message)
            if element not in list:
                cm.error("Error el nombre ingresado no existe en la lista!!!")
            else:   
                bandera = True
                return element
            
    def define_database_name(self):
        self.get_data_bases()
        self.tab_autocomplete(self.data_bases_list)
        self.database_name = self.verify_if_exist_in_list(self.data_bases_list,"Ingresa el nombre de la base de datos (Puedes usar tab para autocompletar el nombre de la base de datos):")
        cm.info(f"Nuevo valor de la base de datos: {self.database_name}")
        self.save_parameters()

    def define_module_name(self):
        module_list = self.get_models_list()
        self.tab_autocomplete(module_list)
        self.module = self.verify_if_exist_in_list(module_list,"Ingresa el nombre del modulo (Puedes usar tab para autocompletar el nombre del modulo) ")
        cm.info(f"Nuevo valor del modulo: {self.module}")
        self.save_parameters()

    def define_modules_path(self):
        while not os.path.exists(self.modules_path):
            self.modules_path = input("Ingresa la ruta de los modulos de Odoo (Ejemplo /home/minor/Custom_Odoo): ")
            if not os.path.exists(self.modules_path):
                cm.error("La ruta no existe")
        cm.info(f"Nuevo valor de la ruta de los modulos: {self.modules_path}")
        self.save_parameters()

    def define_telegram_notifications(self):
        while True:
            cm.info(f"Valor de la opcion de notificaciones por Telegram: {self.use_telegram_bot}")
            cm.info(f"Valor del token del bot: {self.bot_token}")
            cm.info(f"Valor del chat id: {self.bot_chat_id}")
            bot_token = self.bot_token
            bot_chat_id = self.bot_chat_id
            if self.yes_no_option("Deseas configurar las notificaciones por Telegram?"):
                use_telegram_bot = self.yes_no_option("Deseas recibir notificaciones por Telegram?")
                if use_telegram_bot:
                    change_token = self.yes_no_option("Deseas cambiar el token del bot?")
                    if change_token:
                        bot_token = input("Ingresa el token del bot: ")
                    change_chat_id = self.yes_no_option("Deseas cambiar el chat id?")
                    if change_chat_id:
                        bot_chat_id = input("Ingresa el chat id: ")
                    cm.info(f"Valor de la opcion de notificaciones por Telegram: {use_telegram_bot}")
                    cm.info(f"Valor del token del bot: {bot_token}")
                    cm.info(f"Valor del chat id: {bot_chat_id}")
                    answer = self.yes_no_option("Deseas guardar los cambios?")
                    if answer:
                        self.use_telegram_bot = "True"
                        self.bot_token = bot_token
                        self.bot_chat_id = bot_chat_id
                        self.save_parameters()
                        self.is_bot_active("Se activaron las notificaciones por Telegram")
                    break
                else:
                    cm.info(f"Valor de la opcion de notificaciones por Telegram: {use_telegram_bot}")
                    self.use_telegram_bot = use_telegram_bot
                    self.save_parameters()
                    break
            else:
                break    

    def create_data_file(self):
        cm.info("Este archivo contiene los datos de configuracion de la aplicacion, estos pueden ser modificados en cualquier momento")
    
        print("\n Esta sera la base de datos con la cual estaras trabajando \n")
        self.define_database_name()
        
        print("\n Esta ruta es donde tienes guardados tus modulos de Odoo customizados")
        self.define_modules_path()

        cm.list_elements(self.get_models_list())
        print("\n Ingresa el nombre del modulo con el que estaras trabajando (Si aun no tienes uno asignado, selecciona cualquiera. Esta configuracion se puede modificar en cualquier momento)")
        
        self.define_module_name()

        cm.ok("Archivo de configuración se ha creado correctamente\n")
        cm.info(f"Nuevos valores de configuracion:\nBase de datos: {self.database_name}\nModulo: {self.module}\nRuta de los modulos: {self.modules_path}")

    def get_parameters_from_file(self,config_file):

        try:
            data = {
                'db': None,
                'module': None,
                'path': None,
                'use_telegram_bot': None,
                'bot_token': None,
                'bot_chat_id': None
            }
            
            with open(config_file, 'r') as f:
                for line in f:
                    key, value = line.strip().split(',')
                    data[key] = value
            
            self.database_name = data['db']
            self.module = data['module']
            self.modules_path = data['path']
            self.use_telegram_bot = data['use_telegram_bot']
            self.bot_token = data['bot_token']
            self.bot_chat_id = data['bot_chat_id']

        except Exception as e:
            cm.error(f"Error al leer el archivo de configuracion: {e}")
            cm.alert("Se creara un nuevo archivo de configuracion")
            self.create_data_file()

    def is_bot_active(self,message):
        if self.use_telegram_bot == 'True':
            if self.verify_telegram_library():
                try:
                    cm.ok("Enviando notificacion a Telegram...")
                    tn.send_telegram_message(self.bot_token, self.bot_chat_id, message)
                except Exception as e:
                    cm.error(f"Error al enviar notificacion a Telegram: {e}")
                    cm.alert("Configura correctamente el token y el chat id del bot")
                    if self.yes_no_option("Deseas configurar el token y el chat id del bot?"):
                        self.define_telegram_notifications()
                    else: 
                        self.use_telegram_bot = "False"
                        cm.alert("Se desactivaron las notificaciones por Telegram")
        else:
            cm.info("Notificaciones por Telegram desactivadas")

    def check_config_file_exists(self,file):
        if not os.path.exists(file):
            cm.error(f"El archivo {file} no existe se creara uno nuevo ")
            self.create_data_file()

    def _result_process(self,result,message):
        time = datetime.datetime.now()
        cm.separator()
        if result == 0:
            message = f"{message} correctamente"
            cm.ok(message)
            sn.send_notify(f"{message} (⏳ {time.hour}:{time.minute}:{time.second})", "OdooCommander")
        else:
            message = f"{message} con errores"
            cm.error(message)
            sn.send_important_notify(f"{message} (⏳ {time.hour}:{time.minute}:{time.second})", "OdooCommander")
        cm.separator()

        self.is_bot_active(message)

    def verify_telegram_library(self):
        try:
            import telegram
            return True
        except Exception as e:
            cm.error(f"Error al importar la libreria python-telegram-bot: {e}")
            cm.alert("Instala la libreria para poder usar esta funcionalidad")
            return self.install_telegram_library('python-telegram-bot')

    def install_telegram_library(self,library):
        if self.yes_no_option(f"Desea instalar la libreria {library} ? "):
            cm.info(f"Instalando libreria {library}")
            os.system(f"sudo pip install {library}")
            return True
        else:
            cm.alert("No se instalo la libreria")
            self.use_telegram_bot = "False"
            cm.alert("Se desactivaron las notificaciones por Telegram")
            return False
            
    def stop_odoo(self):
        if self.yes_no_option("Se detendra Odoo desea continuar ? "):
            command = "sudo systemctl stop odoo"
            cm.info("Deteniendo servicio de Odoo...")
            os.system(command)
            message = "El servicio de Odoo se ha detenido"
            time = datetime.datetime.now()
            cm.separator()
            cm.ok(message)
            sn.send_notify(f"{message} (⏳ {time.hour}:{time.minute}:{time.second})", "OdooCommander")
            
