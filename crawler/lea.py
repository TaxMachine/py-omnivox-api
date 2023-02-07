import requests
from crawler.getSession import User
from bs4 import BeautifulSoup
from utils.unicodes import normalize

class LEA:
    def __init__(self, username, password, headers):
        self.username = username,
        self.password = password,
        self.headers = headers

    def getNotifications(self):
        # TODO: Make that shit works
        ses = User(self.username, self.password, self.headers).openSession()
        s = ses.session
        parsedhome = BeautifulSoup(ses.home, "lxml")
        req = s.post("https://cegepmontpetit.omnivox.ca/intr/UI/WebParts/Intraflex_QuoiDeNeuf/WebServiceQuoiDeNeuf.asmx/AddItemCache", headers={
            "User-Agent": self.headers["User-Agent"],
            "Content-Type": "application/json"
        })
    
    def getLEA(self):
        # Gives a list of all classes in LEA
        ses = User(self.username, self.password, self.headers).openSession()
        s = ses.session
        link = BeautifulSoup(ses.home, "lxml").find("a", class_=["raccourci", "id-service_CVIE", "code-groupe_lea"]).attrs["href"]
        lea = s.get(f"https://cegepmontpetit.omnivox.ca{link}", headers=self.headers)
        parsedlea = BeautifulSoup(lea.text, "lxml")
        divcentre = parsedlea.find("div", class_=["classes-wrapper", "materialize-wrapper"])
        coursraw = divcentre.find_all("div", class_=["card-panel", "section-spacing"])
        lstCours = []
        for cours in coursraw:
            name = cours.find("div", class_=["card-panel-title"]).text
            desc = cours.find("div", class_=["card-panel-desc"]).text
            
            teacher = desc.split(", ")[-1]
            group = desc.split(" - ")[0]
            lstCours.append(
                {
                    "name": normalize(name),
                    "teacher": normalize(teacher),
                    "group": normalize(group)
                }
            )
        return lstCours