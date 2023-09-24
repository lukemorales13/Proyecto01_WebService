// Preloader
const preloaderWrapped = document.querySelector('.preloader-wrapper');
window.addEventListener('load', function () {
    preloaderWrapped.classList.add('fade-out-animation');
});

// Función para hacer la solicitud al servidor Python y mostrar los datos en la tarjeta (card)
function updateWeatherCard(data) {
  const temperatureSpan = document.getElementById("temperature");
  const descriptionSpan = document.getElementById("description");

  temperatureSpan.textContent = data.temperature + "°C";
  descriptionSpan.textContent = data.description;
}

// Llama a las funciones de búsqueda y muestra los resultados en la tarjeta cuando se hace clic en el botón "Search"
function searchByIata() {
  const inputElement = document.getElementById("search-input");
  const inputValue = inputElement.value.trim();

  if (inputValue === "") {
    alert("Por favor, ingresa un IATA code válido.");
    return;
  }

  // Realiza la búsqueda por IATA code utilizando la función de búsqueda correspondiente
  fetch(`/iata_search?input=${inputValue}`)
    .then(response => {
      if (!response.ok) {
        throw new Error(`Error de red: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      updateWeatherCard(data);
    })
    .catch(error => {
      console.error("Error al obtener datos meteorológicos:", error);
    });
}

function searchByCity() {
  const inputElement = document.getElementById("search-input");
  const inputValue = inputElement.value.trim();

  if (inputValue === "") {
    alert("Por favor, ingresa un nombre de ciudad válido.");
    return;
  }

  // Realiza la búsqueda por nombre de ciudad utilizando la función de búsqueda correspondiente
  fetch(`/city_search?input=${inputValue}`)
    .then(response => {
      if (!response.ok) {
        throw new Error(`Error de red: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      updateWeatherCard(data);
    })
    .catch(error => {
      console.error("Error al obtener datos meteorológicos:", error);
    });
}

function searchByCoordinates() {
  const inputElement = document.getElementById("search-input");
  const inputValue = inputElement.value.trim();

  if (inputValue === "") {
    alert("Por favor, ingresa coordenadas válidas.");
    return;
  }

  // Realiza la búsqueda por coordenadas utilizando la función de búsqueda correspondiente
  fetch(`/massive_search?input=${inputValue}`)
    .then(response => {
      if (!response.ok) {
        throw new Error(`Error de red: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      updateWeatherCard(data);
    })
    .catch(error => {
      console.error("Error al obtener datos meteorológicos:", error);
    });
}

// Asociar las funciones de búsqueda a los eventos clic de los botones correspondientes
const iataSearchButton = document.getElementById("iata-search-button");
iataSearchButton.addEventListener("click", searchByIata);

const citySearchButton = document.getElementById("city-search-button");
citySearchButton.addEventListener("click", searchByCity);

const coordinatesSearchButton = document.getElementById("coordinates-search-button");
coordinatesSearchButton.addEventListener("click", searchByCoordinates);
