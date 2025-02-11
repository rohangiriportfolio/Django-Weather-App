let WeatherData = null;
let lat;
let lon;

document.getElementById('submit-btn').addEventListener('click',()=>{
    
    lon = localStorage.getItem("lon");
    lat = localStorage.getItem("lat");
    console.log(lon);
    console.log(lat);
    range = document.getElementById("input2").value;
    console.log(range);
    
    const details = {
        "startDate": "2025-02-09",
        "endDate": range,
        "lon":lon,
        "lat": lat,
    }
    

    fetch("http://127.0.0.1:8000/home/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(details)
    })
    .then(response => response.json())
    .then(data => {
        console.log("Weather Data:", data);
        alert('Weather Data fetched successfully');
        WeatherData = data;
        
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Error:", error);
    });

    


})


document.getElementById('location-btn').addEventListener('click',()=>{
    window.location.href = "newIndex.html";
})


function getWeather(day){
    if(WeatherData != null){
        let temp = WeatherData.forecast[day-1];
        document.querySelector('.value').removeChild(document.querySelector('.value').firstChild);
        document.querySelector("#temp .value").innerHTML = temp["temperature_2m"].toFixed(2);
        document.querySelector("#hum .value").innerHTML = temp["relative_humidity_2m"].toFixed(2);
        document.querySelector("#cloud .value").innerHTML = temp["cloud_cover"].toFixed(2);
        document.querySelector("#dew .value").innerHTML = temp["dew_point_2m"].toFixed(2);
        document.querySelector("#prec .value").innerHTML = temp["precipitation"].toFixed(2);
        document.querySelector("#rain .value").innerHTML = temp["rain"].toFixed(2);
        document.querySelector("#snow .value").innerHTML = temp["snowfall"].toFixed(2);
        document.querySelector("#pres .value").innerHTML = temp["surface_pressure"].toFixed(2);
        document.querySelector("#wind-direc .value").innerHTML = temp["wind_direction_100m"].toFixed(2);
        document.querySelector("#wind-speed .value").innerHTML = temp["wind_speed_100m"].toFixed(2);


    }
}
document.getElementById('today').addEventListener('click', ()=>getWeather(1));
document.getElementById('tomorrow').addEventListener('click', ()=>getWeather(2));

document.getElementById("input3").addEventListener("keydown", function(event) {
    if (event.key === "Enter") {  // Check if Enter key is pressed
        let inputValue = this.value;
        console.log("Entered Value:", inputValue);
        getWeather(inputValue);
    }
});



const data = null;

const xhr = new XMLHttpRequest();
// xhr.withCredentials = true;

xhr.addEventListener('readystatechange', function () {
	if (this.readyState === this.DONE) {
		console.log(this.responseText);
	}
});

lon = localStorage.getItem("lon");
lat = localStorage.getItem("lat");

xhr.open('GET', `https://geocoding-by-api-ninjas.p.rapidapi.com/v1/reversegeocoding?lat=${lat}&lon=${lon}`);
xhr.setRequestHeader('x-rapidapi-key', '8a37f5c988mshd564d91b5614897p1450a1jsn9abfb9c283d2');
xhr.setRequestHeader('x-rapidapi-host', 'geocoding-by-api-ninjas.p.rapidapi.com');

xhr.send(data);
// console.log(data);

var place;

xhr.onload = function () {
    if (xhr.status >= 200 && xhr.status < 300) {
        place = JSON.parse(xhr.responseText);
        changePlaceName(place)
        // localStorage.setItem("place", place);
    } else {
        console.error("Error:", xhr.statusText);
    }
};
// place=localStorage.getItem("place", place);
console.log(place[0]);

function changePlaceName(){
    let tempPlace = `${place[0]["name"]}, ${place[0]['state']}, ${place[0]['country']}`;

    let placeHTML = document.querySelector('#place');
    let locHTML = document.querySelector('#loc');

    placeHTML.removeChild(placeHTML.firstChild);
    locHTML.removeChild(locHTML.firstChild);

    placeHTML.innerHTML=tempPlace;
    locHTML.innerHTML=tempPlace;
}
