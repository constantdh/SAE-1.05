import csv

input_file = "C:\\Users\\Admin\\Downloads\\saeconstant-20260112T071117Z-3-001\\saeconstant\\post-elipse\\a.txt"
output_file = "C:\\Users\\Admin\\Downloads\\saeconstant-20260112T071117Z-3-001\\saeconstant\\post-elipse\\headers.csv"

headers = []

with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        if line.startswith("15") or line.startswith("HEADER:"):
            headers.append([line])

with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["header"])
    writer.writerows(headers)