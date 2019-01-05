# p1_computacion
Practica 1 de computacion en red

+++++++ Instalación +++++++++
Ejecutar el script install.sh

***Problemas durante la instalación
Durante la autoinstalación pueden aparecer problemas bien por falta de dependencias o por la inexistencia de alguno de los directorios que el script utiliza. Debe tenerse en cuenta que el script de instalación está pensado para ser usado en una máquina corriendo Ubuntu server 18. Sin incluir los posibles problemas de dependencias, que están bien documentados en la salida de cualquier gestor de paquetes, algunos de los problemas pueden ser:
1. En el arranque del servidor mongod alguno de los directorios indicados en el fichero de configuración /etc/mongod.conf no existe o no tiene permisos de acceso.
2. El directorio almacén para las declaraciones de servicios en systemd no es /lib/systemd/system.
