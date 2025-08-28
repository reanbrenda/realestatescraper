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
    encoded="https://www.mallorcasite.com/en/properties-in-mallorca?page=3"
    url=urllib.parse.unquote(encoded)
    url=url.replace('3',number)
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
    links=[]
    divClass="property-item estate-item"
    soup=get_html(correct_encoded_url)
    items=soup.findAll('div', class_=divClass)
    for item in items :
        if (item.findChild("div", class_="property-item__wrapper") and "sale" in item.find("a").get("href") and len(item.find("a").get("href").split("-"))>1 ):
            links.append(item.find("a").get("href")) 
    return links
allHomeDetails=[]
for i in range (1,4):  # Limited to 3 pages for speed
    allHomeDetails+=findHomesOfThePage(correct_encoded_url=findAPageUrl(str(i)))
def decodeStr(encodedString):
    return encodedString#.encode("latin1").decode("utf-8")
class Home:
    def __init__(self,link):
        self.link=link
        self.soup=get_html(link)
    def getNumber(self,pr):
            ans=0
            for l in pr:
                if (l>='0' and l<='9'):
                    ans*=10
                    ans+=int(l)
            return ans
    def findWord(self):
        categories=["villa","apartment","plot","hotel"]
        for category in categories : 
            if (category in self.link) : 
                return category 
        return "other" 
    def getLink(self)->str:
        return self.link
    def getMainImage(self)->str:
        try : 
            return self.soup.find('div',class_="property-gallery__wrapper js-gallery").findChild('a').findChild('img').get('src') 
        except Exception :
            return None 
    def getAllImages(self)->list:
        allA=self.soup.find('div',class_="property-gallery__wrapper js-gallery").findChildren('a')
        return [anA.findChild("img").get("src") for anA in allA]
    def getTitle(self)->str:
        try : 
            return [line.strip() for line in str(self.soup.find('div',class_="property-inner__right").text).splitlines() if line.strip()][0]
        except Exception :
            return None 
    def getLocation(self)->str:
        try :
            return str((self.soup.findAll('div',class_="property-feature")[4]).text).strip()
        except Exception : 
            return None  
    def getDescription(self)->str:
        return '\n'.join(line.strip() for line in str(self.soup.find('p',class_="property-description").text).splitlines() if line.strip())
    def getPrice(self):
        return self.getNumber(self.soup.find('div',class_="property-price").text)
    def getPlatfrom(self)->str:
        return "mallorcasite.com"
    def getLivingSpace(self):
        elements=self.soup.findAll('div',class_="property-feature")
        return self.getNumber(elements[0].text)
    def getLandArea(self):
        elements=self.soup.findAll('div',class_="property-feature")
        return self.getNumber(elements[1].text)
    def getBuiltUp(self):
        return None
    def getBathrooms(self)->int:
        elements=self.soup.findAll('div',class_="property-feature")
        return self.getNumber(elements[3].text)
    def getBedrooms(self)->int:
        elements=self.soup.findAll('div',class_="property-feature")
        return self.getNumber(elements[2].text)
    def getCategory(self):
        return self.findWord()
    def getId(self): 
        return None
    def getAll(self):
        return {
            "platform":decodeStr(str(self.getPlatfrom())),
            "Property ID":decodeStr(str(self.getId())),
            "link":decodeStr(str(self.getLink())),
            "location":decodeStr(str(self.getLocation())),
            "mainImage":decodeStr(str(self.getMainImage())),
            "allImages":decodeStr(str(self.getAllImages())),
            "title":decodeStr(str(self.getTitle())),
            "description":decodeStr(str(self.getDescription())),
            "price":decodeStr(str(self.getPrice())),
            "livingSpace":decodeStr(str(self.getLivingSpace())),
            "landArea":decodeStr(str(self.getLandArea())),
            "builtUp":decodeStr(str(self.getBuiltUp())),
            "bathrooms":decodeStr(str(self.getBathrooms())),
            "bedrooms":decodeStr(str(self.getBedrooms())),
            "category":decodeStr(str(self.getCategory()))
            
        }
homeObjects=[]
for homeLink in allHomeDetails:
    homeObjects.append(Home(homeLink))
homesData=[]
for home in  homeObjects:
    homesData.append(home.getAll())
with open("web_2_data.json","w",encoding="utf-8") as jsonFile:
    json.dump(homesData,jsonFile,ensure_ascii=False,indent=4)
