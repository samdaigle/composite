
from bs4 import BeautifulSoup
import pandas as pd
import requests

url = "https://www.engineeringtoolbox.com/american-wide-flange-steel-beams-d_1319.html"
page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find("table").findAll("td")
text = []
for x in results:
    x = x.text
    if x != "\xa0" and x != "":
        text.append(x)


designation = []
depth = []
width = []
web_thick = []
flange_thick = []

for row in text:
    if "w" in row.lower():
        designation.append(row.lower().replace(" ", ""))
for x in range(len(text)):
    if (x + 1) % 11 == 2:
        depth.append(float(text[x]))
for x in range(len(text)):
    if (x + 1) % 11 == 3:
        width.append(float(text[x]))
for x in range(len(text)):
    if (x + 1) % 11 == 4:
        web_thick.append(float(text[x]))
for x in range(len(text)):
    if (x + 1) % 11 == 5:
        flange_thick.append(float(text[x]))

data = {'Depth': depth, 'Width': width,
        'Web Thickness': web_thick, 'Flange Thickness': flange_thick}

df = pd.DataFrame(data, index=designation)
