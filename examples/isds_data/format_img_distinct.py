import os
import csv
import math

# === INPUTS ===
txt_file = "coordinates_isds.txt"          # your input txt file
image_folder = "/home/aqib/Downloads/isds_20250908173217"  # path to folder with images
output_file = "coordinates.txt"        # output file

# --- Load image filenames and extract timestamps ---
images = []
for fname in os.listdir(image_folder):
    if fname.lower().endswith(".jpg"):
        try:
            ts = float(os.path.splitext(fname)[0])  # timestamp from filename
            images.append((ts, fname))
        except ValueError:
            # skip files not valid numeric timestamp
            continue

# sort by timestamp
images.sort(key=lambda x: x[0])

# --- Read input txt file ---
records = []
with open(txt_file, "r") as infile:
    lines = infile.readlines()

# skip header
for line in lines[1:]:
    parts = line.strip().split()
    if len(parts) < 4:
        continue
    ts = float(parts[0])  # timestamp from txt file
    lat = float(parts[1])
    lon = float(parts[2])
    alt = float(parts[3])
    records.append((ts, lat, lon, alt))

# --- Match txt rows with images ---
used_images = set()
output_rows = []

for ts, lat, lon, alt in records:
    # find closest image by timestamp
    closest = min(images, key=lambda x: abs(x[0] - ts), default=None)
    if closest is None:
        continue

    img_ts, img_name = closest
    if img_name in used_images:
        continue  # avoid duplicates

    used_images.add(img_name)

    # build row
    file_field = f'./isds_20250908173217/{img_name}'  # CSV writer will add quotes
    output_rows.append([
        file_field,
        img_ts,
        lon,
        lat,
        alt,
        0,   # course placeholder
        0,   # pitch placeholder
        0    # roll placeholder
    ])

# --- Write output file ---
with open(output_file, "w", newline="") as outfile:
    writer = csv.writer(outfile, delimiter="\t", quoting=csv.QUOTE_NONNUMERIC)

    # header
    writer.writerow(["File", "Time", "Long", "Lat", "Alt", "course", "pitch", "roll"])

    # rows
    for row in output_rows:
        writer.writerow(row)

print(f"✅ Done! {len(output_rows)} rows written to {output_file}")
