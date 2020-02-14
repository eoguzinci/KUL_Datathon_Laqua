# imports
import json
import numpy as np

def readJson():
    
    with open('LEUVENAIRmeta_final.json') as json_file:
        data = json.load(json_file)
        numrows = len(data)

        # All integers
        SDS011ID = np.zeros(numrows,dtype=np.int)
        DHTID = np.zeros(numrows,dtype=np.int)
        EXPORT = np.zeros(numrows,dtype=np.int)
        POSTALCODE = np.zeros(numrows,dtype=np.int)
        HEIGHT = np.zeros(numrows,dtype=np.int)
        SENSOR_POSITION = np.zeros(numrows,dtype=np.int)
        INDUSTRY = np.zeros(numrows,dtype=np.int)
        WOODSTOVES = np.zeros(numrows,dtype=np.int)
        TRAFFIC = np.zeros(numrows,dtype=np.int)
        SVL = np.zeros(numrows,dtype=np.int)

        # All floats
        LAT = np.zeros(numrows,dtype=np.float64)
        LON = np.zeros(numrows,dtype=np.float64)
        NO2_CN = np.zeros(numrows,dtype=np.float64)

        # All strings
        STREET = []
        CITY = []

        for itr,row in enumerate(data):
            x = row
            SDS011ID[itr] = x['SDS011ID']
            DHTID[itr] = -9999 if (x['DHTID'] is None) else x['DHTID']
            EXPORT[itr] = x['EXPORT']
            POSTALCODE[itr] = x['POSTALCODE']
            HEIGHT[itr] = -9999 if (x['HEIGHT (cm)'] is None) else x['HEIGHT (cm)']
            SENSOR_POSITION[itr] = -9999 if (x['SENSOR POSITION'] is None) else x['SENSOR POSITION']
            INDUSTRY[itr] = -9999 if (x['INDUSTRY'] is None) else x['INDUSTRY']
            WOODSTOVES[itr] = -9999 if (x['WOODSTOVES'] is None) else x['WOODSTOVES']
            TRAFFIC[itr] = -9999 if (x['TRAFFIC'] is None) else x['TRAFFIC']
            SVL[itr] = x['SVL']

            LAT[itr] = x['LAT']
            LON[itr] = x['LON']
            NO2_CN[itr] = -9999 if (x['NO2_CN'] is None) else x['NO2_CN']

            STREET.append(x['STREET'])
            CITY.append(x['CITY'])
        
    fields = {}
    fields['SDS011ID'] = SDS011ID
    fields['DHTID'] = DHTID
    fields['EXPORT'] = EXPORT
    fields['LAT'] = LAT
    fields['LON'] = LON
    fields['STREET'] = STREET
    fields['POSTALCODE'] = POSTALCODE
    fields['CITY'] = CITY
    fields['HEIGHT'] = HEIGHT
    fields['SENSOR_POSITION'] = SENSOR_POSITION
    fields['INDUSTRY'] = INDUSTRY
    fields['WOODSTOVES'] = WOODSTOVES
    fields['TRAFFIC'] = TRAFFIC
    fields['SVL'] = SVL
    fields['NO2_CN'] = NO2_CN    
    
    return fields