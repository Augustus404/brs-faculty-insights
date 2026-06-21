import requests
import json

URL = "https://zacdgymntnrmwwldpdku.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InphY2RneW1udG5ybXd3bGRwZGt1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODAzMTU1NzgsImV4cCI6MjA5NTg5MTU3OH0.m8UWSfTancun4yOHr5a8jkdfeufF9cEp5vjyersUJ38"

headers = {
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json"
}

def get_table(name, select="*"):
    print(f"Fetching {name}...")
    response = requests.get(f"{URL}/rest/v1/{name}?select={select}", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch {name}: {response.status_code}")
        return []

faculty = get_table("faculty")
stats = get_table("faculty_stats")

# Create a mapping by faculty_id
stats_map = {str(s.get('faculty_id')): s for s in stats}

vitfac_data = {}

for f in faculty:
    fid = str(f.get('id'))
    name = f.get('name', 'Unknown')
    f_stats = stats_map.get(fid, {})
    
    vitfac_data[name] = {
        'designation': f.get('designation'),
        'w_pct': f_stats.get('w_pct', 0),
        'total_reviews': f_stats.get('total_reviews', 0),
        'avg_lecture': f_stats.get('avg_lecture', 0),
        'avg_vibe': f_stats.get('avg_vibe', 0),
        'top_lore': f_stats.get('top_lore', {})
    }

with open('vitfac_data.json', 'w', encoding='utf-8') as out:
    json.dump(vitfac_data, out, indent=4)

print(f"Saved {len(vitfac_data)} faculty records to vitfac_data.json")
