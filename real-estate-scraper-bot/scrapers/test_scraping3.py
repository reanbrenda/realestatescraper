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
    encoded="https://mallorcaresidencia.com/properties/#1"
    url=urllib.parse.unquote(encoded)
    url=url.replace('1',number)
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
    divClass="wrap-link"
    soup=get_html(correct_encoded_url)
    items=soup.findAll('a', class_=divClass)
    return[item.get("href") for item in items] 
import requests
from bs4 import BeautifulSoup

def load_more_search_items(base_url, current_page, params):
    """
    Load more search items by sending a POST request and returning a BeautifulSoup object.
    
    :param base_url: Base URL of the website
    :param current_page: The current page number to increment from
    :param params: A dictionary of additional parameters for the request
    :return: BeautifulSoup object of the response HTML
    """
    # Define the target URL
    ajax_url = f"{base_url}/wp-admin/admin-ajax.php"

    # Increment the page number
    current_page += 1

    # Add the required parameters
    params['pageno'] = current_page
    params['action'] = 'more_post_ajax_search'

    # Prepare the POST data as a string
    post_data = "&".join(f"{key}={value}" for key, value in params.items())

    try:
        # Send the POST request
        response = requests.post(ajax_url, data=post_data, headers={
            "Content-Type": "application/x-www-form-urlencoded"
        })

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response using BeautifulSoup
            return current_page,BeautifulSoup(response.text, "html.parser")
        else:
            print(f"Request failed with status code {response.status_code}")
            return None

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Example Usage
base_url = "https://mallorcaresidencia.com"
current_page = 0  # Initial page number
params = {
    "pageno": current_page,  # Incremented during the function call
    "other_param": "example_value",  # Add other required input params here
}
allHomesLinks=[]
numberOfGoes=3  # Limited to 3 pages for speed
while (numberOfGoes>0):
    numberOfGoes-=1 
    current_page,soup = load_more_search_items(base_url, current_page, params)
    if soup:
        # Example of extracting content from the soup
        allA=soup.findAll('a') # Print the formatted HTML content
        allHomesLinks+=[anA.get("href") for anA in allA]       
    else : 
        print("bad")
        break
allHomesLinks=[homeLink.replace("\\","") for homeLink in allHomesLinks]
allHomesLinks=[homeLink.replace('"',"") for homeLink in allHomesLinks]
print(allHomesLinks)
def decodeStr(encodedString):
    return encodedString#.encode("latin1").decode("utf-8")
class Home:
    def __init__(self,link):
        self.link=link
        self.soup=get_html(link)
    def infoClass(self):
        return "info-row col-3 col-md-2 col-lg-auto"
    def getNumber(self,pr):
            ans=0
            for l in pr:
                if (l>='0' and l<='9'):
                    ans*=10
                    ans+=int(l)
                elif (not (l ==" " or l=='.' or l==',')):
                    break
            return ans
    def getTerrace(self):
        try : 
            return self.getNumber(self.soup.find("div",class_=self.infoClass(),title="Terrace").findChild().findNextSibling().text)
        except Exception: 
            return 0 
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
            return self.soup.find("a" , class_="swipebox gallery-img").get("href")
        except Exception :
            return None
    def getAllImages(self)->list:
        id="property-gallery"
        div=self.soup.find('div',id=id)
        allA=div.findAll('a')
        return [anA.get("href") for anA in allA]
    def getTitle(self)->str:
        try : 
            return '\n'.join(line.strip() for line in str(self.soup.find('div',class_="entry-content").findChild().text).splitlines() if line.strip())
        except Exception :
            return None
    def getLocation(self)->str:
        try :
            return '\n'.join(line.strip() for line in str(self.soup.find("div",class_=self.infoClass(),title="Area").findChild().findNextSibling().text).splitlines() if line.strip())
        except Exception : 
            return None  
    def getDescription(self)->str:
        return '\n'.join(line.strip() for line in str(self.soup.find('div',class_="col prop-info").text).splitlines() if (line.strip() and not line.strip().startswith("For more")))
    def getPrice(self):
        try :
            return self.getNumber(self.soup.find('h3',class_="price").text.split(" ")[1])
        except Exception : 
            return 0
    def getPlatfrom(self)->str:
        return "mallorcaresidencia.com"
    def getLivingSpace(self):
        return self.getNumber(self.soup.find("div",class_=self.infoClass(),title="Living area").findChild().findNextSibling().text)
    def getLandArea(self):
        return self.getLivingSpace()+self.getTerrace()
    def getBuiltUp(self):
        return None
    def getBathrooms(self)->int:
        return self.getNumber(self.soup.find("div",class_=self.infoClass(),title="Bathrooms").findChild().findNextSibling().text)
    def getBedrooms(self)->int:
        return self.getNumber(self.soup.find("div",class_=self.infoClass(),title="Bedrooms").findChild().findNextSibling().text)
    def getCategory(self):
        return None 
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
bad=["https://issuu.com/mallorcaresidencia/docs/mallorcaresidencia_2017-2018_catalo"
, "https://seo-iberica.com/mallorca/",
 "https://es.linkedin.com/company/mallorcaresidencia",
"https://seo-iberica.com/mallorca/",
 "https://issuu.com/mallorcaresidencia/docs/mallorcaresidencia_2017-2018_catalo",
 "https://es.linkedin.com/company/mallorcaresidencia"]
import random
random.shuffle(allHomesLinks)
for homeLink in allHomesLinks:
    if not homeLink in bad:
        try : 
            homeObjects.append(Home(homeLink))
            bad.append(homeLink)
        except Exception:
            pass
allHomes=[]
homesData=[]
count=0
for home in  homeObjects:
    try : 
        homesData.append(home.getAll())
        count+=1
    except Exception:
        pass 
with open("web_3_1_data.json","w",encoding="utf-8") as jsonFile:
    json.dump(homesData,jsonFile,ensure_ascii=False,indent=4)
    