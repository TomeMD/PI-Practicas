pi-jorgeac-tomemd-miguelcc

INSTRUCCIONES DE EJECUCIÓN

Para poder ejecutar el programa en tu ordenador personal debes tener un token de la
API de Brawl Stars con tu IP pública dentro de las IPs permitidas, para ello debes
ir a https://developer.brawlstars.com/ y crearte una cuenta.

Una vez creada, te logeas y vas al apartado "My Account", que te aparece al pulsar
sobre tu nombre de usuario en la esquina superior derecha, clickas sobre
"Create new key" y tienes que asegurarte de que en el apartado "ALLOWED IP ADDRESSES"
introduces tu IP pública.

La imagen Docker está disponible en el repositorio mcastro2/brawlstarspi.

	docker pull mcastro2/brawlstarspi

Expone el puerto 8000, que hay que mapear a algún puerto del host, por ejemplo 8000

	docker run -d -p 8000:8000 mcastro2/brawlstarspi

Antes de probar la aplicación web debes introducir el token generado previamente en el 
archivo conf.py de la imagen Docker.
Al ejecutar el comando anterior este te devolvió el id del contenedor Docker, ahora 
debes ejecutar el siguiente comando con el id del contenedor Docker para que se te abrá
una shell desde la que podrás modificar la imagen Docker:

	docker exec -it <id_contenedor> /bin/sh

Donde <id_contenedor> es el id que te devolvió el comando anterior.

Una vez dentro de la shell y con el token que habías generado previamente ejecutarás:

	echo "brawlToken = '<brawl_token>'" > brawlstars/brawlstarsapp/conf.py
	exit

Donde <brawl_token> es el token generado previamente (hay que encerrarlo entre comillas 
simples).

Ahora ya podrás probar la aplicación web, para ello debes buscar en el navegador:

	http://127.0.0.1:8000/ 

Para probar la búsqueda por tag debes loguearte previamente, sin embargo, para probar
simplemente la funcionalidad de mostrar el resumen de estadísticas generales de un jugador,
recomendamos ir a la sección "Best players" y clickar sobre alguno de los jugadores 
del top ya que tienen unas estadísticas más completas y se puede ver mejor el funcionamiento 
de esa funcionalidad.

También recomendamos ciertos tags de jugador con los que hemos estado haciendo pruebas:
 #9P2JLPCR
 #200LCL0VC
 #2009GVCG
 #2QCGR8CC



INSTRUCCIONES DE EJECUCIÓN DEL TESTING

Para probar el testing de esta aplicación web debes clonar el repositorio:

	git clone https://github.com/IntegrativeProgramming/pi-jorgeac-tomemd-miguelcc.git

Y ejecutar los tests:

	cd pi-jorgeac-tomemd-miguelcc/brawlstars
	python3 manage.py test
