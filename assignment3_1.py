# Assignment 3.1 - Maximal author sets
import sys
from collections import Counter,defaultdict
from itertools import combinations

#file openenn en in een lijst van sets zetten
def read_data(filepath):
    publications = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            authors_in_pub = set(author.strip() for author in line.strip().split(',')) # set ipv list
            publications.append(authors_in_pub)
    return publications

def frequent_individual_authors(publications, support):
    """Geeft een lijst van tuples terug met de frequentie van de individuele auteurs die voldoen aan de supportdrempel."""

    author_counts = Counter()   # Output: Counter({'Jan': 3, 'Frank': 2, 'Thomas': 1})

    for pub in publications:
        for author in pub:
            author_counts[author] += 1

    result = {}

    for author, count in author_counts.items():
        if count >= support:
            result[frozenset([author])] = count

    return result

def generate_and_count_candidates(frequent_l_previous, publications, support, k):
    """
    Algemene functie voor elke k >= 2.
    - frequent_l_prev: De frequente itemsets uit de vorige ronde L_{k-1}
    - publications: De lijst met publicaties (elke publicatie is een lijst van auteurs)
    - support: De minimale supportdrempel (getal)
    - k: De gewenste grootte van de nieuwe auteursets
    """
    
    if k == 2:  # Als k=2, dan zijn de kandidaten gewoon alle paren van auteurs in de publicaties, dat is sneller dan combinaties van L_{k-1} te nemen
        counts = Counter()
        for pub in publications:
            for pair in combinations(pub, 2):
                counts[frozenset(pair)] += 1  
        return {itemset: count for itemset, count in counts.items() if count >= support}


    # Stap 1: genereer kandidaten door sets uit L_{k-1} te combineren
    '''
    candidates = set()
    for itemset1 in frequent_l_previous:
    for itemset2 in frequent_l_previous:
        # Combineer twee sets
        union = itemset1 | itemset2
        
        # Voeg alleen toe als de gecombineerde set exact lengte k heeft
        # (wat betekent dat ze exact k-2 elementen delen)
        if len(union) == k:
            candidates.add(union) 
    '''
        
    groups = defaultdict(list)
    for itemset in frequent_l_previous:
        s = tuple(sorted(itemset))               # frozenset -> gesorteerd tuple
        groups[s[:-1]].append(s[-1])             # prefix -> lijst van laatste elementen

    candidates = set()
    for prefix, lasts in groups.items():
        for a, b in combinations(lasts, 2):
            candidates.add(frozenset(prefix + (a, b)))

    # Stap 2: prune. Alle (k-1)-deelsets van een kandidaat moeten zelf frequent zijn ab cd  dan word bv bc eenkoppel dus moet bc frequentz ijn bij de vorige
    pruned = set()
    for candidate in candidates:
        if all(frozenset(sub) in frequent_l_previous for sub in combinations(candidate, k - 1)): #ALL pakt alle deelsets van lengte k-1
            pruned.add(candidate)

    # Stap 3: tel de support van de overgebleven kandidaten
    if not pruned:                                   # geen kandidaten: niet meer door de data lopen
        return {}

    candidate_authors = set().union(*pruned)
    counts = Counter()
    for pub in publications:
        pub = pub & candidate_authors       # alleen auteurs die in een kandidaat zitten
        if len(pub) < k:
            continue
        for combi in combinations(pub, k):
            combi = frozenset(combi)
            if combi in pruned:
                counts[combi] += 1

    # Stap 4: hou alleen de kandidaten over die voldoen aan de support
    return {itemset: count for itemset, count in counts.items() if count >= support}

def maximal_author_sets(frequent):
    """Per grootte k: hoogste support, aantal sets met die support, en een voorbeeld."""

    #per k sorten en in een dict zetten
    by_size = defaultdict(dict)
    for itemset, count in frequent.items():
        by_size[len(itemset)][itemset] = count

    summary = {}
    for k, sets in sorted(by_size.items()):
        best = max(sets.values())
        winners = [s for s, c in sets.items() if c == best]
        summary[k] = (best, len(sets), winners[0])
    return summary

def apriori(publications, support):
    """Geeft een dict terug met alle frequente auteursets en hun frequentie."""
    result = {}

    # L1: frequente individuele auteurs
    frequent_l = frequent_individual_authors(publications, support)
    result.update(frequent_l)

    k = 2
    while frequent_l:
        frequent_l = generate_and_count_candidates(frequent_l, publications, support, k)
        result.update(frequent_l)
        k += 1

    return result

def main():
    # Controleer of beide argumenten zijn meegegeven
    if len(sys.argv) < 3:
        print("Gebruik: python script.py <filepath> <support>")
        sys.exit(1)

    filepath = sys.argv[1]
    
    try:
        support = int(sys.argv[2])
    except ValueError:
        print("Fout: Support moet een geheel getal zijn.")
        sys.exit(1)


    publications = read_data(filepath)
    print(f"Number of publications: {len(publications)}")
    result = apriori(publications, support)
    for k, (best, n, example) in maximal_author_sets(result).items():
        print(f"k={k}: support={best}, aantal={n}, voorbeeld={set(example)}")

if __name__ == "__main__":
    main()
    