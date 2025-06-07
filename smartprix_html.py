import pandas as pd
from bs4 import BeautifulSoup
import numpy as np

with open('mobiles6.html','r',encoding='utf-8') as f:
    html_file = f.read()

soup = BeautifulSoup(html_file,'lxml')
phones = soup.find_all('div',class_='filter filer_finder')

final = pd.DataFrame()
name = []
prices = []
battery = []
processor = []
display = []
camera = []
os = []
for i in phones:
    try:
        name.append(i.find('a', class_='hover_blue_link name gaclick').text)
    except:
        name.append(np.nan)
    try:
        prices.append(i.find('span', class_='price price_padding').text)
    except:
        prices.append(np.nan)
    try:
        battery.append(i.find_all('div', class_='a filter-list-text')[3].text)
    except:
        battery.append(np.nan)

    # df1 = i.find_all('div',class_ = 'a filter-list-text')[3]
    # df = df1.find_all('label')[0].text
    try:
        processor.append(i.find_all('div', class_='a filter-list-text')[0].text)
    except:
        processor.append(np.nan)
    try:
        display.append(i.find_all('div', class_='a filter-list-text')[1].text)
    except:
        display.append(np.nan)
    try:
        camera.append(i.find_all('div', class_='a filter-list-text')[2].text)
    except:
        camera.append(np.nan)

    os.append(i.find('div', class_='os_icon_cat').text.strip())

# print(card)
df = pd.DataFrame(
    {'Phone_Name': name, 'Price': prices, 'Battery_Info': battery, 'Processor_Info': processor, 'Display_Info': display,
     'Camera_Info': camera, 'OS_Info': os})
final = pd.concat([final, df], ignore_index=True)

final.to_csv('mobiel_dataset.csv',index=False,encoding='utf-8')