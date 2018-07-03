//Buscar cancion
document.getElementById("boton1").addEventListener("click", function(){
    var titulo = document.getElementById("campo1").value;

    //Busca canciones
    var peticion = new XMLHttpRequest();

    peticion.onreadystatechange = function() {
        if(peticion.readyState == 4) {
            if(peticion.status == 200) {
                if(peticion.responseText != null) {
                    var jsonObj = JSON.parse(peticion.responseText);
                    var trackList = jsonObj['message']['body']['track_list'];

                    var html ="";

                    if(trackList.length == 0){
                        html = "No se han encontrado resultados :(";
                    }
                    for (var i = 0; i < trackList.length; i++) {
                        var oneTrack = trackList[i]['track'];

                        var artistName = oneTrack['artist_name'];
                        var trackId = oneTrack['track_id'];
                        var trackName = oneTrack['track_name'];

                        artistName = artistName.replace(/'/g, "&#39;");
                        trackName = trackName.replace(/'/g, "&#39;");

                         html += "<a href='/letraCancion?nombreCancion="+ trackName+"&id="+trackId+"&artist="+artistName+"'><b>"+trackName + "</b>, by " + artistName + "<br />";
                    }

                    document.getElementById("resultados1").innerHTML = html;
                }
            }
        }

    };

    if(titulo) {
        peticion.open("POST", "/buscarCancion", true);
        peticion.send(titulo);
    }
});

//Buscar artista
document.getElementById("boton2").addEventListener("click", function(){
    var nombre = document.getElementById("campo2").value;

    //Busca canciones
    var peticion2 = new XMLHttpRequest();

    peticion2.onreadystatechange = function() {
        if(peticion2.readyState == 4) {
            if(peticion2.status == 200) {
                if(peticion2.responseText != null) {
                    var jsonObj = JSON.parse(peticion2.responseText);
                    var artistList = jsonObj['message']['body']['artist_list'];

                    var html = "";

                     if(artistList.length == 0){
                        html = "No se han encontrado resultados :(";
                    }

                    for (var i = 0; i < artistList.length; i++) {
                        var oneArtist = artistList[i]['artist'];

                        var artistName = oneArtist['artist_name'];
                        var artistId = oneArtist['artist_id'];

                        artistName = artistName.replace(/'/g, "&#39;");

                        html += "<a href='/datosArtista?nombreArtista=" + artistName + "&id=" + artistId + "'><b>" + artistName + "</a><br />";
                    }





                    document.getElementById("resultados2").innerHTML = html;
                }
            }
        }

    };

     if(nombre) {
         peticion2.open("POST", "/buscarArtista", true);
         peticion2.send(nombre);
     }
});