// Configuration file for the IFRS frontend

const CONFIG = {
  // API Base URL
  API_BASE_URL: 'http://127.0.0.1:8000',
  
  // Polling intervals (in milliseconds)
  STATS_REFRESH_INTERVAL: 5000,     // 5 seconds
  ALERTS_REFRESH_INTERVAL: 3000,    // 3 seconds
  SURVEILLANCE_UPDATE_INTERVAL: 500, // 500ms for smooth updates
  
  // UI Settings
  MAX_ALERT_DISPLAY: 10,
  ALERT_ANIMATION_DURATION: 300,
  
  // API Endpoints
  ENDPOINTS: {
    STATS: '/stats',
    ALERTS: '/alerts',
    START_SURVEILLANCE: '/start_surveillance/',
    STOP_SURVEILLANCE: '/stop_surveillance/',
    SURVEILLANCE_STATUS: '/surveillance_status/',
    CAMERA_SNAPSHOT: '/camera_snapshot/',
    UPLOAD_CRIMINAL: '/upload_criminal/',
    GET_CRIMINALS: '/criminals',
    GET_ALERTS: '/alerts'
  }
};

// Utility function to get full API URL
function getApiUrl(endpoint) {
  return CONFIG.API_BASE_URL + endpoint;
}

