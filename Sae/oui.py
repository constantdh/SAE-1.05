import pandas as pd

# Chemins à adapter à ton projet
input_csv = r"C:\Users\Admin\SAE-1.05\data\headers_parses.csv"   # ton CSV déjà nettoyé
output_md = r"C:\Users\Admin\SAE-1.05\data\headers_parses.md"

# 1. Lecture du CSV
df = pd.read_csv(input_csv)

# 2. (Optionnel) on garde seulement les colonnes utiles et on enlève 'raw' si elle existe
colonnes_voulues = [
    "time", "ip_source", "ip_destination",
    "src_port", "dst_port",
    "flags", "seq", "ack", "win", "length", "options"
]

colonnes_disponibles = [c for c in colonnes_voulues if c in df.columns]
df = df[colonnes_disponibles]

# 3. Conversion en tableau Markdown
#    index=False pour ne pas avoir une colonne d’index dans le tableau
table_markdown = df.to_markdown(index=False)

# 4. Écriture dans un fichier .md
with open(output_md, "w", encoding="utf-8") as f:
    f.write("# Tableau des paquets réseau\n\n")
    f.write(table_markdown)
    f.write("\n")

print("Fichier Markdown créé :", output_md)