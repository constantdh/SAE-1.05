import re
import pandas as pd

# Chemin vers ton CSV
input_csv = r"C:\Users\Admin\SAE-1.05\Sae\headers.csv"
output_csv = r"C:\Users\Admin\SAE-1.05\Sae\headers_parses.csv"

# Lecture du fichier (une colonne 'header')
df = pd.read_csv(input_csv)

# Regex inspirée du format tcpdump que l’on voit dans ton fichier [file:38]
pattern = re.compile(
    r'^(?P<time>\d{2}:\d{2}:\d{2}\.\d+)\s+'
    r'IP\s+'
    r'(?P<src>[^ >]+)\s*>\s*(?P<dst>[^:]+):\s*'
    r'(?:Flags\s*\[(?P<flags>[^\]]*)\],\s*)?'
    r'(?:seq\s+(?P<seq>[0-9:]+),\s*)?'
    r'(?:ack\s+(?P<ack>[0-9:]+),\s*)?'
    r'(?:win\s+(?P<win>\d+),\s*)?'
    r'(?:options\s+(?P<options>\[[^\]]*\]),\s*)?'
    r'(?:length\s+(?P<length>\d+))?'
)

rows = []

for line in df["header"].astype(str):
    m = pattern.search(line)
    if not m:
        # ligne non IP ou format différent : on peut la garder vide ou ignorer
        rows.append({
            "time": None,
            "ip_source": None,
            "ip_destination": None,
            "src_port": None,
            "dst_port": None,
            "flags": None,
            "seq": None,
            "ack": None,
            "win": None,
            "length": None,
            "options": None,
            "raw": line,           # pour garder la ligne originale
        })
        continue

    time = m.group("time")
    src_full = m.group("src")
    dst_full = m.group("dst")
    flags = m.group("flags")
    seq = m.group("seq")
    ack = m.group("ack")
    win = m.group("win")
    options = m.group("options")
    length = m.group("length")

    # découpe IP:port (ou hostname.port) source/destination
    def split_host_port(s):
        # dernier '.' sépare l’hôte du port (typique tcpdump) [file:38]
        if "." in s and s.rsplit(".", 1)[1].isdigit():
            host, port = s.rsplit(".", 1)
            return host, port
        return s, None

    ip_src, src_port = split_host_port(src_full)
    ip_dst, dst_port = split_host_port(dst_full)

    rows.append({
        "time": time,
        "ip_source": ip_src,
        "ip_destination": ip_dst,
        "src_port": src_port,
        "dst_port": dst_port,
        "flags": flags,
        "seq": seq,
        "ack": ack,
        "win": win,
        "length": length,
        "options": options,
        "raw": line,
    })

parsed_df = pd.DataFrame(rows)

# Tri par ip_source + time si tu veux
parsed_df = parsed_df.sort_values(by=["ip_source", "time"], ascending=[True, True])

# Sauvegarde CSV
parsed_df.to_csv(output_csv, index=False)

print("Terminé, CSV créé :", output_csv)
