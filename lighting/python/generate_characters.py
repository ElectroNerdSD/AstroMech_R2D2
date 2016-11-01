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

def load_json(lightEngine,json_filename="../json/numbers/1.json"):

    try:

        points = []
        name   = None
        type   = None
        value  = None
        height = 0
        length = 0

        #load the json file
        for item in json.load(open(json_filename)):

            if item.has_key("info"):
                if "name" in item['info']:
                    name = item['info']['name']
                if "type" in item['info']:
                    type = item['info']['type']
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

        print "name {} : type {} : value {} : height {} : length {} : points {}".format(name,type,value,height,length,points)
        

    except:

        print "FRACK\n";

def main():
    print "Initializing character objects..."
    lightEngine = R2LightEngine()
    load_json(lightEngine)

if __name__ == '__main__':

    main();
