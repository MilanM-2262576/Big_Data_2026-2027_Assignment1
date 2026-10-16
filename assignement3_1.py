# Assignment 3.1
import sys
from collections import Counter
from itertools import combinations

def read_data(filepath):
    publications = []
    with open(filepath, 'r') as f:
        for line in f:
            authors_in_pub = [author.strip() for author in line.strip().split(',')]# lijst van alle auterrs op een regel
            publications.append(authors_in_pub) # dus een lijst van lijsten, elke lijst is een publicatie(regels) met auteurs
    return publications



def frequent_individual_authors(publications, authors, support):
    """Geeft een lijst van tuples terug met de frequentie van de individuele auteurs die voldoen aan de supportdrempel."""

    author_counts = Counter()   # Output: Counter({'Jan': 3, 'Frank': 2, 'Thomas': 1})
    for pub in publications:
        for author in authors:
            if author in pub:
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
    previous_sets = list(frequent_l_previous.keys())

    # Stap 1: genereer kandidaten door sets uit L_{k-1} te combineren
    candidates = set()
    for i in range(len(previous_sets)):
        for j in range(i + 1, len(previous_sets)):
            union = previous_sets[i] | previous_sets[j]
            if len(union) == k:
                candidates.add(union)

    # Stap 2: prune. Alle (k-1)-deelsets van een kandidaat moeten zelf frequent zijn ab cd  dan word bv bc eenkoppel dus moet bc frequentz ijn bij de vorige
    pruned = set()
    for candidate in candidates:
        if all(frozenset(sub) in frequent_l_previous for sub in combinations(candidate, k - 1)): #ALL pakt alle deelsets van lengte k-1
            pruned.add(candidate)

    # Stap 3: tel hoe vaak elke kandidaat voorkomt in de publicaties, houd ook rekening met deelverzamelingen
    counts = Counter()
    for pub in publications:
        pub_set = set(pub)
        for candidate in pruned:
            if candidate <= pub_set:      # is de kandidaat een deelverzameling van de publicatie?
                counts[candidate] += 1

    # Stap 4: hou alleen de kandidaten over die voldoen aan de support
    return {itemset: count for itemset, count in counts.items() if count >= support}


def apriori(publications, authors, support):
    """Geeft een dict terug met alle frequente auteursets en hun frequentie."""
    result = {}

    # L1: frequente individuele auteurs
    frequent_l = frequent_individual_authors(publications, authors, support)
    result.update(frequent_l)

    # L2, L3, ... totdat er geen frequente sets meer zijn
    k = 2
    while frequent_l:
        frequent_l = generate_and_count_candidates(frequent_l, publications, support, k)
        result.update(frequent_l)
        k += 1

    return result






def main():
    filepath = "datasets/dataset_tiny.txt"
    #support = int(sys.argv[2]) #crasht als te weinign gegevens

    publications = read_data(filepath)
    authors = set().union(*publications) #  * maakt van [[a,b],[c,d]] -> [a,b],[c,d] , union zet alle lijsten in een set dus dubbelee gaan er uit,
    print(f"Number of publications: {len(publications)}")
    print(f"Number of unique authors: {len(authors)}")

    #print(authors)
    #print(publications)

    result = apriori(publications, authors,30)
    print(result)



if __name__ == "__main__":
    main()
    