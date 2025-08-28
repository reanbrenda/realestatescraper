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
    encoded="https://ev-mallorca.com/en/mallorca-properties?page=1"
    encoded=encoded.replace('1',number)
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
    divClass="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10"
    soup=get_html(correct_encoded_url)
    items=soup.find('div', class_=divClass).findChildren("a")
    return [item.get("href") for item in items]
allHomeDetails=[]
firstPage=None
for i in range (1,4):  # Limited to 3 pages for speed
    try :
        pageLinks=findHomesOfThePage(correct_encoded_url=findAPageUrl(str(i)))
        if pageLinks==firstPage : 
            break
        pageLinks=[pageLink for pageLink in pageLinks if "mallorca-property" in pageLink]
        if firstPage==None : 
            firstPage=pageLinks
        allHomeDetails+=pageLinks
    except Exception : 
        pass
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
        return self.soup.find("section",class_="mx-auto max-w-7xl px-6 md:px-4 w-full py-8 space-y-8").find("div",class_="grid grid-cols-2 gap-10 md:gap-16 md:grid-cols-none md:grid-flow-col justify-center")
    def getIconDetails(self,name) : 
        icons=self.soup.find("section",class_="mx-auto max-w-7xl px-6 md:px-4 w-full py-8 space-y-8").find("div",class_="grid grid-cols-2 gap-10 md:gap-16 md:grid-cols-none md:grid-flow-col justify-center").findChildren("div",class_="md:w-auto space-y-2")
        for icon in icons: 
            if name in icon.find("div").find("p",class_="text-gray-1 text-center text-xs").text : 
                return icon.text
        return None
    @safe_return(None)
    def getMainImage(self) -> str:
        return self.soup.find("div",class_="relative h-full").find("div",class_="overflow-hidden h-full relative max-w-full").find("div",class_="flex flex-row h-full").find("div",class_="flex-[0_0_100%] sm:flex-[0_0_auto] w-auto h-full mr-[2px] relative overflow-hidden").findChild('a').get('href')
    @safe_return(None)
    def getAllImages(self) -> list:
        allImages=[self.soup.find("div",class_="relative h-full").find("div",class_="overflow-hidden h-full relative max-w-full").find("div",class_="flex flex-row h-full").find("div",class_="flex-[0_0_100%] sm:flex-[0_0_auto] w-auto h-full mr-[2px] relative overflow-hidden")]
        allImages+= self.soup.find("div",class_="relative h-full").find("div",class_="overflow-hidden h-full relative max-w-full").find("div",class_="flex flex-row h-full").findChildren("div",class_="flex-[0_0_100%] sm:flex-[0_0_auto] w-auto h-full mr-[2px] relative")
        return [img.findChild('a').get('href') for img in allImages]
    @safe_return("No tiltle")
    def getTitle(self) -> str:
        return self.soup.find("section",class_="mx-auto max-w-7xl px-6 md:px-4 w-full py-8 space-y-8").find("div", class_="space-y-4 flex flex-col text-center mx-auto max-w-3xl").findChild("h1").text.strip()
    @safe_return(None)
    def getLocation(self) -> str:
        return self.soup.find("section",class_="mx-auto max-w-7xl px-6 md:px-4 w-full py-8 space-y-8").find("div", class_="space-y-4 flex flex-col text-center mx-auto max-w-3xl").findChild("p").text.strip().split("\n")[-1].strip()
    @safe_return(None)
    def getDescription(self) -> str:
        description=self.soup.find("div", class_="box-outer property-product-panel").findChild("div").findChild("div").findChild("div").findNextSibling("div",class_="row essential-panel").findChild("div",class_="cell col-lg-8 col-md-9 col-xs-12").text
        return '\n'.join(line.strip() for line in str(description).splitlines() if line.strip())

    @safe_return(None)
    def getPrice(self):
        return self.getNumber(self.getEssntialDetails().findChild("div",class_="col-span-2 md:col-span-1 md:order-last md:w-auto space-y-2").text.strip())
    @safe_return(None)
    def getPlatfrom(self) -> str:
        return "ev-mallorca.com/en/mallorca-property"

    def getLivingSpace(self): 
        try : 
            return self.getNumber(self.getIconDetails("Living space"))
        except Exception :
            return self.getLandArea()
    @safe_return(None)
    def getLandArea(self):
        return self.getNumber(self.getIconDetails("Total surface"))

    @safe_return(None)
    def getBuiltUp(self):
        return self.getNumber(self.getIconDetails("Plot size"))

    @safe_return(None)
    def getBathrooms(self) -> int:
        return self.getNumber(self.getIconDetails("Bathrooms"))

    @safe_return(None)
    def getBedrooms(self) -> int:
        return self.getNumber(self.getIconDetails("Bedrooms"))

    @safe_return(None)
    def getCategory(self):
       return self.soup.find("section",class_="mx-auto max-w-7xl px-6 md:px-4 w-full py-8 space-y-8").find("div", class_="space-y-4 flex flex-col text-center mx-auto max-w-3xl").findChild("p").text.strip().split("\n")[0].replace(",","")
    @safe_return(None)
    def getId(self):
        return None 
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
with open("web_6_1_data.json","w",encoding="utf-8") as jsonFile:
    json.dump(homesData,jsonFile,ensure_ascii=False,indent=4)
