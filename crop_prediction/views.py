from django.shortcuts import render, redirect
from django.http import HttpResponse
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler
import requests
import json
from urllib.request import urlopen

# Create your views here.
def Homepage(request):
# try:
    if request.method == 'POST':
        N = float(request.POST.get('N'))
        P = float(request.POST.get('P'))
        K = float(request.POST.get('K'))
        area = float(request.POST.get('area')) #hecters(ha)
        ph = float(request.POST.get('ph'))
        rainfall = float(request.POST.get('rainfall'))
        

        data_loc = json.load(urlopen("http://ipinfo.io/json"))
        lat = data_loc['loc'].split(',')[0]
        lon = data_loc['loc'].split(',')[1]
        api = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=ed1c36608f89e90d3d522300706a8c89"
        resp = requests.get(api)
        decoded = resp.content.decode("utf-8")
        resp = json.loads(decoded)
        avg_year_temp = float(float(resp['main']['temp']) - 273.15)

        loaded_model=pickle.load(open('crop_prediction/requirements/forest_classifier.pkl','rb'))
        loaded_scale=pickle.load(open('crop_prediction/requirements/scale.pkl','rb'))
        data =loaded_scale.transform(np.array([[avg_year_temp, ph, rainfall, N, P, K]]))
        prediction = loaded_model.predict(data)

        loaded_model2=pickle.load(open(f'crop_prediction/requirements/additional_files/crop_{prediction[0]}.csv.pkl','rb'))
        loaded_scale2=pickle.load(open(f'crop_prediction/requirements/additional_files/crop_{prediction[0]}.csv_scaler.pkl','rb'))
        inp2=[area, avg_year_temp, rainfall]
        data2=loaded_scale2.transform([inp2])
        prediction2 = loaded_model2.predict(data2) #metric tonnes
    

        context = {'result': prediction[0], 'result2':prediction2[0]}
        return render(request, 'crop_prediction/Resultpage.html', context)
    context = {}
    return render(request, 'crop_prediction/Homepage.html', context)
# except:
    return HttpResponse("Invalid inputs entered or validation error")
