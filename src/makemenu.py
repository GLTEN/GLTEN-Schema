'''
Created on 6 Nov 2019

@author: castells
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

def prepareTOCphp(TOC):
    php = ''
    stations = ['Rothamsted', 'Broom\s Barn', 'Saxmundham', 'Woburn']
    for station in stations:
        
        php += '\n<li class="col-md-3 dropdown-item">'
        php += '\n\t<ul>'
        php += '\n\t\t<li class="dropdown-header">'
        php += '\n\t\t\t<a href="farm.php?farm={0}">{0}</a>\n\t\t</li>'.format(station)
        for expt in TOC:
            if expt['station']== station[0].lower():
                title = expt['Title'].replace (station, '')
                title = title.replace('-', '')
                title = title.replace('  ',' ')
                php += '\n\t\t<li><a href="expt.php?expt={0}">{1}</a></li>'.format(expt['exptID'], title)
#             if expt['station'][0].lower() == station[0].lower():
#                 php += '<li><a href="expt.php?expt={0}">{1}</a></li>'.format(expt['exptID'], expt['Title'])
            
        php += '\n\t</ul>\n</li>\n'
    return php

if __name__ == '__main__':
    GLTENIDs = rest.getGLTENIDs()
    TOC = prepareTOC(GLTENIDs)
    TOCJson = json.dumps(TOC, indent=4)
    xname = settings.STAGE+ "metadata/default/experiments.json"
    fxname = open(xname,'w+')
    fxname.write(TOCJson)
    fxname.close()
    print("experiments.json saved in  = " + xname)
    phpstr = prepareTOCphp(TOC)
    print(phpstr)
    