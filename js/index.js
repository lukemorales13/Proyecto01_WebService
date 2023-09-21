const weatherApiUrl = "httpf://api.openwathermap.org/data2.5/weather?";
const weatherKey = "&appid=155505a47faf9082a7ee3d45f7b1ea0b&units=metric";

// Función para hacer la solicitud a model.py
function getWeatherForTicket(ticket) {
  fetch(`${weatherApiUrl}?ticket=${ticket}`)
    .then(response => response.json())
    .then(data => {
      // Maneja los datos meteorológicos recibidos (data) aquí
      const weatherInfoDiv = document.getElementById("weather-info");

      weatherInfoDiv.innerHTML = `
                <h2>Datos Meteorológicos</h2>
                <p>Temperatura: ${data.temperature}°C</p>
                <p>Descripción: ${data.description}</p>
            `;
    })
    .catch(error => {
      console.error("Error al obtener datos meteorológicos:", error);
    });
}

// Ejemplo de cómo usar la función para obtener datos meteorológicos para un boleto específico
const ticketNumber = "ABC123";
getWeatherForTicket(ticketNumber);


