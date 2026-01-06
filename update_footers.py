#!/usr/bin/env python3
import os
import re

NEW_FOOTER = '''<footer class="site-footer">
    <div class="footer-container">
      <div class="footer-section">
        <h4>ℹ️ Informacje</h4>
        <ul>
          <li><a href="{% url 'info' %}">O nas</a></li>
          <li><a href="{% url 'info' %}#godziny-otwarcia">Godziny otwarcia</a></li>
          <li><a href="{% url 'kontakt' %}">Kontakt</a></li>
          <li><a href="{% url 'faq' %}">FAQ</a></li>
        </ul>
      </div>

      <div class="footer-section">
        <h4>📍 Lokalizacja</h4>
        <div id="map" class="map-container"></div>
      </div>

      <div class="footer-section">
        <h4>📱 Media Społecznościowe</h4>
        <div class="social-links">
          <a href="https://facebook.com" target="_blank" rel="noopener" class="social-icon" title="Facebook">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
          </a>
          <a href="https://instagram.com" target="_blank" rel="noopener" class="social-icon" title="Instagram">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0m0 2.16c2.716 0 3.05.01 4.122.06 1.065.049 1.644.228 2.025.379.51.197.873.434 1.255.816.382.382.619.745.816 1.255.151.381.33.96.379 2.025.05 1.072.06 1.406.06 4.122 0 2.716-.01 3.05-.06 4.122-.049 1.065-.228 1.644-.379 2.025-.197.51-.434.873-.816 1.255-.382.382-.745.619-1.255.816-.381.151-.96.33-2.025.379-1.072.05-1.406.06-4.122.06-2.716 0-3.05-.01-4.122-.06-1.065-.049-1.644-.228-2.025-.379-.51-.197-.873-.434-1.255-.816-.382-.382-.619-.745-.816-1.255-.151-.381-.33-.96-.379-2.025-.05-1.072-.06-1.406-.06-4.122 0-2.716.01-3.05.06-4.122.049-1.065.228-1.644.379-2.025.197-.51.434-.873.816-1.255.382-.382.745-.619 1.255-.816.381-.151.96-.33 2.025-.379 1.072-.05 1.406-.06 4.122-.06m0 3.697c-2.9 0-5.252 2.353-5.252 5.252 0 2.9 2.353 5.252 5.252 5.252 2.9 0 5.252-2.353 5.252-5.252 0-2.9-2.353-5.252-5.252-5.252m0 8.666c-1.886 0-3.414-1.529-3.414-3.414 0-1.886 1.529-3.414 3.414-3.414 1.887 0 3.414 1.529 3.414 3.414 0 1.886-1.527 3.414-3.414 3.414m5.464-8.993c0 .678-.549 1.227-1.227 1.227-.678 0-1.228-.549-1.228-1.227s.55-1.227 1.228-1.227c.678 0 1.227.549 1.227 1.227"/></svg>
          </a>
          <a href="https://x.com" target="_blank" rel="noopener" class="social-icon" title="X">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24h-6.627l-5.1-6.694-5.867 6.694h-3.306l7.73-8.835L2.882 2.25h6.791l4.623 6.11 5.348-6.11zM17.15 18.738h1.828L5.966 4.156H4.081l13.069 14.582z"/></svg>
          </a>
          <a href="https://youtube.com" target="_blank" rel="noopener" class="social-icon" title="YouTube">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
          </a>
        </div>
      </div>
    </div>

    <div class="footer-bottom">
      <p><span id="year"></span> 🎬 Kino — Wszelkie prawa zastrzeżone.</p>
      <p style="font-size: 0.8rem; margin-top: 0.5rem;">
        <a href="{% url 'polityka' %}">Polityka prywatności</a> | 
        <a href="{% url 'regulamin' %}">Regulamin</a> | 
        <a href="{% url 'cookies' %}">Cookies</a>
      </p>
    </div>
  </footer>

  <script src="{% static 'js/main.js' %}"></script>
<script>
document.addEventListener('DOMContentLoaded', function() {
  const mapContainer = document.getElementById('map');
  if (mapContainer && typeof L !== 'undefined') {
    const randomLat = 52.0 + (Math.random() - 0.5) * 0.15;
    const randomLng = 21.0 + (Math.random() - 0.5) * 0.15;
    
    const map = L.map('map').setView([randomLat, randomLng], 13);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors',
      maxZoom: 19
    }).addTo(map);
    
    L.marker([randomLat, randomLng]).addTo(map)
      .bindPopup('📍 Nasze kino w Warszawie');
  }
});
</script>'''

templates_dir = 'templates'
count = 0
updated = []

for root, dirs, files in os.walk(templates_dir):
    for file in files:
        if file.endswith('.html') and file != 'index.html':
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            old_content = content
            content = re.sub(r'<footer.*?</script>\n</body>', NEW_FOOTER + '\n</body>', content, flags=re.DOTALL)
            content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
            
            if content != old_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                updated.append(filepath)
                count += 1
                print(f'Updated: {filepath}')

print(f'\nTotal files updated: {count}')
