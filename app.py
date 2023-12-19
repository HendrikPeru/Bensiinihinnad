from flask import Flask, render_template, request
from geopy.geocoders import Nominatim
from geopy.distance import great_circle

app = Flask(__name__)

def saa_koordinaadid(koht):
    geokooder = Nominatim(user_agent="minu_rakendus")
    asukoht = geokooder.geocode(koht)

    if asukoht:
        laiuskraad = asukoht.latitude
        pikkuskraad = asukoht.longitude
        return laiuskraad, pikkuskraad
    else:
        return None

def vahemaa(asukoht1, asukoht2):
    kaugus = great_circle(asukoht1, asukoht2).kilometers
    return kaugus

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    if request.method == 'POST':
        koht1 = request.form['koht1']
        koht2 = request.form['koht2']
        
        asukoht1 = saa_koordinaadid(koht1)
        asukoht2 = saa_koordinaadid(koht2)
        
        if asukoht1 and asukoht2:
            kaugus = vahemaa(asukoht1, asukoht2)
            if kaugus < 1:
                tulemus = f"Kahe asukoha vaheline kaugus: {round(kaugus*1000)} meetrit"
            else:
                tulemus = f"Kahe asukoha vaheline kaugus: {round(kaugus, 2)} kilomeetrit"
            return render_template('result.html', tulemus=tulemus)
        else:
            return "Üks või mõlemad asukohad ei leitud."

if __name__ == '__main__':
    app.run(debug=True
