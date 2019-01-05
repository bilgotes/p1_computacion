# p1_computacion
Practica 1 de computacion en red

_______ v.2.0 _________
- Eliminado instalacion de virtualenv en script de instalacion
- Cambio dinamico de propietario en lugar de fijo en la linea 7 del script de instalacion
- Añadido al script de instalacion las ordenes sed para que cabie el usuario de los demonios acorde a la maquina destino, los copie al path de systemd y los active.
- Se cambian los demonios para que sed pueda cambiar $USER por el usuario real de la maquina.
- Se elimina el fichero mongod.conf del path principal. Queda en mongo_files/conf/.
- Se añade esta descripción.
- Se modifica el código de recolector.py para comentar los prints.
- Se modifica mongod.config para que no genere un fork y esté preparado para entrar en set de replicación.

+++++++ Instalación +++++++++
Ejecutar el script install.sh

***Problemas durante la instalación
Durante la autoinstalación pueden aparecer problemas bien por falta de dependencias o por la inexistencia de alguno de los directorios que el script utiliza. Debe tenerse en cuenta que el script de instalación está pensado para ser usado en una máquina corriendo Ubuntu server 18. Sin incluir los posibles problemas de dependencias, que están bien documentados en la salida de cualquier gestor de paquetes, algunos de los problemas pueden ser:
1. En el arranque del servidor mongod alguno de los directorios indicados en el fichero de configuración /etc/mongod.conf no existe o no tiene permisos de acceso.
2. El directorio almacén para las declaraciones de servicios en systemd no es /lib/systemd/system.
