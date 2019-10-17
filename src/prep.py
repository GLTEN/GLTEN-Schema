"""@package prep.py
Created on 11 June 2019

@author: castells
@description: Prepare the staging area. 

Define your staging main folder in settings.py 
When this is ran, it prepares a staging area with all the folders for each experiment. 
It also prepares the experiments.json file and places it in the default directory.

When it is ran again, only newly created experiment folders are added. 
Folders are not removed. 

If a new structure is needed, we may want to rebuild a  new staging area and rerun the programs

The staging area is a metadata folder with a folder per experiment.

This uses the mssql database to make the relevant folders. A json string is not generated. 
"""

import pyodbc
import json
import settings
import os
import stat
import sys 
import configparser
"""
def connect():
    
    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=U:\website development\accessTools\timeline.accdb;')    
    return conn
"""
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

class Expt:
    """The class that will define an experiment and we can use that to make the folder. The row is the result of a query in the table
    
    SELECT Experiments.[ExptCode], Experiments.Experiment, Experiments.KeyRefCode, Experiments.type, Experiments.[exp-ID]
    FROM Experiments
    WHERE ((Not (Experiments.type)="Other"))
    ORDER BY Experiments.Experiment;
    """
    def __init__(self, row):      
        self.Experiment = row.experiment_name 
        self.exptID = ''.join(ch for ch in row.experiment_code if ch.isalnum()).lower() 
        
    def asExptJson(self):
        expt =  {
              "Experiment": self.Experiment,
              "Expt-Code": self.exptID        
            }        
        return expt
    def mkExptDir(self):
        status = " created"
        newDir = settings.STAGE+'metadata/'+self.exptID
        if not os.path.isdir(newDir):
            os.makedirs(newDir,  exist_ok = True)
            os.chmod(newDir, stat.S_IRWXO)
            status = " created"
        else: 
            os.chmod(newDir, stat.S_IRWXO)
            status = " here"
        return newDir + status
            

def getExperiments():
    """This gets the experiments. We only need experiments and farms
    
    SELECT Experiments.[Expt-Code], Experiments.Experiment, Experiments.KeyRefCode, Experiments.type, Experiments.[exp-ID]
    FROM Experiments
    WHERE ((Not (Experiments.type)="Other"))
    ORDER BY Experiments.Experiment;

    """
    cur = getCursor()

    sql = f'Select * from experiment where GLTENID >0 '
    cur.execute(sql)
    results = cur.fetchall() 
    return results 

def makeJSON(results):
    expts =  []   
    for row in results: 
        ex = Expt(row)        
        expts.append(ex.asExptJson())  
    return expts

def makedirectories(results):  
    testString = ""
    for row in results: 
        ex = Expt(row)        
        testString += ex.mkExptDir() + '\n'
    return testString

if __name__ == '__main__':

    results = getExperiments()
    expts = makeJSON(results)
    strJsonExpts =  json.dumps(expts, indent=4)
    dirs = makedirectories(results)    
    print(strJsonExpts)
    print ("-----Directory Creation-----")
    print(dirs)
    
    #xname = settings.STAGE+settings.DEFAULT+'experiments.json'    
    #fxname = open(xname,'w+')
    #fxname.write(strJsonExpts)
    #fxname.close()
    #print('Experiment file saved in '+xname)

