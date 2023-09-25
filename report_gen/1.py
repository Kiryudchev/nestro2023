import folium
import branca.colormap as cm

import json

GEOJSON_NAME = 'geoBoundaries-BIH-ADM2_4.geojson'
map_geojson = json.loads(open(GEOJSON_NAME, encoding='utf-8').read())

max_probability = 0
min_probability = 1

colormap = cm.LinearColormap(["green", "yellow"], vmin=max_probability, vmax=min_probability)

# Create a base map
m = folium.Map(location=[44.2, 17.8], zoom_start=7)

map_val = {i['properties']['shapeID']: i['properties']['probability'] for i in
           json.loads(open(GEOJSON_NAME).read())['features']}
points = {"type": "FeatureCollection", "features": [{
    "type": "Feature",
    "properties": {
        "name": k,
        "address": v['address'],
    },
    "geometry": {
        "type": "Point",
        "coordinates": [v['lng'], v['lat']]
    }
} for k, v in json.loads(open('existing_AZS.json').read()).items()]}

VALID_ROAD_KEYS = {'type', 'geometry', 'properties'}

tooltip = folium.GeoJsonTooltip(
    fields=["shapeName", "population", "area", "density", "probability"],
    aliases=["Название:", "Население:", "Площадь:", "Плотность:", "Вероятность:"],
    localize=True,
    sticky=False,
    labels=True,
    style="""
        background-color: #F0EFEF;
        border: 2px solid black;
        border-radius: 3px;
        box-shadow: 3px;
    """,
    max_width=800,
)
fg_map = folium.FeatureGroup(name="Прогноз спроса на топливо").add_to(m)
folium.GeoJson(
    map_geojson,
    name='geojson',
    tooltip=tooltip,
    style_function=lambda feature: {
        "fillColor": colormap(map_val[feature['properties']['shapeID']]),
        "color": "black",
        "weight": 1,
        # "dashArray": "5, 5",
        "fillOpacity": 0.3,

    },
    highlight_function=lambda feature: {
        "fillColor": (
            "green" if "e" in feature["properties"]["shapeName"].lower() else "#ffff00"
        ),
    },
).add_to(fg_map)

fg = folium.FeatureGroup(name="Заправки", show=False).add_to(m)

folium.GeoJson(
    points,
    marker=folium.Marker(icon=folium.Icon(icon='star')),
    popup=folium.GeoJsonPopup(fields=["name", "address"]),
).add_to(fg)


competitor_filling_stations = {"type": "FeatureCollection", "features": []}
for k, v in json.loads(open('all_stations.json').read()).items():
    for i in v:
        competitor_filling_stations['features'].append({
            "type": "Feature",
            "properties": {
                "place_id": i['place_id'],
                "type": i['type'],
                "name": i['name'],
                "road": i['road'],
                "state_district": i['state_district'],
            },
            "geometry": {
                "type": "Point",
                "coordinates": [i['lon'], i['lat']]
            }
        })

fg2 = folium.FeatureGroup(name="Заправки конкурентов", show=False).add_to(m)
folium.GeoJson(
    competitor_filling_stations,
    marker=folium.Marker(icon=folium.Icon(icon='star', color='red')),
    popup=folium.GeoJsonPopup(
        fields=["type", "name", "road", "state_district"],
        aliases=["Тип топлива:", "Название фирмы конкурента:", "Название дороги:", "Район:"]
    )
).add_to(fg2)

folium.LayerControl().add_to(m)

legend_html = '''
    <div style="position: fixed; bottom: 50px; left: 50px; z-index: 9999; font-size:14px; background-color: silver; padding: 10px; border-radius: 10px; border: 1px solid black ">
        &nbsp; <b>Legend</b><br>
        &nbsp; <i style="color:green">◍</i> 0 - Потенциально минимальный спрос<br>
        &nbsp; <i style="color:yellow">◍</i> 1 - Потенциально максимальный спрос<br>
    </div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

if __name__ == '__main__':
    m.save('bosnia_regions_map.html')
