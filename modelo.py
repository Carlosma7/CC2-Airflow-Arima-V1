from statsmodels.tsa.arima_model import ARIMA
import pandas as pd
import pmdarima as pm
import pymongo
import pickle
from datetime import datetime, timedelta
from zipfile import ZipFile
import zipfile
import time


class Modelo:
    def __init__(self):
        client = pymongo.MongoClient("mongodb+srv://"+"CC2"+":"+"UGR"+"@grandquiz.fo6ph.mongodb.net/CC2?retryWrites=true&w=majority")
        datos = client.CC2['SanFrancisco']
        # Crear dataframe de datos
        datos = pd.DataFrame(list(datos.find()))
        # Omisión valores perdidos
        datos = datos.dropna()

        # Modelo temperatura
        modelo_temp = pm.auto_arima(
            datos['TEMP'].dropna(),
            start_p=1, start_q=1,
            test='adf',       # use adftest to find optimal 'd'
            max_p=3, max_q=3, # maximum p and q
            m=1,              # frequency of series
            d=None,           # let model determine 'd'
            seasonal=False,   # No Seasonality
            start_P=0,
            D=0,
            trace=True,
            error_action='ignore',
            suppress_warnings=True,
            stepwise=True)

        # Serialización y exportación
        pickle.dump(modelo_temp, open("./modelo_temp.pickle", "wb" ) )

        model_hum = pm.auto_arima(
            datos['HUM'].dropna(),
            start_p=1, start_q=1,
            test='adf',       # use adftest to find optimal 'd'
            max_p=3, max_q=3, # maximum p and q
            m=1,              # frequency of series
            d=None,           # let model determine 'd'
            seasonal=False,   # No Seasonality
            start_P=0,
            D=0,
            trace=True,
            error_action='ignore',
            suppress_warnings=True,
            stepwise=True)
        
        # Serialización y exportación
        pickle.dump(modelo_temp, open("./modelo_hum.pickle", "wb" ) )

        with ZipFile('./modelo_temp.pickle.zip', 'w', zipfile.ZIP_DEFLATED) as zip:
            zip.write('./modelo_temp.pickle')

        with ZipFile('./modelo_hum.pickle.zip', 'w', zipfile.ZIP_DEFLATED) as zip:
            zip.write('./modelo_hum.pickle')


if __name__ == "__main__":
    m = Modelo()