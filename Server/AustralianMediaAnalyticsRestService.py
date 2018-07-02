# Author: shajidm@student.unimelb.edu.au
# Australian Socail Media Analytics Rest Service

from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask.ext.jsonpify import jsonify

import shapefile
from shapely.geometry import Polygon
from shapely.geometry import Point
import numpy as np
import os 
from couchdb.design import ViewDefinition
import couchdb
from datetime import datetime
import pytz
import pandas as pd
import statsmodels.formula.api as sm
import json
import matplotlib.pyplot as plt

import scipy as sp
from numpy import *

app = Flask(__name__)
api = Api(app)

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)

class AustralianMediaAnalyticsRestService(Resource):
    def get(self):

        returnDataType = request.args.get('return') 

        PATH='/Users/shajid/Documents/MyWorks/CCC/datas/datas.prj'
        PATH2='/Users/shajid/Documents/MyWorks/CCC/data.csv'

        sf = shapefile.Reader(PATH)

        shape = sf.shapes()
        len(shape)

# pmD is the data frame read from csv# pmD i
#data = pd.read_csv('file1.csv', error_bad_lines=False)
        pmD = pd.read_csv(PATH2)

        pmD = pmD.replace(r'null', np.nan, regex=True)

# extract from data frame
        area_code = pmD.iloc[:,0]
        area_name = pmD.iloc[:,1]
        female_divorce = pmD.iloc[:,2]
        female_sep = pmD.iloc[:,3]
        male_divorce = pmD.iloc[:,4]
        male_sep = pmD.iloc[:,5]

        zero = [0]*66

#record of coordinates
        record = sf.shapeRecords()

        record[0].shape.points
        len(record)

        rawCoord = []
        for i in range(len(record)):
            rawCoord.append(Polygon(record[i].shape.points))
        rawCoord[0:2]


        LGAcoord = dict(zip(area_code,rawCoord))


# Connect to sc_tweets couchDB and retrieve the Coordinate values along with sentiment analysis
        user = 'admin'
        password = 'admin'
        try:
            couch = couchdb.Server('http://%s:%s@115.146.95.146:5984/' % (user, password))
            db_sc_tweets = couch['sc_tweets']
            db_sentiment_tweets = couch['sentiment_tweets']
            print('Connection Success')
        except:
            print('Connection Failed')
    
# Connect to sc_tweets couchDB and retrieve the Coordinate values along with sentiment analysis
        scGen = []
        for row in db_sc_tweets.view('_design/DocsWithCoordinates/_view/CoordinatesNSentiments'): 
            coordinates = row.key
            score = row.value
            scGen.append([coordinates,score])
        areaDictUC = dict(zip(area_code,zero))
        for tw in range(len(scGen)):
          for area in LGAcoord:
                if LGAcoord[area].contains(Point(scGen[tw][0][0],scGen[tw][0][1])):
                   areaDictUC[area] += 1

        urbanCulture = np.array([ v for v in areaDictUC.values() ])

# Connect to sentiment_tweets couchDB and retrieve the Coordinate values along with sentiment scores
        stressGen = []
        for row in db_sentiment_tweets.view('_design/DocsWithCoordinates/_view/CoordinatesNSentiments'): 
            coordinates = row.key
            score = row.value
            stressGen.append([coordinates,score])

# extract negative tweets
        negative = 0
        negTweets = []
        for i in range(len(stressGen)):
          if stressGen[i][1] <= 0:
        #print(stressGen[i])
             negTweets.append(stressGen[i][0])
             negative += 1

## extract positive tweets
        positive = 0
        posTweets = []
        for i in range(len(stressGen)):
         if stressGen[i][1] > 0:
               posTweets.append(stressGen[i][0])
               positive += 1

        #print(positive)
        #print(negative)
# prepare dictionary
        areaDictNegSent = dict(zip(area_code,zero))
        areaDictPosSent = dict(zip(area_code,zero))

        for tw in range(len(negTweets)):
         for area in LGAcoord:
               if LGAcoord[area].contains(Point(negTweets[tw][0],negTweets[tw][1])):
                    areaDictNegSent[area] += 1

        for tw in range(len(posTweets)):
            for area in LGAcoord:
                if LGAcoord[area].contains(Point(posTweets[tw][0],posTweets[tw][1])):
                    areaDictPosSent[area] += 1

        list_Negvalues = [ v for v in areaDictNegSent.values() ]
        list_Posvalues = [ v for v in areaDictPosSent.values() ]

# convert list to numpy array
        negSentiment = np.array(list_Negvalues)
        posSentiment = np.array(list_Posvalues)

        pmfDivorce = np.array(female_divorce, dtype = np.float)
        pmfSeparation = np.array(female_sep, dtype = np.float)

        pmmDivorce = np.array(male_divorce, dtype = np.float)
        pmmSeparation = np.array(male_sep, dtype = np.float)

        pmDivorce=pmfDivorce + pmmDivorce
        pmSeparation=pmfSeparation + pmmSeparation

        df = pd.DataFrame({"pmDivorce": pmDivorce ,"pmSeparation": pmSeparation , 
                   "negSentiment": negSentiment, "posSentiment": posSentiment, 
                   "urbanCulture":urbanCulture, "area_code":area_code, 
                   "area_name":area_name})
        df[25:76] # data for regressions


        model = sm.ols(formula="pmDivorce ~ negSentiment + posSentiment + urbanCulture", data=df, missing = 'drop').fit()

        model = sm.ols(formula="pmSeparation ~ negSentiment + posSentiment + urbanCulture", data=df, missing = 'drop').fit()

        sp.stats.pearsonr(posSentiment,pmDivorce)

        sp.stats.pearsonr(posSentiment,pmSeparation)

        sentimentDictExport = {"negativeSentiment":list(negSentiment), "positiveSentiment":list(posSentiment), "area_code":list(area_code), 
                          "area_name": list(area_name)}

        rowList = []
        for row in range(len(df)):
            rowList.append(list(list(df.iloc[[row]].values)[0]))


        area_codeS = list(map(str, area_code))
#area_codeS
        dataVisualize = dict(zip(area_codeS, rowList))
#dataVisualize

        dataVisualize['fieldname'] = list(df)

# for visualization on JavaScript front end
        with open('visualizeSentiment.json', 'w') as fp:
          json.dump(dataVisualize, fp)

# testing visualization before exporting to Javascript

        m1, b1 = np.polyfit(pmDivorce,negSentiment,1)
        m2, b2 = np.polyfit(pmDivorce,posSentiment,1)
        m3, b3 = np.polyfit(pmDivorce,urbanCulture,1)
        m4, b4 = np.polyfit(pmSeparation,negSentiment,1)
        m5, b5 = np.polyfit(pmSeparation,posSentiment,1)
        m6, b6 = np.polyfit(pmSeparation,urbanCulture,1)


        divorceVsNeg = []
        for i in range(len(pmDivorce)):
          divorceVsNeg.append([list(pmDivorce)[i], list(negSentiment)[i]])

        dataDivorceVsNeg = {"slope":m1,"constant":b1,"DivorceVsNeg":json.dumps(divorceVsNeg, cls=MyEncoder)}


        divorceVsPos = []
        for i in range(len(pmDivorce)):
            divorceVsPos.append([list(pmDivorce)[i], list(posSentiment)[i]])

        dataDivorceVsPos = {"slope":m2,"constant":b2,"DivorceVsPos":json.dumps(divorceVsPos, cls=MyEncoder)}


        divorceVsUrban = []
        for i in range(len(pmDivorce)):
            divorceVsUrban.append([list(pmDivorce)[i], list(urbanCulture)[i]])

        dataDivorceVsUrban = {"slope":m3,"constant":b3,"DivorceVsUrban":json.dumps(divorceVsUrban, cls=MyEncoder)}


        sepVsNeg = []
        for i in range(len(pmSeparation)):
            sepVsNeg.append([list(pmSeparation)[i], list(negSentiment)[i]])

        dataSepVsNeg = {"slope":m4,"constant":b4,"SepVsNeg":json.dumps(sepVsNeg, cls=MyEncoder)}


        sepVsPos = []
        for i in range(len(pmSeparation)):
            sepVsPos.append([list(pmSeparation)[i], list(posSentiment)[i]])

        dataSepVsPos = {"slope":m5,"constant":b5,"SepVsPos":json.dumps(sepVsPos, cls=MyEncoder)}

        sepVsUrban = []
        for i in range(len(pmSeparation)):
            sepVsUrban.append([list(pmSeparation)[i], list(urbanCulture)[i]])

        dataSepVsUrban = {"slope":m6,"constant":b6,"SepVsUrban":json.dumps(sepVsUrban, cls=MyEncoder)}

        if returnDataType == 'DivorceVsNeg':
            datax = dataDivorceVsNeg
        elif returnDataType == 'DivorceVsPos':
            datax = dataDivorceVsPos
        elif returnDataType == 'DivorceVsUrban':
            datax = dataDivorceVsUrban
        elif returnDataType == 'SepVsNeg':
            datax = dataSepVsPos
        elif returnDataType == 'SepVsPos':
            datax = dataSepVsNeg
        elif returnDataType == 'SepVsUrban':
            datax = dataSepVsUrban

        return jsonify(datax)

api.add_resource(AustralianMediaAnalyticsRestService, '/AustralianMediaAnalyticsRestService')


if __name__ == '__main__':
     app.run(host="0.0.0.0",port=8003)
