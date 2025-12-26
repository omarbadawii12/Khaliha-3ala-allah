# map_view.py (النسخة المعدلة)

import folium
from folium.plugins import PolyLineTextPath

def draw_map(cities, path, algorithm_name="A* Algorithm"):
    start_city = path[0]
    end_city = path[-1]

    # حساب المركز التقريبي للخريطة (موقع القاهرة عادةً يكون مناسب)
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

    # إضافة العنوان في أعلى يسار الخريطة
    title_html = f'''
        <div style="position: fixed; 
                    top: 10px; left: 50px; width: 300px; height: 50px; 
                    background-color: white; border:2px solid grey; 
                    z-index:9999; font-size:20px; padding: 10px;
                    border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                    font-weight: bold; text-align: center;">
            <b>{algorithm_name}</b>
        </div>
    '''
    m.get_root().html.add_child(folium.Element(title_html))

    # حفظ الخريطة
    m.save("tsp_egypt_map.html")