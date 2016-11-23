#!/usr/bin/env python

"""
    Script to simulate led character objects from each json file.
    No cli argument, results in test string "HELLO WORLD", pass in a custom
    string to be evaluated as argument.
"""

import glob
import sys
import os
from pprint import pprint
from R2LightEngine import R2LightEngine
from R2ErrorClass  import R2Error

def main():

    json_dir = "{}/../json/".format(os.path.abspath(os.path.dirname(__file__)))

    try:

        #create the lighting engine
        lightEngine = R2LightEngine()

        #parse through the json directories to get all the character files
        for dir_name in ["text", "numbers", "custom"]:
            #build lists of any json extension files
            fileList = glob.glob("{}/{}/*.json".format(json_dir, dir_name))
            #basic ascii sort
            fileList.sort()
            #create object for each json file
            for file_name in fileList:
                ledObj = lightEngine.loadJson(file_name)

        #hello world
        ledArray = lightEngine.buildString()

    except R2Error as e:
        print e.value

if __name__ == '__main__':

    main()
