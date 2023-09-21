// Función para hacer la solicitud al servidor Python y mostrar los datos en la tarjeta (card)
function updateWeatherCard(data) {
  const temperatureSpan = document.getElementById("temperature");
  const descriptionSpan = document.getElementById("description");

  temperatureSpan.textContent = data.weather1.main.temp + "°C";
  descriptionSpan.textContent = data.weather1.weather[0].description;
}

// Llama a la API para obtener los datos meteorológicos cuando se hace clic en el botón
function getWeatherForTicket() {
  const ticketInput = document.getElementById("ticket-input");
  const ticketNumber = ticketInput.value.trim();

  if (ticketNumber === "") {
      alert("Por favor, ingresa un número de boleto válido.");
      return;
  }

  fetch(`/get_weather?ticket=${ticketNumber}`)
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

// Asociar la función getWeatherForTicket al evento clic del botón de búsqueda
const searchButton = document.getElementById("search-button");
searchButton.addEventListener("click", getWeatherForTicket);
