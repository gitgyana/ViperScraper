var existingPopup = document.getElementById('scraper-popup');
var existingOverlay = document.getElementById('scraper-blur-overlay');
var existingStyle = document.getElementById('scraper-style');

if (existingPopup) existingPopup.remove();
if (existingOverlay) existingOverlay.remove();
if (existingStyle) existingStyle.remove();

// Blur overlay
var overlay = document.createElement('div');
overlay.id = 'scraper-blur-overlay';
overlay.style.cssText = `
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    backdrop-filter: blur(8px);
    background-color: rgba(0,0,0,0.2);
    z-index: 99998;
`;

// Popup
var popup = document.createElement('div');
popup.id = 'scraper-popup';
popup.innerHTML = `
    <div id="scraper-popup-close" style="position:absolute;top:10px;right:15px;cursor:pointer;font-size:18px;">✖</div>
    <div>py__message__</div>
`;
popup.style.cssText = `
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px 30px;
    border-radius: 10px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    font-family: Arial, sans-serif;
    font-size: 18px;
    font-weight: bold;
    z-index: 99999;
    animation: slideIn 0.5s ease-out;
    min-width: 320px;
    text-align: center;
`;

// Animation
var style = document.createElement('style');
style.id = 'scraper-style';
style.textContent = `
    @keyframes slideIn {
        from { transform: translate(-50%, -60%); opacity: 0; }
        to { transform: translate(-50%, -50%); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translate(-50%, -50%); opacity: 1; }
        to { transform: translate(-50%, -60%); opacity: 0; }
    }
`;

document.head.appendChild(style);
document.body.appendChild(overlay);
document.body.appendChild(popup);

document.getElementById('scraper-popup-close').onclick = function () {
    popup.style.animation = 'slideOut 0.5s ease-out';
    setTimeout(() => {
        popup.remove();
        overlay.remove();
        style.remove();
    }, 500);
};
