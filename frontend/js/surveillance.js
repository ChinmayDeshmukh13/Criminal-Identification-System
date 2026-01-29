// Surveillance page logic

let surveillanceActive = false;
let surveillanceIntervals = [];
let detectionCount = 0;
let statusCheckInterval = null;
let snapshotInterval = null;
let canvas = null;
let canvasCtx = null;

/**
 * Initialize the surveillance page
 */
function initializeSurveillance() {
  // Update button states
  updateSurveillanceButtonState();
  
  // Load initial surveillance status
  checkSurveillanceStatus();
  
  // Start periodic status checks
  if (statusCheckInterval) clearInterval(statusCheckInterval);
  statusCheckInterval = setInterval(checkSurveillanceStatus, 3000);
}

/**
 * Check current surveillance status
 */
async function checkSurveillanceStatus() {
  try {
    const status = await getSurveillanceStatus();
    if (status.running && !surveillanceActive) {
      // Surveillance was started externally
      surveillanceActive = true;
      detectionCount = status.alerts_count || 0;
      updateSurveillanceButtonState();
      document.getElementById('surveillance-status-text').innerText = 'Running';
      document.getElementById('surveillance-status').className = 'status-badge active';
      document.getElementById('surveillance-status').innerText = '● Live';
      document.getElementById('detection-count').innerText = detectionCount;
      startStatusUpdates();
    } else if (!status.running && surveillanceActive) {
      // Surveillance was stopped externally
      surveillanceActive = false;
      updateSurveillanceButtonState();
      document.getElementById('surveillance-status-text').innerText = 'Stopped';
      document.getElementById('surveillance-status').className = 'status-badge inactive';
      document.getElementById('surveillance-status').innerText = '● Stopped';
      stopStatusUpdates();
    }
  } catch (error) {
    console.error('Failed to check surveillance status:', error);
  }
}

/**
 * Start surveillance
 */
async function startSurveillance() {
  if (surveillanceActive) {
    showNotification('Surveillance is already running', 'info');
    return;
  }

  try {
    const btn = document.getElementById('btn-start-surveillance');
    btn.disabled = true;
    btn.innerText = 'Starting...';

    const result = await startSurveillanceAPI();

    if (result && (result.status === 'surveillance started' || !result.error)) {
      surveillanceActive = true;
      detectionCount = 0;
      updateSurveillanceButtonState();

      // Update status display
      document.getElementById('surveillance-status-text').innerText = 'Running';
      document.getElementById('surveillance-status').className = 'status-badge active';
      document.getElementById('surveillance-status').innerText = '● Live';
      document.getElementById('detection-count').innerText = '0';

      showNotification('✅ Surveillance started successfully!', 'success');
      
      // Start status updates
      startStatusUpdates();
        // Start fetching snapshots for live preview
        startVideoStreamPolling();
    } else {
      throw new Error(result.error || 'Failed to start surveillance');
    }
  } catch (error) {
    console.error('Failed to start surveillance:', error);
    showNotification('❌ Failed to start surveillance: ' + error.message, 'error');
    document.getElementById('btn-start-surveillance').disabled = false;
    document.getElementById('btn-start-surveillance').innerText = '▶️ Start Surveillance';
  }
}

/**
 * Stop surveillance
 */
async function stopSurveillance() {
  try {
    const btn = document.getElementById('btn-stop-surveillance');
    btn.disabled = true;
    btn.innerText = 'Stopping...';

    const result = await stopSurveillanceAPI();

    if (result && (result.status === 'surveillance stopped' || !result.error)) {
      surveillanceActive = false;
      updateSurveillanceButtonState();

      // Update status display
      document.getElementById('surveillance-status-text').innerText = 'Stopped';
      document.getElementById('surveillance-status').className = 'status-badge inactive';
      document.getElementById('surveillance-status').innerText = '● Stopped';

      // Clear intervals
      stopStatusUpdates();

      showNotification('Surveillance stopped', 'success');
    } else {
      throw new Error(result.error || 'Failed to stop surveillance');
    }
  } catch (error) {
    console.error('Failed to stop surveillance:', error);
    showNotification('Failed to stop surveillance: ' + error.message, 'error');
    document.getElementById('btn-stop-surveillance').disabled = false;
    document.getElementById('btn-stop-surveillance').innerText = '⏹️ Stop Surveillance';
  }
}

/**
 * Fetch latest camera snapshot from backend and draw to canvas
 */
async function fetchAndDrawFrame() {
  try {
    if (!canvasCtx) {
      canvas = document.getElementById('videoCanvas');
      if (!canvas) return;
      canvasCtx = canvas.getContext('2d');
    }

    const url = getApiUrl(CONFIG.ENDPOINTS.CAMERA_SNAPSHOT);
    const res = await fetch(url, { cache: 'no-store' });
    if (!res.ok) return;

    const blob = await res.blob();
    const img = await createImageBitmap(blob);
    // Fit image to canvas
    canvasCtx.clearRect(0, 0, canvas.width, canvas.height);
    canvasCtx.drawImage(img, 0, 0, canvas.width, canvas.height);
  } catch (err) {
    // Silent fail - snapshot may not be ready yet
    // console.debug('snapshot error', err);
  }
}

function startVideoStreamPolling() {
  stopVideoStreamPolling();
  // immediate fetch
  fetchAndDrawFrame();
  snapshotInterval = setInterval(fetchAndDrawFrame, CONFIG.SURVEILLANCE_UPDATE_INTERVAL);
}

function stopVideoStreamPolling() {
  if (snapshotInterval) {
    clearInterval(snapshotInterval);
    snapshotInterval = null;
  }
}

/**
 * Start status update intervals
 */
function startStatusUpdates() {
  // Clear existing intervals
  stopStatusUpdates();
  
  // Update alerts and detection count every 2 seconds
  const updateInterval = setInterval(async () => {
    if (!surveillanceActive) {
      clearInterval(updateInterval);
      return;
    }
    
    try {
      const alerts = await getAlerts();
      const newCount = alerts.length;
      
      if (newCount > detectionCount) {
        detectionCount = newCount;
        document.getElementById('detection-count').innerText = detectionCount;
        
        // Play a subtle notification
        showNotification(`🚨 Detection! ${alerts[alerts.length - 1].name} detected`, 'warning');
      }
    } catch (error) {
      console.error('Error updating alerts:', error);
    }
  }, 2000);
  
  surveillanceIntervals.push(updateInterval);
}

/**
 * Stop status update intervals
 */
function stopStatusUpdates() {
  surveillanceIntervals.forEach(id => clearInterval(id));
  surveillanceIntervals = [];
}

/**
 * Update button visibility based on surveillance state
 */
function updateSurveillanceButtonState() {
  const startBtn = document.getElementById('btn-start-surveillance');
  const stopBtn = document.getElementById('btn-stop-surveillance');

  if (surveillanceActive) {
    startBtn.style.display = 'none';
    stopBtn.style.display = 'flex';
    stopBtn.disabled = false;
  } else {
    startBtn.style.display = 'flex';
    startBtn.disabled = false;
    stopBtn.style.display = 'none';
  }
}

/**
 * Display a notification message
 */
function showNotification(message, type = 'info') {
  // Create notification element
  const notification = document.createElement('div');
  notification.className = `notification notification-${type}`;
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 16px 20px;
    background: ${type === 'success' ? '#064e3b' : type === 'error' ? '#7f1d1d' : type === 'warning' ? '#78350f' : '#1e293b'};
    color: ${type === 'success' ? '#86efac' : type === 'error' ? '#fca5a5' : type === 'warning' ? '#fcd34d' : '#cbd5f5'};
    border-radius: 8px;
    border-left: 4px solid ${type === 'success' ? '#22c55e' : type === 'error' ? '#ef4444' : type === 'warning' ? '#f59e0b' : '#0ea5e9'};
    z-index: 10000;
    animation: slideIn 0.3s ease;
    max-width: 400px;
  `;
  notification.innerText = message;

  document.body.appendChild(notification);

  // Auto-remove after 5 seconds
  setTimeout(() => {
    notification.style.animation = 'slideOut 0.3s ease';
    setTimeout(() => notification.remove(), 300);
  }, 5000);
}

// Add animation styles if not already present
if (!document.getElementById('notification-styles')) {
  const style = document.createElement('style');
  style.id = 'notification-styles';
  style.innerHTML = `
    @keyframes slideIn {
      from {
        transform: translateX(400px);
        opacity: 0;
      }
      to {
        transform: translateX(0);
        opacity: 1;
      }
    }

    @keyframes slideOut {
      from {
        transform: translateX(0);
        opacity: 1;
      }
      to {
        transform: translateX(400px);
        opacity: 0;
      }
    }
  `;
  document.head.appendChild(style);
}

