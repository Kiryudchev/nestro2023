#trace roads with Regions incide BiH

import json
import csv
import random
from shapely.geometry import Point, Polygon

f = open('geoBoundaries-BIH-ADM2.geojson', encoding='utf-8')
data = json.load(f)
f.close()

f = open('bosnian_roads.json', encoding='utf-8')
roads = json.load(f)
f.close()


area_polygons = []


#    writer.writeheader()
for k in data["features"]:

#    area = json.loads("{'name':'','poly':[],'roads':[]}")
    area = {'name':"",'poly':[],'roads':[]}
    area["name"] = k["properties"]["shapeName"]
    for i in k["geometry"]["coordinates"]:
        for j in i:
            if len(j)<3:
                area['poly'].append(Point(j[0], j[1]))
            else:
                for m in j:
                    area['poly'].append(Point(m[0], m[1]))
    area_polygons.append(area)


print("poligons:",len(area_polygons))
print("roads:",len(roads[0]["features"]) )

area_names=[]
for t in area_polygons:
    a = {'name':t["name"],'roads':t["roads"]}
    area_names.append(a)


with open("areas_roads1.json","w", encoding='utf-8') as jsonfile:
    json.dump(area_names,jsonfile,ensure_ascii=False)

ch = 0
y=1
for k in roads[0]["features"]:
    try:
        print("road:",k["properties"]["name"],", number:",ch)
        y=1
    except:
        y=0
    try:
        if int(k["properties"]["lanes"])>2:
            w=1
        else:
            w=0
    except:
        w=0
    if w==1:
        for i in k["geometry"]["coordinates"]:
            p = Point(i[0], i[1])
            for j in area_polygons:
                if p.within(Polygon(j['poly'])):
                    if y==1:
                        j['roads'].append(k["properties"]["name"])
                    else:
                        j['roads'].append("unnamed")
                    break
    ch = ch +1


area_names=[]
for t in area_polygons:
    a = {'name':t["name"],'roads':t["roads"]}
    area_names.append(a)


with open("areas_roads4.json","w", encoding='utf-8') as jsonfile:
    json.dump(area_names,jsonfile,ensure_ascii=False)

#with open("areas_roads.json","w", encoding='utf-8') as jsonfile:
#    json.dump({'names':area_polygons['name'],'roads':area_polygons['roads']},jsonfile,ensure_ascii=False)

