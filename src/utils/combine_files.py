"""Helper file to combine output files into one file."""
# in output/level_one folder there are many csv files, each with the same header
# I want to combine them into one

import csv
from os import listdir
from os.path import isfile, join

folder = "output/gpt-4-1106-preview_single_guess"
outfile = "output/combined.csv"
game_ids = sorted(
    [int(f.split(".csv")[0]) for f in listdir(folder) if isfile(join(folder, f))]
)
print(game_ids)
filenames = [f"{folder}/{game_id}.csv" for game_id in game_ids]

header = []
rows = []
for filename in filenames:
    with open(filename, "r") as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            print(filename, row)
            rows.append(row)

with open(outfile, "w") as file:
    writer = csv.writer(file)
    writer.writerow(header)
    for row in rows:
        writer.writerow(row)
