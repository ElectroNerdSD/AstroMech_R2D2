from R2ErrorClass import R2Error
from R2LEDCharacterClass import R2LEDCharacter

import sys

try:
    import json
except ImportError:
    import simplejson as json

class R2LightEngine(object):

    def __init__(self,appObject=None):

        self.R2AppObject = appObject
        self._data       = {}

    def buildCharacter(self,name,char_type,tag,value,height,length,points,json_filename):

        try:
            ledChar = R2LEDCharacter(name,char_type,tag,value,height,length,points,json_filename,self.R2AppObject)
            return(ledChar)

        except R2Error as e:
            raise(e)

    def loadJson(self,json_filename="../json/text/A.json"):

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
                    pass

            self.buildCharacter(name,char_type,tag,value,height,length,points,json_filename)
            return(self.buildCharacter(name,char_type,tag,value,height,length,points,json_filename))

        except R2Error as e :

            raise e

        except: 

            raise R2Error("ERROR: {},while reading {}".format(sys.exc_info()[0],json_filename))

