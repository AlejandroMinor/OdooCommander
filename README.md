## Descripción
---
El objetivo de esta herramienta es mejorar el flujo de trabajo de los desarrolladores de Odoo. Proporciona una interfaz de terminal que elimina la necesidad de recordar los comandos relacionados con las actividades cotidianas en el uso de Odoo.

Con OdooCommander, los desarrolladores pueden realizar fácilmente tareas como actualizar la base de datos, actualizar módulos específicos, actualizar traducciones, reiniciar Odoo, mostrar registros de log y cambiar la fecha de caducidad de la base de datos. La herramienta ofrece opciones intuitivas y claras para cada una de estas acciones, lo que facilita su ejecución sin la necesidad de escribir comandos complejos.

Además, OdooCommander almacena la configuración actual, como la base de datos y los módulos seleccionados, en un archivo de configuración llamado "data.txt". Esto evita la necesidad de recordar y volver a escribir esta información cada vez que se utiliza la herramienta.

En resumen, OdooCommander simplifica y agiliza las tareas diarias de los desarrolladores de Odoo, brindando una forma conveniente de ejecutar comandos relacionados con la administración de Odoo sin tener que recordarlos manualmente. Esto mejora la productividad y el flujo de trabajo, permitiendo a los desarrolladores centrarse en tareas más importantes.


## Uso  
___
**Instalar**

Instalar los paquetes necesarios con pip

```shell
pip3 install -r requirements.txt
```

**Ejecutar**

```shell
python3 OdooCommander
```

**Primera configuración**

Al ejecutar por primera vez el programa, pedirá algunas configuraciones simples:
1. El sistema mostrará en pantalla las bases de datos de Postgres.
2. Ingresar el nombre de la base con la que se va a trabajar (esto se puede cambiar después).
3. Ingresar la ruta donde se encuentran los módulos personalizados de Odoo.
4. Se listarán los módulos que se tienen en el sistema.
5. Ingresar el nombre de cualquier módulo personalizado (esto se puede cambiar después).

**Archivo data.txt**

Es el archivo que almacena las configuraciones y preferencias

## Características y opciones
___
  La herramienta OdooCommander proporciona las siguientes características y opciones:

0. Detiene el servicio de Odoo.
1. Actualizar la base: Permite actualizar todos los módulos de la base de datos especificada.
2. Actualizar módulo: Permite actualizar los módulos específicos de la base de datos especificada.
3. Actualizar traducciones: Actualiza las traducciones en la base de datos especificada.
4. Reiniciar Odoo: Reinicia el servicio de Odoo.
5. Mostrar Logs: Permite mostrar los registros de log de Odoo en una nueva ventana de terminal. (La filtrada solo mostrará los mensajes de root, por ejemplo, los generados por `logging.info`).
6. Cambiar fecha de caducidad a base de datos: Cambia la fecha de caducidad de la base de datos especificada.
7. Definir parámetros: Permite cambiar la base de datos actual, el módulo a actualizar y la configuración del bot para enviar notificaciones por Telegram (esto se explica en detalle después).
8. Ejecutar Odoo en modo terminal con la base seleccionada.
9. Ejecutar Odoo en modo pruebas unitarias en el módulo seleccionado.
10. Limpiar Pantalla: Limpia la pantalla de la terminal.
11. Pruebas de seguridad: Permite analizar el módulo actual mediante la herramienta Bandit.
12. Verificar actualizaciones del repositorio.
13. Restaurar bases de datos manualmente: Permite restaurar bases de datos por medio de una interfaz grafica o via terminal permitiendo copiar filestore y dar los permisos necesarios, crear la base de datos y ejecutar el sql para importar los datos. Durante la restauracion pedira contraseñas de usuario y postgres para poder realizar las acciones.  Para más info ver el proyecto
[OdooDBRestore: Restaura bases de datos de odoo de manera manual (github.com)](https://github.com/AlejandroMinor/OdooDBRestore)

  
## Configuración
___
### Data.txt

El código utiliza un archivo de configuración llamado "data.txt" para almacenar la base de datos actual y los módulos seleccionados. Si el archivo no existe, se crea automáticamente con valores predeterminados. Este archivo se escribe y actualiza solo, no necesita ser modificado manualmente.

### Notificaciones por telegram

La herramienta permite enviar notificaciones por Telegram, lo que permite dejar actualizaciones largas (como cargar todos los módulos) y recibir una notificación con una respuesta positiva o negativa según corresponda al estado de ejecución (si terminó con errores o no).

Para recibir las notificaciones, se debe crear un bot personalizado en Telegram, ya que el TOKEN y el ChatId serán elementos necesarios para realizar esta tarea.

**Crear bot de telegram**

1. Abre Telegram y busca a `BotFather`.
2. Inicia una conversación con `BotFather` y escribe `/newbot`.
3. Sigue las instrucciones para darle un nombre a tu bot y un nombre de usuario. Recibirás un mensaje con el token de acceso de tu bot.

**Obtener el ID de Chat**

1. Busca tu bot.
2. Envía un mensaje al bot (no importa el contenido).
3. Abre un navegador y ve a la siguiente URL, reemplazando `<TOKEN>` con el token de tu bot: `https://api.telegram.org/bot<TOKEN>/getUpdates`
4. Busca el campo `"chat":{"id":` en la respuesta JSON. El número después de `"id":` es el ID de chat.

**Configuración en la herramienta OdooCommander**

1. Abre la herramienta
2. Ingresa a la opción 7
3. Seleccionar el configurador de Telegram
4. Ingresa los datos solicitados
5. Si todo es correcto se enviará una notificación de prueba (Caso contrario revisar el TOKEN o Chat ID)
6. La configuración se guardara automaticamente en el archivo data.txt

## Requisitos
___
- Python 3.x

## Errores 
___
### Postgres

Si marca error hay que colocar los siguientes valores en el archivo de configuracion de postgres :

```shell
sudo nano /etc/postgresql/12/main/pg_hba.conf
```

  
El archivo debe coincidir con los siguientes valores:

``` c
# Database administrative login by Unix domain socket
local all postgres peer

# TYPE DATABASE USER ADDRESS METHOD
local all odoo trust

# "local" is for Unix domain socket connections only
local all all md5

# IPv4 local connections:
host all all 127.0.0.1/32 md5

# IPv6 local connections:
host all all ::1/128 md5

# Allow replication connections from localhost, by a user with the
# replication privilege.
local replication all peer
host replication all 127.0.0.1/32 md5
host replication all ::1/128 md5
```

  
## Notas adicionales
___
- El código utiliza bibliotecas externas. Por tanto es importante instalarlas con el archivo requirements.txt 
- Algunas acciones, como la actualización de los módulos y las traducciones, requieren privilegios de superusuario, por lo que se utiliza el comando `sudo` para ejecutar ciertos comandos
- Puede llegar a solicitar la contraseña de usuario de postgres para realizar algunas acciones
