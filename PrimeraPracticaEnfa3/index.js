let searchInput;
let searchButton;
let estacionesMeteorologicas=[];
let map;
// Importe la función de Python en JavaScript



function initMap() {
    searchInput = document.getElementById("pais")
    searchButton = document.getElementById("filtrar")
    searchButton.addEventListener("click",click)
    //------------------------------------------
    loadPyodideAndRun()

}
function mapaCreate(center){
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 4,
        center: center
    });
}
function pointCreate(cord,title){
    var marker = new google.maps.Marker({
        position: cord,
        map: map,
        title: title
    });
}

function loadPyodideAndRun(pais="US") {
    fetch(`http://127.0.0.1:5000/filtrar_por_pais?pais=${pais}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        //console.log(data);
        
        let myLatLng = {lat: parseFloat(data[0][0]), lng: parseFloat(data[0][1])};
        mapaCreate(myLatLng)
        data.forEach(element => {
            let myLatLng = {lat: parseFloat(element[0]), lng: parseFloat(element[1])};
            pointCreate(myLatLng,element[2])
        });
        
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function click(){
    if (searchInput.value != ""){
        loadPyodideAndRun(searchInput.value.toUpperCase())
    }
}