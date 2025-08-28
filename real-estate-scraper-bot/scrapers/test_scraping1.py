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
    encoded="https://www.lucie-hauri.com/en/alle-objekte/?frymo_query=%7B%22suche-alle%22:%7B%22pagenum%22:%222%22%7D%7D"
    url=urllib.parse.unquote(encoded)
    url=url.replace('2',number)
    parsed_url = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    encoded_query = urllib.parse.urlencode(query_params, doseq=True)
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
    classH="elementor-element elementor-element-ebefb06 e-flex e-con-boxed e-con e-child"
    soup=get_html(correct_encoded_url)
    links=soup.findAll('a', class_=classH)
    return [link.get("href") for link in links] 
allHomeDetails=[]
for i in range (1,4):  # Limited to 3 pages for speed
    allHomeDetails+=findHomesOfThePage(correct_encoded_url=findAPageUrl(str(i)))
allHomeDetails
def decodeStr(encodedString):
    return encodedString#.encode("latin1").decode("utf-8")
class Home:
    def __init__(self,link):
        self.link=link
        self.soup=get_html(link)
    def getNumber(self,pr):
            pr=str(pr).strip()
            ans=0
            pr=pr.replace("ca.","")
            for l in pr:
                if (l>='0' and l<='9'):
                    ans*=10
                    ans+=int(l)
                elif (not (l ==" " or l=='.' or l==',')):
                    break
            return ans
    def getLink(self)->str:
        return self.link
    def getMainImage(self)->str:
        return self.soup.find('img',class_="swiper-slide-image").get("src") 
    def getAllImages(self)->list:
        allImages=self.soup.findAll('img',class_="swiper-slide-image")
        return [img.get("src") for img in allImages]
    def getTitle(self)->str:
        try : 
            return  self.soup.find('h1').text
        except Exception :
            return None 
    def getLocation(self)->str:
        locations=self.soup.findAll('div',class_="frymo-short-overview-item")
        for location in locations: 
            if location.get("data-key")=='Ort':
                return  '\n'.join(line.strip() for line in str(location.findChild(class_="frymo-short-overview-item-value").text).splitlines() if line.strip())

        return None 
    def getDescription(self)->str:
        div=self.soup.find('div',class_="elementor-element elementor-element-11ee2ce8 elementor-widget elementor-widget-text-editor")
        return '\n'.join(line.strip() for line in str(div.findChild('div',class_="elementor-widget-container").text).splitlines() if line.strip())
    def getPrice(self):
        prices=self.soup.findAll('div',class_="frymo-short-overview-item")
        for price in prices: 
            if price.get("data-key")=="Kaufpreis":
                return self.getNumber((price.findChild().findNextSibling().text))
        return None
    def getPlatfrom(self)->str:
        return "lucie-hauri"
    def getLivingSpace(self):
        elements=self.soup.findAll('div',class_="frymo-short-overview-item")
        for el in elements: 
            if str(el.get("data-key")).startswith("WohnflÃ¤che"):
                return self.getNumber(el.findChild(class_="frymo-short-overview-item-value").text)
        return self.getBuiltUp()
    def getLandArea(self):
        elements=self.soup.findAll('div',class_="frymo-short-overview-item")
        for el in elements: 
            if 'Plot' in str(el.findChild().text) : #or Grundstücksfläche:
                return self.getNumber(el.findChild(class_="frymo-short-overview-item-value").text)
        return None
    def getBuiltUp(self):
        elements=self.soup.findAll('div',class_="frymo-short-overview-item")
        for el in elements: 
            if str(el.get("data-key")).startswith("Bebaute FlÃ¤che"):
                return self.getNumber(el.findChild(class_="frymo-short-overview-item-value").text)
        return None
    def getBathrooms(self)->int:
        elements=self.soup.findAll('div',class_="frymo-short-overview-item")
        for el in elements: 
            if str(el.get("data-key")).startswith("Anzahl Badezimmer"):
                return self.getNumber(el.findChild(class_="frymo-short-overview-item-value").text)
        return  None
    def getBedrooms(self)->int:
        elements=self.soup.findAll('div',class_="frymo-short-overview-item")
        for el in elements: 
            if str(el.get("data-key")).startswith("Anzahl Schlafzimmer"):
                return self.getNumber(el.findChild(class_="frymo-short-overview-item-value").text)
        return None
    def getCategory(self):
        elements=self.soup.findAll('div',class_="frymo-short-overview-item")
        for el in elements: 
            if str(el.get("data-key")).startswith("Objektart"):
                return  '\n'.join(line.strip() for line in str(el.findChild(class_="frymo-short-overview-item-value").text).splitlines() if line.strip())

        return None
    def getId(self): 
        return str(self.soup.find("div",class_="elementor-element elementor-element-e3d1dbb e-con-full e-flex e-con e-child").find("div",class_="elementor-element elementor-element-7ba3fa55 elementor-icon-list--layout-traditional elementor-list-item-link-full_width elementor-widget elementor-widget-icon-list").text).strip()
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
allHomes=set([home for home in allHomeDetails])
homesObjects=[Home(home) for home in allHomes]
homesData=[]
for home in homesObjects:
    homesData.append(home.getAll())
with open("web_1_1_data.json","w",encoding="utf-8") as jsonFile:
    json.dump(homesData,jsonFile,ensure_ascii=False,indent=4)
    
