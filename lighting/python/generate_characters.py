#!/usr/bin/env python

"""
comments go here
"""

from R2LightEngine import R2LightEngine
from R2ErrorClass  import R2Error
import glob
import sys

def main():

    print "Initializing character objects..."

    try:

        lightEngine = R2LightEngine()

        if len(sys.argv) == 2:

            print "Reading {}\n".format(sys.argv[1])
            ledObj = lightEngine.loadJson(sys.argv[1])
            print "{}\n".format(ledObj)

        else:

            #parse through the json directories to get all the character files
            for dir in ["../json/text","../json/numbers","../json/custom"]:
                #build lists of any json extension files
                fileList = glob.glob("{}/*.json".format(dir))
                #basic ascii sort
                fileList.sort()
                #create object for each json file
                for file in fileList:
                    ledObj = lightEngine.loadJson(file)
                    print "{}\n".format(ledObj)

    except R2Error as e:
        print e.value
                
if __name__ == '__main__':

    main();
