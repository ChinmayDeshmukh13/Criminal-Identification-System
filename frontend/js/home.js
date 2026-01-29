// Home/Dashboard page logic

let dashboardIntervals = {
  stats: null,
  alerts: null
};

/**
 * Initialize the dashboard
 */
function initializeDashboard() {
  // Clear any existing intervals
  clearDashboardIntervals();

  // Load initial data
  loadDashboardStats();
  loadDashboardAlerts();

  // Set up auto-refresh intervals
  dashboardIntervals.stats = setInterval(loadDashboardStats, CONFIG.STATS_REFRESH_INTERVAL);
  dashboardIntervals.alerts = setInterval(loadDashboardAlerts, CONFIG.ALERTS_REFRESH_INTERVAL);
}

/**
 * Load and display system statistics
 */
async function loadDashboardStats() {
  try {
    const stats = await getStats();
    
    if (stats) {
      document.getElementById('stat-cameras').innerText = stats.connected_cameras || '–';
      document.getElementById('stat-criminals').innerText = stats.total_criminals || '–';
      document.getElementById('stat-faces').innerText = stats.faces_detected_today || '–';
      document.getElementById('stat-detected').innerText = stats.criminals_detected || '–';
    }
  } catch (error) {
    console.error('Failed to load stats:', error);
    // Show error state
    ['stat-cameras', 'stat-criminals', 'stat-faces', 'stat-detected'].forEach(id => {
      document.getElementById(id).innerText = '⚠️ Error';
    });
  }
}

/**
 * Load and display recent alerts
 */
async function loadDashboardAlerts() {
  try {
    const alerts = await getAlerts();
    const alertList = document.getElementById('alertList');
    
    if (!alertList) return;

    // Get most recent alerts
    const recentAlerts = alerts.slice(-CONFIG.MAX_ALERT_DISPLAY).reverse();

    if (recentAlerts.length === 0) {
      alertList.innerHTML = '<p class="loading">No alerts yet</p>';
      return;
    }

    alertList.innerHTML = recentAlerts.map(alert => {
      const timestamp = new Date(alert.timestamp || Date.now()).toLocaleTimeString();
      return `
        <div class="alert">
          <div class="alert-icon">🚨</div>
          <div class="alert-content">
            <div class="alert-name">${alert.name || 'Unknown'}</div>
            <div class="alert-time">Camera ${alert.camera || '–'} | Confidence: ${alert.confidence || '–'} | ${timestamp}</div>
          </div>
        </div>
      `;
    }).join('');
  } catch (error) {
    console.error('Failed to load alerts:', error);
    document.getElementById('alertList').innerHTML = '<p class="loading">Failed to load alerts</p>';
  }
}

/**
 * Clear all dashboard intervals
 */
function clearDashboardIntervals() {
  if (dashboardIntervals.stats) clearInterval(dashboardIntervals.stats);
  if (dashboardIntervals.alerts) clearInterval(dashboardIntervals.alerts);
  dashboardIntervals = { stats: null, alerts: null };
}
