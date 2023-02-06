import crawler.account as cr
from crawler.mio import MIO
import json, requests

def config():
    with open("config.json", "r") as f:
        conf = json.loads(f.read())
    return conf

config = config()

omnivoxacc = cr.OmnivoxAccount(config["username"], config["password"], config["headers"])
#name = omnivoxacc.getFullname()
#mail = omnivoxacc.getEMail()
#addrp = omnivoxacc.getAdressePrincipale()
#phone = omnivoxacc.getPhoneNumber()
#photo = omnivoxacc.getStudentPicture()
mio = MIO(config["username"], config["password"], config["headers"])
getmio = mio.getMIO()