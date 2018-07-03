document.getElementById("boton2").addEventListener("click", function(){

    // aqui se supone que cojemos la letra de la cancion
    var letra = document.getElementById("letraCancion").innerText;
    var titulo = document.getElementById("titulo").innerText;
    var artista = document.getElementById("artista").innerText;

    //Busca canciones
    var peticion = new XMLHttpRequest();

    peticion.onreadystatechange = function() {
        if(peticion.readyState == 4) {
            if(peticion.status == 200) {
                if(peticion.responseText != null) {

                    if(peticion.responseText === "False"){
                        document.getElementById("mensaje").innerHTML = "Sesion caducada o no has iniciado sesión en Dropbox<br /><a href='/'>Inicia Sesión</a>";
                    }else if(peticion.responseText === "True"){
                        document.getElementById("mensaje").textContent = "La cancion se ha guardado correctamente en Dropbox";
                    }else{
                        document.getElementById("mensaje").textContent = peticion.responseText;
                    }
                }
            }
        }

    };

    peticion.open("POST", "/SaveSongDropBox", true);
    peticion.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    peticion.send("titulo="+titulo+"&letra="+letra+"&artista="+artista);
});