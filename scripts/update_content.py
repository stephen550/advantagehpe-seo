"""
Advantage HPE — Daily SEO Content Updater
Runs via GitHub Actions every morning.
Fetches seasonal/weather signals and refreshes page content via Claude API.
"""

import anthropic
import requests
import json
import os
import re
from datetime import datetime

CITIES = [
    {"name": "Fort Walton Beach", "slug": "fort-walton-beach", "county": "Okaloosa County", "lat": 30.4058, "lon": -86.6187},
    {"name": "Destin", "slug": "destin", "county": "Okaloosa County", "lat": 30.3935, "lon": -86.4958},
    {"name": "Niceville", "slug": "niceville", "county": "Okaloosa County", "lat": 30.5177, "lon": -86.4772},
    {"name": "Navarre", "slug": "navarre", "county": "Santa Rosa County", "lat": 30.4016, "lon": -86.8630},
    {"name": "Crestview", "slug": "crestview", "county": "Okaloosa County", "lat": 30.7460, "lon": -86.5711},
]

# Pages to refresh daily (rotate through to avoid API overuse)
PAGE_TYPES = [
    "ev-charger-installation",
    "generator-installation", 
    "tankless-water-heater-installation",
    "mini-split-installation",
    "no-hot-water",
    "lights-flickering",
]

def get_weather(lat, lon):
    """Get current weather for a city using Open-Meteo (free, no API key)."""
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,weather_code&temperature_unit=fahrenheit&forecast_days=1"
        r = requests.get(url, timeout=10)
        data = r.json()
        current = data.get("current", {})
        temp = current.get("temperature_2m", 75)
        humidity = current.get("relative_humidity_2m", 70)
        return {"temp_f": round(temp), "humidity": humidity}
    except:
        return {"temp_f": 78, "humidity": 72}

def get_season():
    month = datetime.now().month
    if month in [12, 1, 2]: return "winter"
    if month in [3, 4, 5]: return "spring"
    if month in [6, 7, 8]: return "summer"
    return "fall"

def refresh_faq_section(client, page_type, city, weather):
    """Use Claude to generate a fresh, seasonally-relevant FAQ answer."""
    season = get_season()
    temp = weather["temp_f"]
    humidity = weather["humidity"]
    
    prompt = f"""You are writing SEO content for Advantage HPE, an HVAC/Plumbing/Electrical company serving {city['name']}, FL ({city['county']}).

Current conditions in {city['name']}: {temp}°F, {humidity}% humidity, {season} season.
Today's date: {datetime.now().strftime('%B %d, %Y')}

Write ONE fresh FAQ answer (2-3 sentences) for this page type: {page_type}
The question: "Is now a good time to install a {page_type.replace('-', ' ')} in {city['name']}?"

Requirements:
- Mention current temperature or season naturally
- Reference {city['county']} or the Florida Panhandle
- Include a call to action for 850-438-2639
- Sound like a real local contractor, not a robot
- Under 60 words

Return ONLY the answer text, no quotes, no formatting."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=150,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text.strip()

def update_page(page_path, city, page_type, fresh_answer):
    """Inject the fresh FAQ answer into the HTML file."""
    if not os.path.exists(page_path):
        return False
    
    with open(page_path, 'r') as f:
        html = f.read()
    
    # Add/update a "seasonal tip" div after the local-box
    seasonal_block = f'''<div class="local-box" style="margin-top:12px;background:#fff8e1;border-left-color:#f59e0b;">
      <strong>Right Now in {city['name']}:</strong> {fresh_answer}
    </div>'''
    
    # Remove old seasonal block if present
    html = re.sub(r'<div class="local-box" style="margin-top:12px;background:#fff8e1.*?</div>', 
                  '', html, flags=re.DOTALL)
    
    # Insert after local-box
    html = html.replace('</div>\n</div>\n<div class="section">', 
                       f'{seasonal_block}\n</div>\n</div>\n<div class="section">')
    
    with open(page_path, 'w') as f:
        f.write(html)
    
    return True

def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("No ANTHROPIC_API_KEY — skipping content refresh")
        return
    
    client = anthropic.Anthropic(api_key=api_key)
    updated = 0
    
    print(f"Starting daily SEO update — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    # Today's page type to refresh (rotate by day of month)
    day = datetime.now().day
    todays_type = PAGE_TYPES[day % len(PAGE_TYPES)]
    print(f"Today's page type: {todays_type}")
    
    for city in CITIES:
        weather = get_weather(city["lat"], city["lon"])
        print(f"  {city['name']}: {weather['temp_f']}°F, {weather['humidity']}% humidity")
        
        page_path = f"{todays_type}-{city['slug']}/index.html"
        
        if not os.path.exists(page_path):
            print(f"    Skipping — page not found: {page_path}")
            continue
        
        fresh_answer = refresh_faq_section(client, todays_type, city, weather)
        print(f"    Fresh content: {fresh_answer[:80]}...")
        
        if update_page(page_path, city, todays_type, fresh_answer):
            print(f"    ✅ Updated {page_path}")
            updated += 1
    
    print(f"\nComplete: {updated} pages updated")

if __name__ == "__main__":
    main()
