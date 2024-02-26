
Tento projekt slouzi k extrahovani vysledku z parlamentnich voleb z roku 2017.

Odkaz k prohlednuti: https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ

Knihovny viz. requirements.txt

Po instalaci doporucuji pouzit nove virtualni prostredi a s nainstalovanym manazerem spustit nasledovne:

py -3 -m pip venv virtualenv

source myenv\Scripts\activate

python3 pip freeze requirements.txt

Spusteni souboru election-scraper.py v ramci prikazoveho radku pozaduje dva povinnne argumenty.

python election-scraper <odkaz-uzemniho-celku> <vysledny-soubor>

Nasledne se vam stahnou vyslekdy jako soubor s priponou .csv.

Ukazka projektu:
code	location	registered	envelopes	valid	Občanská demokratická strana	Řád národa - Vlastenecká unie
                        
598925	Albrechtice	3173	1957	1944	109	4
                        
599051	Bohumín	17613	9040	8973	579	12
                        
598933	Český Těšín	19635	10429	10361	698	15
                        
598941	Dětmarovice	3507	2061	2048	148	3

Vysledky hlasovani pro okres karvina: 

1.argument: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8103
2.argument: vysledky_karvina.csv

Spusteni programu:

python election-scraper.py 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8103' 'vysledky_karvina.csv'

Prubeh stahovani:

STAHUJI DATA Z VYBRANEHO URL: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8103
UKLADAM DO SOUBORU: vysledky_karvina.csv
UKONCUJI election-scraper

Castecny vystup:







