import os
import subprocess

from click import command


class oddoCommander :

    def __init__ (self):
        #Revisar si existe el archivo data.txt y si no existe crearlo
        if not os.path.exists('data.txt'):
            with open('data.txt', 'w') as f:
                f.write("odoo,all")
        
        with open('data.txt', 'r') as f:
            data = f.read()
            self.database_name = data.split(',')[0]
            self.module = data.split(',')[1]
        self.menu()

    def menu (self):
        selected_option = ''

        while selected_option !=4 :
            
            print(f"➡ Base actual {self.database_name}")

            print("1.- Actualizar la base \n2.- Actualizar solo un modulo\n3.- Cambiar base\n4.- Reinciar Odoo \n5.- Salir")
            selected_option = input("Acción a realizar: \n")

            if selected_option == "1" :
                option = input (f"Se actualizara toda la base {self.database_name} desea continuar ? (S/N) \n")
                if option == "S" or option == "s":                    
                    command(self.database_name,'all')

            elif selected_option == "2" :
                changeModule = input (f"Modulo actual {self.module} desea cambiarlo? (S/N)\n")
                if changeModule == "S" or changeModule == "s":
                     self.module = input("Ingresa el nombre del modulo (si son varios separar signo de coma sin usar espacios ejemplo modulo1,modulo2) ")   
                option = input (f"Se actualizara la base {self.database_name} con {self.module} desea continuar ? (S/N) \n")
                if option == "S" or option == "s":
                    command(self.database_name,self.module)

            elif selected_option == "3":
                print("Para ver el listado de bases en el sistema porfavor ingreses la contraseña del usuario odoo")
                command_psql = "psql -h localhost -U odoo -d postgres -1 -c '\l'" 
                process = subprocess.Popen(command_psql, stdout=subprocess.PIPE, shell=True)
                # Obtener la salida del comando
                output, error = process.communicate()

                # Imprimir la salida del comando
                print(output.decode("utf-8"))
                self.database_name = input("Ingresa el nombre de la base de datos: ")
                
            elif selected_option == "4":
                option = input (f"Se reiniciara Odoo desea continuar ? (S/N) \n")
                if option == "S" or option == "s":
                    restart_command = "sudo systemctl restart odoo"
                    os.system(restart_command)
                    # Mostrar la respuesta de la terminal en la consola
                    print("Reiniciando Odoo...")

            elif selected_option == "5":
                print("Adios")
                break

            # Guardar los datos de las variables self.database_name y self.module en un archivo de texto
            with open('data.txt', 'w') as f:
                f.write(f"{self.database_name},{self.module}")


def command (db_name,module):
    command = f"sudo -u odoo odoo -c /etc/odoo/odoo.conf -d {db_name} -u {module} -p 8069 --no-http --load-language=es_MX --stop-after-init"
    os.system(command)

init = oddoCommander
init()
