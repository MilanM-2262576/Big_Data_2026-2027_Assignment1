# Assignment 3.2 - Association rules
import sys
from itertools import combinations
from assignment3_1 import read_data, apriori

def generate_association_rules(frequent_itemsets, min_confidence, max_rhs_size):
    """
    Generates association rules L -> R from frequent itemsets.
    :param frequent_itemsets: Dict mapping frozenset -> integer support count
    :param min_confidence: Float threshold (e.g., 0.5, 0.8, 1.0)
    :param max_rhs_size: Optional int to limit max authors on the RHS (|R|)
    :return: List of tuples (L, R, confidence, support_S)
    """

    rules = []
    for itemset, support in frequent_itemsets.items():
        if len(itemset) < 2:
            continue

        for r in range(1, min(max_rhs_size, len(itemset) - 1) + 1):
            for rhs in combinations(itemset, r):
                rhs = frozenset(rhs)
                lhs = itemset - rhs
                
                # lhs is altijd frequent (monotoniciteit), dus staat in de dict
                conf = support / frequent_itemsets[lhs]
                if conf >= min_confidence:
                    rules.append((lhs, rhs, conf, support))
                    
    return rules

def get_confidence(rule):
    return rule[2]  # Index 2 is de confidence

def main():
    
    if len(sys.argv) < 4:
        print("Gebruik: python association_rules.py <filepath> <support> <min_confidence> [max_rhs]")
        sys.exit(1)
 
    filepath = sys.argv[1]
    support = int(sys.argv[2])
    min_confidence = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
    max_rhs = int(sys.argv[4]) if len(sys.argv) > 4 else 3

 
    publications = read_data(filepath)
    frequent_sets = apriori(publications, support)
    print(f"Support: {support}, max aantal auteurs rechts: {max_rhs}")
    print(f"Aantal frequente sets: {len(frequent_sets)}")
 
    all_rules = generate_association_rules(frequent_sets, min_confidence, max_rhs)
    print(f"Totaal aantal gevonden regels: {len(all_rules)}\n")

    # Sorteer regels op confidence (hoogste eerst) voor een mooi overzicht
    all_rules.sort(key=get_confidence, reverse=True)

    print("Eerste 5 regels met hoogste confidence:")
    for lhs, rhs, conf, supp in all_rules[:5]:
        lhs_str = ", ".join(lhs)
        rhs_str = ", ".join(rhs)
        print(f"  {{{lhs_str}}} ==> {{{rhs_str}}} (Confidence: {conf:.2f}, Support: {supp})")

 
if __name__ == "__main__":
    main()



