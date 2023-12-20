from flask import Flask, render_template, request
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def saa_koordinaadid(koht):
    geokooder = Nominatim(user_agent="minu_rakendus")
    asukoht = geokooder.geocode(koht)
    if asukoht:
        laiuskraad = asukoht.latitude
        pikkuskraad = asukoht.longitude
        return laiuskraad, pikkuskraad

def scrape_gas_prices(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    gas_data = {}

    # Leitakse kõik tabelid
    tables = soup.find_all('table')

    for table in tables:
        rows = table.find_all('tr')[1:]  # Ignoreerime päiseid

        for row in rows:
            columns = row.find_all('td')

            # Kui veerge on vähem kui oodatakse, siis jäetakse rida vahele
            if len(columns) < 5:
                continue

            # Leia aadress, mis on br ja small tagide vahel
            address_tag = columns[0].find('br').find_next('small')
            if address_tag:
                address = address_tag.text.strip()  # Aadressi tekst

                # Kütusehindade tuple
                prices = (
                    columns[1].text.strip(),
                    columns[2].text.strip(),
                    columns[3].text.strip(),
                    columns[4].text.strip()
                )

                # Lisatakse sõnastik listi
                gas_data[address] = prices

    return gas_data

def find_closest_gas_stations(user_address, max_distance):
    url = "https://gas.didnt.work/?country=ee&brand=&city="
    all_gas_stations = scrape_gas_prices(url)

    user_coords = saa_koordinaadid(user_address)
    close_stations = {}

    if user_coords:
        for address, coords in all_gas_stations.items():
            station_coords = saa_koordinaadid(address)
            if station_coords:
                distance = great_circle(user_coords, station_coords).kilometers
                if distance <= max_distance:
                    close_stations[address] = all_gas_stations[address]

        if close_stations:
            return close_stations
        else:
            return "Ühtegi sobivat tanklat ei leitud antud kauguse piires."

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_address = request.form['address']
        max_dist = float(request.form['max_distance'])
        result = find_closest_gas_stations(user_address, max_dist)
        if isinstance(result, dict):
            return render_template('tulemused.html', result=result)
        else:
            return render_template('tulemused.html', error=result)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
