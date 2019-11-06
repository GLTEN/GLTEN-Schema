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
#from pygments.lexers import sql
import rest

def prepareTOC(GLTENIDs):
    '''experiment_name = row.experiment_name,
            folder = row.experiment_code.replace('/','').lower(),
            GLTENID = row.GLTENID
            '''
    TOC = []
    for ID in GLTENIDs:
        TOC.append(dict(
            exptID= ID['folder'],
            Title= ID['experiment_name'],
            station = ID['folder'][0]                        
            ))
    return TOC

def process(exptID):
    data = rest.getData(exptID)
    if data != ' - ':
        for items in GLTENIDs:
            if items['GLTENID']== exptID:
                folder = items['folder']
      
        print(folder)
        
        experiment = rest.prepareExperiment(data) 
        experimentJson =  json.dumps(experiment, indent=4)
        xname = settings.STAGE+ "metadata/"+str(folder)+"/experiment.json"
        fxname = open(xname,'w+')
        fxname.write(experimentJson)
        fxname.close()
        print("experiment.json saved in  = " + xname)
          
        site = rest.prepareSite(data)
        siteJson =  json.dumps(site, indent=4)
        xname = settings.STAGE+ "metadata/"+str(folder)+"/site.json"
        fxname = open(xname,'w+')
        fxname.write(siteJson)
        fxname.close()
        print("site.json saved in  = " + xname)
        
           
        persons = dict (contributors = rest.preparePersons(data))
        personJson =  json.dumps(persons, indent=4)
        xname = settings.STAGE+ "metadata/"+str(folder)+"/person.json"
        fxname = open(xname,'w+')
        fxname.write(personJson)
        fxname.close()
        print("person.json saved in  = " + xname) 
        
        design = rest.prepareDesigns(data)
        designsJson = json.dumps(design, indent=4)
        xname = settings.STAGE+ "metadata/"+str(folder)+"/design.json"
        fxname = open(xname,'w+')
        fxname.write(designsJson)
        fxname.close()
        print("design.json saved in  = " + xname) 
        
        orgs = rest.prepareOrganization(data)
        orgsJson = json.dumps(orgs, indent=4)
        xname = settings.STAGE+ "metadata/"+str(folder)+"/orgs.json"
        fxname = open(xname,'w+')
        fxname.write(orgsJson)
        fxname.close()
        print("orgs.json saved in  = " + xname)
    else: 
        print('DATA NOT READY') 
 
if __name__ == '__main__':
    
  
    GLTENIDs = rest.getGLTENIDs()
    TOC = prepareTOC(GLTENIDs)
    TOCJson = json.dumps(TOC, indent=4)
    xname = settings.STAGE+ "metadata/default/experiments.json"
    fxname = open(xname,'w+')
    fxname.write(TOCJson)
    fxname.close()
    print("experiments.json saved in  = " + xname)
    
    IDs = []
         
    for items in GLTENIDs:
        print (" %s (%s) GLTENID =  %s" % (items['experiment_name'],items['folder'], items['GLTENID']))
        exptID = items['GLTENID']
        print(exptID)
        process(exptID)
        print('\n')
