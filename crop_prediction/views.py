from django.shortcuts import render, redirect
from django.http import HttpResponse
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler

# Create your views here.
def Homepage(request):
    if request.method == 'POST':
        avg_year_temp = float(request.POST.get('avg_year_temp'))
        ph = float(request.POST.get('ph'))
        rainfall = float(request.POST.get('rainfall'))
        sowing_temp = float(request.POST.get('sowing_temp'))
        harvesting_temp = float(request.POST.get('harvesting_temp'))
        N = float(request.POST.get('N'))
        P = float(request.POST.get('P'))
        K = float(request.POST.get('K'))
        area = float(request.POST.get('area'))
        temperature = float(request.POST.get('temperature'))

  
        loaded_model=pickle.load(open('crop_prediction/requirements/forest_classifier.pkl','rb'))
        loaded_scale=pickle.load(open('crop_prediction/requirements/scale.pkl','rb'))
        data =loaded_scale.transform(np.array([[avg_year_temp, ph, rainfall, sowing_temp, harvesting_temp, N, P, K]]))
        prediction = loaded_model.predict(data)


        loaded_model2=pickle.load(open(f'crop_prediction/requirements/additional_files/crop_{prediction[0]}.csv.pkl','rb'))
        loaded_scale2=pickle.load(open(f'crop_prediction/requirements/additional_files/crop_{prediction[0]}.csv_scaler.pkl','rb'))
        inp2=[area, temperature, rainfall, sowing_temp, harvesting_temp]
        data2=loaded_scale2.transform([inp2])
        prediction2 = loaded_model2.predict(data2)
       

        context = {'result': prediction[0], 'result2':prediction2[0]}
        return render(request, 'crop_prediction/Resultpage.html', context)
    context = {}
    return render(request, 'crop_prediction/Homepage.html', context)
