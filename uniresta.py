from urllib import urlopen
import StringIO
import htmllib
import formatter
import time

BASE_URL = "http://www.uniresta.fi/tulostettava_ruokalista.php" \
           "?ravintola=%s&viikko=%s&vuosi=%s"

raflat = dict()
raflat["aula"] = "2"
raflat["discus"] = "3"
raflat["julinia"] = "4"
raflat["kastari"] = "5"
raflat["snellmania"] = "6"
raflat["pruxis"] = "7"
raflat["datania"] = "8"
raflat["caio"] = "9"
raflat["vanilla"] = "10"

paivat = dict()
paivat[1] = "Maanantai"
paivat[2] = "Tiistai"
paivat[3] = "Keskiviikko"
paivat[4] = "Torstai"
paivat[5] = "Perjantai"

def uniresta(msg):
    vastaus = str()
    ravintola = "aula"
    paiva = int(time.strftime("%w"))
    
    if paiva not in paivat:
        return "Et saa ruokaa"
    
    words = msg.split()
    if len(words) > 1 and words[1] != "":
        for key in raflat.iterkeys():
            if key.lower().startswith(words[1].lower()):
                ravintola = key
    
    raflanumero = raflat[ravintola]
    viikko = str(int(time.strftime("%W")) + 1)
    vuosi = time.strftime("%Y")
    
    url = BASE_URL % (raflanumero, viikko, vuosi)
    
    html = urlopen(url).read()
    outfile = StringIO.StringIO()
    writer = formatter.DumbWriter(outfile)
    my_formatter = formatter.AbstractFormatter(writer)
    parser = htmllib.HTMLParser(my_formatter)
    parser.feed(html)
    parser.close()
    data = outfile.getvalue()
    outfile.close()
    
    data = data[data.find("Maanantai"):]
    
    if paivat[paiva] == "Perjantai":
        perjantai_paikka = data.find(paivat[paiva])
        menu = data[perjantai_paikka:]
    else:
        tanaan_paikka = data.find(paivat[paiva])
        huomenna_paikka = data.find(paivat[paiva+1])
        menu = data[tanaan_paikka:huomenna_paikka]
    
    rafla = ravintola.capitalize()
    menu = menu.strip().replace("\n", " ")
    
    if menu != "":
        vastaus = "%s tarjoaa %s" % (rafla, menu)
    else:
        vastaus = "Ilmeisesti %s ei tarjoa ruokaa nyt." % rafla
    
    return vastaus
