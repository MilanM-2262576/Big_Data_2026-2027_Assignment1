# Assignment: Frequent Itemsets & Association Rules
**Course:** Big Data Analytics  
**Academic Year:** 2026-2027  

**Group Members:**
* **Name Student 1:** [Thomas Timmermans] - **Student ID:** [2365790]
* **Name Student 2:** [Milan Muroni] - **Student ID:** [2262576]

---

## 1. Data Exploration

We zien dat in elke file een regel word voorgesteld als een publicatie, dus eigenlijk gewoon per regel wat namen gescheiden door een komma.

| Dataset | Publications | Unique Authors | Avg. Authors / Publication |
| :--- | :---: | :---: | :---: |
| `dataset_tiny.txt` | 629 | 290 | 3.32 |
| `dataset_medium1.txt` | 22 779 | 14 885 | 3.47 |
| `dataset_medium2.txt` | 21 092 | 17 707 | 4.01 |
| `dataset_large.txt` | 2 004 723 | 1 258 951 | 3.03 |
| `dataset_all.txt` | 7 142 501 | 3 658 503 | 3.38 |


---

## 2. Implementatiedetails

### 2.1 Apriori-algoritme & Maximale Auteursets
* **Datastructuren:** 
    -  Voor <u>sets als key in dictionaries</u> gebruiken we frozensets, dit hebben we gevonden in de tip van de assignment. Dit is ook nodig aangezien we de sets anders niet als key kunnen gebruiken in python omdat gewone sets mutable zijn.

    - Voor <u>publications</u> gebruiken we een gewone lijst [] waar we alle publicaties behouden als sets van de auteurs van die publicatie ==>  [(milan, thomas), (jan van de bussche, bart)]

    - Voor het <u>tellen van het voorkomen van de auteurs</u> gebruiken we de klasse Counter()
    Hierin houden we makkelijk bijh oevaak iemand voorkomt  Output: Counter({'Jan': 3, 'Frank': 2, 'Thomas': 1})

    - Verder gebruiken we ook tijdens het berekenen voor de kandidaten bij te houden etc sets


* **Prefix-gebaseerde Kandidaatgeneratie:** 
Om kandidaatsets $C_k$ voor $k > 2$ efficiënt te genereren uit de frequente itemsets $L_{k-1}$, sorteren we de elementen binnen elke itemset in $L_{k-1}$ tot een tuple. Vervolgens groeperen we deze tuples op hun prefix van lengte $k-2$ (via `defaultdict`). Twee itemsets uit $L_{k-1}$ die exact dezelfde eerste $k-2$ elementen delen, worden gecombineerd door alle paarsgewijze combinaties van hun laatste elementen te nemen. Dit voorkomt dat we onnodig alle mogelijke paren uit $L_{k-1}$ moeten vergelijken. 
bv> {B, C} em {B, D} ==> {B, C, D}

* **Pruning-stap:** 
Het Apriori-principe stelt dat elke deelset van een frequente itemset zelf ook frequent moet zijn (anti-monotonie van support). Voor elke gegenereerde kandidaat van lengte $k$ genereren we alle mogelijke sub-itemsets van lengte $k-1$ (met `itertools.combinations`). Indien er minstens één sub-itemset niet in $L_{k-1}$ zit, wordt de kandidaat onmiddellijk gefilterd en niet meegeteld in de dataset.
Stel {B, D} en {B, C} zitten in L2 maar {C, D} NIET? ==> prune {B, C, D} / gooi het weg


- **Optimalisaties:**
  * **Directe paarsgewijze telling voor $k=2$:** Voor $k=2$ slaan we de algemene prefix-combinatiestap over. We doorlopen de publicaties rechtstreeks en tellen alle auteursparen met `combinations(pub, 2)`. Dit is aanzienlijk sneller dan het bouwen en filteren van kandidaten op basis van $L_1$.

  * **Filteren van publicaties op kandidaat-auteurs:** Voordat we in stap 3 kandidaten tellen over de dataset, bepalen we eerst de unie van alle auteurs die in de overgebleven (geprunede) kandidaten voorkomen (`candidate_authors`). Per publicatie nemen we de doorsnede `pub & candidate_authors`. Publicaties die na deze filter minder dan $k$ auteurs overhouden, worden direct overgeslagen. Dit verkleint de combinatorische explostie van `combinations(pub, k)` aanzienlijk bij grote publicaties.


### 2.2 Associatieregels Genereren
Dit deeltje ging eigenlijk zeer vlot, door gewoon de funcies uit het eerste deeltje te gebruiken en dan de formule voor confidence. 

### 2.3 Uitdagingen & Knelpunten (Bottlenecks)
* **Snelheid:** Onze initiele code was te traag, na 45 min kwam hij er niet uit bij de large dataset bij apriori. Toen zijn we gaan timen per k, we zagen dat k=2 er niet door kwam. we hebben dan na overleg/brainstorm met genai zijn we er op uit gekomen dat het interessant zou zijn om voor k=2 een appart deeltje te maken dat puur alle paren maakt binnen een publicatie, stap 1 heeft ook een aanpassing gekregen. onze oude code staat er nog bij in commentaar. Nu werken we met prefeix en last, dit is na het testen ook weer een mooie sneheidswinst.

---

## 3. Resultaten

### 3.1 Maximale Auteursets (Apriori)

Voor elke dataset rapporteren we of de verwerking is geslaagd, de gebruikte supportdrempel en de maximale auteursets per grootte $k \ge 1$.

#### Dataset: `dataset_tiny.txt` (Support Drempel $s = 5$)
* **Aantal publicaties:** 629
* **Status:** Geslaagd

| $k$ | Max Support | Aantal Sets | Voorbeeld Maximale Set |
| :--- | :--- | :--- | :--- |
| **1** | 250 | 79 | Jan Van den Bussche |
| **2** | 67 | 150 | Dirk Van Gucht, Marc Gyssens |
| **3** | 25 | 106 | Dirk Van Gucht, Yuqing Wu, Marc Gyssens |
| **4** | 14 | 57 | Dirk Van Gucht, Yuqing Wu, George H. L. Fletcher, Marc Gyssens |
| **5** | 11 | 25 | Dirk Van Gucht, Jan Van den Bussche, Stijn Vansummeren, George H. L. Fletcher, Marc Gyssens |
| **6** | 9 | 7 | Dirk Van Gucht, Jan Van den Bussche, Yuqing Wu, George H. L. Fletcher, Stijn Vansummeren, Marc Gyssens |
| **7** | 6 | 1 | Dirk Van Gucht, Jan Van den Bussche, Yuqing Wu, George H. L. Fletcher, Dirk Leinders, Stijn Vansummeren, Marc Gyssens |

#### Dataset: `dataset_medium1.txt` (Support Drempel $s = 5$)
* **Aantal publicaties:** 22.779
* **Status:** Geslaagd

| $k$ | Max Support | Aantal Sets | Voorbeeld Maximale Set |
| :--- | :--- | :--- | :--- |
| **1** | 762 | 2.835 | Moshe Y. Vardi |
| **2** | 182 | 4.974 | Dirk Habich, Wolfgang Lehner |
| **3** | 104 | 2.938 | Maurizio Lenzerini, Diego Calvanese, Giuseppe De Giacomo |
| **4** | 37 | 1.082 | Maurizio Lenzerini, Diego Calvanese, Riccardo Rosati 0001, Giuseppe De Giacomo |
| **5** | 25 | 309 | Domenico Lembo, Diego Calvanese, Giuseppe De Giacomo, Maurizio Lenzerini, Riccardo Rosati 0001 |
| **6** | 11 | 72 | Barbara Weber, Matthias Weidlich 0001, Dirk Fahland, Stefan Zugal, Jan Mendling, Hajo A. Reijers |
| **7** | 9 | 12 | Barbara Weber, Matthias Weidlich 0001, Dirk Fahland, Stefan Zugal, Jan Mendling, Hajo A. Reijers, Jakob Pinggera |
| **8** | 6 | 1 | Sergio Tessaris, Daniela Loreti, Marco Montali, Federico Chesani, Chiara Ghidini, Chiara Di Francescomarino, Paola Mello, Fabrizio Maria Maggi |

#### Dataset: `dataset_medium2.txt` (Support Drempel $s = 5$)
* **Aantal publicaties:** 21.092
* **Status:** Geslaagd

| $k$ | Max Support | Aantal Sets | Voorbeeld Maximale Set |
| :--- | :--- | :--- | :--- |
| **1** | 634 | 3.090 | Noga Alon |
| **2** | 184 | 6.061 | Dirk Habich, Wolfgang Lehner |
| **3** | 104 | 5.015 | Diego Calvanese, Maurizio Lenzerini, Giuseppe De Giacomo |
| **4** | 37 | 4.522 | Diego Calvanese, Maurizio Lenzerini, Riccardo Rosati 0001, Giuseppe De Giacomo |
| **5** | 25 | 5.983 | Diego Calvanese, Domenico Lembo, Maurizio Lenzerini, Giuseppe De Giacomo, Riccardo Rosati 0001 |
| **6** | 11 | 8.928 | Dirk Fahland, Stefan Zugal, Barbara Weber, Jan Mendling, Matthias Weidlich 0001, Hajo A. Reijers |
| **7** | 9 | 11.902 | Dirk Fahland, Stefan Zugal, Barbara Weber, Jakob Pinggera, Jan Mendling, Matthias Weidlich 0001, Hajo A. Reijers |
| **8** | 6 | 13.059 | Abdeslem Djaoui, Paul Taylor, James Magowan, David O'Callaghan, Linda Cornwall, Norbert Podhorszki, Stuart Kenny, Roney Cordenonsi |
| **9** | 6 | 11.497 | Abdeslem Djaoui, Paul Taylor, James Magowan, David O'Callaghan, Linda Cornwall, Norbert Podhorszki, Werner Nutt, Stuart Kenny, Roney Cordenonsi |
| **10** | 6 | 8.019 | Abdeslem Djaoui, Paul Taylor, James Magowan, David O'Callaghan, Linda Cornwall, Norbert Podhorszki, Werner Nutt, Steve Fisher, Stuart Kenny, Roney Cordenonsi |
| **11** | 6 | 4.369 | Abdeslem Djaoui, Paul Taylor, James Magowan, David O'Callaghan, Linda Cornwall, Norbert Podhorszki, Werner Nutt, Steve Fisher, Rob Byrom, Stuart Kenny, Roney Cordenonsi |
| **12** | 6 | 1.820 | Abdeslem Djaoui, Paul Taylor, James Magowan, David O'Callaghan, Linda Cornwall, Norbert Podhorszki, Werner Nutt, Steve Fisher, Rob Byrom, Antony J. Wilson, Steve Hicks, Roney Cordenonsi |
| **13** | 6 | 560 | Abdeslem Djaoui, Paul Taylor, James Magowan, David O'Callaghan, Linda Cornwall, Norbert Podhorszki, Werner Nutt, Steve Fisher, Rob Byrom, Antony J. Wilson, Steve Hicks, Stuart Kenny, Roney Cordenonsi |
| **14** | 6 | 120 | Abdeslem Djaoui, Paul Taylor, James Magowan, David O'Callaghan, Linda Cornwall, Norbert Podhorszki, Werner Nutt, Steve Fisher, Rob Byrom, Antony J. Wilson, Steve Hicks, Stuart Kenny, Andrew W. Cooke, Roney Cordenonsi |
| **15** | 6 | 16 | Abdeslem Djaoui, Paul Taylor, James Magowan, David O'Callaghan, Linda Cornwall, Norbert Podhorszki, Werner Nutt, Steve Fisher, Rob Byrom, Antony J. Wilson, Steve Hicks, Brian A. Coghlan, Stuart Kenny, Andrew W. Cooke, Roney Cordenonsi |
| **16** | 5 | 1 | Paul Taylor, James Magowan, Linda Cornwall, Werner Nutt, Rob Byrom, Steve Hicks, Stuart Kenny, Andrew W. Cooke, Brian A. Coghlan, Abdeslem Djaoui, David O'Callaghan, Norbert Podhorszki, Steve Fisher, Antony J. Wilson, Laurence Field, Roney Cordenonsi |

#### Dataset: `dataset_large.txt` (Support Drempel $s = 25$)
* **Aantal publicaties:** 2.004.723
* **Status:** Geslaagd

| $k$ | Max Support | Aantal Sets | Voorbeeld Maximale Set |
| :--- | :--- | :--- | :--- |
| **1** | 906 | 43.451 | H. Vincent Poor |
| **2** | 242 | 7.826 | Tomoya Enokido, Makoto Takizawa 0001 |
| **3** | 122 | 984 | Tetsuya Ogata, Kazunori Komatani, Hiroshi G. Okuno |
| **4** | 53 | 199 | Alberto Bosio, Luigi Dilillo, Patrick Girard 0001, Arnaud Virazel |
| **5** | 44 | 60 | Margaret J. Wright, Katie McMahon, Greig I. de Zubicaray, Arthur W. Toga, Paul M. Thompson |
| **6** | 31 | 13 | Alberto Gil-Solla, Manuel Ramos Cabrer, José Juan Pazos-Arias, Ana Fernández Vilas, Jorge García Duque, Rebeca P. Díaz Redondo |
| **7** | 25 | 1 | Alberto Gil-Solla, Manuel Ramos Cabrer, José Juan Pazos-Arias, Ana Fernández Vilas, Martín López Nores, Jorge García Duque, Rebeca P. Díaz Redondo |

#### Dataset: `dataset_all.txt` (Support Drempel $s = 25$)
* **Aantal publicaties:** 7.142.501
* **Status:** Geslaagd

| $k$ | Max Support | Aantal Sets | Voorbeeld Maximale Set |
| :--- | :--- | :--- | :--- |
| **1** | 2.986 | 182.401 | H. Vincent Poor |
| **2** | 531 | 60.799 | Makoto Takizawa 0001, Tomoya Enokido |
| **3** | 282 | 11.651 | Yiqun Liu 0001, Min Zhang 0006, Shaoping Ma |
| **4** | 149 | 5.726 | Raul Muñoz 0001, Ricardo Martínez 0001, Ricard Vilalta, Ramon Casellas |
| **5** | 100 | 10.757 | Peter Michaleas, Matthew Hubbell, Albert Reuther, David Bestor, Jeremy Kepner |
| **6** | 98 | 22.239 | Peter Michaleas, Matthew Hubbell, Albert Reuther, David Bestor, Andrew Prout, Jeremy Kepner |
| **7** | 96 | 37.244 | Peter Michaleas, Matthew Hubbell, Albert Reuther, David Bestor, William Arcand, Andrew Prout, Jeremy Kepner |
| **8** | 94 | 49.298 | Peter Michaleas, Matthew Hubbell, Albert Reuther, David Bestor, William Arcand, Andrew Prout, Jeremy Kepner, Antonio Rosa |
| **9** | 92 | 51.473 | Peter Michaleas, Matthew Hubbell, Albert Reuther, David Bestor, William Arcand, Andrew Prout, Jeremy Kepner, Antonio Rosa, Chansup Byun |
| **10** | 83 | 42.193 | Peter Michaleas, Matthew Hubbell, Albert Reuther, David Bestor, William Arcand, Andrew Prout, Jeremy Kepner, Antonio Rosa, Chansup Byun, Vijay Gadepally |
| **11** | 79 | 26.866 | Peter Michaleas, Matthew Hubbell, Albert Reuther, David Bestor, William Arcand, Andrew Prout, Jeremy Kepner, Antonio Rosa, Chansup Byun, Vijay Gadepally, Charles Yee |
| **12** | 69 | 13.051 | Peter Michaleas, Matthew Hubbell, Albert Reuther, David Bestor, William Arcand, Lauren Milechin, Andrew Prout, Jeremy Kepner, Antonio Rosa, Michael Jones 0001, Chansup Byun, Vijay Gadepally |
| **13** | 65 | 4.704 | Peter Michaleas, Matthew Hubbell, Albert Reuther, David Bestor, William Arcand, Lauren Milechin, Andrew Prout, Siddharth Samsi, Jeremy Kepner, Antonio Rosa, Michael Jones 0001, Chansup Byun, Vijay Gadepally |
| **14** | 61 | 1.206 | Peter Michaleas, Matthew Hubbell, Albert Reuther, David Bestor, William Arcand, Lauren Milechin, Andrew Prout, Siddharth Samsi, Jeremy Kepner, Antonio Rosa, Michael Jones 0001, Chansup Byun, Vijay Gadepally, Charles Yee |
| **15** | 51 | 206 | Peter Michaleas, Matthew Hubbell, Siddharth Samsi, David Bestor, William Arcand, Albert Reuther, Andrew Prout, Lauren Milechin, Jeremy Kepner, Julie Mullen, Antonio Rosa, Michael Jones 0001, Chansup Byun, Vijay Gadepally, Charles Yee |
| **16** | 40 | 21 | Peter Michaleas, Matthew Hubbell, Siddharth Samsi, David Bestor, William Arcand, Andrew Prout, Jeremy Kepner, Julie Mullen, Anna Klein, Albert Reuther, Lauren Milechin, Antonio Rosa, Michael Jones 0001, Chansup Byun, Vijay Gadepally, Charles Yee |
| **17** | 26 | 1 | Peter Michaleas, Matthew Hubbell, Siddharth Samsi, David Bestor, William Arcand, Andrew Prout, Jeremy Kepner, Julie Mullen, Michael Houle 0001, Anna Klein, Albert Reuther, Lauren Milechin, Antonio Rosa, Michael Jones 0001, Chansup Byun, Vijay Gadepally, Charles Yee |

### 3.2 Associatieregels

Overzicht van het aantal gevonden associatieregels met $\text{max\_rhs} = 1$ (maximaal 1 auteur aan de rechterzijde van de regel).

| Dataset | Support Drempel ($s$) | Max RHS | Regels ($\text{Conf} \ge 0.5$) | Regels ($\text{Conf} \ge 0.8$) | Regels ($\text{Conf} = 1.0$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `dataset_tiny.txt` | 5 | 1 | 747 | 564 | 498 |
| `dataset_medium1.txt` | 5 | 1 | 16.908 | 13.185 | 11.014 |
| `dataset_medium2.txt` | 5 | 1 | 568.819 | 562.133 | 525.559 |
| `dataset_large.txt` | 25 | 1 | 12.396 | 6.652 | 1.817 |
| `dataset_all.txt` | 25 | 1 | 2.297.531 | 2.016.383 | 1.320.703 |

---

### 3.3 Bespreking van de Resultaten

Uit de resultaten in Tabel 3.2 vallen een aantal duidelijke trends op:

1. **Invloed van de Confidence Drempel:**
   * Hoe hoger de minimale confidence ($\text{Conf}$), hoe strenger de filter en hoe minder regels er overblijven.
   * Bij `dataset_large.txt` daalt het aantal regels bijvoorbeeld sterk van $12.396$ ($\text{Conf} \ge 0.5$) naar slechts $1.817$ bij een perfecte confidence ($\text{Conf} = 1.0$).
   * Bij datasets zoals `medium2.txt` en `dataset_all.txt` blijft zelfs bij $\text{Conf} = 1.0$ een heel groot deel van de regels over. Dit wijst op erg vaste onderzoeksgroepen die vrijwel altijd samen publiceren.

2. **Verschil tussen Datasets:**
   * Hoewel `medium1.txt` en `medium2.txt` ongeveer evenveel publicaties bevatten (~21.000–22.000), levert `medium2.txt` gigantisch veel meer regels op ($568.819$ vs $16.908$ bij $\text{Conf} \ge 0.5$). Dit komt doordat `medium2.txt` langere frequente auteursets bevat (tot $k=16$).
   * Op de grootste dataset (`dataset_all.txt`) vinden we bij $s=25$ meer dan 2,2 miljoen regels met minstens $50\%$ confidence, en meer dan 1,3 miljoen regels met $100\%$ confidence.

3. **Opmerking over `max_rhs`:**
   * Alle bovenstaande resultaten zijn berekend met $\text{max\_rhs} = 1$ (maximaal 1 auteur aan de rechterkant). 
   * Als we $\text{max\_rhs} > 1$ zouden toelaten, ontstaat er voor grote itemsets een explosie aan mogelijke combinaties. Dit zou leiden tot een hoger aantal regels.
