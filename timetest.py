# Assignment 3.1 - Maximal author sets (geoptimaliseerde A-Priori)
import sys
import time
from collections import Counter, defaultdict
from itertools import combinations
from math import comb


def read_data(filepath):
    pubs = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            pubs.append({a.strip() for a in line.strip().split(',')})
    return pubs


def prepare(publications, support):
    """L1 + omzetten naar int-ids, alleen frequente auteurs, gesorteerde tuples."""
    counts = Counter()
    for pub in publications:
        counts.update(pub)

    frequent = [a for a, c in counts.items() if c >= support]
    ids = {a: i for i, a in enumerate(frequent)}
    names = frequent

    transactions = []
    for pub in publications:
        t = tuple(sorted(ids[a] for a in pub if a in ids))
        if len(t) >= 2:
            transactions.append(t)

    l1 = {(ids[a],): counts[a] for a in frequent}
    return l1, transactions, names


def count_pairs(transactions, support):
    """k=2: geen kandidaten genereren, direct paren tellen in de data."""
    counts = Counter()
    for t in transactions:                      # t is gesorteerd tuple van ints
        counts.update(combinations(t, 2))

    frequent = {p: n for p, n in counts.items() if n >= support}
    del counts                                  # geheugen vrijgeven

    # transaction reduction: alleen auteurs die in een frequent paar zitten
    pair_authors = set()
    for a, b in frequent:
        pair_authors.add(a)
        pair_authors.add(b)

    reduced = []
    for t in transactions:
        t = tuple(a for a in t if a in pair_authors)
        if len(t) >= 3:                         # voor k>=3 zijn minstens 3 auteurs nodig
            reduced.append(t)
    return frequent, reduced


def join_and_prune(l_prev, k):
    """Klassieke apriori-gen voor k >= 3: join op gemeenschappelijk prefix, dan prune."""
    prev_set = set(l_prev)

    groups = defaultdict(list)
    for itemset in sorted(l_prev):
        groups[itemset[:-1]].append(itemset[-1])

    candidates = []
    for prefix, lasts in groups.items():
        for a, b in combinations(lasts, 2):          # lasts is gesorteerd
            cand = prefix + (a, b)
            if all(sub in prev_set for sub in combinations(cand, k - 1)):
                candidates.append(cand)
    return candidates


def count_candidates(candidates, transactions, k, support):
    cand_set = set(candidates)
    cand_authors = set()
    for c in candidates:
        cand_authors.update(c)

    counts = Counter()
    reduced = []                                     # transaction reduction
    n_cands = len(candidates)

    for t in transactions:
        t = tuple(a for a in t if a in cand_authors)
        if len(t) < k:
            continue
        reduced.append(t)

        if comb(len(t), k) <= n_cands:
            for combi in combinations(t, k):         # t is gesorteerd -> combi ook
                if combi in cand_set:
                    counts[combi] += 1
        else:
            ts = set(t)
            for c in candidates:
                if ts.issuperset(c):
                    counts[c] += 1

    frequent = {c: n for c, n in counts.items() if n >= support}
    return frequent, reduced


def apriori(publications, support):
    start = time.time()
    l_prev, transactions, names = prepare(publications, support)
    print(f"k=1: {len(l_prev)} frequente auteurs, {len(transactions)} bruikbare publicaties "
          f"({time.time()-start:.1f}s)")

    result = dict(l_prev)

    # k=2: direct tellen
    t0 = time.time()
    l_prev, transactions = count_pairs(transactions, support)
    print(f"[k=2] frequent: {len(l_prev)} | publicaties over: {len(transactions)} "
          f"| {time.time()-t0:.1f}s")
    result.update(l_prev)

    # k>=3: join + prune + tellen
    k = 3
    while l_prev:
        t0 = time.time()
        candidates = join_and_prune(l_prev, k)
        print(f"[k={k}] kandidaten na join+prune: {len(candidates)}")
        if not candidates:
            break
        l_prev, transactions = count_candidates(candidates, transactions, k, support)
        print(f"[k={k}] frequent: {len(l_prev)} | publicaties over: {len(transactions)} "
              f"| {time.time()-t0:.1f}s")
        result.update(l_prev)
        k += 1

    print(f"Totaal klaar in {time.time()-start:.1f}s")
    # terug naar namen
    return {frozenset(names[i] for i in itemset): c for itemset, c in result.items()}


def main():
    if len(sys.argv) < 3:
        print("Gebruik: python script.py <filepath> <support>")
        sys.exit(1)

    t_read = time.time()
    publications = read_data(sys.argv[1])
    print(f"Data ingelezen in {time.time()-t_read:.1f}s | publicaties: {len(publications)}")

    result = apriori(publications, int(sys.argv[2]))
    print(f"Totaal aantal frequente itemsets: {len(result)}")
    print(result)


if __name__ == "__main__":
    main()