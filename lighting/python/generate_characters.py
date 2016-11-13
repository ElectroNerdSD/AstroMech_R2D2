#!/usr/bin/env python

"""
comments go here
"""

from R2LightEngine import R2LightEngine
from R2ErrorClass  import R2Error

try:
    import json
except ImportError:
    import simplejson as json

def load_json(lightEngine,json_filename="../json/text/P.json"):

    try:

        points    = []
        name      = None
        char_type = None
        tag       = None
        value     = None
        height    = 0
        length    = 0

        #load the json file
        for item in json.load(open(json_filename)):

            if item.has_key("info"):
                if "name" in item['info']:
                    name = item['info']['name']
                if "type" in item['info']:
                    char_type = item['info']['type']
                if "tag" in item['info']:
                    tag = item['info']['tag']
                if "value" in item['info']:
                    value = item['info']['value']

            elif item.has_key("points"):

                mytup = tuple(item['points'])
                tuplen = len(mytup)
                if(tuplen>length):
                    length = tuplen
                points.append(mytup)

                #increase the height
                height = height+1

            else:
                print "error: item has bad key\n"

        lightEngine.buildCharacter(name,char_type,tag,value,height,length,points,json_filename)
        ledObj = lightEngine.buildCharacter(name,char_type,tag,value,height,length,points,json_filename)
        print "{}\n".format(ledObj)
        

    except R2Error as e :

        print "{}\n".format(e.value);

def main():
    print "Initializing character objects..."
    lightEngine = R2LightEngine()
    load_json(lightEngine)

if __name__ == '__main__':

    main();
