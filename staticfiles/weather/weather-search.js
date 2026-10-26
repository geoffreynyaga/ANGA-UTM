// Weather lookup for the Weather screen (weather/weather-js.html).
(function () {
    const API_KEY = '249fa68233e35cb23e8dceb9b0c87396';
    const API = 'https://api.openweathermap.org/data/2.5/weather';

    const form = document.getElementById('weather-search');
    const input = document.getElementById('weather-city');
    const locateButton = document.getElementById('weather-locate');
    const empty = document.getElementById('weather-empty');
    const result = document.getElementById('weather-result');
    const error = document.getElementById('weather-error');

    const COMPASS = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'];
    const compass = (degrees) => COMPASS[Math.round(degrees / 45) % 8];
    const kmh = (metresPerSecond) => Math.round(metresPerSecond * 3.6);
    const set = (id, text) => { document.getElementById(id).textContent = text; };

    function showError(message) {
        error.textContent = message;
        error.classList.remove('hidden');
    }

    function show(data) {
        error.classList.add('hidden');
        empty.classList.add('hidden');
        result.classList.remove('hidden');
        const condition = data.weather && data.weather[0] ? data.weather[0] : { description: '', icon: '01d' };
        set('weather-place', [data.name, data.sys && data.sys.country].filter(Boolean).join(', '));
        set('weather-description', condition.description);
        document.getElementById('weather-icon').src = `https://openweathermap.org/img/wn/${condition.icon}@2x.png`;
        set('weather-temp', `${Math.round(data.main.temp)}°C`);
        set('weather-feels', `Feels like ${Math.round(data.main.feels_like)}°C`);
        set('weather-wind', `${kmh(data.wind.speed)} km/h ${compass(data.wind.deg || 0)}`);
        set('weather-gust', data.wind.gust ? `${kmh(data.wind.gust)} km/h` : '—');
        set('weather-visibility', data.visibility != null ? `${(data.visibility / 1000).toFixed(1)} km` : '—');
        set('weather-humidity', `${data.main.humidity}%`);
        set('weather-clouds', data.clouds ? `${data.clouds.all}%` : '—');
        set('weather-rain', data.rain && data.rain['1h'] ? `${data.rain['1h']} mm/h` : 'None');
    }

    function load(query) {
        fetch(`${API}?${query}&units=metric&appid=${API_KEY}`)
            .then((response) => response.json().then((body) => ({ ok: response.ok, body })))
            .then(({ ok, body }) => {
                if (!ok) throw new Error(body.message === 'city not found' ? 'No place found with that name.' : 'Weather is not available right now.');
                show(body);
            })
            .catch((err) => showError(err.message || 'Weather is not available right now.'));
    }

    form.addEventListener('submit', (event) => {
        event.preventDefault();
        const city = input.value.trim();
        if (city) load(`q=${encodeURIComponent(city)}`);
    });

    locateButton.addEventListener('click', () => {
        if (!navigator.geolocation) {
            showError('Your browser cannot share its location. Search for a city instead.');
            return;
        }
        navigator.geolocation.getCurrentPosition(
            (position) => load(`lat=${position.coords.latitude}&lon=${position.coords.longitude}`),
            () => showError('Your location could not be found. Search for a city instead.')
        );
    });
})();
