from R2ErrorClass import R2Error

class R2Phrase(object):

    def __init__(self,displaySize="large",appObj=None):

        self.displaySize = displaySize
        self.points      = None
        self.length      = 0

    def append(self,ledChar):

        self.length = self.length+ledChar.length

        if self.points:
            for idx in range(0,len(ledChar.points)):
                for idx2 in range(0,len(ledChar._colorData[idx])):
                    self.points[idx].append(ledChar._colorData[idx][idx2])
        else:
            self.points = ledChar._colorData 

        #for idx in range(ledChar.height-1,-1,-1):

    def __str__(self):

        point_string = ""

        for point_set in self.points:
            point_string = "{}{}\n\n".format(point_string,point_set)

        return "{}\n{}".format(repr(self),point_string)

