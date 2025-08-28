import requests
from bs4 import BeautifulSoup
import json
import re
import html
import os
def get_html(url): # function for geting the html using request
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, "html.parser")
    else:
        print(f"Failed to fetch {url}")
        return None
def findAPageUrl(number:str):
    import urllib.parse
    encoded="https://www.john-taylor.com/spain/sale/mallorca/p1"
    encoded=encoded.replace('1',number)
    if encoded.endswith("1"): 
        encoded=encoded[:-2]
    url=urllib.parse.unquote(encoded)
    # Parse the URL into components
    parsed_url = urllib.parse.urlparse(url)
    # Parse and re-encode the query parameters
    query_params = urllib.parse.parse_qs(parsed_url.query)
    encoded_query = urllib.parse.urlencode(query_params, doseq=True)
    # Reassemble the URL
    correct_encoded_url = urllib.parse.urlunparse((
        parsed_url.scheme,
        parsed_url.netloc,
        parsed_url.path,
        parsed_url.params,
        encoded_query,
        parsed_url.fragment
    ))

    return correct_encoded_url
def findHomesOfThePage(correct_encoded_url):
    divClass="cell col-lg-4 col-sm-6 col-xs-12 row"
    soup=get_html(correct_encoded_url)
    items=soup.findAll('div', class_=divClass)
    return [item.findChild("div",  class_="cell product-holder").findChild("a").get("href") for item in items]
allHomeDetails=[]
firstPage=None
for i in range (1,4):  # Limited to 3 pages for speed
    pageLinks=findHomesOfThePage(correct_encoded_url=findAPageUrl(str(i)))
    if pageLinks==firstPage : 
        break
    if firstPage==None : 
        firstPage=pageLinks
    allHomeDetails+=pageLinks
allHomeDetails
def decodeStr(encodedString):
    return encodedString#.encode("latin1").decode("utf-8")
def safe_return(default=None):
    """Decorator that returns a default value if an exception occurs."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                return default
        return wrapper
    return decorator
def findImage(img):
    pattern = r"\(\'(.+)\'\)"
    if img :
        # re.DOTALL allows '.' to match newlines as well.
        matches = re.findall(pattern, img )
        return matches[0]
class Home:
    def __init__(self, link):
        self.link = link
        self.soup = get_html(link)
    
    def getNumber(self, pr):
        ans = 0
        for l in pr:
            if '0' <= l <= '9':
                ans *= 10
                ans += int(l)
        return ans
    def findPrice(self,price):
        pattern=r'content=\"(.*)\.00\"'
        return  re.findall(pattern,price)[0]
    @safe_return(None)
    def getLink(self) -> str:
        return self.link
    def getEssntialDetails(self):
        return self.soup.find("div", class_="box-outer property-product-panel").findChild("div").findChild("div").findChild("div").findNextSibling("div",class_="row essential-panel").findChild("div",class_="cell col-lg-3 col-md-3 col-xs-12")
    def getIconDetails(self,name) : 
        icons=self.soup.find("div", class_="box-outer property-product-panel").findChild("div").findChild("div").findChild("div").findAll("span",class_="list_icons")
        for icon in icons: 
            if name in icon.text : 
                return icon.text
        raise (" no resualt for the name: ", name)
    @safe_return(None)
    def getMainImage(self) -> str:
        return findImage(str(self.soup.findChild("main").findChild("section").findChild("div",class_="box-outer").find("div",class_="clic-picture")))
    @safe_return(None)
    def getAllImages(self) -> list:
        allImages= self.soup.findChild("main").findChild("section").findChild("div",class_="box-outer").findAll("div",class_="clic-picture")
        return  [findImage(str(img)) for img in allImages]
    @safe_return("No tiltle")
    def getTitle(self) -> str:
        return [line.strip() for line in str(self.soup.find('div', class_="box-inner property-product-header").text).splitlines() if line.strip()][0]

    @safe_return(None)
    def getLocation(self) -> str:
        return str((self.soup.findAll('div', class_="property-feature")[4]).text).strip()

    @safe_return(None)
    def getDescription(self) -> str:
        description=self.soup.find("div", class_="box-outer property-product-panel").findChild("div").findChild("div").findChild("div").findNextSibling("div",class_="row essential-panel").findChild("div",class_="cell col-lg-8 col-md-9 col-xs-12").text
        return '\n'.join(line.strip() for line in str(description).splitlines() if line.strip())

    @safe_return(None)
    def getPrice(self):
        return self.findPrice(str(self.getEssntialDetails().find("h2",class_="inherith2 h2_price")))

    @safe_return(None)
    def getPlatfrom(self) -> str:
        return "john-taylor.com/spain/sale/mallorca"

    @safe_return(None)
    def getLivingSpace(self):
        return self.getNumber(self.getIconDetails("m²"))

    @safe_return(None)
    def getLandArea(self):
        return self.getNumber(self.getIconDetails("m²"))

    @safe_return(None)
    def getBuiltUp(self):
        # something
        return None

    @safe_return(None)
    def getBathrooms(self) -> int:
        return self.getNumber(self.getIconDetails("Bathrooms"))

    @safe_return(None)
    def getBedrooms(self) -> int:
        return self.getNumber(self.getIconDetails("Bedrooms"))

    @safe_return(None)
    def getCategory(self):
        return self.getEssntialDetails().find("ul",class_="prod-bullets prod-bullets2 row").findChildren("li")[-1].text

    @safe_return(None)
    def getId(self):
        return self.getEssntialDetails().find("ul",class_="prod-bullets prod-bullets2 row").find("li").text

    def getAll(self):
        return {
            "platform": decodeStr(str(self.getPlatfrom())),
            "Property ID": decodeStr(str(self.getId())),
            "link": decodeStr(str(self.getLink())),
            "location": decodeStr(str(self.getLocation())),
            "mainImage": decodeStr(str(self.getMainImage())),
            "allImages": decodeStr(str(self.getAllImages())),
            "title": decodeStr(str(self.getTitle())),
            "description": decodeStr(str(self.getDescription())),
            "price": decodeStr(str(self.getPrice())),
            "livingSpace": decodeStr(str(self.getLivingSpace())),
            "landArea": decodeStr(str(self.getLandArea())),
            "builtUp": decodeStr(str(self.getBuiltUp())),
            "bathrooms": decodeStr(str(self.getBathrooms())),
            "bedrooms": decodeStr(str(self.getBedrooms())),
            "category": decodeStr(str(self.getCategory()))
        }
 
homesData=[]
homeObjects=[Home(home) for home in allHomeDetails]
for home in  homeObjects:
    homesData.append(home.getAll())
with open("web_5_1_data.json","w",encoding="utf-8") as jsonFile:
    json.dump(homesData,jsonFile,ensure_ascii=False,indent=4)