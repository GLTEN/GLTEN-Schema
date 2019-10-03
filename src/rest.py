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

def prepareFunders(data):
    funders = "NOT in GLTEN"
    
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
    return funders

def prepareCitation(data):
    citation = []
    for details in data['literature']:
        citation.append(dict(
            type= "creativeWork",
            identifier= details['doi'],
            sameAs= details['doi'],
            citation= details['title'],
            inLanguage=  details['language'],
            relationType= "isCitedBy"
            
            ))
# [    
#         {
#             "type": "creativeWork",
#             "identifier": "https://doi.org/10.1111/j.1475-2743.2006.00003.x",
#             "sameAs": "https://doi.org/10.1111/j.1475-2743.2006.00003.x",
#             "title": "Gibbs, P. A. , Chambers, B. J. , Chaudri, A. M. , McGrath, S. P. , Carlton-Smith, C. H. , Bacon, J. R. , Campbell, C. D. and Aitken, M. N. (2006) \"Initial results from a long-term, multi-site field study of the effects on soil fertility and microbial activity of sludge cakes containing heavy metals\", Soil Use and Management, 22, 11-21",
#             "inLanguage": "English",
#             "relationType": "isCitedBy"
#         },
#         {
#             "type": "creativeWork",
#             "identifier": "https://doi.org/10.1111/j.1475-2743.2006.00003.x",
#             "sameAs": "https://doi.org/10.1111/j.1475-2743.2006.00003.x",
#             "title": "Gibbs, P. A. , Chambers, B. J. , Chaudri, A. M. , McGrath, S. P. , Carlton-Smith, C. H. , Bacon, J. R. , Campbell, C. D. and Aitken, M. N. (2006) \"Initial results from a long-term, multi-site field study of the effects on soil fertility and microbial activity of sludge cakes containing heavy metals\", Soil Use and Management, 22, 11-21",
#             "inLanguage": "English",
#             "relationType": "isCitedBy"
#         }
#     ]
    return citation

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
    funder= prepareFunders(data) ,
    citation = prepareCitation(data)
)
    
def prepareSoilProperties(data):
    soilProperties = []
    for details in data['site_soil_properties']:
        soilProperties.append(dict (  
            variableMeasured= details['variable_term'],
            isEstimated= details['is_estimated'],
            isBaseline= details['is_baseline'],
            valueReference= details['typical_value'],
            minValue= details['min_value'],
            maxValue= details['max_value'],
            minSampleDepth= details['min_depth'],
            maxSampleDepth= details['max_depth'],
            unitCode= details['unit_term'],
            unitText= details['unit_label'],
            refYear= details['reference_year'],
            measurementTechnique= "NOT IN GLTN",
            description= "NOT IN GLTN"
            )
        )
    return soilProperties


def prepareSite(data):
    return dict(
        
    administrative= dict (
        name=  data['site_name'],
        identifier=  data['site_local_code'],
        type = data['site_type_label'],
        sameAs=  data['data_statement_label'],
        doi=  data['site_doi'],
        visitsAllowed=  data['site_visits_allowed'],
        visitingArrangements= data['site_visiting_arrangements'],
        description= data['site_history'],
        management= data['site_management']
    ),
    location= dict(
        addressLocality= data['site_locality'],
        addressRegion= data['site_region'],
        addressCountry= data['site_country'],
        geoLocationPoint= dict(
            pointLongitude= data['site_centroid_longitude'],
            pointLatitude= data['site_centroid_latitude']
            ),
        geoLocationPlace= data['site_country'],
        polygon= "NOT IN GLTEN",
        elevation= data['site_elevation'],
        elevationUnit= data['site_elevation_unit'],
        slope= data['site_slope'],
        slopeAspect= data['site_slope_aspect']
    ),
    soil= dict (
        soilTypeLabel= data['site_soil_type_label'],
        soilDescription= data['site_soil_description']
    ),
    soilProperty= prepareSoilProperties(data),
    climate= dict(
        name= data['site_climatic_type_label'],
        description= data['site_soil_description'],
        weatherStation= dict(
            weatherStationID= "NOT IN GLTEN",
            name= "NOT IN GLTEN",
            distance="NOT IN GLTEN",
            direction="NOT IN GLTEN"
            )
        )
    

        )

def preparePersons(data):
    contributors = []
    for details in data['people']:
        sname = details['name'].split() 
        #assuming name = givenName familyName
        contributors.append(dict
                            (  
                                type= "Person",
            jobTitle= details['role_term'],
            name= details['name'],
            givenName= sname[0],
            familyName= sname[1],
            sameAs= details['orcid'],
            address= dict(
                type= "PostalAddress",
                streetAddress= "not in GLTEN",
                addressLocality= "not in GLTEN",
                addressRegion= "not in GLTEN",
                postalCode= "not in GLTEN",
                addressCountry= "not in GLTEN"
            ),
            affiliation= dict (
                type= "Organization",
                name= "Computational and Analytical Sciences, Rothamsted Research",
                address= ", West Common, Harpenden, Hertfordshire, AL5 2JQ, United Kingdom"
            )
            )
                            )
    return contributors
       
if __name__ == '__main__':
    exptID = 0
    while type(exptID) != int or exptID == 0:
        exptID = int(input('Which experiment GLTENID? '))
        
    
    data = getData(exptID)
    experiment = prepareExperiment(data)   
    site = prepareSite(data)
    persons = dict (contributors = preparePersons(data))
    
    experimentJson =  json.dumps(experiment, indent=4)
    print("experiment = " + experimentJson)
    siteJson =  json.dumps(site, indent=4)
    print("site = " + siteJson)
    personJson =  json.dumps(persons, indent=4)
    print("person = " + personJson)