import requests, bs4, json

class User:
    def __init__(self, username, password, header):
        self.username = username
        self.password = password
        self.header = header

    def openSession(self):
        # Opens an Omnivox session to store all the cookies because ASP.NET fucking sucks why they didn't made a fucking graphql JSON API 😠
        s = requests.Session()
        getform = s.get(f"https://cegepmontpetit.omnivox.ca/Login/Account/Login?ReturnUrl=%2fintr%2f", headers=self.header)
        parsedform = bs4.BeautifulSoup(getform.text, features="lxml")
        token = parsedform.find("input", attrs={"name": "k"}).attrs["value"]
        mainpage = s.post("https://cegepmontpetit.omnivox.ca/intr/Module/Identification/Login/Login.aspx", headers=self.header, data={
            "k": token,
            "TypeLogin": "PostSolutionLogin",
            "TypeIdentification": "Etudiant",
            "ReturnUrl": "/intr/",
            "NoDA": self.username,
            "PasswordEtu": self.password
        })

        home = s.post(
            "https://cegepmontpetit.omnivox.ca/intr/",
            headers=self.header
        )
        self.session = s
        self.home = home.text
        return self