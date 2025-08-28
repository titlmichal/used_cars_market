import requests
from bs4 import BeautifulSoup, Tag

class usedCar:
    def __init__(self, name):
        self.name = name
        self.link = ""

r = requests.get("https://www.sauto.cz/inzerce/osobni")
if r.status_code != 200:
    raise Exception("Error. Request unsuccesful!")

html_soup = BeautifulSoup(r.content, "html.parser")
# html_soup.prettify
# print(html_soup.body.contents)
html_body = html_soup.find("body")
counter = 0
for descendant in html_body.descendants:   
    # descendants are all indirect children but that all means
    # ...that even simple strings within the tags are indirect children
    if type(descendant) != Tag:
        continue
    # print(descendant)

    if "class" in descendant.attrs.keys():
        # tags attributes are stored like dicts
        if len(descendant.attrs["class"]) > 0:
            # if attribute value of class = "" it will be counted in len but not found via index
            if "c-item__data-wrap" in descendant.attrs["class"]:
                # this class should be unique identifier of car item --> DOUBLE CHECK THAT
                for content in descendant.contents:
                    print(content)
                    print()
                print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    else:
        continue
    # print(descendant.attrs.keys())
    # print(counter)
    
    # counter += 1
    # print()