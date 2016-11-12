from R2ErrorClass import R2Error
from types import IntType
import re

class R2LEDCharacter(object):

    def __init__(self,name,char_type,value,height,length,points,json_filename,appObj=None):

        #do some basic error checks
        if name is None:
            raise R2Error("ERROR: \"name\" entry in {} is not defined properly or is missing.".format(json_filename))
        if char_type is None:
            raise R2Error("ERROR: \"char_type\"  entry in {} is not defined properly or is missing.".format(json_filename))
        if value is None:
            raise R2Error("ERROR: \"value\"  entry in {} is not defined properly or is missing.".format(json_filename))
        if height is None:
            raise R2Error("ERROR: \"height\"  entry in {} is not defined properly or is missing.".format(json_filename))
        if length is None:
            raise R2Error("ERROR: \"length\"  entry in {} is not defined properly or is missing.".format(json_filename))
        if len(points) == 0:
            raise R2Error("ERROR: \"points\"  entry in {} is not defined properly, doesn't seem to have a list of points or is missing.".format(json_filename))
        if len(points) != height:
            raise R2Error("ERROR: \"points\"  entry in {} is not defined properly, should have a height of {} but is {} items high.".format(json_filename,height,len(points)))

        for point_set in points:
            if len(point_set) != length:
                raise R2Error("ERROR: \"points\" set {} in {} should be {} items long.".format(point_set,json_filename,length))
            for point in point_set:
                if (type(point) != IntType) or  (point < 0  or point >1):
                    raise R2Error("ERROR: \"points\" set {} in {} should only contain integers 0 or 1.".format(point_set,json_filename))
                else:
                    print "{}".format(type(point)==IntType)

        self.name      = name
        self.char_type = char_type
        self.value     = value
        self.height    = height
        self.length    = length
        self.points    = points
        self.json      = json_filename

    def __str__(self):
        for point_set in self.points:
            print "{}".format(point_set)
        return repr(self)

