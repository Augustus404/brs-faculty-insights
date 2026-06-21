import pandas as pd
import json
import re
import os

df = pd.read_excel('BRS Fall 26-27.xlsx')

# Forward fill for merged cells in Excel
df['Course title'] = df['Course title'].ffill()
df['SLOT'] = df['SLOT'].ffill()

# Load WhatsApp messages
chat_files = [
    "WhatsApp Chat with '29 FFCS 1.2.txt", 
    "WhatsApp Chat with '29 FFCS 2.1.txt"
]
all_messages = []
for file in chat_files:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                match = re.search(r'^\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}\s*[apAP][mM] - (.*?): (.*)', line)
                if match:
                    all_messages.append(match.group(2))
                else:
                    if re.search(r'^\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}\s*[apAP][mM] - ', line):
                        continue
                    if all_messages:
                        all_messages[-1] += " " + line.strip()

positive_words = ['good', 'great', 'excellent', 'best', 'goat', 'nice', 'friendly', 'helpful', 'chill', 'lenient', 'marks', 'easy', 'fair', 'awesome', 'amazing']
negative_words = ['strict', 'bad', 'worst', 'avoid', 'terrible', 'hard', 'tough', 'boring', 'toxic', "don't", 'dont', 'mat len', 'galti', 'poor', 'run']

# Load VITFac data
with open('vitfac_data.json', 'r', encoding='utf-8') as f:
    vitfac_data = json.load(f)

def norm_name(n):
    return re.sub(r'[^a-z]', '', n.lower())

vitfac_norm_map = {norm_name(k): k for k in vitfac_data.keys()}

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

teacher_cache = {}

def get_teacher_info(teacher_name):
    if teacher_name in teacher_cache:
        return teacher_cache[teacher_name]
        
    common_parts = {'kumar', 'kumari', 'singh', 'reddy', 'rao', 'das', 'sharma', 'dr', 'dr.', 'prof', 'prof.', 'mr', 'mrs', 'ms'}
    parts = [p for p in teacher_name.split() if len(p) > 2 and p.lower() not in common_parts]
    if not parts:
        parts = [teacher_name.replace(" ", "")]
    question_phrases = [
        'which one', 'who is', 'how is', 'anyone know', 'any idea', 'suggest some', 'is he good', 'is she good', 
        "how's", 'hows', 'any reviews', 'what about', 'any info', 'is he', 'is she', 'should i', 'can i', 'do you', 
        'did anyone', 'has anyone', 'does anyone', 'recommendations for', 'any recommendation', 'tell me about',
        'any review', 'is it easy', 'is it hard', 'looking for', 'suggest a', 'suggest me', 'best pick'
    ]

    messages = []
    for msg in all_messages:
        if len(msg) > 300:
            continue
        if '?' in msg:
            continue
            
        msg_lower = msg.lower()
        
        is_question = False
        for qp in question_phrases:
            if qp in msg_lower:
                is_question = True
                break
                
        if is_question:
            continue

        for part in parts:
            part_lower = part.lower()
            if part_lower in msg_lower:
                # Prevent matching if followed by a different single-letter initial
                matches = re.findall(r'\b' + re.escape(part_lower) + r'\s+([a-z])\b', msg_lower)
                conflict = False
                for m in matches:
                    if m not in ['a', 'i', 'u'] and m not in teacher_name.lower().split():
                        conflict = True
                        break
                
                if not conflict:
                    messages.append(msg)
                    break
                
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

    t_norm = norm_name(teacher_name)
    vitfac_info = None
    if t_norm in vitfac_norm_map:
        v_key = vitfac_norm_map[t_norm]
        vitfac_info = vitfac_data[v_key]
        
        v_green = get_vitfac_lore(vitfac_info['top_lore'], 'green')
        v_red = get_vitfac_lore(vitfac_info['top_lore'], 'red')
        
        for g in v_green:
            if len(merits) < 4: merits.append("VITFac: " + g)
        for r in v_red:
            if len(demerits) < 4: demerits.append("VITFac: " + r)
            
    if not merits: merits = ['No specific merits mentioned.']
    if not demerits: demerits = ['No specific demerits mentioned.']
    
    info = {
        'name': teacher_name,
        'score': score,
        'remarks': remarks,
        'merits': merits,
        'demerits': demerits,
        'vitfac': vitfac_info
    }
    teacher_cache[teacher_name] = info
    return info

courses_dict = {}
processed_teacher_names = set()

for index, row in df.iterrows():
    course = str(row['Course title']).strip()
    slot = str(row['SLOT']).strip()
    if slot == 'nan' or slot == 'NIL':
        lab_slot = str(row['LAB SLOT']).strip()
        if lab_slot != 'nan' and lab_slot != 'NIL':
            slot = lab_slot
    fac_name = str(row['FACULTY NAME']).strip()
    
    if course == 'nan' or fac_name == 'nan':
        continue
        
    if course not in courses_dict:
        courses_dict[course] = {}
        
    if slot not in courses_dict[course]:
        courses_dict[course][slot] = []
        
    teacher_info = get_teacher_info(fac_name)
    processed_teacher_names.add(norm_name(fac_name))
    
    existing = [t['name'] for t in courses_dict[course][slot]]
    if fac_name not in existing:
        courses_dict[course][slot].append(teacher_info)

# Convert to list structure
courses_list = []
for course, slots in courses_dict.items():
    slots_list = []
    for slot, teachers in slots.items():
        slots_list.append({
            'slot_name': slot,
            'teachers': teachers
        })
    courses_list.append({
        'course_name': course,
        'slots': slots_list
    })

with open('data.js', 'w', encoding='utf-8') as f:
    f.write('const coursesData = ' + json.dumps(courses_list, indent=4) + ';')

print("data.js successfully generated with ffill and all teachers.")
