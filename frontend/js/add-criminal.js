// Add Criminal page logic

/**
 * Handle image preview
 */
function handleImagePreview(event) {
  const file = event.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = (e) => {
    const preview = document.getElementById('imagePreview');
    const previewImg = document.getElementById('previewImg');
    
    previewImg.src = e.target.result;
    preview.style.display = 'block';
  };
  reader.readAsDataURL(file);
}

/**
 * Handle add criminal form submission
 */
async function handleAddCriminal(event) {
  event.preventDefault();

  const nameInput = document.getElementById('criminalName');
  const fileInput = document.getElementById('criminalImage');
  const statusDiv = document.getElementById('uploadStatus');
  const submitBtn = event.target.querySelector('button[type="submit"]');

  const name = nameInput.value.trim();
  const file = fileInput.files[0];

  // Validation
  if (!name) {
    showUploadStatus('Please enter a name', 'error', statusDiv);
    return;
  }

  if (!file) {
    showUploadStatus('Please select an image', 'error', statusDiv);
    return;
  }

  // Validate file type
  if (!file.type.startsWith('image/')) {
    showUploadStatus('Please upload an image file', 'error', statusDiv);
    return;
  }

  // Validate file size (max 5MB)
  if (file.size > 5 * 1024 * 1024) {
    showUploadStatus('Image must be smaller than 5MB', 'error', statusDiv);
    return;
  }

  // Disable button and show loading state
  submitBtn.disabled = true;
  submitBtn.innerText = '⏳ Uploading...';

  try {
    showUploadStatus('Uploading criminal data...', 'info', statusDiv);

    const result = await uploadCriminal(name, file);

    if (result.error) {
      throw new Error(result.error);
    }

    // Success
    showUploadStatus(`✅ Successfully added ${name} to database!`, 'success', statusDiv);

    // Reset form
    event.target.reset();
    document.getElementById('imagePreview').style.display = 'none';
    nameInput.focus();

    // Auto-clear success message after 5 seconds
    setTimeout(() => {
      statusDiv.style.display = 'none';
    }, 5000);

  } catch (error) {
    console.error('Upload failed:', error);
    showUploadStatus(`❌ Error: ${error.message || 'Failed to add criminal'}`, 'error', statusDiv);
  } finally {
    submitBtn.disabled = false;
    submitBtn.innerText = '✅ Add Criminal';
  }
}

/**
 * Show upload status message
 */
function showUploadStatus(message, type, element) {
  element.innerHTML = message;
  element.className = `status-message ${type}`;
  element.style.display = 'block';
}

/**
 * Load criminal records
 */
async function loadCriminalRecords() {
  const container = document.getElementById('criminalsList');
  
  try {
    container.innerHTML = '<p class="loading">Loading criminals...</p>';
    
    const criminals = await getCriminals();

    if (!criminals || criminals.length === 0) {
      container.innerHTML = '<p class="loading">No criminal records found</p>';
      return;
    }

    container.innerHTML = criminals.map(criminal => {
      const photoSrc = criminal.photo 
        ? `data:image/jpeg;base64,${criminal.photo}`
        : 'https://via.placeholder.com/250?text=No+Image';
      
      const addedDate = criminal.added_date 
        ? new Date(criminal.added_date * 1000).toLocaleDateString()
        : 'Unknown';
      
      return `
        <div class="criminal-card">
          <img src="${photoSrc}" alt="${criminal.name}" onerror="this.src='https://via.placeholder.com/250?text=Error'">
          <h3>${escapeHtml(criminal.name)}</h3>
          <p>Added: ${addedDate}</p>
        </div>
      `;
    }).join('');
  } catch (error) {
    console.error('Failed to load criminals:', error);
    container.innerHTML = '<p class="loading">Failed to load criminal records</p>';
  }
}

/**
 * Load all alerts
 */
async function loadAllAlerts() {
  const container = document.getElementById('alertsContainer');
  
  try {
    container.innerHTML = '<p class="loading">Loading alerts...</p>';
    
    const alerts = await getAlerts();

    if (!alerts || alerts.length === 0) {
      container.innerHTML = '<p class="loading">No alerts recorded</p>';
      return;
    }

    // Reverse to show newest first
    const sortedAlerts = [...alerts].reverse();

    container.innerHTML = sortedAlerts.map(alert => {
      const timestamp = new Date(alert.timestamp || alert.time || Date.now());
      const timeString = timestamp.toLocaleString();
      
      const photoSrc = alert.photo
        ? `data:image/jpeg;base64,${alert.photo}`
        : 'https://via.placeholder.com/100?text=No+Image';
      
      return `
        <div class="alert-item critical">
          <img src="${photoSrc}" alt="${alert.name}" class="alert-photo" onerror="this.src='https://via.placeholder.com/100?text=Error'">
          <div class="alert-info">
            <h4>🚨 ${escapeHtml(alert.name || 'Unknown')}</h4>
            <p>Camera: ${alert.camera || 'Unknown'} | Confidence: ${((alert.confidence || 0) * 100).toFixed(2)}%</p>
          </div>
          <div class="alert-time">${timeString}</div>
        </div>
      `;
    }).join('');
  } catch (error) {
    console.error('Failed to load alerts:', error);
    container.innerHTML = '<p class="loading">Failed to load alerts</p>';
  }
}

/**
 * Filter alerts by time period
 */
function filterAlerts(period) {
  // Update active button
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.classList.remove('active');
  });
  event.target.classList.add('active');

  const container = document.getElementById('alertsContainer');
  const now = new Date();
  let filterDate;

  if (period === 'today') {
    filterDate = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  } else if (period === 'week') {
    filterDate = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
  }

  // Reload and filter alerts
  getAlerts().then(alerts => {
    let filtered = alerts;

    if (filterDate) {
      filtered = alerts.filter(a => {
        const alertDate = new Date(a.timestamp || a.time || Date.now());
        return alertDate >= filterDate;
      });
    }

    if (filtered.length === 0) {
      container.innerHTML = '<p class="loading">No alerts for this period</p>';
      return;
    }

    const sortedAlerts = [...filtered].reverse();
    container.innerHTML = sortedAlerts.map(alert => {
      const timestamp = new Date(alert.timestamp || alert.time || Date.now());
      const timeString = timestamp.toLocaleString();
      
      const photoSrc = alert.photo
        ? `data:image/jpeg;base64,${alert.photo}`
        : 'https://via.placeholder.com/100?text=No+Image';
      
      return `
        <div class="alert-item critical">
          <img src="${photoSrc}" alt="${alert.name}" class="alert-photo" onerror="this.src='https://via.placeholder.com/100?text=Error'">
          <div class="alert-info">
            <h4>🚨 ${escapeHtml(alert.name || 'Unknown')}</h4>
            <p>Camera: ${alert.camera || 'Unknown'} | Confidence: ${((alert.confidence || 0) * 100).toFixed(2)}%</p>
          </div>
          <div class="alert-time">${timeString}</div>
        </div>
      `;
    }).join('');
  });
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
  const div = document.createElement('div');
  div.innerText = text;
  return div.innerHTML;
}

// Attach event listener to file input
document.addEventListener('DOMContentLoaded', () => {
  const fileInput = document.getElementById('criminalImage');
  if (fileInput) {
    fileInput.addEventListener('change', handleImagePreview);
  }
});
