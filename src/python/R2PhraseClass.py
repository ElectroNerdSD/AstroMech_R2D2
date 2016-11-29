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
                for idx2 in range(0,len(ledChar.points[idx])):
                    self.points[idx].append(ledChar.points[idx][idx2])
        else:
            self.points = ledChar._colorData 

        #for idx in range(ledChar.height-1,-1,-1):

    def __str__(self):

        char_string = ""

        for point_set in self.points:
            point_string = ""
            for point in point_set:
                point_string = "{}{}".format(point_string,"*" if point==1 else " ")
            char_string = "{}\t\t{}\t\t{}\n".format(char_string,point_set,point_string)

        return "{}\n\tname :{}\n\ttag  : {}\n\tfile :{}\n\tvalue:\n{}".format(repr(self),self.name,self.tag,self.json,char_string)

