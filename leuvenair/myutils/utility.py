# imports
import json
import numpy as np
import pandas as pd
from scipy import interpolate

def readJson(filename='./LEUVENAIRmeta_final.json'):
    """
    Converts the tabular overview of the LEUVENAIR sensors (downloadable as a JSON file) into
    ndarray.
    Source: https://data.leuvenair.be/meta-l.html
    
    Arguments:
        filename -- Path of json file to be read
    
    Returns:
        fields -- python dictionary containing ndarray corresponding to all the 15 fields
        (except GMAPS and MADAVI)
    """
    with open(filename) as json_file:
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

def getSensorData(filename_json = './LEUVENAIRmeta_final.json', filename='./LEUVENAIRfulldump2019.csv'):
    """
    Parses the complete data dump to extract data corresponding to each sensor
    
    Arguments:
        filename_json -- Path of json file to be read
        filename -- Path of .csv file to be read
    
    Returns:
        fields -- python dictionary containing ndarray corresponding to each sensor
    """
    fields = readJson(filename_json)
    allSensors = fields['SDS011ID']
    dframe = pd.read_csv(filename, skiprows=0, nrows = None, usecols = None)
    dframe = dframe.sort_values(['SDS011ID', 'DATEUTC'], ascending=[True, True])
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
            print('sensor:',sensor,' 1st obs:',timeOfsensor[0],' last:',timeOfsensor[-1],end='')
            print(' median dt: ', np.median(dt).astype(int),' min, total obs:',df.values.shape[0])
    print('Total observations across all sensors = ',numval)
    return fields
        
def interpolate1D(x,y,xnew):
    f = interpolate.interp1d(x,y)
    return f(xnew)
    
def getSensorInterpolatedData(fields,tstart='2019-03-31 16:00:00',tstop='2019-04-01 20:00:00',fid=4):
    """
    The function reads sensor data and interpolates from a non-uniformly sampled data (in time) to
    uniformly spaced data in time. This is particularly useful for taking mean, median etc across
    several sensor data.
    
    Arguments:
        fields -- python dictionary containing ndarray corresponding to each sensor
        tstart --  starting time point
        tstop -- stopping time point
        fid -- field index (for example for PM2.5 index is 4)
        
    Returns:
        baseline -- the uniformly spaced array on which data is interpolated
        interpVal -- the corressponding interpolated values
        xaxis  -- time as x axis
    """
    
    deltaT = pd.to_datetime(tstop)-pd.to_datetime(tstart)
    print('Extracting data over duration ',deltaT,' starting at ',pd.to_datetime(tstart))
    tmin = 0; tmax = deltaT.total_seconds()/60 # convert into minutes;
    dt = 1 # 1 minute resolution
    print('Sampling resolution = ',dt,' minute')
    baseline = np.arange(tmin,tmax,dt)
    interpVal = np.zeros((len(fields),baseline.shape[0]),dtype=np.float64)
    for row,sensor in enumerate(fields):
        #print('Processing data for sensor',str(sensor))
        sdata = fields[str(sensor)]
        timeUTC = sdata[:,0]; PM25 = sdata[:,fid];
        flag = ((timeUTC>tstart) & (timeUTC<tstop))
        timeUTC_April = timeUTC[flag]; PM25_April = PM25[flag];
        if(timeUTC_April.shape[0]>1):
            timeUTC_April = pd.to_datetime(timeUTC_April)
            deltaTime = timeUTC_April-timeUTC_April[0]
            X = deltaTime.astype('timedelta64[m]') # convert into minutes
            Y = PM25_April
            func = interpolate.interp1d(X,Y,bounds_error=False,fill_value=0)
            interpVal[row,:] = func(baseline)
    xaxis = pd.to_datetime(tstart)+pd.to_timedelta(list(baseline), unit='m')
    return baseline.reshape((1,baseline.shape[0])), interpVal, xaxis  

def find_event(fields, startmonth=1, stopmonth=13, startday=1, stopday=30):
    """
    This function loops over a range of days (and months). The time step is 1 day.
    It computes min, max, standard deviation and average of the pollutant PM2.5
    over the duration of time step (of the median values across all sensors).
    
    Arguments:
        fields -- python dictionary containing ndarray corresponding to each sensor
        startmonth --  starting month
        stopmonth -- one before last month
        startday -- starting day
        stopday -- one before last day
        
    Returns:
        eventdict: a dict which can be accessed via key of form day-month
        fullmatrix: a numpy array containing all the statistics
    """
    eventdict = {}
    fullmatrix = np.empty(shape=(0,7))
    itr = 0
    for month in range(startmonth,stopmonth):
        fmonth = "{:02d}".format(month)
        for day in range(startday,stopday):
            fday = "{:02d}".format(day)
            fdayplus = "{:02d}".format(day+1)
            start = str('2019-')+str(fmonth)+'-'+str(fday)+'  00:00:00'
            stop = str('2019-')+str(fmonth)+'-'+str(fdayplus)+'  00:00:00'
            X, Y, xaxis = getSensorInterpolatedData(fields, tstart=start, tstop=stop, fid=4)
            temp = np.squeeze(np.nanmedian(Y,axis=0))
            print('start time = ',start,' stop time = ',stop)
            print('Min = ',np.min(temp),'Max = ',np.max(temp),'Standard deviation = ',np.std(temp),'Mean  = ',np.mean(temp))
            arr = np.array([itr, day, month, np.min(temp), np.max(temp), np.std(temp), np.mean(temp)]).reshape(1,7)
            eventdict[str(day)+'-'+str(month)] = arr
            fullmatrix = np.append(fullmatrix, arr, axis = 0)
            itr = itr+1
    return eventdict, fullmatrix