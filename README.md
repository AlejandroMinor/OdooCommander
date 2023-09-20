## Descripción

El objetivo de esta herramienta, es mejorar el flujo de trabajo de los desarrolladores de Odoo. Proporciona una interfaz de terminal que elimina la necesidad de recordar los comandos relacionados con las actividades cotidianas en el uso de Odoo.

Con oddoCommander, los desarrolladores pueden realizar fácilmente tareas como actualizar la base de datos, actualizar módulos específicos, actualizar traducciones, reiniciar Odoo, mostrar registros de log y cambiar la fecha de caducidad de la base de datos. La herramienta ofrece opciones intuitivas y claras para cada una de estas acciones, lo que facilita su ejecución sin la necesidad de escribir comandos complejos.

Además, oddoCommander almacena la configuración actual, como la base de datos y los módulos seleccionados, en un archivo de configuración llamado "data.txt". Esto evita la necesidad de recordar y volver a escribir esta información cada vez que se utiliza la herramienta.

En resumen, oddoCommander simplifica y agiliza las tareas diarias de los desarrolladores de Odoo, brindando una forma conveniente de ejecutar comandos relacionados con la administración de Odoo sin tener que recordarlos manualmente. Esto mejora la productividad y el flujo de trabajo, permitiendo a los desarrolladores centrarse en tareas más importantes.

## Uso

Para utilizar la herramienta oddoCommander, simplemente ejecuta el archivo Python que contiene el código. A continuación, se muestra un ejemplo:

```shell
python3 odooCommander.py 
```

## Características y opciones

La herramienta oddoCommander proporciona las siguientes características y opciones:

0.  Salir: Cierra la herramienta oddoCommander
1. Actualizar la base: Permite actualizar todos los módulos de la base de datos especificada. 
2.  Actualizar módulo(s): Permite actualizar los módulos específicos de la base de datos especificada.
3.  Actualizar traducciones: Actualiza las traducciones en la base de datos especificada.
4.  Reiniciar Odoo: Reinicia el servicio de Odoo.
5.  Mostrar Logs: Permite mostrar los registros de log de Odoo en una nueva ventana de terminal.
6.  Cambiar fecha de caducidad a base de datos: Cambia la fecha de caducidad de la base de datos especificada.
7.  Definir parámetros [Base de datos y Módulo(s)]: Permite cambiar la base de datos actual y los módulos a actualizar.
8.  Ejecuta odoo en modo terminal con la base seleccionada
9.  Ejecuta odoo en modo pruebas unitarias en el modulo seleccionado
10.  Limpiar Pantalla: Limpia la pantalla de la terminal.


## Configuración

El código utiliza un archivo de configuración llamado "data.txt" para almacenar la base de datos actual y los módulos seleccionados. Si el archivo no existe, se crea automáticamente con valores predeterminados. Este archivo se escribe y actualiza solo, no necesita ser modificado manualmente. 


## Requisitos

El código tiene los siguientes requisitos:

-   Python 3.x
-   El paquete `click` (se puede instalar mediante `pip install click`)

Si marca error hay que colocar los siguientes valores en el archivo de configuracion de postgres :

```shell
sudo nano /etc/postgresql/12/main/pg_hba.conf
```

El archivo debe coincidir con los siguientes valores: 

``` c
# Database administrative login by Unix domain socket
local   all             postgres                                peer

# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   all             odoo            trust
# "local" is for Unix domain socket connections only
local   all             all                                     md5
# IPv4 local connections:
host    all             all             127.0.0.1/32            md5
# IPv6 local connections:
host    all             all             ::1/128                 md5
# Allow replication connections from localhost, by a user with the
# replication privilege.
local   replication     all                                     peer
host    replication     all             127.0.0.1/32            md5
host    replication     all             ::1/128                 md5
```


## Ejemplo de integración

El código proporcionado puede ser integrado en una aplicación más grande o en un flujo de trabajo automatizado. Se puede utilizar como una herramienta independiente para la administración de Odoo o como un módulo dentro de un sistema más amplio.

## Notas adicionales

-   El código utiliza la biblioteca `readline` para proporcionar la capacidad de autocompletar y recordar el historial de comandos.
-   Algunas acciones, como la actualización de los módulos y las traducciones, requieren privilegios de superusuario, por lo que se utiliza el comando `sudo` para ejecutar ciertos comandos.
-   La herramienta utiliza la biblioteca `subprocess` para ejecutar comandos en una nueva ventana de terminal mediante el uso del comando `gnome-terminal`.
