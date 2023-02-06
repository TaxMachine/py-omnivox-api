import crawler.getSession as cr, bs4, requests

def getSchedule(username, password):
    s = cr.User(username, password).getUseraccount()
    parsedmain = bs4.BeautifulSoup(mainpage.text, "lxml")
    horairelink1 = parsedmain.find("a", attrs={"id": "ctl00_partOffreServices_offreV2_HOR"}).attrs["href"]
    horaire1 = s.get(f"https://cegepmontpetit.omnivox.ca{horairelink1}", headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    })
    parsedhoraire1 = bs4.BeautifulSoup(horaire1.text, "lxml")
    replacedreqlink = parsedhoraire1.find("body", attrs={"text": "#000000"}).attrs["onload"]
    cleanedreqlink = unquote(replacedreqlink.split("'")[1])
    horaire2 = s.get(f"https://cegepmontpetit-estd.omnivox.ca/estd/hrre/{cleanedreqlink}", headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    })
    print(horaire2)
        #horairelink2 = parsedhoraire1.find("form", attrs={"autocomplete": "off"})

        #horaire2 = s.post(f"https://cegepmontpetit-estd.omnivox.ca/estd/hrre{horairelink2}")
    return mainpage.text