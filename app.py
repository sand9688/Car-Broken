
from ast import Yield
import os
from unittest import result
from flask import Flask, render_template, request
import pandas as pd
import googlemaps
import folium


carcent_list = pd.read_csv('C:/Workspace/01.PythoenWeb/00.Project_1/static/광주_자동차정비업체.csv')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/function', methods=['GET','POST'])
def input():
    if request.method == 'POST':
        val = request.form['주소']

        gmaps = googlemaps.Client(key='AIzaSyC1ozHs1I96tzadkejUGanL7zD3ALzRbqI')
        geocode_result = gmaps.geocode(val, language='ko')
        x=geocode_result[0]['geometry']['location']['lat']
        y=geocode_result[0]['geometry']['location']['lng']
        df2 = carcent_list
        map = folium.Map(location=[df2.위도.mean(), df2.경도.mean()], zoom_start=15,
        max_bounds=True,
        min_zoom=15,
        max_zoom=15,
        min_lat=x,
        max_lat=x,
        min_lon=y,
        max_lon=y,
        zoom_control=False,
        no_touch=True)
        for i in df2.index:
            folium.Marker(
                location=[df2.위도[i], df2.경도[i]],
                popup=folium.Popup(f"<a href='https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query={df2.장소[i]}', target=_'blink'>{df2.도로명주소[i]}</a>",
                max_width=100),
                tooltip=df2.장소[i]
            ).add_to(map)
        folium.Marker(
            location=[x,y],
            popup=folium.Popup('주소', max_width=200),
            tooltip='사고위치',
            icon=folium.Icon('darkred', icon='ok')
        ).add_to(map)
        folium.CircleMarker(
            radius=200,
            location=[x, y],
            color="#ffffff",        # RGB, 16진수
            fill=True,
            fill_color="ffffff"
        ).add_to(map)
        map.save('C:/Workspace/01.PythoenWeb/00.Project_1/templates/marker.html')
        
        

        f_image = request.files['image']
        fname= f_image.filename
        print(val, fname, map)
        filename= os.path.join(app.static_folder,'upload/')+fname
        f_image.save(filename)

        return render_template('output.html', result=val, fname=fname)
    else:
        return render_template('input.html')

@app.route('/near')
def near_carcentr():
    return render_template('marker.html')


@app.route('/center_list', methods=['GET','POST'])
def center_list():
    car_list=carcent_list.to_dict('list')
    manu_list = ['장소', '도로명주소', '위도', '경도']
    car_dic = {}
    for j in range(len(car_list['장소'])):
        a = []
        for i in manu_list:
            a.append(car_list[i][j])
        car_dic[j] = a

    carcenter=car_dic

    if request.method=='POST':
        car_index = request.form['']

        return render_template('map.html', result=carcenter, x=car_index)
        
    else:
        return render_template('carcenter_list.html', result=carcenter)
        

        





@app.route('/oil', methods=['GET','POST'])
def expend_list():
    return render_template('oil.html')





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
