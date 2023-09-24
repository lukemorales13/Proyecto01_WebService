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

// Llama a la API para obtener los datos meteorológicos cuando se hace clic en el botón
function getWeatherData(inputValue) {
  fetch(`/get_weather?input=${inputValue}`)
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

// Asociar la función getWeatherData al evento clic del botón de búsqueda
const searchButton = document.getElementById("search-button");
searchButton.addEventListener("click", function () {
  const inputElement = document.getElementById("ticket-input");
  const inputValue = inputElement.value.trim();

  if (inputValue === "") {
    alert("Por favor, ingresa un número de boleto o una ciudad válida.");
    return;
  }

  getWeatherData(inputValue);
});
