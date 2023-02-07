from crawler.getSession import User
from bs4 import BeautifulSoup
from utils.unicodes import normalize
class MIO:
    def __init__(self, username, password, headers):
        self.username = username
        self.password = password
        self.headers = headers

    def getMIO(self):
        # Gives a list of all the MIO sent and received
        ses = User(self.username, self.password, self.headers).openSession()
        s = ses.session
        mioredirect = s.get("https://cegepmontpetit.omnivox.ca/intr/Module/ServicesExterne/RedirigeMio.ashx", headers=self.headers)
        parsedredir = BeautifulSoup(mioredirect.text, "lxml")
        miodetaillien = parsedredir.find("frame", attrs={"id": "frMilieu"}).attrs["src"]
        miolist = s.get(f"https://cegepmontpetit.omnivox.ca{miodetaillien}", headers=self.headers)
        parsedmiolist = BeautifulSoup(miolist.text, "lxml")
        mioparsedlist = parsedmiolist.find("frame", attrs={"id": "FrListeHaut", "name": "FrListeHaut"}).attrs["src"]
        miomailshtml = s.get(f"https://cegepmontpetit.omnivox.ca{mioparsedlist}", headers=self.headers)
        parsedmailtg = BeautifulSoup(miomailshtml.text, "lxml")
        mailids = parsedmailtg.find_all("div")
        tempdivlist = []
        for m in mailids:
            if m.has_attr("data-message"):
                tempdivlist.append(m)
        mios = []
        for ids in tempdivlist:
            id = ids.attrs["data-message"]
            ma = s.get(f"https://cegepmontpetit.omnivox.ca/WebApplication/Module.MIOE/Commun/Message/MioDetail.aspx?C=EDM&E=P&L=FRA&Ref=20230205175100&m={id}", headers=self.headers)
            parsedmail = BeautifulSoup(ma.text, "lxml")
            emeteur = parsedmail.find("td", class_=["cDe"]).text
            date = parsedmail.find("td", class_=["cDate"]).text
            subject = parsedmail.find("td", class_=["cSujet"]).text,
            content = parsedmail.find("div", attrs={"id": "contenuWrapper"}).text
            mios.append({
                "id": id,
                "emeteur": normalize(emeteur),
                "date": normalize(date),
                "subjet": normalize(subject),
                "content": normalize(content)
            })
        return mios