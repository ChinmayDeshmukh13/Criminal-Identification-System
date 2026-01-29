// Navigation and page switching logic

let currentPage = 'home';
let statsInterval = null;
let alertsInterval = null;

/**
 * Navigate between pages
 */
function navigateTo(page) {
  // Hide all pages
  const pages = document.querySelectorAll('.page');
  pages.forEach(p => p.style.display = 'none');

  // Remove active state from all nav links
  const navLinks = document.querySelectorAll('.nav-link');
  navLinks.forEach(link => link.classList.remove('active'));

  // Show selected page
  const targetPage = document.getElementById(`page-${page}`);
  if (targetPage) {
    targetPage.style.display = 'block';
  }

  // Set active nav link
  const targetLink = document.getElementById(`nav-${page}`);
  if (targetLink) {
    targetLink.classList.add('active');
  }

  currentPage = page;

  // Page-specific initialization
  if (page === 'home') {
    initializeDashboard();
  } else if (page === 'surveillance') {
    initializeSurveillance();
  } else if (page === 'criminals') {
    loadCriminalRecords();
  } else if (page === 'alerts') {
    loadAllAlerts();
  }
}

/**
 * Attach navigation event listeners
 */
function setupNavigation() {
  // Navigation is already set up with onclick handlers in HTML
  // But we can add keyboard shortcuts here if needed
  document.addEventListener('keydown', (e) => {
    if (e.ctrlKey) {
      switch(e.key) {
        case '1': navigateTo('home'); break;
        case '2': navigateTo('surveillance'); break;
        case '3': navigateTo('add-criminal'); break;
        case '4': navigateTo('criminals'); break;
        case '5': navigateTo('alerts'); break;
      }
    }
  });
}

/**
 * Initialize when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', () => {
  setupNavigation();
  navigateTo('home');
});
