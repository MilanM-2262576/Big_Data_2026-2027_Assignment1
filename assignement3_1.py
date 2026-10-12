# Assignment 3.1
import sys

def read_data(filepath):
    publications = []
    with open(filepath, 'r') as f:
        for line in f:
            authors_in_pub = [author.strip() for author in line.strip().split(',')]# lijst van alle auterrs op een regel
            publications.append(authors_in_pub) # dus een lijst van lijsten, elke lijst is een publicatie(regels) met auteurs
    return publications

def main():
    filepath = "datasets/dataset_tiny.txt"
    #support = int(sys.argv[2]) #crasht als te weinign gegevens

    publications = read_data(filepath)
    authors = set().union(*publications) #  * maakt van [[a,b],[c,d]] -> [a,b],[c,d] , union zet alle lijsten in een set dus dubbelee gaan er uit,
    print(f"Number of publications: {len(publications)}")
    print(f"Number of unique authors: {len(authors)}")





if __name__ == "__main__":
    main()
    