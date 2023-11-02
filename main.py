import requests
from bs4 import BeautifulSoup
import json
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.graphics.mosaicplot import mosaic

### The commented code below is used to scrape data from Wikipedia and store in data.json file ###
# def get_soup(url):
#   r = requests.get(url)
#   r.raise_for_status()
#   html = r.text.encode("utf-8")
#   soup = BeautifulSoup(html, "html.parser")
#   return soup
#
# def get_categories(url):
#   soup = get_soup(url)
#   data = {}
#   # Select and extract category animals here
#   categories = soup.find_all("dl")
#
#   for category in categories:
#     category_name = category.find("dt").get_text()
#     category_animals = category.find_all("a")
#     data[category_name] = category_animals
#   return data
#
# def get_animal(url):
#   soup = get_soup(url)
#   table = soup.find("table", {"class": "infobox biota"})
#   if not table:
#     return "No class found."
#   rows = table.find_all("tr")
#   for row in rows:
#     if "Class:" in row.get_text():
#       animal_class = row.find("a").contents[0]
#   return animal_class
#
# category_data = get_categories("https://en.wikipedia.org/wiki/Endangered_species")
#
# animal_class = get_animal("https://en.wikipedia.org/wiki/Honey_badger")
#
# collected_data = []
#
# for category in category_data:
#   for animal in category_data[category]:
#     animal_href = animal["href"]
#     animal_name = animal.contents[0]
#     animal_class = get_animal("https://en.wikipedia.org/" + animal_href)
#
#     if len(animal_class) > 3:
#       collected_data.append({
#         "Category": category,
#         "Animal Name": animal_name,
#         "Animal Class": animal_class
#       })
#
# with open("data.json", "w") as jsonfile:
#   json.dump(collected_data, jsonfile)



with open("data.json", "r") as text:
  data = json.load(text)

for item in data:
  item["Category"] = re.compile(" [\.(]").split(item["Category"])[0]


classes = ["Mammalia", "Aves", "Reptilia"]
statuses = ["Endangered", "Critically endangered", "Vulnerable"]

mosaic_data = []

for item in data:
  if item["Animal Class"] in classes and item["Category"] in statuses:
    mosaic_data.append(item)

properties = {
  "Endangered": {"color": "#FACDB6"},
  "Critically endangered": {"color": "#C5CADE"},
  "Vulnerable": {"color": "#A8DBD2"}
}

plt.rc("font", size=8)

mosaic_dataframe = pd.DataFrame(mosaic_data)

fig = mosaic(mosaic_dataframe, ["Category", "Animal Class"], title="Conservation Status by Animal Class", gap=[0.02, 0.02], axes_label=True, properties=lambda x: properties[x[0]])

plt.savefig("endangered_species.png")