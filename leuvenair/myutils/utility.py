# imports
import json
import pandas as pd
import numpy as np
from scipy import interpolate

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
    
    print('Note: sensors 8799 and 8827 are repeated in the json file!')
    
    return fields

def getSensorData():
    fields = readJson()
    allSensors = fields['SDS011ID']
    dframe = pd.read_csv('LEUVENAIRfulldump2018.csv', skiprows=0, nrows = None, usecols = None)
    print('The complete pandas frame has shape ',dframe.values.shape)
    fields = {}
    numval = 0
    for sensor in np.unique(allSensors):
        df = dframe.loc[dframe['SDS011ID'] == sensor]
        fields[str(sensor)] = df.values
        numval = numval + df.values.shape[0]
        timeOfsensor = pd.to_datetime(df.values[:,0])
        
#        datetime = pd.to_datetime(np.squeeze(df.values[:,0]))
#        seconds = datetime.second
#        minutes = datetime.minute
#        hours = datetime.hour
#        days = datetime.day
#        weeks = datetime.week
#        months = datetime.month
#        years = datetime.year

        dt = np.diff(timeOfsensor).astype('timedelta64[m]')
        if(df.values.shape[0]==0):
            print('sensor:',sensor,'did not record any observation.')
        else:
            print('sensor:',sensor,' 1st obs:',timeOfsensor[0],' last:',timeOfsensor[-1],' median dt: ', np.median(dt).astype(int),' min, total obs:',df.values.shape[0])
    print('Total observations across all sensors = ',numval)
    return fields
        
def interpolate1D(x,y,xnew):
    f = interpolate.interp1d(x,y)
    return f(xnew)
    
def getSensorInterpolatedAvg(fields,tmin='2018-04-01 16:00:00',tmax='2018-04-01 20:00:00',fid=4,xmin=0,dx=1,xmax=240):
    baseline = np.arange(xmin,xmax+dx,dx)
    interpVal = np.zeros((len(fields),baseline.shape[0]),dtype=np.float64)
    numvalidrows = 0
    for row,sensor in enumerate(fields):
        #print('Processing data for sensor',str(sensor))
        sdata = fields[str(sensor)]
        timeUTC = sdata[:,0]; PM25 = sdata[:,fid];
        flag = ((timeUTC>tmin) & (timeUTC<tmax))
        timeUTC_April = timeUTC[flag]; PM25_April = PM25[flag];
        if(timeUTC_April.shape[0]>0):
            numvalidrows = numvalidrows+1
            timeUTC_April = pd.to_datetime(timeUTC_April)
            deltaTime = timeUTC_April-timeUTC_April[0]
            X = deltaTime.astype('timedelta64[m]')
            Y = PM25_April
            func = interpolate.interp1d(X,Y,bounds_error=False,fill_value=Y[-1])
            interpVal[row,:] = func(baseline)
    return baseline.reshape((1,baseline.shape[0])), interpVal    
    
        
    
        
            
        
		
