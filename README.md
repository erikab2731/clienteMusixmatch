# clienteMusixmatch
Aplicación web para buscar y reproducir canciones

# Autores 
Erika Bracamonte
Paula de Jaime

# Navegadores recomendados  
- Google Chrome (Version 66.0.3359.139)

Es posible que ciertas funcionalidades no se muestren o se muestren erróneamente en otros navegadores, ya que se ha utilizado Chrome en todo el proceso de desarrollo.

NOTA: La reprodución de la canción no funciona en Mozilla Firefox por no ser compatible.

# Utilizados   
- API iTunes
- API musixmatch
- API dropbox
- WebScrapping con BeautifulSoup

# Breve Descripción  
Con la aplicación creada (https://swgae10.appspot.com) se puede iniciar sesión mediante Google y Dropbox.

Una vez iniciada la sesión, se pueden buscar letras de canciones introduciendo el título de la canción en el recuadro de "Buscar Canción". Ejemplo "Skyscraper".

Cuando se pulse "Buscar" se imprimirán por pantalla el conjunto de canciones encontradas. Si se quiere visualizar la letra de alguna, se pinchará encima.

La letra de la canción se ha obtenido "scrappeando" la web "musixmatch.com", y a los usuarios identificados con Dropbox se les da la opción de guardar dicha letra. Cuando la letra se guarde se imprimirá un mensaje por pantalla.

Mediante iTunes, el usuario es capaz de escuchar una breve preview de la canción elegida.

Por otro lado, si se introduce el nombre de un cantante en "Buscar Cantante" y se pulsa "Buscar", se imprimirán todos los cantantes coincidentes.

Al pulsar en alguno obtendremos sus veinte canciones más populares. Si se clicka en alguna de esas canciones veremos la letra de la canción.

Finalmente, si se clicka en un artista del top 5 se redirecciona a la página que muestra las canciones del artista seleccionado.  
