#!/usr/bin/env python

"""
    Script to generate led character objects from each json file.
    No cli argument, results in all objects created, pass in single json 
    file as first argument and that file will be loaded individually.
"""

import glob
import sys
import os
from R2LightEngine import R2LightEngine
from R2ErrorClass  import R2Error

def main():

    json_dir = "{}/../json/".format(os.path.abspath(os.path.dirname(__file__)))
    print "Initializing character objects from {}...".format(json_dir)

    try:

        lightEngine = R2LightEngine()

        if len(sys.argv) == 2:

            print "Reading {}\n".format(sys.argv[1])
            ledObj = lightEngine.loadJson(sys.argv[1])
            print "{}\n".format(ledObj)

        else:

            #parse through the json directories to get all the character files
            for dir_name in ["text", "numbers", "custom"]:
                #build lists of any json extension files
                fileList = glob.glob("{}/{}/*.json".format(json_dir, dir_name))
                #basic ascii sort
                fileList.sort()
                #create object for each json file
                for file_name in fileList:
                    ledObj = lightEngine.loadJson(file_name)
                    print "{}\n".format(ledObj)

    except R2Error as e:
        print e.value

if __name__ == '__main__':

    main()
