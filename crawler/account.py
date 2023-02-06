import crawler.getSession as cr
import requests, base64
from urllib.parse import unquote
from bs4 import BeautifulSoup

class OmnivoxAccount:
    def __init__(self, username, password, headers):
        self.username = username
        self.password = password
        self.headers = headers

    def getFullname(self):
        ses = cr.User(self.username, self.password, self.headers).openSession()
        parsedmain = BeautifulSoup(ses.home, "lxml")
        nom = parsedmain.find("span", attrs={"id": "headerNavbarProfileUserName"}).text.replace("\r\n ", "")
        return nom

    def getDossierPerso(self):
        ses = cr.User(self.username, self.password, self.headers).openSession()
        s = ses.session
        parsedmain = BeautifulSoup(ses.home, features="lxml")
        dossierurl = parsedmain.find("a", attrs={"id": "ctl00_partOffreServices_offreV2_ADR"}).attrs["href"]
        dossierpersoget = s.get(f"https://cegepmontpetit.omnivox.ca{dossierurl}", headers=self.headers)
        fetchlink = unquote(BeautifulSoup(dossierpersoget.text, "lxml").find("body").attrs["onload"].split("'")[1])
        dossierloadsession = s.get(f"https://cegepmontpetit-estd.omnivox.ca/estd/{fetchlink}", headers=self.headers)
        dossier = s.get("https://cegepmontpetit-estd.omnivox.ca/estd/ress/Dossier.ovx", headers=self.headers)
        dossierpass = s.post("https://cegepmontpetit-estd.omnivox.ca/estd/ress/Dossier.ovx", headers=self.headers, data={
            "txtPassword_frmConfirmPassword": self.password,
            "txtPassword": ""
        })
        dossierperso = BeautifulSoup(dossierpass.text, "lxml")
        self.session = s
        self.addrP = dossierperso.find("a", attrs={"onmouseover": "self.status='Adresse principale'; return true"}).attrs["href"]
        self.addrS = dossierperso.find("a", attrs={"onmouseover": "self.status='Adresse secondaire'; return true"}).attrs["href"]
        self.phone = dossierperso.find("a", attrs={"onmouseover": "self.status='Numéros de téléphone'; return true"}).attrs["href"]
        self.email = dossierperso.find("a", attrs={"onmouseover": "self.status='Courriel'; return true"}).attrs["href"]
        self.photo = dossierperso.find("a", attrs={"onmouseover": "self.status='Photo d\\'identité'; return true"}).attrs["href"]
        return self

    def getEMail(self):
        ses = self.getDossierPerso()
        s = ses.session
        mailpage = s.get(ses.email, headers=self.headers)
        parsed = BeautifulSoup(mailpage.text, "lxml")
        return parsed.find("span", attrs={"style": "margin:0 15px 5px 0;display:inline-block"}).text

    def getAdressePrincipale(self):
        ses = self.getDossierPerso()
        s = ses.session
        addrp = s.get(f"https://cegepmontpetit-estd.omnivox.ca/estd/ress/{ses.addrP}")
        parsedp = BeautifulSoup(addrp.text, "lxml")
        iframearr = parsedp.find_all("iframe")[0]
        iframe = iframearr.attrs["src"]
        addrpform = s.get(iframe, headers=self.headers)
        addrpage = BeautifulSoup(addrpform.text, "lxml")
        adresses = addrpage.find_all("input", attrs={"name": "uSaisieAdresse$uSaisieAutomatique$txtNoCiv"})
        self.codepostal = addrpage.find("input", attrs={"name": "uSaisieAdresse$uSaisieAutomatique$txtCodePostal"}).attrs["value"]
        self.adresse = adresses[0].attrs["value"]
        self.rue = addrpage.find("select", attrs={"name": "uSaisieAdresse$uSaisieAutomatique$ddlRue"}).find("option", attrs={"selected": "true"}).attrs["value"]
        self.appartement = adresses[0].attrs["value"]
        self.ville = addrpage.find("select", attrs={"name": "uSaisieAdresse$uSaisieAutomatique$ddlVille"}).find("option", attrs={"selected": "true"}).attrs["value"]
        self.province = addrpage.find("select", attrs={"name": "uSaisieAdresse$uSaisieAutomatique$ddlProvince"}).find("option", attrs={"selected": "true"}).attrs["value"]
        self.pays = addrpage.find("select", attrs={"name": "uSaisieAdresse$uSaisieAutomatique$ddlPays"}).find("option", attrs={'selected':"true"}).text.strip()
        return self

    def getAdresseSecondaire(self):
        ses = self.getDossierPerso()
        s = ses.session
        addrp = s.get(f"https://cegepmontpetit-estd.omnivox.ca/estd/ress/{ses.addrS}")
        parsedp = BeautifulSoup(addrp.text, "lxml")
        iframearr = parsedp.find_all("iframe")[0]
        iframe = iframearr.attrs["src"]
        addrpform = s.get(iframe, headers=self.headers)
        addrpage = BeautifulSoup(addrpform.text, "lxml")
        adresses = addrpage.find_all("input", attrs={"name": "uSaisieAdresse$uSaisieAutomatique$txtNoCiv"})
        self.codepostal = addrpage.find("input", attrs={"name": "uSaisieAdresse$uSaisieAutomatique$txtCodePostal"}).attrs["value"]
        self.adresse = adresses[0].attrs["value"]
        self.rue = addrpage.find("select", attrs={"name": "uSaisieAdresse$uSaisieAutomatique$ddlRue"}).find("option", attrs={"selected": "true"}).attrs["value"]
        self.appartement = adresses[0].attrs["value"]
        self.ville = addrpage.find("select", attrs={"name": "uSaisieAdresse$uSaisieAutomatique$ddlVille"}).find("option", attrs={"selected": "true"}).attrs["value"]
        self.province = addrpage.find("select", attrs={"name": "uSaisieAdresse$uSaisieAutomatique$ddlProvince"}).find("option", attrs={"selected": "true"}).attrs["value"]
        self.pays = addrpage.find("select", attrs={"name": "uSaisieAdresse$uSaisieAutomatique$ddlPays"}).find("option", attrs={'selected':"true"}).text.strip()
        return self

    def getPhoneNumber(self):
        ses = self.getDossierPerso()
        s = ses.session
        phonepage = s.get(f"https://cegepmontpetit-estd.omnivox.ca/estd/ress/{self.phone}", headers=self.headers)
        parsed = BeautifulSoup(phonepage.text, "lxml")
        allphone = parsed.find_all("font", attrs={"face": "Arial, Helvetica", "size": "2"})
        self.principal = allphone[1].text
        self.travail = allphone[3].text
        self.secondaire = allphone[5].text
        return self

    def getStudentPicture(self):
        ses = self.getDossierPerso()
        s = ses.session
        auth = s.get(f"https://cegepmontpetit-estd.omnivox.ca{self.photo}", headers=self.headers)
        parsed = BeautifulSoup(auth.text, "lxml")
        img = parsed.find("img", attrs={"id": "cntFormulaire_imgPhotoDossier"}).attrs["src"]
        imageget = s.get(f"https://cegepmontpetit-estd.omnivox.ca/WebApplication/Module.PHOE/Etudiant/{img}", headers=self.headers)
        return base64.b64encode(imageget.content)