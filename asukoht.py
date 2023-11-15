from geopy.geocoders import Nominatim
from geopy.distance import great_circle

def saa_koordinaadid(koht):
    geokooder = Nominatim(user_agent="minu_rakendus")
    asukoht = geokooder.geocode(koht)

    if asukoht:
        laiuskraad = asukoht.latitude
        pikkuskraad = asukoht.longitude
        return laiuskraad, pikkuskraad
    else:
        print(koht, 'ei leitud.')

koht1 = input('Sisesta enda asukoht: ')
koht2 = input('Sisesta sihtpunkt: ')

asukoht1 = saa_koordinaadid(koht1)
asukoht2 = saa_koordinaadid(koht2)

def vahemaa(asukoht1, asukoht2):
    kaugus = great_circle(asukoht1, asukoht2).kilometers
    return kaugus

kaugus = vahemaa(asukoht1, asukoht2)
if kaugus < 1:
    print('Kahe asukoha vaheline kaugus:' ,round(kaugus*1000), 'meetrit')
else:
    print('Kahe asukoha vaheline kaugus:' ,round(kaugus,2), 'kilomeetrit')