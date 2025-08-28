import requests
from bs4 import BeautifulSoup
import json
import re
import html
import os
import time
import random 
def extract_td_text(tr_string: str) -> list:
    pattern = r'<td[^>]*>(.*?)</td>'
    matches = re.findall(pattern, tr_string, flags=re.DOTALL)
    # Strip whitespace from each matched string and return the list.
    return [match.strip() for match in matches]
def decodeStr(encodedString):
    return encodedString#.encode("latin1").decode("utf-8")
def get_html(url): # function for geting the html using request
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, "html.parser")
    else:
        print(f"Failed to fetch {url}")
        return None
def imageDFS(node, targetTag, targetClass):
    classes = node.get('class', [])
    # Check if this node matches
    if node.name == targetTag and targetClass in classes:
        return [img.get("src") for img in node.find_all("img")]
    # Otherwise, search the children
    children = node.findChildren()
    for child in children:
        images = imageDFS(child, targetTag, targetClass)
        if len(images) > 0:
            return images
    return []
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
                elif (not (l =="c" or l=="a" or l ==" " or l=='.' or l==',')):
                    break
            return ans
    # def getTerrace(self):
    #     try : 
    #         return self.getNumber(self.soup.find("div",class_=self.infoClass(),title="Terrace").findChild().findNextSibling().text)
    #     except Exception: 
    #         return 0 
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
            return self.soup.find("body").findChild("div",class_="container container-for-component vp-subpage").findChild("div",class_="row container sub-page-container").findChild("div",class_="col-sm-6 col-md-8 col-lg-8").findChild("div",class_="galleria").findChild("img").get("src")
        except Exception as e :
            tmp=self.soup.find("div",_class="galleria-image")
            print(f"main image error \n okay this is your object {tmp}",f"the error is {e} \n",  "for the link :" , self.link)
    def getAllImages(self)->list:
            try : 
                #x= # .findChild("div",class_="galleria-container notouch galleria-theme-classic").findChild("div",class_="galleria-thumbnails-container galleria-carousel").findChild("div",class_="galleria-thumbnails-list").findChild("div",class_="galleria-thumbnails")
                return imageDFS(self.soup.find("body").findChild("div",class_="container container-for-component vp-subpage").findChild("div",class_="row container sub-page-container").findChild("div",class_="col-sm-6 col-md-8 col-lg-8").findChild("div",class_="galleria"),targetTag="div",targetClass="galleria")
            except Exception as e : 
                print ("errorrrr, detail : ",e)
            # def getEnergyCerteficate(self): 
            #     try : 
            #         table=self.soup.findAll("div", class_="col-md-12 details-table-duplicate-1")[1]
            #         raise NotImplementedError # here add the right code for geting energy certeficate 
            #     except Exception : 
            #         return None
    def getPeroperties(self, name):
        table = self.soup.find("div", class_="col-md-12 details-table-duplicate-1")
        if not table:
            raise Exception(f"No details table found in {self.link}")
        tbody=table.find("tbody", class_="grid" )   
        # Adjust these as needed based on the actual HTML structure:
        rows = tbody.findChildren()
        # print(type(rows))
        # exit()
        if not rows:
            
            raise Exception(f"No rows found in the details table on {self.link}")
        words=[]
        for row in rows:
            words+=extract_td_text(str(row)) 
        for i in range(len(words)-1):
            if (words[i]==name) :
                return words[i+1]
        raise Exception(f"{name} is not in {self.link}")

    def getTitle(self)->str:
        try : 
            return '\n'.join(line.strip() for line in str(self.soup.find('h1',class_="object-title-text").text).splitlines() if line.strip())
        except Exception :
            return None
    def getLocation(self)->str:
        try :
            return '\n'.join(line.strip() for line in str(self.soup.find("div",class_=self.infoClass(),title="Area").findChild().findNextSibling().text).splitlines() if line.strip())
        except Exception : 
            return None  
    def getDescription(self)->str:
        try : 
            subpages=self.soup.find("body").findChild("div",class_="container container-for-component vp-subpage").findChild("div",class_="row container sub-page-container").findChild("div",class_="col-sm-6 col-md-8 col-lg-8").findChildren('div',class_="subpage-block")
           # print(subpages)
            texts=""
            for subpage in subpages:
              try :   
                texts+=str('\n'.join(line.strip() for line in str(subpage.find('div',class_="title").text+"\n"+subpage.find('div',class_="text").text).splitlines()))+"\n\n\n"
              except Exception : 
                  pass
            return texts
        except Exception : 
            print ("description not found for : ", self.link)
    def getPrice(self):
        try :
            return self.getNumber(self.getPeroperties("Purchase Price"))
        except Exception : 
             print ("price not found for : ", self.link)
    def getPlatfrom(self)->str:
        return "https://www.von-poll.com/en/mallorca"
    def getLivingSpace(self):
        return self.getNumber(self.getPeroperties("Living Space"))
    def getLandArea(self):
        return None 
    def getBuiltUp(self):
        return None
    def getBathrooms(self)->int:
        return self.getNumber(self.getPeroperties("Bathrooms"))
    def getBedrooms(self)->int:
        return self.getNumber(self.getPeroperties("Bedrooms"))
    def getCategory(self):
        return None 
    def getId(self): 
        return self.getPeroperties("Property ID")
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
def findAPageUrl(number:str):
    import urllib.parse
    encoded="https://www.von-poll.com/en/search?n=5&f=1&page=2&anbieters%5B%5D=290&anbieters%5B%5D=20&anbieters%5B%5D=220&anbieters%5B%5D=299&anbieters%5B%5D=307&anbieters%5B%5D=352&anbieters%5B%5D=416&anbieters%5B%5D=391&searchtype=mallorca&business_area=1&menuselected=wohnen&us=0&r_p=1&rent_purchase=3&price=&bedrooms_min=&bedrooms_max=999999&use_range_sliders=0&living_space_min=&t%5B%5D=0&search-input="
    url=urllib.parse.unquote(encoded)
    url=url.replace('page=2',f"page={number}")
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
def findAllPages(number):
    allPages=[]
    for i in range(1,number):
        tmpLink=findAPageUrl(str(i))
        if tmpLink==None : 
            print(f"for i : {i} , there is not any page of homes!")
            break
        allPages.append(tmpLink) 
    return allPages
allPages=findAllPages(3)  # Limited to 3 pages for speed
def findAllHomes(pages):
    allHomesLinks=[]
    baseUrl="https://www.von-poll.com"
    for page in pages :
        soup=get_html(page) 
        allHomesLinks+=[baseUrl+link.get('href') for link in soup.findAll("a",class_="property-link")]
    return allHomesLinks
allHomesLinks=findAllHomes(allPages)
assert(len(allHomesLinks)==len(set(allHomesLinks)))
random.shuffle(allHomesLinks) 
def tests(homes):
    for home in homes :
        assert(len(home.getAllImages())>0)
        assert(not home.getMainImage()==None)
        print (home.getMainImage())
homeObjects=[Home(homeLink) for homeLink in allHomesLinks ]
homesData=[]
count=0
for home in homeObjects:
    try : 
        homesData.append(home.getAll())
        count+=1
    except Exception:
        pass 
with open("web_4_1_data.json","w",encoding="utf-8") as jsonFile:
    json.dump(homesData,jsonFile,ensure_ascii=False,indent=4)
print ("success")