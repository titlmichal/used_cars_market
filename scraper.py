import requests
from bs4 import BeautifulSoup, Tag, NavigableString

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

# parsing the html to find the individual car data --> REFACTOR!
# most likely the best would be to write a function to find a tag by its class name
# find_all method may be a good fix
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
                    # car seems to have 3 tag: 1st has link and name start, 2nd has overview details and 3rd has price
                    # but those are divs, the details are in nested divs inside
                    if "href" in content.attrs.keys():
                        # getting hyperlinks if the element has such attribute
                        print(content.attrs["href"])
                    elif "c-item__info-wrap" in content.attrs["class"]:
                        # getting main info tag (contains name, year, mileage)
                        for i in content.descendants:
                            if isinstance(i, NavigableString):
                                print(i)
                    elif "c-item__data" in content.attrs["class"]:
                        # getting tag with price
                        for i in content.descendants:
                            if not isinstance(i, NavigableString) and "c-item__price" in i.attrs["class"]:
                                print("This is price:", i.string)
                    print()
                print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    else:
        continue