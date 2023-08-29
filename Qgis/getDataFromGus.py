import urllib
import json
from qgis.core import *
from qgis.gui import *

@qgsfunction(args='auto', group='Custom')


def getInfo(GUSid, region, feature, parent):
        baseurl = 'https://bdl.stat.gov.pl/api/v1/data/by-unit/'+ str(GUSid) +'?'
        params={
            'format': 'json',
            'lang': 'pl',
            'var-id': [4313,4314,4315]
            }
        url = baseurl + urllib.parse.urlencode(params, True)
        try:
            response = urllib.request.urlopen(url)  
            sresults = response.read()
            results = json.loads(sresults)
            results = results['results']
            data = [i['values'] for i in results]
            for list in data:
                for dict in list:
                    dict.pop('attrId')
            sup = []
            for item in data[0]:
                sup.append([i for i in item.values()][1])
    
            performance = []
            for item in data[1]:
                performance.append([i for i in item.values()][1])
        
            harvest = []
            for item in data[2]:
                harvest.append([i for i in item.values()][1])
    
            years = list(range(1999,2023))
    
            html = '<table><thead><tr><h3>Region ' + region + '</h3></tr><tr><th>Rok</th><th>Powierzchnia(ha)</th><th>Plony z 1 ha(dt)</th><th>Zbiory(dt)</th><tbody>'

            for h, i , j, k in zip(years, sup, performance, harvest):
                html+= "<tr><td>" + str(h) + "</td><td>" + str(i) + "</td><td>" + str(j) + "</td><td>" + str(k) + "</td></tr>"
            html+='</tbody></table>'
            return html
    
        except:
            return "Something went wrong"