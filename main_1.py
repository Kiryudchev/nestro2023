'''
import pandas as pd

with open('BiH_regional_data.json', encoding='utf-8') as inputfile:
    df = pd.read_json(inputfile)

print(df[1].head())

#df.to_csv('csvfile.csv', encoding='utf-8', index=False)
'''
import json
import csv
import random
import math

f = open('geoBoundaries-BIH-ADM2.geojson', encoding='utf-8')
data = json.load(f)
f.close()

f = open('vocab.json', encoding='utf-8')
vocab = json.load(f)
f.close()

f = open('areas_roads4.json', encoding='utf-8')
roads = json.load(f)
f.close()
print("areas_roads4:",len(roads))

f = open('BiH_regional_data.json')
data_reg_data = json.load(f)
f.close()
print("BiH_regional_data:",len(data_reg_data["Regional data"]))


'''
gdp =[]

for k in data_gdp["GDP 2010"]:
    names.append(k["properties"]["shapeName"])
print(names)GDP 2010
'''
#x = json.loads(data)
#print(data["Regional data"])

#f = csv.writer(open("test.csv", "wb+"))
#f.write(open('test.csv', 'w', encoding='utf8'))

#names =[]

for k in data["features"]:
    k["properties"]['population'] = ""
    k["properties"]['area'] = ""
    k["properties"]['density'] = ""

max_pop=0
max_area=0
max_dens=0
for i in data_reg_data["Regional data"]:
#    i["population"]=i["population"].replace(',', '.')
#    i["area"]=i["area"].replace(',', '.')
#    i["density"]=i["density"].replace(',', '.')
    try:
        if int(i["population"])>max_pop:
            max_pop = int(i["population"])
    except:
        print(i["name"])
    if i["area"]!='':
        if float(i["area"].replace(',', '.'))>max_area:
            max_area = float(i["area"].replace(',', '.'))
#    except:
#        print(i["name"])
    if i["density"]!='':
        if float(i["density"].replace(',', '.'))>max_dens:
            max_dens = float(i["density"].replace(',', '.'))


max_prob =0

for k in data["features"]:
#    names.append(k["properties"]["shapeName"])
    for i in data_reg_data["Regional data"]:
        for j in vocab:
            if i["name"]==j["lookup"]:
                i["name"]=j["replacement"]
        if k["properties"]["shapeName"] == i["name"]:
            k["properties"]['population'] = i['population']
            k["properties"]['area'] = i['area']
            k["properties"]['density'] = i['density']
    for i in roads:
        if k["properties"]["shapeName"] == i["name"]:
            if(len(i["roads"]))>0:
                k["properties"]['probability'] = math.log(len(i["roads"])*float(k["properties"]['density'].replace(',', '.')))
            else:
                k["properties"]['probability'] = 0
            if k["properties"]['probability']>max_prob:
                max_prob = k["properties"]['probability']

for k in data["features"]:
    k["properties"]['probability'] = k["properties"]['probability']/max_prob


print("features:",len(data["features"]))
#    k["properties"]['value1']= random.randrange(0, 10)

print("Pop:",max_pop," Area:",max_area," Dens:",max_dens)

with open("geoBoundaries-BIH-ADM2_4.geojson","w", encoding='utf-8') as jsonfile:
    json.dump(data,jsonfile,ensure_ascii=False)

'''
with open('test.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ["name", "canton", "entity", "state", "population","area","density"]
    writer = csv.DictWriter(csvfile, delimiter=';',fieldnames=fieldnames)
    writer.writeheader()
    for k in data["Regional data"]:
        writer.writerow(k)

f.writerow(["name", "canton", "entity", "state", "population","area","density"])
for k in data["Regional data"]:
    f.writerow([k["name"],
                k["canton"],
                k["entity"],
                k["state"],
                k["population"],
                k["area"],
                k["density"]])
'''

