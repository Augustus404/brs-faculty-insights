import pandas as pd

file_path = 'BRS Fall 26-27.xlsx'
df = pd.read_excel(file_path)

new_data = [
    ("MUTHUNAGAI", "D1+TD1+T"),
    ("PULAK KONAR", "D2+TD2+T"),
    ("AVINASH KUMAR MITTAL", "D1+TD1+T"),
    ("SRIRAMAN R", "D1+TD1+T"),
    ("NATHIYA N", "D2+TD2+T"),
    ("RAJIVGANTHI", "D2+TD2+T"),
    ("SUKAVANAM N", "D2+TD2+T"),
    ("DAVID MAXIM GURURAJ A", "D2+TD2+T"),
    ("UMA MAHESWARI S", "D2+TD2+T"),
    ("RAJESH KUMAR MOHAPATRA", "D1+TD1+T"),
    ("RADHA S", "D1+TD1+T"),
    ("ASHISH KUMAR", "D2+TD2+T"),
    ("PADMAJA N", "D1+TD1+T"),
    ("ASHIS BERA", "D1+TD1+T"),
    ("AVINASH KUMAR MITTAL", "D2+TD2+T"),
    ("BASUA DEBANANDA", "D1+TD1+T"),
    ("SANKARSAN TARAI", "D2+TD2+T"),
    ("RADHA S", "D2+TD2+T"),
    ("DHANASEKAR S", "D2+TD2+T"),
    ("RUPCHAND SUTRADHAR", "D1+TD1+T"),
    ("MEGALA M", "D1+TD1+T"),
    ("SHARATH JOSE", "D1+TD1+T"),
    ("DHANASEKAR S", "D1+TD1+T"),
    ("SARANYA G", "D1+TD1+T")
]

new_rows = []
for name, slot in new_data:
    new_rows.append({
        'Course title': 'Discrete Mathematics and Linear Algebra',
        'Course code ': 'BAMAT205',
        'SLOT': slot,
        'FACULTY NAME': name
    })

new_df = pd.DataFrame(new_rows)
df = pd.concat([df, new_df], ignore_index=True)

df.to_excel(file_path, index=False)
print("Added teachers and saved excel.")
