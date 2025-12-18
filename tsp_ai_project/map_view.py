import folium
from folium.plugins import PolyLineTextPath

def draw_map(cities, path):
    start_city = path[0]
    end_city = path[-1]

    m = folium.Map(location=cities[start_city], zoom_start=6)

    points = []

    for i, city in enumerate(path):
        lat, lon = cities[city]
        points.append((lat, lon))

        if city == start_city:
            color = "green"
            text = f"START: {city}"
        elif city == end_city:
            color = "red"
            text = f"END: {city}"
        else:
            color = "blue"
            text = f"{i}. {city}"

        folium.Marker(
            (lat, lon),
            popup=text,
            icon=folium.Icon(color=color, icon="info-sign")
        ).add_to(m)

    # رسم المسار الأساسي
    route = folium.PolyLine(
        points,
        color="blue",
        weight=5,
        opacity=0.8
    ).add_to(m)

    # إضافة الأسهم على الخط
    PolyLineTextPath(
        route,
        ' ▶ ',
        repeat=True,
        offset=7,
        attributes={
            'fill': 'black',
            'font-weight': 'bold',
            'font-size': '16'
        }
    ).add_to(m)

    m.save("tsp_egypt_map.html")
