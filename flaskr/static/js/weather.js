const input = document.getElementById("city-input");
const btn = document.getElementById("search-btn");
const errorEl = document.getElementById("error");
const loadingEl = document.getElementById("loading");
const resultsEl = document.getElementById("results");

function iconUrl(code) {
  return `https://openweathermap.org/img/wn/${code}@2x.png`;
}

function dayName(dt) {
  return new Date(dt * 1000).toLocaleDateString("en-US", { weekday: "short" });
}

function showError(msg) {
  errorEl.textContent = msg;
  errorEl.style.display = "block";
  resultsEl.style.display = "none";
}

function clearError() {
  errorEl.style.display = "none";
}

async function fetchWeather(city) {
  clearError();
  loadingEl.style.display = "block";
  resultsEl.style.display = "none";

  try {
    // Get geocode data
    const geoRes = await fetch(`/api/geocode?city=${encodeURIComponent(city)}`);
    if (!geoRes.ok) {
      const e = await geoRes.json();
      throw new Error(e.message || "City not found");
    }
    const geoData = (await geoRes.json())[0];

    // Get weather and forecast data using geocode
    const [weatherRes, forecastRes] = await Promise.all([
      fetch(
        `/api/weather?lon=${encodeURIComponent(geoData.lon)}&lat=${encodeURIComponent(geoData.lat)}`,
      ),
      fetch(
        `/api/forecast?lon=${encodeURIComponent(geoData.lon)}&lat=${encodeURIComponent(geoData.lat)}`,
      ),
    ]);

    const weatherData = await weatherRes.json();
    const forecastData = await forecastRes.json();

    loadingEl.style.display = "none";
    renderCurrent(weatherData);
    renderForecast(forecastData);
    resultsEl.style.display = "block";
  } catch (err) {
    loadingEl.style.display = "none";
    showError(err.message || "Something went wrong. Please try again.");
  }
}

function renderCurrent(d) {
  document.getElementById("city-label").textContent =
    `${d.name}, ${d.sys.country}`;
  document.getElementById("condition-label").textContent =
    d.weather[0].description;
  document.getElementById("temp-label").textContent =
    `${Math.round(d.main.temp)}°C`;
  document.getElementById("weather-icon").src = iconUrl(d.weather[0].icon);
  document.getElementById("humidity-label").textContent = `${d.main.humidity}%`;
  document.getElementById("wind-label").textContent =
    `${Math.round(d.wind.speed)} m/s`;
}

function renderForecast(data) {
  const daily = {};
  data.list.forEach((item) => {
    const date = new Date(item.dt * 1000).toDateString();
    if (!daily[date]) {
      daily[date] = {
        highs: [],
        lows: [],
        icon: item.weather[0].icon,
        dt: item.dt,
      };
    }
    daily[date].highs.push(item.main.temp_max);
    daily[date].lows.push(item.main.temp_min);
  });

  const days = Object.values(daily).slice(0, 5);
  document.getElementById("forecast-grid").innerHTML = days
    .map(
      (d) => `
    <div class="fc-card">
      <div class="fc-day">${dayName(d.dt)}</div>
      <img class="fc-icon" src="${iconUrl(d.icon)}" alt="icon" />
      <div class="fc-temp">${Math.round(Math.max(...d.highs))}°</div>
      <div class="fc-lo">${Math.round(Math.min(...d.lows))}°</div>
    </div>
  `,
    )
    .join("");
}

btn.addEventListener("click", () => {
  const c = input.value.trim();
  if (c) fetchWeather(c);
});

input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    const c = input.value.trim();
    if (c) fetchWeather(c);
  }
});
