import pandas as pd
import re
import json
import os

# 1. Read Excel
df = pd.read_excel('BRS Fall 26-27.xlsx')

# Clean teacher names and build course mapping
teachers_data = {}
for index, row in df.iterrows():
    fac_name = str(row['FACULTY NAME']).strip()
    course = str(row['Course title']).strip()
    slot = str(row['SLOT']).strip()
    
    if fac_name == 'nan' or not fac_name:
        continue
        
    if fac_name not in teachers_data:
        teachers_data[fac_name] = {'courses': set(), 'slots': set(), 'messages': []}
    
    if course != 'nan':
        teachers_data[fac_name]['courses'].add(course)
    if slot != 'nan':
        teachers_data[fac_name]['slots'].add(slot)

# 2. Read Whatsapp Chats
chat_files = ["WhatsApp Chat with '29 FFCS 1.2.txt", "WhatsApp Chat with '29 FFCS 2.1.txt"]
all_messages = []

for file in chat_files:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                # Basic parsing: timestamp - sender: message
                # Example: 25/12/2025, 12:19 am - +91 78450 61036: Is it possible...
                match = re.search(r'\d{2}/\d{2}/\d{4}, \d{1,2}:\d{2}\s*[ap]m - (.*?): (.*)', line)
                if match:
                    sender = match.group(1)
                    msg = match.group(2)
                    all_messages.append(msg)
                else:
                    # Might be a continuation of a previous message
                    if all_messages:
                        all_messages[-1] += " " + line.strip()

# 3. Match messages to teachers
for teacher in teachers_data.keys():
    # Create simple matchers based on first/last name
    parts = [p for p in teacher.split() if len(p) > 2] # ignore initials
    if not parts:
        parts = [teacher.replace(" ", "")]
    
    for msg in all_messages:
        msg_lower = msg.lower()
        # If any significant part of the name is in the message
        for part in parts:
            if part.lower() in msg_lower:
                teachers_data[teacher]['messages'].append(msg)
                break

# Convert sets to lists
for teacher in teachers_data:
    teachers_data[teacher]['courses'] = list(teachers_data[teacher]['courses'])
    teachers_data[teacher]['slots'] = list(teachers_data[teacher]['slots'])

with open('teacher_data.json', 'w', encoding='utf-8') as f:
    json.dump(teachers_data, f, indent=4)

print(f"Processed {len(teachers_data)} teachers.")
