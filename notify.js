var existingPopup = document.getElementById('scraper-popup');
if (existingPopup) {{
    existingPopup.remove();
}}

var popup = document.createElement('div');
popup.id = 'scraper-popup';
popup.innerHTML = '{py__message__}';
popup.style.cssText = `
    position: fixed;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 15px 25px;
    border-radius: 8px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    font-family: Arial, sans-serif;
    font-size: 16px;
    font-weight: bold;
    z-index: 99999;
    animation: slideIn 0.5s ease-out;
    text-align: center;
    min-width: 300px;
`;

var style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {{
from {{ transform: translateX(-50%) translateY(-50px); opacity: 0; }}
to {{ transform: translateX(-50%) translateY(0); opacity: 1; }}
    }}
`;
document.head.appendChild(style);

document.body.appendChild(popup);

setTimeout(function() {{
    if (popup && popup.parentNode) {{
        popup.style.animation = 'slideIn 0.5s ease-out reverse';
        setTimeout(function() {{
            if (popup && popup.parentNode) {{
                popup.remove();
            }}
        }}, 500);
    }}
}}, 5000);
