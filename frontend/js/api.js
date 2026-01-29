// API helper functions for IFRS

class APIClient {
  constructor(baseUrl) {
    this.baseUrl = baseUrl;
  }

  /**
   * Generic GET request handler
   */
  async get(endpoint) {
    try {
      const response = await fetch(this.baseUrl + endpoint);
      if (!response.ok) {
        throw new Error(`HTTP Error: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error(`GET ${endpoint} failed:`, error);
      throw error;
    }
  }

  /**
   * Generic POST request handler with FormData
   */
  async postFormData(endpoint, formData) {
    try {
      const response = await fetch(this.baseUrl + endpoint, {
        method: 'POST',
        body: formData
      });
      if (!response.ok) {
        throw new Error(`HTTP Error: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error(`POST ${endpoint} failed:`, error);
      throw error;
    }
  }

  /**
   * Generic POST request handler with JSON
   */
  async post(endpoint, data) {
    try {
      const response = await fetch(this.baseUrl + endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });
      if (!response.ok) {
        throw new Error(`HTTP Error: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error(`POST ${endpoint} failed:`, error);
      throw error;
    }
  }
}

// Create global API client instance
const api = new APIClient(CONFIG.API_BASE_URL);

/**
 * Get system statistics
 */
async function getStats() {
  try {
    return await api.get(CONFIG.ENDPOINTS.STATS);
  } catch (error) {
    console.error('Failed to fetch stats:', error);
    return null;
  }
}

/**
 * Get all alerts
 */
async function getAlerts() {
  try {
    const data = await api.get(CONFIG.ENDPOINTS.ALERTS);
    return Array.isArray(data) ? data : [];
  } catch (error) {
    console.error('Failed to fetch alerts:', error);
    return [];
  }
}

/**
 * Get all criminals with photos
 */
async function getCriminals() {
  try {
    const data = await api.get(CONFIG.ENDPOINTS.GET_CRIMINALS);
    return Array.isArray(data) ? data : [];
  } catch (error) {
    console.error('Failed to fetch criminals:', error);
    return [];
  }
}

/**
 * Get surveillance status
 */
async function getSurveillanceStatus() {
  try {
    return await api.get(CONFIG.ENDPOINTS.SURVEILLANCE_STATUS);
  } catch (error) {
    console.error('Failed to get surveillance status:', error);
    return { running: false, alerts_count: 0 };
  }
}

/**
 * Start surveillance
 */
async function startSurveillanceAPI() {
  try {
    return await api.get(CONFIG.ENDPOINTS.START_SURVEILLANCE);
  } catch (error) {
    console.error('Failed to start surveillance:', error);
    throw error;
  }
}

/**
 * Stop surveillance
 */
async function stopSurveillanceAPI() {
  try {
    return await api.get(CONFIG.ENDPOINTS.STOP_SURVEILLANCE);
  } catch (error) {
    console.error('Failed to stop surveillance:', error);
    throw error;
  }
}

/**
 * Upload criminal image and data
 */
async function uploadCriminal(name, file) {
  try {
    const formData = new FormData();
    formData.append('name', name);
    formData.append('file', file);

    return await api.postFormData(CONFIG.ENDPOINTS.UPLOAD_CRIMINAL, formData);
  } catch (error) {
    console.error('Failed to upload criminal:', error);
    throw error;
  }
}

/**
 * Retry logic helper
 */
async function retryWithBackoff(fn, maxRetries = 3, delay = 1000) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise(resolve => setTimeout(resolve, delay * Math.pow(2, i)));
    }
  }
}

