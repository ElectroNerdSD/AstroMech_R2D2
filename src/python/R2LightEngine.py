from R2ErrorClass import R2Error
from R2LEDCharacterClass import R2LEDCharacter
from R2PhraseClass import R2Phrase

import re
import sys

try:
    import json
except ImportError:
    import simplejson as json

class R2LightEngine(object):

    def __init__(self,appObject=None):

        self.R2AppObject = appObject
        self._ledData    = {}
        self._phrases    = {}
        self._minHeight  = 5   #height all characters must be

    def buildCharacter(self,name,char_type,tag,value,height,length,points,json_filename):

        try:

            #build a led character object for each json file
            ledChar = R2LEDCharacter(name,char_type,tag,value,height,length,points,json_filename,self.R2AppObject)

            if ledChar.char_type == "custom":
                lookup = ledChar.tag
            else:
                lookup = ledChar.value

            #check to make sure a object with same look up doesn't already exist
            if self._ledData.has_key(lookup):
                raise R2Error("ERROR: It appears json file {} contains a duplicate value/tag entry, please check the other json files for value or tag \"{}\".".format(ledChar.name,lookup))
            elif ledChar.height != self._minHeight:
                raise R2Error("ERROR: It appears json entry {} doesn't meet the min height requirement, please check the json file.".format(ledChar.name))
            else:
                #store the objects for later
                self._ledData[lookup]=ledChar

            return(ledChar)

        except R2Error as e:
            raise(e)

    def buildMessageObjects(self,messageString="<tag:left_arrow> <tag:heart> HELLO WORLD <tag:heart> <tag:right_arrow>",displayName="rearLogic",onColor=(255, 0 , 0 ),offColor=( 0 , 0 , 0 ),keepColor=True):

        #replace all white space with tag for space
        whiteSpace = re.compile(r'\s')
        messageString = whiteSpace.sub("<tag:space>",messageString)

        #regex to break up letters and capture custom tags
        lookupRegex = re.compile(r'([A-Z0-9])|<tag:\s*(\w+)\s*>')
        matchList = lookupRegex.findall(messageString)

        if displayName == "rearLogic":
            displaySize = "large"
        elif displayName == "frontLogicUpper" or displayName == "frontLogicLower":
            displaySize = "small"
        else:
            raise R2Error("ERROR: display size, for display named {} for buildMessageObject not support".format(displayName))

        phraseObj = R2Phrase(displaySize,self.R2AppObject)

        #what size logic display are we using
        if displaySize=="large":
            blank = self._ledData['large_blank']
        elif displaySize=="small":
            blank = self._ledData['small_blank']
        else:
            pass

        #add the blank at front of display
        blank.processPoints(onColor,offColor,keepColor)
        phraseObj.append(blank)

        for tag in matchList:

            try:
                if len(tag[0]):
                    ledChar = self._ledData[tag[0]]
                elif len(tag[1]):
                    ledChar = self._ledData[tag[1]]
                else:
                    pass

                #fill the matrix with colors, if needed
                ledChar.processPoints(onColor,offColor,keepColor)

            except KeyError as e:
                raise R2Error("ERROR: It appears json files are missing a character for tag: {}.\n".format(e))

            #create a list of led objects that contain the message
            phraseObj.append(ledChar)

        self._phrases[displayName] = phraseObj

        return(phraseObj)

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

            return(self.buildCharacter(name,char_type,tag,value,height,length,points,json_filename))

        except R2Error as e :

            raise(e)

        except: 

            raise R2Error("ERROR: {},while reading {}".format(sys.exc_info()[0],json_filename))

