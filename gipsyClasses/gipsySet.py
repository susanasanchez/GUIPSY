import gipsy
from gipsy import *

import sys
import math
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from xreverse import *

from new_exceptions import *
from general import *

GIPSYLOG="./GIPSY.LOG"
HEADER_TMP="./header.tmp"



#def calculateMNMX(setname):
#    command="MNMX INSET=%s;"%(setname)
#    id=newId()
#    #notifykey = 'TASKCOMX'+unicode(id)+'='
#    try:
#        xeq(command) 
#    except XeqError:
#        raise gipsyException("%s \n Gets an error "%(command))
#        return
#    else:
#        #output="gipsy.xeq(\""+command+"\",\""+notifykey+"\")\n"
#        output="gipsy.xeq(\""+command+"\")"
#        
#    return output
    
class gipsySet(object):
    ''' This class implements the interface between gipsy software and the application.
    
    **Attributes**
    
    
    fitsname : String
        The pathname of the fits file, if the set is builded from a fits file
    setname : String
        The pathname of the set without the extension .image or .descr
    filename : String
        The pathname of the set with the extension .image
    varname : String
        The pathname of the set used in the log sentence. It is composed by setname and a counter in order
        to avoid repetitions of setname in the workflow text.
    history : String
        History text of the set
    properties : String
        Properties text of the set
    __S : gipsySet
        An instance of Set class of gipsy package
    
    '''

    
        

    def __init__(self):
       
        self.fitsname= ""
        self.setname= ""
        self.filename= ""
        self.varname=""
        self.properties=""
        self.history=""
        self.comments=""
        self.__S= None
        self.tables=None
        self.cnt=counter()

#    def loadSet(self,setname,fitsname=None):
    def loadSet(self,setname):
        """Read the set. If the set is in a fits file, build the corresponding set.When it gets a XeqError exception raises a gipsyException with a
            properly message
    
        **Returns:**
            output (str) Python sentences with the executed task
        
        **Raises:**
            gipsyException
            
        """
       
        output=""   
        self.setname=unicode(setname)
        self.filename=self.setname
  
        #output=output+calculateMNMX(setname)
        try:
            self.__S=Set(self.setname, create=False, write=True, gethdu=None, getalt=None)
        except GdsError as g:
                 raise gipsyException("Couldn't create a set instance:\n %s"%(unicode(g)))
                 return
        #Getting the tables
        #self.tables = self.__S.tablis()
        maxtables = 200
        attempts = 0
        while attempts >= 0:
            try:   
                tablist = self.__S.tablis(nitems=maxtables)
                attempts = -1
            except:
                maxtables += maxtables/2
                attempts += 1
        self.tables=tablist
        #Choosing a good variable name for the workflow log
        c=self.cnt()
        #The variable name should not contain -
        self.varname=os.path.basename(self.setname).replace("-", "_")+unicode(c)
        #self.varname=os.path.basename(self.setname)+unicode(c)

        
        output = output+"%s = gipsy.Set(\"%s\", create=False, write=True, gethdu=None, getalt=None)"%(self.varname,  self.setname)+"\n"
        
        
        return output
 
    
    def loadSetRO(self, setPath):
        self.setname=unicode(setPath)
        self.filename=setPath
       
        try:
            self.__S=Set(self.setname, create=False, write=False, gethdu=None, getalt=None)
        except GdsError as g:
            raise gipsyException("Couldn't create a set instance:\n %s"%(unicode(g)))
            return
       

        #Getting the tables
        #self.tables = self.__S.tablis()
        maxtables = 200
        attempts = 0
        while attempts >= 0:
            try:   
                tablist = self.__S.tablis(nitems=maxtables)
                attempts = -1
            except:
                maxtables += maxtables/2
                attempts += 1
        self.tables=tablist
        
    def deleteSet(self):
        """Delete the set. If it gets a XeqError exception raises a gipsyException with a
            properly message
        
        **Returns:**
            output (str) :  Python sentences with the executed task
        
        **Raises:**
            gipsyException
            
        
        """
        
        try:
            self.__S.delete()
        except GdsError as g:
            raise gipsyException("Couldn't delete the set:\n %s"%(unicode(g)))
            return
        else:
            output="%s.delete()\n"%(self.varname)
            return output
            
    
    def deleteSetFromFile(self, setPath):
        self.setname=unicode(setPath)
        self.filename=setPath
       
        try:
            self.__S=Set(self.setname, create=False, write=False, gethdu=None, getalt=None)
        except GdsError as g:
            raise gipsyException("Couldn't create a set instance:\n %s"%(unicode(g)))
            return
        
        try:
            self.__S.delete()
        except GdsError as g:
            raise gipsyException("Couldn't delete the set:\n %s"%(unicode(g)))
            return
            
            
    def getProperties(self):
        """Get the properties text of the set reading and parsing the gipsy log file, just after run HEADER task. If it gets a XeqError exception raises a gipsyException with a
            properly message
        
        **Raises:**
            gipsyException
           
        
        """
        if(self.properties!=""):
            return self.properties
        elif( self.setname!=None):
            try:
                xeq("HEADER INSET=%s MODE=AF FILENAME=%s"%(self.setname,HEADER_TMP))
            except XeqError as x:
                raise gipsyException("%s: HEADER error %s"%(self.setname, unicode(x)))
                return
            try:
                f=open(HEADER_TMP,"r")
            except:
                raise gipsyException("Unable to read header temporary file created by HEADER task")
                return
        tmp=f.read()
        parts=tmp.split("********************************************************************************")
        if len(parts)>2:
            self.properties=parts[1]+"\n********************************************************************************\n"+parts[0]
        else:
            self.properties=tmp
        f.close()
        os.remove(HEADER_TMP)
        
        return self.properties

            
    def getPropertiesModeG(self):
        """Get the properties text of the set reading and parsing the gipsy log file, just after run HEADER task. If it gets a XeqError exception raises a gipsyException with a
            properly message
        
        **Raises:**
            gipsyException
           
        
        """
        if(self.properties!=""):
            return self.properties
        elif( self.setname!=None):
            try:
                xeq("HEADER INSET=%s MODE=G FILENAME=%s"%(self.setname,HEADER_TMP))
            except XeqError as x:
                raise gipsyException("%s: HEADER error %s"%(self.setname, unicode(x)))
                return
            try:
                f=open(HEADER_TMP,"r")
            except:
                raise gipsyException("Unable to read header temporary file created by HEADER task")
                return
        tmp=f.read()
        parts=tmp.split("********************************************************************************")
        if len(parts)>2:
            self.properties=parts[1]+"\n********************************************************************************\n"+parts[0]
        else:
            self.properties=tmp
        f.close()
        os.remove(HEADER_TMP)
        
        return self.properties            
            
    def getHistory(self):
         """Get the history text of the set reading and parsing the gipsy log file, just after run HEADER task. When it gets a XeqError exception raises a gipsyException with a
            properly message
        
         **Raises:**
            gipsyException
            
        
         """
         if(self.history!=""):
            return self.history
         elif(self.setname!=None):
            try:
                xeq("HEADER INSET=%s"%(self.setname))
            except XeqError:
                raise gipsyException("%s: HEADER error"%(self.setname))
                return
            f = open(GIPSYLOG,"r")
            rev = [ line for line in xreverse(f) ]
            history="" 
            for line in rev:
                if line.startswith('='):
                    self.history=history
                    return history
                elif line.startswith("HISTORY"):
                    #skip 'history='
                    #begin=line.find('=') +1
                    #history=line[begin:].lstrip()+history
                    history=line+history
            f.close()

    def getComments(self):
         """Get the properties text of the set reading and parsing the gipsy log file, just after run HEADER task. When it gets a XeqError exception raises a gipsyException with a
            properly message
        
         **Raises:**
            gipsyException
            
         
         """
        
         if(self.comments!=""):
            return self.comments
         elif(self.setname!=None):
            try:
                xeq("HEADER INSET=%s"%(self.setname))
            except XeqError:
                raise gipsyException("%s: HEADER error"%(self.setname))
                return
            f = open(GIPSYLOG,"r")
            rev = [ line for line in xreverse(f) ]
            comments="" 
            for line in rev:
                if line.startswith('='):
                    self.comments=comments
                    return comments
                elif line.startswith("COMMENT"):
                    #skip 'comment='
                    begin=line.find('=') +1
                    comments=line[begin:].lstrip()+comments

    def updateComments(self, comments):
        """Update the comments of the set.
        
        **Parameters:**
            comments (str):  All the comments inserted by the user
            
        **Returns:**
            output (str): Python sentences with the executed task
            
        """
        
        output=""
        #update comments only if new comments are different from old
        if(self.comments!=comments):
            self.comments=comments
            self.__S[0,'COMMENT']=None
            output="%s[0,\'COMMENT\']=None\n"%(self.varname)
            
            listComments=comments.split("\n")
            for comment in listComments:
                if(comment!=""):
                    self.__S.wcomment(unicode(comment[:72]))
                    output=output+"%s.wcomment(\"%s\")\n"%(self.varname, comment[:72])
            
            self.__S.update()
            output=output+"%s.update()\n"%(self.varname)
        return output
        
    def getHeaderItems(self):
        """Returns the list of header items of the set
        
        **Returns:**
            __S.items: list
        
        """
        return self.__S.items(0)

    def getFilename(self):
        """Returns the pathname of the set with the extension .image
        
        **Returns:**
            filename (str)
            
        """
        return self.filename
    def getSetname(self):
        """Returns the pathname of the set without the extension .image
        
        **Returns:**
            setname (str)
            
        """
        return self.setname
    
    def getImageValue(self, ra, dec):
        """In case the set is a image (2D) returns the value corresponding to the given coordinate
        In other case it returns None
        
        **Returns:** 
            value (double)
            
        """
        lower=self.__S.slo
        sum_x=abs(lower[0])
        sum_y=abs(lower[1])
        
        shape=self.__S.image.shape
        if len(shape)==2:
            g = self.__S.togrid([ra, dec])
            x=g[0]+sum_x
            y=g[1]+sum_y
            
            #It seems the indexes in image arrary are INVERTED
            if x>=0 and y>=0 and shape[0]>y and shape[1]>x:
                value=self.__S.image[y][x]
                return value
            else:
                return None
        
        return None
    
    def getDistanceToCenter(self, ra, dec, centrex, centrey):
        """In case the set is a image (2D) returns the distance of the point to the center
        
        **Returns:** 
            value (double)
            
        """
        #The following lines convert the ra dec in grid coordinates, and calculate the distance of the point to the center of the grid
#        shape=self.__S.image.shape
#        if len(shape)==2:
#            g = self.__S.togrid([ra, dec])
#            x=g[0]
#            y=g[1]
#            value=math.sqrt((x**2)+(y**2))
#            return value

        #Since both points are in physical coordinates (degrees)
        value=math.sqrt(((ra-centrex)**2)+((dec-centrey)**2))
        #It is needed to convert the result to arcsec which are the units for RADII, ELLINT,RESWRI,GALMOD,VELFI
        return value*60*60

    def updateHeaderKey(self, key, val):
        """Update a header item
        
        **Parameters:**
        
            key (str): Name of the header item
            val (str): New value for the header item
            
        **Returns:**
            output (str): Python sentences with the executed task
  
        """
        output="val=\"%s\"\n"%val
        if(self.__S[0, key]!=val):
            #Find the type of the value
            
            try:
                val_cast=int(val)
            except:
                val_cast=val.replace("D", "E")
                try:
                    val_cast=float(val_cast)
                except:
                    try:
                        val_cast=str(val)
                    except UnicodeEncodeError as u:
                        raise u
                    else:
                        output=output+"val=str(val)\n"
                else:
                    output=output+"val=float(val.replace(\"D\",\"E\"))\n"
            else:
                output=output+"val=int(val)\n"
            try:
                self.__S[ 0, key]=val_cast
            except GdsError as g:
                raise gipsyException("Error updating %s header, value=%s key:\n%s"%(key, val, unicode(g)))
            else:
                self.__S.update()
                output=output+"%s[0,\'%s\']=val"%(self.varname, key)+"\n"+"%s.update()"%(self.varname)
        return output
        
    def deleteHeaderKey(self, key):
        """Delete a header item. When it gets a GDsError exception raises a gipsyException with a
            properly message
        
        **Parameters:**
            key (str): Name of the header item
            
        **Returns:** 
            output (str): Python sentences with the executed task
        
        **Raises:** 
            gipsyException
            
  
        """
        try:
            del self.__S[ 0, key]
        except GdsError:
            raise gipsyException("Error deleting %s header key"%key)
            return
        self.__S.update()
        output="del %s[0,\'%s\']"%(self.varname, key)+"\n"+"%s.update"%(self.varname)
        return output
    
    def newHeaderKey(self, key, val):
        """Add a new header item
        
        **Parameters:**
            key (str): Name of the new header item
            val (str): Value for the new header item
            
        **Returns:**
            output (str): Python sentences with the executed task
            
        """
        try:
            key=str(key)
            val=str(val)
        except UnicodeEncodeError as u:
            raise u
        else:
            self.__S[ 0, key]=val
            self.__S.update()
            output="%s[0,\'%s\']=%s"%(self.varname, key, val)+"\n"+"%s.update()"%(self.varname)
            return output

    def getInfo(self):
        """Returns information about dimensions and axes of the set.
        
        Returns
            output (str)
     
        """
        dim = self.__S.naxis
        output="Dimension: %s\n"%(dim)
        # Get coordinate words of first data point in set and of the last one
        lo, hi = self.__S.range(0)

        # Print the axis name and the range in grids for all the axes in the set
        for i in range(dim):
            output=output+"%s: from %d to %d\n" % (self.__S.axname(i), self.__S.grid(i, lo), self.__S.grid(i, hi))

        return output
    
    def getInfoAxes(self):
        
        dim = self.__S.naxis
        output=range(dim)
        # Get coordinate words of first data point in set and of the last one
        lo, hi = self.__S.range(0)
        # Print the axis name and the range in grids for all the axes in the set
        for i in range(dim):
            output[i]=(self.__S.axname(i),"%s %s"%(self.__S.grid(i, lo), self.__S.grid(i, hi)))
           
        return output
        
    def getAxes(self):
        output=[]
        dim = self.__S.naxis
        # Print the axis name and the range in grids for all the axes in the set
        for i in range(dim):
            output.append(self.__S.axname(i))
           
        return output
    
    def getThirdDimension(self):
        if self.__S.naxis >=3:
            return self.__S.axname(2)
        else:
            return self.__S.axname(self.__S.naxis-1)

    def getTablesInfo(self):
        tablesInfo=range(len(self.tables))
        i=0
        for tabl in self.tables:

            tablename = tabl[0]
            subset = tabl[1]
            cols = self.__S.tabinq(tablename, subset=subset)      # Get the columns for this table at this subset level
            n_cols=len(cols)
            tablesInfo[i]=(i,tablename,subset,n_cols)
            i += 1
        return tablesInfo

    def getTableData(self,numTable):
        table = self.tables[numTable]
        tablename, subset = table
        cols = self.__S.tabinq(tablename, subset=subset)
        rows={}
        for col in cols:
            rows[col]=self.__S[subset, tablename, col, :]
        return rows
        
    def deleteTable(self, tablename, subset):
        output=""

        try:
            tsubset=int(subset)
        except:
            raise gipsyException("Unable to delete the table %s %s . The subset is not an integer"%(tablename, subset))
        else:
            try:
                self.__S.deltab(tablename, tsubset)
            except:
                raise gipsyException("Unable to delete the table %s %s "%(tablename, subset))
            else:
                output="%s.deltab(%s, %s)"%(self.varname, tablename, tsubset)
        return output
        
    def clearTables(self, except_table):
        
        log="maxtables = 200\n\
attempts = 0\n\
while attempts >= 0:\n\
    try:\n\
        tablist = %s.tablis(nitems=maxtables)\n\
        attempts = -1\n\
    except:\n\
        maxtables += maxtables/2\n\
        attempts += 1\n"%self.varname
        if except_table==None:
            for tablename, subset in self.tables:
                self.__S.deltab(tablename, subset)
            log+="for tablename, subset in tablist:\n    %s.deltab(tablename, subset)\n"%self.varname
        else:
            for tablename, subset in self.tables:
                if tablename!=except_table:
                    self.__S.deltab(tablename, subset)
            log+="for tablename, subset in tablist:\n    if tablename!=%s\n        %s.deltab(tablename, subset)\n"%(except_table, self.varname)
        
        return log
    def getHeaderValue(self, key):
        try:
            value= unicode(self.__S[0, key])
        except KeyError:
            raise gipsyException("Unable to access to %s header item"%unicode(key))
            return
        return value
 
    def closeSet(self):
        self.__S.close()
        log = "%s.close()"%(self.varname)+"\n"
        return log
    
    def tryOpenSet(self, inputset, box):
        try:
            s = Set(inputset, create=False, write=False, gethdu=None, getalt=None)
        except:
            raise gipsyException("Cannot process this set: %s"%inputset)
        else:
            try:
                s.setbox(box)
            except:
                raise gipsyException("The box is not correct: %s"%box)
                s.close()
            else:
                s.close()
    
    def imageArray(self):
        return self.__S.image
