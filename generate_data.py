import json
import re

with open('teacher_data.json', 'r', encoding='utf-8') as f:
    teachers_data = json.load(f)

with open('vitfac_data.json', 'r', encoding='utf-8') as f:
    vitfac_data = json.load(f)

positive_words = ['good', 'great', 'excellent', 'best', 'goat', 'nice', 'friendly', 'helpful', 'chill', 'lenient', 'marks', 'easy', 'fair', 'awesome', 'amazing']
negative_words = ['strict', 'bad', 'worst', 'avoid', 'terrible', 'hard', 'tough', 'boring', 'toxic', 'don\'t', 'dont', 'mat len', 'galti', 'poor', 'run']

results = []
processed_names = set()

def get_vitfac_lore(lore_obj, lore_type):
    if not isinstance(lore_obj, dict):
        if isinstance(lore_obj, str):
            try:
                lore_obj = json.loads(lore_obj)
            except:
                return []
        else:
            return []
    if not isinstance(lore_obj, dict):
        return []
    items = lore_obj.get(lore_type, [])
    if isinstance(items, list):
        return [item['text'] if isinstance(item, dict) and 'text' in item else str(item) for item in items]
    return []

# Helper to normalize names
def norm_name(n):
    return re.sub(r'[^a-z]', '', n.lower())

vitfac_norm_map = {norm_name(k): k for k in vitfac_data.keys()}

# First process all teachers from Excel/WhatsApp
for teacher, data in teachers_data.items():
    processed_names.add(teacher)
    t_norm = norm_name(teacher)
    
    messages = data['courses'] # wait, no, messages is messages
    messages = data['messages']
    courses = data['courses']
    slots = data['slots']
    
    pos_count = 0
    neg_count = 0
    merits = []
    demerits = []
    
    for msg in messages:
        msg_lower = msg.lower()
        is_pos = False
        is_neg = False
        
        for word in positive_words:
            if re.search(r'\b' + word + r'\b', msg_lower):
                pos_count += 1
                is_pos = True
                
        for word in negative_words:
            if re.search(r'\b' + word + r'\b', msg_lower):
                neg_count += 1
                is_neg = True
                
        if is_pos and msg not in merits and len(merits) < 2:
            merits.append(msg)
        if is_neg and msg not in demerits and len(demerits) < 2:
            demerits.append(msg)
            
    total = pos_count + neg_count
    score = 'N/A'
    remarks = 'not available'
    if total > 0:
        score_val = 5 + (pos_count - neg_count) / total * 5
        score = round(max(0, min(10, score_val)), 1)
        if score > 7: remarks = "Highly recommended by seniors."
        elif score > 4: remarks = "Mixed reviews. Proceed with caution."
        else: remarks = "Generally avoided by seniors."
    
    # Check if in vitfac
    vitfac_info = None
    if t_norm in vitfac_norm_map:
        v_key = vitfac_norm_map[t_norm]
        vitfac_info = vitfac_data[v_key]
        processed_names.add(v_key)
        
        v_green = get_vitfac_lore(vitfac_info['top_lore'], 'green')
        v_red = get_vitfac_lore(vitfac_info['top_lore'], 'red')
        
        for g in v_green:
            if len(merits) < 4: merits.append("VITFac: " + g)
        for r in v_red:
            if len(demerits) < 4: demerits.append("VITFac: " + r)
            
    if not merits: merits = ['No specific merits mentioned.']
    if not demerits: demerits = ['No specific demerits mentioned.']
    
    results.append({
        'name': teacher,
        'courses': courses,
        'slots': slots,
        'score': score,
        'remarks': remarks,
        'merits': merits,
        'demerits': demerits,
        'vitfac': vitfac_info
    })

# Now add remaining from vitfac
for v_name, v_info in vitfac_data.items():
    if v_name in processed_names:
        continue
    if norm_name(v_name) in [norm_name(n) for n in processed_names]:
        continue
        
    v_green = get_vitfac_lore(v_info['top_lore'], 'green')
    v_red = get_vitfac_lore(v_info['top_lore'], 'red')
    
    merits = ["VITFac: " + g for g in v_green]
    demerits = ["VITFac: " + r for r in v_red]
    
    if not merits: merits = ['No specific merits mentioned.']
    if not demerits: demerits = ['No specific demerits mentioned.']
    
    results.append({
        'name': v_name,
        'courses': [],
        'slots': [],
        'score': 'N/A', # Our custom score is N/A
        'remarks': 'Data from VITFac Website',
        'merits': merits[:4],
        'demerits': demerits[:4],
        'vitfac': v_info
    })

with open('data.js', 'w', encoding='utf-8') as f:
    f.write('const teachersData = ' + json.dumps(results, indent=4) + ';')

print("data.js generated with vitfac integration.")
