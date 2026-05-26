import { useState, useEffect } from 'react';
import axios from 'axios';
import { ChevronDown, CloudRain, Sun, Cloud, Snowflake, Loader2, CloudLightning } from 'lucide-react';
import './index.css';

// Remove the default App.css import if it exists

const LOCATIONS = [
  { id: 'blr', name: 'Bengaluru' },
  { id: 'hyd', name: 'Hyderabad' },
  { id: 'delhi', name: 'New Delhi' },
  { id: 'mumbai', name: 'Mumbai' }
];

const getWeatherIcon = (weatherLabel) => {
  if (!weatherLabel) return <Sun size={24} />;
  
  const label = weatherLabel.toLowerCase();
  if (label.includes('sun')) return <Sun size={24} />;
  if (label.includes('cloud')) return <Cloud size={24} />;
  if (label.includes('fog')) return <Cloud size={24} color="#94a3b8" />;
  if (label.includes('rain')) return <CloudRain size={24} />;
  if (label.includes('snow')) return <Snowflake size={24} />;
  if (label.includes('storm')) return <CloudLightning size={24} />;
  
  return <Sun size={24} />;
};

const getWeatherDescription = (weatherLabel) => {
  if (!weatherLabel) return 'Unknown';
  
  const label = weatherLabel.toLowerCase();
  if (label.includes('sun')) return 'Sunny';
  if (label.includes('cloud')) return 'Cloudy';
  if (label.includes('fog')) return 'Foggy';
  if (label.includes('rain')) return 'Rainy';
  if (label.includes('snow')) return 'Snowy';
  if (label.includes('storm')) return 'Stormy';
  
  return weatherLabel.charAt(0).toUpperCase() + weatherLabel.slice(1);
};

function App() {
  const [selectedLocation, setSelectedLocation] = useState('');
  const [forecast, setForecast] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchForecast = async (location) => {
    if (!location) {
      setForecast(null);
      return;
    }
    
    setLoading(true);
    setError(null);
    try {
      // Need to use the backend URL, assuming it runs on localhost:8000
      const response = await axios.get(`http://127.0.0.1:8000/forecast/${location}`);
      setForecast(response.data.forecast);
    } catch (err) {
      console.error(err);
      setError('Failed to fetch forecast. Is the backend running?');
    } finally {
      setLoading(false);
    }
  };

  const handleLocationChange = (e) => {
    const loc = e.target.value;
    setSelectedLocation(loc);
    fetchForecast(loc);
  };

  return (
    <div className="app-container">
      <div className="header">
        <h1>Weather Forecast</h1>
        <p>7-Day AI Predictions</p>
      </div>

      <div className="controls-card">
        <div className="select-wrapper">
          <select 
            value={selectedLocation} 
            onChange={handleLocationChange}
            className="location-select"
          >
            <option value="" disabled>Select a location</option>
            {LOCATIONS.map(loc => (
              <option key={loc.id} value={loc.id}>{loc.name}</option>
            ))}
          </select>
          <ChevronDown className="select-icon" size={20} />
        </div>
      </div>

      {loading && (
        <div className="loading-container">
          <Loader2 size={40} className="animate-spin" />
          <p>Analyzing AI predictions...</p>
        </div>
      )}

      {error && (
        <div style={{ color: '#ef4444', marginTop: '1rem' }}>
          {error}
        </div>
      )}

      {!loading && forecast && (
        <div className="forecast-grid">
          {forecast.map((dayData, index) => {
            const date = new Date(dayData.date);
            const isToday = index === 0;
            const dayName = isToday ? 'Today' : date.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' });
            
            return (
              <div key={index} className="forecast-card" style={{ animationDelay: `${index * 0.1}s` }}>
                <div className="card-header">
                  <span className="day-label">{dayName}</span>
                  <div className="weather-icon-container">
                    {getWeatherIcon(dayData.weather)}
                  </div>
                </div>
                
                <div className="temp-details">
                  <div className="temp-item">
                    <span className="temp-label">Min</span>
                    <span className="temp-value min">{dayData.min_temp.toFixed(1)}°C</span>
                  </div>
                  <div className="temp-item" style={{ alignItems: 'flex-end' }}>
                    <span className="temp-label">Max</span>
                    <span className="temp-value max">{dayData.max_temp.toFixed(1)}°C</span>
                  </div>
                </div>

                <div className="weather-desc">
                  <span style={{width: '8px', height: '8px', borderRadius: '50%', background: 'var(--accent-1)'}}></span>
                  {getWeatherDescription(dayData.weather)}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

export default App;
