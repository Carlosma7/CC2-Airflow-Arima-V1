from flask import Flask, Response, jsonify
import json
import pickle
import pandas as pd
import pmdarima as pm
import os
from statsmodels.tsa.arima_model import ARIMA
import time
from datetime import datetime, timedelta
import modelo
from zipfile import ZipFile

# Definición de la aplicación
app = Flask(__name__)


def predecir_modelo(interval):

    with ZipFile('./modelo_temp.pickle.zip', 'r') as myzip:
        myzip.extractall('./')

    with ZipFile('./modelo_hum.pickle.zip', 'r') as myzip:
        myzip.extractall('./')

    modelo_temp = pickle.load( open( './modelo_temp.pickle', "rb" ) )
    predicc_temp, confint = modelo_temp.predict(n_periods=interval, return_conf_int=True)

    modelo_hum = pickle.load( open( './modelo_hum.pickle', "rb" ) )
    predicc_hum, confint2 = modelo_hum.predict(n_periods=interval, return_conf_int=True)


    fecha_actual = datetime.now() + timedelta(hours=3)
    fechas_intervalo = pd.date_range(fecha_actual.replace(second=0, microsecond=0), periods=interval, freq='H')
    prediccion = []

    for tiempo, temp, hum in zip(fechas_intervalo, predicc_temp, predicc_hum):
        dt = time.mktime(tiempo.timetuple())
        # Almacenar prediccion
        prediccion.append(
            {'hour': datetime.utcfromtimestamp(dt).strftime('%d-%m %H:%M'),
            'temp': temp,  
             'hum': hum
            })
    return prediccion

@app.route("/servicio/v1/prediccion/24horas",methods=['GET'])
def hours_24():
    response = Response(json.dumps(predecir_modelo(24)), status=200)
    response.headers['Content-Type']='application/json'
    return response

@app.route("/servicio/v1/prediccion/48horas",methods=['GET'])
def hours_48():
    response = Response(json.dumps(predecir_modelo(48)), status=200)
    response.headers['Content-Type']='application/json'
    return response

@app.route("/servicio/v1/prediccion/72horas",methods=['GET'])
def hours_72():
    response = Response(json.dumps(predecir_modelo(72)), status=200)
    response.headers['Content-Type']='application/json'
    return response