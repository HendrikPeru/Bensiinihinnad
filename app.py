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

def saa_kütusehinnad(url):
    vaste = requests.get(url)
    soup = BeautifulSoup(vaste.text, 'html.parser')
    kütusehinnad = {}

    # Leitakse kõik tabelid
    tabelid = soup.find_all('table')

    for tabel in tabelid:
        read = tabel.find_all('tr')[1:]  # Ignoreerime päiseid

        for rida in read:
            veerud = rida.find_all('td')

            # Kui veerge on vähem kui oodatakse, siis jäetakse rida vahele
            if len(veerud) < 5:
                continue

            # Leia aadress, mis on br ja small tagide vahel
            aadress_tag = veerud[0].find('br').find_next('small')
            if aadress_tag:
                aadress = aadress_tag.text.strip()  # Aadressi tekst

                # Kütusehindade ennik
                hinnad = (
                    veerud[1].text.strip(),
                    veerud[2].text.strip(),
                    veerud[3].text.strip(),
                    veerud[4].text.strip()
                )

                # Lisatakse sõnastik listi
                kütusehinnad[aadress] = hinnad

    return kütusehinnad

def lähimad_tanklad(kasutaja_aadress, max_distants):
    # Kasutab funktsiooni saa_kütusehinnad, et saada kõikide tanklate kütusehinnad
    url = "https://gas.didnt.work/?country=ee&brand=&city="
    kõik_tanklad = saa_kütusehinnad(url)

    # Kasutab funktsiooni saa_koordinaadid, et saada kasutaja aadressi koordinaadid
    koordinaadid = saa_koordinaadid(kasutaja_aadress)
    lähedal_olevad_tanklad = {}

    # Kui koordinaadid on olemas, siis leitakse kõik tanklad, mis on antud kauguse piires
    if koordinaadid:
        for aadress, koordinaat in kõik_tanklad.items():
            tanklakoordinaat = saa_koordinaadid(aadress)
            if tanklakoordinaat:
                distants = great_circle(koordinaadid, tanklakoordinaat).kilometers
                if distants <= max_distants:
                    lähedal_olevad_tanklad[aadress] = kõik_tanklad[aadress]
        # Kui leiti sobivaid tanklaid, siis tagastatakse need
        if lähedal_olevad_tanklad:
            return lähedal_olevad_tanklad
        # Kui ei leitud sobivaid tanklaid, siis tagastatakse veateade
        else:
            return "Ühtegi sobivat tanklat ei leitud antud kauguse piires."

# Kui kasutaja sisestab aadressi ja maksimaalse kauguse, siis tagastatakse talle sobivad tanklad
@app.route('/', methods=['GET', 'POST'])
def index():
    # Kui kasutaja vajutab nuppu, siis võetakse vormist andmed
    if request.method == 'POST':
        kasutaja_aadress = request.form['address']
        max_dist = float(request.form['max_distance'])
        result = lähimad_tanklad(kasutaja_aadress, max_dist)
        # Kui tulem on sõnastik, siis tagastatakse sobivad tanklad
        if isinstance(result, dict):
            return render_template('tulemused.html', result=result)
        # Kui tulem on veateade, siis tagastatakse veateade
        else:
            return render_template('tulemused.html', error=result)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
