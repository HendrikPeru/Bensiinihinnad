import requests
from bs4 import BeautifulSoup
import csv

def veebist(url, css_selector):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    andmed = soup.select(css_selector)
    return andmed

def csvfail(veerud, read, failinimi):
    with open(failinimi, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')  
        writer.writerow(veerud)
        for rida in read:
            for veerg in rida:
                writer.writerow([veerg])

veebileht = "https://gas.didnt.work/?country=ee&brand=&city="
css_selector = ".table"  
veebiandmed = veebist(veebileht, css_selector)

if veebiandmed:
    veerud = [header.get_text(strip=True) for header in veebiandmed[0].find_all('th')]
    read = [[td.get_text(strip=True) for td in rida.find_all('td')] for rida in veebiandmed]
    failinimi = 'veebi_andmed.csv'
    csvfail(veerud, read, failinimi)
    print("Andmed on salvestatud faili:", failinimi)
else:
    print("Andmete skreipimisel tekkis probleem.")
