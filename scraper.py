import requests
import math
from bs4 import BeautifulSoup, Tag, NavigableString

class usedCar:
    def __init__(self, name):
        self.name = name
        self.link = ""

page_nr = 1
r = requests.get(f"https://www.sauto.cz/inzerce/osobni/?strana={page_nr}")
if r.status_code != 200:
    raise Exception("Error. Request unsuccesful!")

html_soup = BeautifulSoup(r.content, "html.parser")
# html_soup.prettify
# print(html_soup.body.contents)
html_body = html_soup.find("body")

# parsing the html to find the individual car data --> REFACTOR!
# most likely the best would be to write a function to find a tag by its class name
# find_all method may be a good fix
scraped_cars_dicts = []

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
                car_dict = {}
                for content in descendant.contents:
                    # car seems to have 3 tag: 1st has link and name start, 2nd has overview details and 3rd has price
                    # but those are divs, the details are in nested divs inside
                    if "href" in content.attrs.keys():
                        # getting hyperlinks if the element has such attribute
                        car_dict["url"] = content.attrs["href"]
                    elif "c-item__info-wrap" in content.attrs["class"]:
                        # getting main info tag (contains name, year, mileage)
                        info_contents = []
                        # main info is in multiple tags within this one hence the list
                        for i in content.descendants:
                            if isinstance(i, NavigableString):
                                # choosing only string contents (not tag objects)
                                info_contents.append(i)
                        try:
                            # tags contents follow same order, hence this --> REFACTOR later!
                            car_dict["name"], car_dict["features"], car_dict["year_kms"] = info_contents[0], info_contents[1], info_contents[2]
                            car_dict["fuel"], car_dict["gearbox"] = info_contents[3], info_contents[4]
                        except:
                            car_dict["name"], car_dict["features"], car_dict["year_kms"] = "There is", "some missing", "data"
                            car_dict["fuel"], car_dict["gearbox"] = "for this", "car :("
                    elif "c-item__data" in content.attrs["class"]:
                        # getting tag with price
                        next_tag_is_price = False
                        for i in content.descendants:
                            if next_tag_is_price:
                                # this is trying to solve price format issues (doesnt solve it --> REFACTOR)
                                car_dict["price"] = i
                                next_tag_is_price = False
                            if not isinstance(i, NavigableString) and "c-item__price" in i.attrs["class"]:
                                # car_dict["price"] = i.string
                                next_tag_is_price = True
                scraped_cars_dicts.append(car_dict)
    else:
        continue
# for car in scraped_cars_dicts:
#     # final data dict
#     print(car)

offers_total_count = html_body.find(attrs={"class": "c-item-list__count c-item-list__count--list"}).string
    # getting adverts count --> to later use for scraping more than the 1st page
offers_total_count = int("".join([text for text in offers_total_count.split() if text.isnumeric()]))
offers_page_count = len(html_body.find_all(attrs={"class": "sds-surface sds-surface--clickable sds-surface--00 c-item__link"}))
    # getting how many offers are on one page
page_count = math.ceil(offers_total_count/offers_page_count)
    # getting estimated pages count (rounded up)
for current_page in range(page_nr, page_count + 1):
    # NEED TO REFACTOR (ideally into functions) the page data processing (to loop over all)
    pass

    # REFACTORING THE PAGE PROCESSING
    # here the desired function should take in unique identifier of general tag
    # ... that contains all the used car offer info and also additional arg
    # ... to identify the cars data and price (--> likely at least 2 args then)
for used_car_tag in html_body.find_all(attrs={"class": "c-item__data-wrap"}):
    print(used_car_tag)
    print()
    print(f"Descendants: ({len([used_car for used_car in used_car_tag.descendants])})\n")
    for descendant_tag in used_car_tag.descendants:
        print(descendant_tag)
    print("XXX \n")