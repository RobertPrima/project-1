# projekt_3.py: třetí projekt do Engeto Online Python Akademie

# author: Robert Prima
# email: x.zidy@seznam.cz
# discord: prima.robert

import requests
from bs4 import BeautifulSoup
import csv
import sys
import re




def download_data(url):
    """
    Stáhne data ze zadané URL adresy a analyzuje je pomocí BeautifulSoup.

    :param url: URL adresa, ze které se mají stáhnout data.
    :return: Objekt BeautifulSoup s analyzovanými daty.
    """
    response = requests.get("https://volby.cz/pls/ps2017nss/{0}".format(url))
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    else:
        print("Chyba při stahování stránky:", response.status_code, url)
        return None


def get_statistics(url, statistic):
    """
    Získává statistiky ze stahovaných dat a ukládá je do statistiky.

    :param url: URL adresa, ze které se mají získat statistiky.
    :param statistic: Slovník, do kterého se ukládají statistiky.
    """
    soup = download_data(url[1])
    if soup:
        for h3 in soup.find_all('h3'):
            if ('Obec:' in h3.get_text()):
                statistic['name'] = h3.get_text().split('Obec: ')[1].strip()

        if len(soup.find_all('table')) > 1:
            for i, table in enumerate(soup.find_all('table')):
                if (i == 0):
                    ## okrskova tabulka
                    registered_td = table.find('td', class_="cislo", attrs={"headers": "sa2"})
                    if (registered_td):
                        statistic['registered'] += to_int(registered_td.get_text())
                    envelopes_td = table.find('td', class_="cislo", attrs={"headers": "sa3"})
                    if (envelopes_td):
                        statistic['envelopes'] += to_int(envelopes_td.get_text())
                    valid_td = table.find('td', class_="cislo", attrs={"headers": "sa6"})
                    if (valid_td):
                        statistic['valid'] += to_int(valid_td.get_text())

                else:
                    ## tabulka stran
                    for tr in table.find_all('tr'):
                        candidate = {'number': 0, 'name': '', 'total': 0}
                        for td in tr.find_all('td'):
                            for head in td['headers']:
                                if 'sb1' in head:
                                    candidate['number'] = td.get_text()
                                elif 'sb2' in head:
                                    candidate['name'] = td.get_text()
                                elif 'sb3' in head:
                                    candidate['total'] = to_int(td.get_text())
                        if (candidate['name'] and candidate['number'] and candidate['name'] != '-'):
                            upsert_candidate(statistic['candidates'], candidate)
        else:
            for a in soup.find('table').find_all('a'):
                get_statistics([url[0], a['href']], statistic)


def upsert_candidate(candidates, candidate):
    """
    Přidává nebo aktualizuje informace o kandidátovi v seznamu kandidátů.

    :param candidates: Seznam kandidátů.
    :param candidate: Kandidát, který se má přidat nebo aktualizovat.
    """
    exist_candidate = next((x for x in candidates if x['number'] == candidate['number']), None)
    if exist_candidate:
        exist_candidate['total'] += candidate['total']
    else:
        candidates.append(candidate)


def statistic_to_array(statistic):
    """
    Převádí statistiky na pole pro CSV výstup.

    :param statistic: Slovník se statistikami.
    :return: Pole s hodnotami statistik.
    """
    data = [statistic['code'], statistic['name'], statistic['registered'], statistic['envelopes'], statistic['valid']]
    for candidate in statistic['candidates']:
        data.append(candidate['total'])

    return data


def statistics_to_csv(statistics, output_name):
    """
    Ukládá statistiky do CSV souboru.

    :param statistics: Seznam statistik k uložení.
    :param output_name: Název výstupního CSV souboru.
    """
    csv.register_dialect('myDialect', delimiter=',', quoting=csv.QUOTE_NONNUMERIC, skipinitialspace=True)
    with open(output_name, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, dialect='myDialect')
        header = ['code', 'location', 'registered', 'envelopes', 'valid']
        if len(statistics) > 0:
            for candidate in statistics[0]['candidates']:
                if (candidate['name'] and candidate['number']):
                    header.append(candidate['name'])

        writer.writerow(header)
        for stat in statistics:
            writer.writerow(statistic_to_array(stat))
        f.close()


def is_valid_url(url):
    # Regulární výraz pro kontrolu URL
    url_regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// nebo https:// nebo ftp://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # doménové jméno
        r'localhost|' # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ...nebo IP
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # ...nebo [IPv6]
        r'(?::\d+)?' # volitelný port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return re.match(url_regex, url) is not None

def to_int(val):
    return int(re.sub(r'\D', '', val))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Chybný počet argumentů. Použijte skript s dvěma argumenty.")
        sys.exit(1)

    # První argument (sys.argv[0]) je název skriptu, takže začneme od indexu 1
    url = sys.argv[1]
    output_name = sys.argv[2]

    if is_valid_url(url) == False:
        print("První argument není validní URL")
        sys.exit(1)

    if '.csv' not in output_name:
        print("Druhý argument neobsahuje příponu .csv")
        sys.exit(1)

    
    response = requests.get(url)

    
    if response.status_code == 200:
        print(f"STAHUJI DATA Z VYBRANEHO URL: {url}")
        print(f"UKLADAM DO SOUBORU: {output_name}")
        soup = BeautifulSoup(response.content, 'html.parser')

        urls = []
        for table in soup.find_all('table'):
            for tr in table.find_all('tr'):
                code = ''
                url = ''
                for a in tr.find_all('a'):
                    if (a.get_text() == 'X'):
                        url = a['href']
                    else:
                        code = a.get_text()
                if (code):
                    urls.append([code, url])

        statistics = []
        for url in urls:
            statistic = {'code': url[0], 'registered': 0, 'envelopes': 0, 'valid': 0, 'candidates': []}
            get_statistics(url, statistic)
            statistics.append(statistic)

        statistics_to_csv(statistics, output_name)
        print("UKONCUJI election-scraper")
    else:
        print("Chyba při stahování stránky:", response.status_code, url)