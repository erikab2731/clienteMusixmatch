document.getElementById("boton3").addEventListener("click", function(){

    // aqui se supone que cojemos la info de la cancion
    var titulo = document.getElementById("titulo").innerText;
    var artista = document.getElementById("artista").innerText;

    //Busca canciones
    var peticion = new XMLHttpRequest();

    peticion.onreadystatechange = function() {
        if(peticion.readyState == 4) {
            if(peticion.status == 200) {
                if(peticion.responseText != null) {

                    if(peticion.responseText === "False"){
                        document.getElementById("bloqueEscucha").innerHTML = "No se han encontrado resultados :(";
                    }else{
                         var jsonObj = JSON.parse(peticion.responseText);
                         var canciones = jsonObj["results"];

                         var unaCancion;
                         var linkAudio;
                          for (var i = 0; i < canciones.length; i++) {
                              unaCancion = canciones[i]
                              var link = getAudioLink(unaCancion);
                              if(link !== "false"){
                                  linkAudio = link;
                                  break;
                              }
                          }

                          if(!linkAudio){
                              document.getElementById("bloqueEscucha").innerHTML = "No se han encontrado resultados :(";
                          }else{
                              document.getElementById("bloqueEscucha").innerHTML = "<audio src=\"" + linkAudio +"\" controls></audio>\n";
                          }

                    }
                }
            }
        }

    };

    peticion.open("POST", "/RequestSong", true);
    peticion.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    titulo = encodeURIComponent(titulo);
    artista = encodeURIComponent(artista);
    peticion.send("titulo="+titulo+"&artista="+artista);
});

function getAudioLink(unaCancion){
    var link;
    if(unaCancion.hasOwnProperty('previewUrl')){
        link = unaCancion["previewUrl"];
    }else{
        link = "false";
    }

    return link;
}

