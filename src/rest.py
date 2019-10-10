'''
Created on 1 Oct 2019
This tests the fact that I can use rest to interrogate GLTEN and return their json string

@author: castells

@TODO: colect the IDs that come from GLTN so that I can get the labels from there. 
'''
import pyodbc
import requests
import settings
import configparser
import json
from pygments.lexers import sql

class APIError(Exception):
    """An API Error Exception"""

    def __init__(self, status):
        self.status = status

    def __str__(self):
        return "APIError: status={}".format(self.status)
    
def connect():
    config = configparser.ConfigParser()
    config.read('config.ini')
    dsn=config['SQL_SERVER']['DSN']
    uid = config['SQL_SERVER']['UID']
    pwd = config['SQL_SERVER']['PWD']
    con = pyodbc.connect('DSN='+dsn+';uid='+uid+';pwd='+pwd)
    #con = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=Z:\website development\datacite\DataCite Metadata database.accdb;')
    #con = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:\code\access\DataCite Metadata database.accdb;')
    return con


def getCursor():
    """Returns a new Cursor object using the connection"""
    con = connect()
    cur = con.cursor()
    return cur


def getGLTENIDs():
    """
    Returns a dictionary with all the timelines. This is then printed to offer use the choice
    """
    cur = getCursor()
    GLTENIDs = []
    sql = 'SELECT  experiment_name, experiment_code,  GLTENID FROM experiment where GLTENID is not null;'
    cur.execute(sql)
    results = cur.fetchall()    
    for row in results: 

        GLTENIDs.append(dict(
            experiment_name = row.experiment_name,
            folder = row.experiment_code.replace('/','').lower(),
            GLTENID = row.GLTENID
            ))
           
    return GLTENIDs

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

def prepareRelatedExperiments(REdata):
    
    relatedExperiments = []
    if REdata:
        for detailRE in REdata:
            relatedExperiments.append(dict(
                type= "Experiment",
                identifier= "10.23637/Sax-rrn2-1 - that would be the DOI - Unique Identifier",
                localIdentifier= "rrn2 - Use the code for the experiment - Local Identifier",
                name= "Saxmundahm Rotation 2"
                ))
    else: 
        relatedExperiments = "NA"
    return relatedExperiments

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
        #relatedExperiment= prepareRelatedExperiments(data['related_experiments'])
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
#             address= dict(
#                 type= "PostalAddress",
#                 streetAddress= "not in GLTEN",
#                 addressLocality= "not in GLTEN",
#                 addressRegion= "not in GLTEN",
#                 postalCode= "not in GLTEN",
#                 addressCountry= "not in GLTEN"
#             ),
            affiliation= dict (
                type= "Organization",
                name= "Computational and Analytical Sciences, Rothamsted Research",
                address= ", West Common, Harpenden, Hertfordshire, AL5 2JQ, United Kingdom"
            )
            )
                            )
    return contributors

def prepareLevel(leveldata):
    levels = []
    for leveldetails in leveldata:
        levels.append(dict(
            id= leveldetails['id'],
            name= leveldetails['factor_variant_label'],
                        amount= leveldetails['amount'],
                        unitCode= leveldetails['amount_unit_term'],
                        unitText= leveldetails['amount_unit_label'],
                        appliedToCrop= leveldetails['crop_id'],
                        dateStart= leveldetails['start_year'],
                        dateEnd= leveldetails['end_year'],
                        frequency= leveldetails['application_frequency'],
                        method= leveldetails['application_method_label'],
                        chemicalForm= leveldetails['chemical_form_label'],
                        notes= leveldetails['note']
            ))
    return levels

def prepareFactors(factordata):
    factors = []
    
    for factordetails in factordata:
        factors.append(dict(
            id= factordetails['id'],
            name =  factordetails['factor_term'],                 
            description = factordetails['description'],
            effect= factordetails['effect'],                 
            plotApplication= factordetails['factor_term'],
            level= prepareLevel(factordetails['levels'])             
     ))
    return factors

def prepareFCFactors (FCFactorData, factordata):
    FCFactors = []
    for FCFDetails in FCFactorData:
        for item in factordata:            
            if item['id']==FCFDetails['factor_id']:
                factorName = item['factor_term']
                for levelitems in item['levels']:                    
                    if levelitems['id'] == FCFDetails['factor_level_id']:
                        levelNameText = levelitems['factor_variant_term']  
                        levelNameCode =  levelitems['factor_variant_label']             
                
        FCFactors.append(dict(
            Factor= factorName,
            levelCode= levelNameCode,
            levelText = levelNameText,
            Comment= FCFDetails['comment']
            ))
    return FCFactors
    
def prepareFactorCombinations(factorcombinationData, factordata):
    factorCombinations = []
    if factorcombinationData:
        for FCDetails in factorcombinationData:
            preparedfactor= prepareFCFactors(FCDetails['members'],factordata) if FCDetails['members'] else "NA"
            factorCombinations.append(dict(
                name= FCDetails['name'],
                    dateStart= FCDetails['start_year'],
                    dateEnd= FCDetails['end_year'],
                    description= FCDetails['description'],
                    factor= preparedfactor 
            ))
    return factorCombinations

def prepareCrops(cropData):
    crops = []
    for detailCrop in cropData:
        crops.append(dict(
            name= detailCrop['crop_term'],
                #identifier= detailCrop['crop_term'],
                #sameAs= detailCrop['crop_label'],
                dateStart= detailCrop['start_year'],
                dateEnd= detailCrop['end_year']
            ))
    return crops

def preparePhases(phaseData):
    phases = []
    for phaseDetail in phaseData:
        phases.append(dict(
            samePhase= phaseDetail['same_phase'],
            crop= phaseDetail['crop_id'],
            description= phaseDetail['notes']
            ))
    return phases

def prepareCropRotations(rotationdata):
    rotations = []
    for detailRotation in rotationdata:
        preparedrotationPhases=preparePhases(detailRotation['phases']) if detailRotation['phases'] else "Not in GLTEN"
        rotations.append(dict(
            name= detailRotation['name'],
                dateStart= detailRotation['start_year'],
                dateEnd= detailRotation['end_year'],
                phasing= detailRotation['phasing'],
                isTreatment= detailRotation['is_treatment'],
                rotationPhases= preparedrotationPhases
            ))
    return rotations
def prepareMeasurements(measurementData):
    measurements = []
    for detailMeasurements in measurementData:
        measurements.append(dict(
            variable= detailMeasurements['variable_term'],
            unitCode= detailMeasurements['unit_term'],
            unitText= detailMeasurements['unit_label'],
            collectionFrequency= detailMeasurements['collection_frequency'],
            scale= detailMeasurements['scale'],
            material= detailMeasurements['material'],
            description= detailMeasurements['comment'],
            crop = detailMeasurements['crop_id']
        ))
    return measurements

def prepareDesigns(data):
    designs = []
    item = 0
    for details in data['periods']:
        preparedcrops = prepareCrops(details['crops']) if details['crops'] else "NA"
        preparedcropRotations = prepareCropRotations(details['rotations']) if details['rotations'] else "NA"
        preparedfactor = prepareFactors(details['factors']) if details['factors'] else "NA"
        preparedfactorCombinations = prepareFactorCombinations(details['factor_combinations'],details['factors']) if details['factor_combinations'] else "NA"
        preparedmeasurements = prepareMeasurements(details['measurements']) if details['measurements'] else "NA"
        
        designs.append(dict ( 
            administrative= dict( 
            type= "experiment",
            identifier= details['name'],
            localIdentifier= details['name'],
            name= details['name'],
            url= details['name'],
            description= str(details['design_description']) if details['design_description'] else ''  + str(details['description']) if details['description'] else ''
        ),
        design= dict( 
            dateStart= details['start_year'],
            dateEnd= details['end_year'],
            description= details['description'],
            studyDesign= details['name'],
            factorNumber= details['name'],
            numberOdBlocks = details['number_of_blocks'],
            numberOfPlots= details['number_of_plots'],
            numberOfReplicates= details['number_of_replicates'],
            numberOfSubplots= details['number_of_subplots'],            
#             area= "Experiment area",
#             areaUnit= "Experiment area units",
#             plotWidth= "Plot width",
#             plotWidthUnit= "Plot width Unit",
#             plotLength= "Plot length",
#             plotLengthUnit= "Plot length Unit",
#             plotArea= "Plot area",
#             plotAreaUnit= "Plot area Unit",
#             plotSpacing= "Plot spacing",
#             plotSpacingUnit= "Plot spacing Unit",
#             plotOrientation= "Plot orientation",
#             numberHarvest= "Number of harvests per year"
        ),
        crops = preparedcrops,
        cropRotations = preparedcropRotations,
        factor = preparedfactor,
        factorCombinations = preparedfactorCombinations,
        measurements = preparedmeasurements
        
        )
            )
        
        item += 1
    return designs

def process(exptID):
    data = getData(exptID)
    
    for items in GLTENIDs:
        if items['GLTENID']== exptID:
            folder = items['folder']
  
    print(folder)
    
    experiment = prepareExperiment(data) 
    experimentJson =  json.dumps(experiment, indent=4)
    xname = settings.STAGE+ "metadata/"+str(folder)+"/experiment.json"
    fxname = open(xname,'w+')
    fxname.write(experimentJson)
    fxname.close()
    print("experiment.json saved in  = " + xname)
      
    site = prepareSite(data)
    siteJson =  json.dumps(site, indent=4)
    xname = settings.STAGE+ "metadata/"+str(folder)+"/site.json"
    fxname = open(xname,'w+')
    fxname.write(siteJson)
    fxname.close()
    print("site.json saved in  = " + xname)
    
       
    persons = dict (contributors = preparePersons(data))
    personJson =  json.dumps(persons, indent=4)
    xname = settings.STAGE+ "metadata/"+str(folder)+"/person.json"
    fxname = open(xname,'w+')
    fxname.write(personJson)
    fxname.close()
    print("person.json saved in  = " + xname) 
    
    design = prepareDesigns(data)
    designsJson = json.dumps(design, indent=4)
    xname = settings.STAGE+ "metadata/"+str(folder)+"/design.json"
    fxname = open(xname,'w+')
    fxname.write(designsJson)
    fxname.close()
    print("design.json saved in  = " + xname) 


if __name__ == '__main__':
    
    while True:
        exptID = 0
    
        GLTENIDs = getGLTENIDs()
        IDs = []
          
        for items in GLTENIDs:
            print (" %s (%s) GLTENID =  %s" % (items['experiment_name'],items['folder'], items['GLTENID']))
            IDs.append(items['GLTENID'])
        
        print(IDs)
        print('\n')
    
    
        while exptID == 0:
            val = input('Which experiment GLTENID? ')
            try: 
                exptID = int(val)
                if exptID  not in IDs:
                    print("not in the list")
                    exptID = 0
            except ValueError:
                print("No.. input string is not an Integer. It's a string")
      
        process(exptID)
        new_game = input("Would you like to do another one? Enter 'y' or 'n' ")
        if new_game[0].lower()=='y':
            playing=True
            continue
        else:
            print("Thanks for your work!")
            break
        
    