import os
import subprocess
from click import command
import readline


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
        while selected_option !=4 :
            
            print("""
   ___     _             ___                              _         
  / _ \ __| |___  ___   / __|___ _ __  _ __  __ _ _ _  __| |___ _ _ 
 | (_) / _` / _ \/ _ \ | (__/ _ \ '  \| '  \/ _` | ' \/ _` / -_) '_|
  \___/\__,_\___/\___/  \___\___/_|_|_|_|_|_\__,_|_||_\__,_\___|_|                                                               
""")
            print(f"➡ Base actual {self.database_name}")
            print("1.- Actualizar la base \n2.- Actualizar solo un modulo\n3.- Cambiar base\n4.- Reinciar Odoo \n5.- Limpiar pantalla \n6.- Salir")
            
            selected_option = input("Acción a realizar: \n")

            
            if selected_option == "1" :
                option = input (f"Se actualizara toda la base {self.database_name} desea continuar ? (S/N) \n")
                if option == "S" or option == "s":
                    # Llamar al metodo command y pasarle como parametro el nombre de la base y el modulo                    
                    command(self.database_name,'all')

            if selected_option == "2" :
                changeModule = input (f"Modulo actual {self.module} desea cambiarlo? (S/N)\n")
                if changeModule == "S" or changeModule == "s":
                     self.module = input("Ingresa el nombre del modulo (si son varios separar signo de coma sin usar espacios ejemplo modulo1,modulo2) ")   
                option = input (f"Se actualizara la base {self.database_name} con {self.module} desea continuar ? (S/N) \n")
                if option == "S" or option == "s":
                    # Llamar al metodo command y pasarle como parametro el nombre de la base y el modulo
                    command(self.database_name,self.module)

            if selected_option == "3":
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

                
            if selected_option == "4":
                option = input (f"Se reiniciara Odoo desea continuar ? (S/N) \n")
                if option == "S" or option == "s":
                    restart_command = "sudo systemctl restart odoo"
                    print("Reiniciando Odoo...")
                    os.system(restart_command)
                    print("Odoo reiniciado")
            if selected_option == "5":
                    clear_command = "clear"
                    os.system(clear_command)

            if selected_option == "6":
                print("Adios")
                break

            # Guardar los datos de las variables self.database_name y self.module en el archivo data.txt
            with open('data.txt', 'w') as f:
                f.write(f"db,{self.database_name}\n")
                f.write(f"module,{self.module}")

def command (db_name,module):
    command = f"sudo -u odoo odoo -c /etc/odoo/odoo.conf -d {db_name} -u {module} -p 8069 --no-http --load-language=es_MX --stop-after-init"
    os.system(command)

init = oddoCommander
init()
