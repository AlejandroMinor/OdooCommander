import os
import subprocess

from click import command


class oddoCommander :

    def __init__ (self):
        self.database_name = 'default'
        self.module = 'all'
        self.menu()

    def menu (self):
        selected_option = ''

        while selected_option !=4 :
            
            print(f"➡ Base actual {self.database_name}")

            print("1.- Actualizar la base \n2.- Actualizar solo un modulo\n3.- Cambiar base\n4.- Salir")
            selected_option = input("Acción a realizar: \n")

            if selected_option == "1" :
                option = input (f"Se actualizara toda la base {self.database_name} desea continuar ? (S/N) \n")
                if option == "S" or option == "s":                    
                    command(self.database_name,'all')

            if selected_option == "2" :
                changeModule = input (f"Modulo actual {self.module} desea cambiarlo? (S/N)\n")
                if changeModule == "S" or changeModule == "s":
                     self.module = input("Ingresa el nombre del modulo (si son varios separar signo de coma sin usar espacios ejemplo modulo1,modulo2) ")   
                option = input (f"Se actualizara la base {self.database_name} con {self.module} desea continuar ? (S/N) \n")
                if option == "S" or option == "s":
                    command(self.database_name,self.module)

            if selected_option == "3":
                print("Para ver el listado de bases en el sistema porfavor ingreses la contraseña del usuario odoo")
                command_psql = "psql -h localhost -U odoo -d postgres -1 -c '\l'" 
                process = subprocess.Popen(command_psql, stdout=subprocess.PIPE, shell=True)
                # Obtener la salida del comando
                output, error = process.communicate()

                # Imprimir la salida del comando
                print(output.decode("utf-8"))
                self.database_name = input("Ingresa el nombre de la base de datos: ")

            if selected_option == "4":
                print("Adios")
                break


def command (db_name,module):
    command = f"sudo -u odoo odoo -c /etc/odoo/odoo.conf -d {db_name} -u {module} -p 8069 --no-http --load-language=es_MX --stop-after-init"
    os.system(command)

init = oddoCommander
init()
