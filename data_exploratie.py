
import sys

FILES = ["datasets/dataset_tiny.txt", "datasets/dataset_medium1.txt", "datasets/dataset_medium2.txt",
         "datasets/dataset_large.txt", "datasets/dataset_all.txt"]


def explore(path):
    authors = set()
    n_pub = 0
    n_slots = 0   # totaal aantal (auteur, publicatie) paren
    with open(path, encoding="utf-8") as f:
        for line in f:
            names = set(line.strip().split(","))   # set: dubbele auteurs tellen 1x
            authors |= names
            n_pub += 1
            n_slots += len(names)
    print(f"{path}")
    print(f"  publicaties:        {n_pub:,}")
    print(f"  unieke auteurs:     {len(authors):,}")
    print(f"  gem. auteurs/publ.: {n_slots / n_pub:.2f}\n")


for path in sys.argv[1:] or FILES:
    explore(path)