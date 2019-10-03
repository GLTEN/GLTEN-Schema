'''
Created on 1 Oct 2019
This tests the fact that I can use rest to interrogate GLTEN and return their json string

@author: castells
'''
import requests
import json

class APIError(Exception):
    """An API Error Exception"""

    def __init__(self, status):
        self.status = status

    def __str__(self):
        return "APIError: status={}".format(self.status)

def getData(exptID):
    base = "https://glten.org/api/v0/public/experiment/"
    exptID = str(exptID)
    gltenData = requests.get(base + exptID)
    
    if gltenData.status_code != 200:
        # This means something went wrong.
        raise APIError('GET /tasks/ {}'.format(gltenData.status_code))
    #for todo_item in resp.json():
        #print('{} {}'.format(todo_item['id'], todo_item['summary']))
    data =  gltenData.json()
    return data
def prepareRelatedExperiments():
#      [
#             {
#                 "type": "Experiment",
#                 "identifier": "10.23637/Sax-rrn2-1 - that would be the DOI - Unique Identifier",
#                 "localIdentifier": "rrn2 - Use the code for the experiment - Local Identifier",
#                 "name": "Saxmundahm Rotation 2"
#             },
#             {
#                 "type": "Experiment",
#                 "identifier": "10.23637/Sax-rrn2-1 - that would be the DOI - Unique Identifier",
#                 "localIdentifier": "rrn2 - Use the code for the experiment - Local Identifier",
#                 "name": "Saxmundahm Rotation 2"
#             }
#         ]
    return "TODO"

def prepareFunders():
#     [
#         {
#             "type": "organization",
#             "name": "Biotechnology and Biological Sciences Research Council",
#             "sameAs": "http://dx.doi.org/10.13039/501100000268",
#             "award": "BBS/E/C/000J0300 - The Rothamsted Long - Term Experiments - National Capability",
#             "identifier": "https://gtr.ukri.org/projects?ref=BBS%2FE%2FC%2F000J0300",
#             "startDate": "2000",
#             "endDate": "2010"
#         },        {
#             "type": "organization",
#             "name": "Biotechnology and Biological Sciences Research Council",
#             "sameAs": "http://dx.doi.org/10.13039/501100000268",
#             "award": "BBS/E/C/000J0300 - The Rothamsted Long - Term Experiments - National Capability",
#             "identifier": "https://gtr.ukri.org/projects?ref=BBS%2FE%2FC%2F000J0300",
#             "startDate": "2000",
#             "endDate": "2010"
#         }
#     ]
    return "TODO"

def prepareExperiment(data):
    return dict(
    administrative= dict( 
        type= "Experiment",
        identifier=  data['name'],
        localIdentifier=  data['local_identifier'],
        name= data['name'],
        url=  data['url'],
        description= data['description'],
        disambiguatingDescription= data['objective'],
        relatedExperiment= prepareRelatedExperiments()
    ),
    dataAccess= dict(
        type= "creativeWork",
        conditionsOfAccess= data['data_statement_label'],
        isAccessibleForFree= data['data_policy_status'],
        publishingPrinciples= data['data_url'],
        actionableFeedbackPolicy= data['objective'],
        correctionsPolicy= data['objective'],
        unnamedSourcesPolicy= data['data_policy_url']
    ),
    license= dict(
        type= "CreativeWork",
        name= "CC-by-4",
        license= "http://creativecommons.org/licenses/by/4.0"
    ),
    temporalCoverage= "1953/1970 from schema",
    dateStart= data['start_year'],
    dateEPEnd= data['establishment_period_end'],
    dateEnd= data['end_year'],
    funder= prepareFunders() 
)
    
if __name__ == '__main__':
    exptID = 0
    while type(exptID) != int or exptID == 0:
        exptID = int(input('Which experiment GLTENID? '))
        
    
    data = getData(exptID)
    experiment = prepareExperiment(data)   
    
    strJsDoc =  json.dumps(experiment, indent=4)
    print(strJsDoc)