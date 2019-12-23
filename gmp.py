#######################################
###
### GENERATOR MIKRORACHUNKU PODATKOWEGO
###
#######################################

import requests

# na podstawie długości input_data określana jest informacja czy wprowadzono NIP czy PESEL
input_data = "5252674798"

url_nip = 'https://www.podatki.gov.pl/umbraco/surface/TaxAccountNumberSearch/GetAccountNumberByNip'
url_pesel = 'https://www.podatki.gov.pl/umbraco/surface/TaxAccountNumberSearch/GetAccountNumberByPesel'

cookies = {
    'cookieconsent_status': 'dismiss',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:71.0) Gecko/20100101 Firefox/71.0',
    'Accept': '*/*',
    'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
    'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://www.podatki.gov.pl',
    'Connection': 'keep-alive',
    'Referer': 'https://www.podatki.gov.pl/generator-mikrorachunku-podatkowego',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}

if len(input_data)==10: # NIP-10cyfr, PESEL=11cyfr
    data = { 'nip': input_data }
    url = url_nip
else:
    data = { 'pesel': input_data }
    url = url_pesel

try:
    response = requests.post(url, headers=headers, cookies=cookies, data=data)
    txt = str(response.content).upper()
    if "PODATKOWY" in txt:
        pos1 = txt.find(": PL")
        pos2 = txt.find("</SPAN>", pos1)
        if not(pos1==-1 or pos2==-1):
            txt = txt[pos1+1:pos2].strip()
            print(txt)
        else:
            print("Nie znaleziono numeru mikrorachunku podatkowego")
    else:
        print("Nie znaleziono numeru mikrorachunku podatkowego")
except Exception as exc:
    print("Wystąpił wyjątek: ",str(exc))
