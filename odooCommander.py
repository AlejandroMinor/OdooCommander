import datetime
import os
import subprocess
from click import command
import readline
import subprocess


class oddoCommander :

    def __init__ (self):

        # Configurar el historial de comandos
        histfile = os.path.join(os.environ['HOME'], '.pythonhistory')
        try:
            readline.read_history_file(histfile)
            readline.set_history_length(1000)
        except FileNotFoundError:
            pass
        import atexit
        atexit.register(readline.write_history_file, histfile)


        # Inicializar las variables self.database_name y self.module
        self.database_name = ''
        self.module = ''


        #Revisar si existe el archivo data.txt y si no existe crearlo
        if not os.path.exists('data.txt'):
            with open('data.txt', 'w') as f:
                f.write(f"db, defaul \n")
                f.write(f"module,all")
        
        # Leer el archivo data.txt y guardar el dato de la clave db en la variable self.database_name y el dato de la clave module en la variable self.module
        with open('data.txt', 'r') as f:
            for line in f:
                if line.startswith('db'):
                    self.database_name = line.split(',')[1].strip()
                if line.startswith('module'):
                    self.module = line.split(',')[1].strip()

        # Llamar al metodo menu     
        self.menu()

    def menu (self):
        # Inicializar la variable selected_option
        selected_option = ''
        # Ciclo para mostrar el menu
        while selected_option !=0 :
            
            print("""
  __         _                   
 /  )_/     / )  _  _  _   _/_ _ 
(__/(/()() (__()//)//)(//)(/(-/                                                                                     
""")
            print(f"➡ Base actual {self.database_name} | Modulo actual {self.module}")
            
            print("""\
    0. Salir
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
            """)

            selected_option = input("Acción a realizar: \n")

            if selected_option == "0":
                print("Adios")
                break
            
            if selected_option == "1" :
                
                if YesNoOption(f"Se actualizara toda la base {self.database_name} desea continuar ? "):
                    # Llamar al metodo upDateOdooModules y pasarle como parametro el nombre de la base y el modulo                    
                    upDateOdooModules(self.database_name,'all')
                    print("=============================================")
                    print("El proceso de actualizacion de todos los modulos ha finalizado ")
                    print("=============================================")


            if selected_option == "2" :
                if YesNoOption(f"Se actualizara la base {self.database_name} con {self.module} desea continuar ? "):
                    # Llamar al metodo upDateOdooModules y pasarle como parametro el nombre de la base y el modulo
                    upDateOdooModules(self.database_name,self.module)
                    print("=============================================")
                    print("El proceso de actualizacion del modulo ha finalizado ")
                    print("=============================================")
            
            if selected_option == "3":
                if YesNoOption(f"Se actualizaran las traducciones {self.database_name} desea continuar ? "):
                    # Llamar al metodo upDateOdooModules y pasarle como parametro el nombre de la base y el modulo                    
                    updateTraduction(self.database_name)
                    print("=============================================")
                    print("➡ Reiniciar sistema para que los cambios surtan efecto")
                    print("=============================================")
                
            if selected_option == "4":
                
                if YesNoOption("Se reiniciara Odoo desea continuar ? "):
                    # Reinicia odoo con el comando systemctl
                    restart_command = "sudo systemctl restart odoo"
                    print("Reiniciando Odoo...")
                    os.system(restart_command)
                    print("=============================================")
                    print("➡ Reinicio completado")
                    print("=============================================")

            if selected_option == "5":
                # Inicializar la variable menu_logs_selected_option
                menu_logs_selected_option = ''
                # Ciclo para mostrar el menu
                while menu_logs_selected_option !=0 :
                    print("""
  __         _                   
 /  )_/     / )  _  _  _   _/_ _ 
(__/(/()() (__()//)//)(//)(/(-/                                                                                     
""")
                    print(f"➡ Base actual {self.database_name} | Modulo actual {self.module}")
                    
                    print("""\
    1. Mostrar log filtrado root (Nueva ventana)
    2. Mostrar log sin filtrado (Nueva ventana)
    0. Regresar...
                    """)
                    menu_logs_selected_option = input("Acción a realizar: \n")

                    if menu_logs_selected_option == "0":
                        break

                    if menu_logs_selected_option == "1":
                        if YesNoOption("Se mostrara el log filtrado por root desea continuar ?"):
                            # Ejecuta el comando tail para mostrar el log filtrado por root en una nueva ventana por medio de grep
                            executeCommandNewTerminal("echo 'Mostrando log de root:' && sudo tail -f /var/log/odoo/odoo-server.log | grep root")
                    
                    if menu_logs_selected_option == "2":
                        if YesNoOption("Se mostrara el log sin filtrar desea continuar ?"):
                            # Ejecuta el comando tail para mostrar el log sin filtrar por grep en una nueva ventana
                            executeCommandNewTerminal("echo 'Mostrando log sin filtrar:' && sudo tail -f /var/log/odoo/odoo-server.log")

            if selected_option == "6":
                if YesNoOption("Desea cambiar la fecha de caducidad de la base de datos ?"):
                    # Obtener la fecha actual y sumarle 1 mes para actualizar la fecha de caducidad
                    expiration_date = datetime.date.today() + datetime.timedelta(days=30)
                    # Ejecutar el comando psql para actualizar la fecha de caducidad
                    os.system(f"sudo -u odoo psql -d {self.database_name} -c \"UPDATE ir_config_parameter SET value = '{expiration_date}' WHERE key='database.expiration_date';\"")
                    print(f"La fecha de caducidad de la base de datos {self.database_name} se actualizo a {expiration_date}")
                    print("➡ Reiniciar sistema para que los cambios surtan efecto")           

            if selected_option == "7":
                
                # Inicializar la variable menu_parameters_selected_option
                menu_parameters_selected_option = ''
                # Ciclo para mostrar el menu
                while menu_parameters_selected_option !=3 :
                    
                    print("""
  __         _                   
 /  )_/     / )  _  _  _   _/_ _ 
(__/(/()() (__()//)//)(//)(/(-/                                                                                     
""")
                    print(f"➡ Base actual {self.database_name} | Modulo actual {self.module}")
                    
                    print("""\
    1. Cambiar de base
    2. Cambiar modulo(s)
    0. Regresar...
                    """)

                    menu_parameters_selected_option = input("Acción a realizar: \n")

                    if menu_parameters_selected_option == "0":
                        break

                    if menu_parameters_selected_option == "1":                    
                        print("Puedes usar tab para autocompletar el nombre de la base de datos")
                        # Ejecutar el comando psql para obtener el listado de bases de datos
                        #command_psql = "psql -h localhost -U odoo -d postgres -1 -c '\l'" 
                        command_psql = "psql -U odoo -l -t | cut -d'|' -f 1 | sed -e 's/ //g' -e '/^$/d'"
                        process = subprocess.Popen(command_psql, stdout=subprocess.PIPE, shell=True)
                        # Obtener la salida del comando
                        output, error = process.communicate()
                        # Guardar cada linea en una lista y luego imprimirlo
                        lines = [""]
                        for line in output.decode("utf-8").splitlines():
                            lines.append(f"{line}")
                            print(line)

                        # Definir la lista de elementos
                        elementos = lines

                        # Configurar la autocompletación con la lista de elementos
                        def completer(text, state):
                            options = [x for x in elementos if x.startswith(text)]
                            if state < len(options):
                                return options[state]
                            else:
                                return None

                        readline.set_completer(completer)
                        readline.parse_and_bind("tab: complete")

                        # Inicializar la variable bandera
                        bandera = False
                        while bandera == False:
                            self.database_name = input("Ingresa el nombre de la base de datos: ")
                            # verificar si la base de datos ingresada existe en line y si no existe mostrar un mensaje de error
                            if self.database_name not in lines:
                                print("LA BASE DE DATOS INGRESADA NO EXISTE!!!")
                            else:   
                                bandera = True
                    if menu_parameters_selected_option == "2":
                        if YesNoOption(f"Modulo actual {self.module} desea cambiarlo? "):
                            self.module = input("Ingresa el nombre del modulo (si son varios separar signo de coma sin usar espacios ejemplo modulo1,modulo2) ")

            if selected_option == "8":
                if YesNoOption(f"Se ejecutara Odoo en modo terminal desea continuar ? "):
                    executeCommandNewTerminal(f"echo 'Iniciando odoo en modo terminal:' && sudo -u odoo odoo shell -c /etc/odoo/odoo.conf -d {self.database_name}")
                    

            if selected_option == "9":
                if YesNoOption(f"Se ejecutaran pruebas unitarias del modulo seleccionado desea continuar ? "):
                    executeCommandNewTerminal(f"echo 'Iniciando pruebas unitarias:' && sudo odoo --test-enable --stop-after-init -d '{self.database_name}' -i '{self.module}' -c /etc/odoo/odoo.conf")

            if selected_option == "10":
                    os.system("clear")

            # Guardar los datos de las variables self.database_name y self.module en el archivo data.txt
            with open('data.txt', 'w') as f:
                f.write(f"db,{self.database_name}\n")
                f.write(f"module,{self.module}")

def upDateOdooModules (db_name,module):
    #Funcion que recibe dos parametros el nombre de la base de datos y el modulo a actualizar para completar el comando y ejecutarlo
    command = f"sudo -u odoo odoo -c /etc/odoo/odoo.conf -d {db_name} -u {module} -p 8069 --no-http --load-language=es_MX --stop-after-init"
    os.system(command)

def updateTraduction (db_name):
    #Funcion que recibe un parametro el nombre de la base de datos para completar el comando y ejecutarlo
    command = f"sudo -u odoo odoo -c /etc/odoo/odoo.conf -d {db_name} -p 8069 --no-http --load-language=es_MX --stop-after-init" 
    os.system(command)

def YesNoOption (message):
    #Funcion que recibe un parametro el mensaje a mostrar y devuelve True si la respuesta es S o s y False si la respuesta es N o n
    option = input (f"{message} (S/N) \n")
    if option == "S" or option == "s":
        return True
    else:
        return False

def executeCommandNewTerminal (command):
    # Funcion que recibe un parametro el comando a ejecutar y lo ejecuta en una nueva ventana
    subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', command])

# Inicializar la clase oddoCommander
init = oddoCommander
init()
