import csv
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from collections import defaultdict

# Chemins des fichiers
input_csv = "C:/Users/Admin/SAE-1.05/Sae/headers.csv"  # Le CSV créé précédemment
output_excel = "rapport_headers.xlsx"

# Lire le CSV
df = pd.read_csv(input_csv)          # lit la colonne 'header'
df = df.rename(columns={'header': 'ip_source'})
df_sorted = df.sort_values(by=['ip_source'], ascending=True)

# === OPTION 1 : Trier par IP source (simple) ===
df_sorted = df.sort_values(by=['ip_source'], ascending=True)

# === OPTION 2 : Ajouter des statistiques par IP source ===
# Créer un résumé avec le nombre de paquets par IP
stats = df.groupby('ip_source').agg({
    'length': ['sum', 'mean', 'count'],
    'ip_destination': 'nunique'
}).round(2)

stats.columns = ['Total_Bytes', 'Avg_Length', 'Nb_Packets', 'Unique_Destinations']
stats = stats.sort_values(by='Nb_Packets', ascending=False)

# === Créer le fichier Excel avec deux feuilles ===
with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
    
    # Feuille 1 : Données triées détaillées
    df_sorted.to_excel(writer, sheet_name='Détail Trafic', index=False)
    
    # Feuille 2 : Statistiques par IP source
    stats.to_excel(writer, sheet_name='Statistiques')
    
    # Optionnel : formater les feuilles
    workbook = writer.book
    
    # Formater la feuille "Détail Trafic"
    ws1 = writer.sheets['Détail Trafic']
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True)
    
    for cell in ws1[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center')
    
    # Ajuster la largeur des colonnes
    for column in ws1.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        ws1.column_dimensions[column_letter].width = min(max_length + 2, 50)
    
    # Formater la feuille "Statistiques"
    ws2 = writer.sheets['Statistiques']
    for cell in ws2[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center')

print(f"✓ Fichier Excel créé : {output_excel}")
print(f"✓ Nombre de lignes triées : {len(df_sorted)}")
print(f"✓ IPs sources uniques : {df_sorted['ip_source'].nunique()}")
