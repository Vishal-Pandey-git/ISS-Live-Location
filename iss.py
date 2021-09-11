from flask import Flask, render_template, redirect, url_for
import requests
import folium
from folium import plugins
from branca.element import Figure
import requests

app = Flask(__name__)


@app.route('/')
def index():
    return redirect('issdat')


@app.route('/issloc')
def loc():
    r = requests.get(url='http://api.open-notify.org/iss-now.json')
    space_station_location = (r.json())
    space_station_longitude = float(
        space_station_location['iss_position']['longitude'])
    space_station_latitude = float(
        space_station_location['iss_position']['latitude'])
    start_coords = (space_station_latitude, space_station_longitude)

    tooltip = "I'm here" + str(start_coords)
    folium_map = folium.Map(zoom_start=17,
                            tiles="Stamen Terrain",
                            world_copy_jump=True)
    folium.Marker(start_coords,
                  popup="<i>International Space Station</i>",
                  tooltip=tooltip,
                  icon=folium.Icon(color="red",
                                   icon="info-sign")).add_to(folium_map)
    #points=(0,0)
    folium.CircleMarker(start_coords, radius=50, fill=True,
                        color='red').add_to(folium_map)

    plugins.Terminator().add_to(folium_map)
    #folium.PolyLine(points).add_to(folium_map)
    #plotmap
    #return (render_template ("/index.html",plotmap=folium_map._repr_html_()))
    return folium_map._repr_html_()


@app.route('/issdat')
def dat():
    r = requests.get(url='http://api.open-notify.org/astros.json')
    k = r.json()
    number = k['number']
    loom = []
    print(number)
    for name in k['people']:
        loom.append((name['name']))
    return (render_template("/index.html", num=number, astro=loom))


if __name__ == '__main__':
    app.run(debug=True)