import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *


p=os.environ.get("HOME")
GUIPSYDIR=p+"/.gipsy/"
TASKFILES=GUIPSYDIR+"guipsyfiles/"
#LASTPATH=os.getcwd()
FORMATS={
         "FITS":"FITS (*.fits);;*", 
         "SET":"Set (*.image)", 
         "SESSION":"Session files (*.ses)", 
         "TABLE":"DAT (*.dat);; TXT (*.txt);; XML (*.xml);;*", 
         "VOTABLE":"XML (*.xml);;*", 
         "IMAGE":"Image files (%s);; EPS (*.eps)" % " ".join(["*.%s" % unicode(format).lower()  for format in QImageReader.supportedImageFormats()]), 
         "PYFILE":"PY (*.py);;PYC (*.pyc)", 
         "TEXT":"TXT (*.txt);;*", 
         "COLA":"COL (*.col);;*", 
         "PARAM":"Parameters (*.param)"
         }
menuTips={

#FILE MENU
        "empty_cola_file":"Create an empty  cola file", 
        "empty_python_file":"Create an empty python file", 
        "new_text_file":"Create text file",
        "new_session":"Create a new session", 
        
        "open_set":"Open Set",
        "open_fits":"Create the Set associated to the fits and open it",
        "open_table":"Open ASCII Table ", 
        "open_image":"Open Image File",
        "open_pyfile": "Open Python File", 
        "open_cola":"Open Cola File",
        "open_text":"Open Text File",
        "open_session":"Open Session", 
        
        "save_session": "Save Current Session", 
        "save": "Save Current File", 
        "save_as": "Save the file using a new name",
        "save_as_fits":"Save the Set as fits using WFITS task", 
        "save_as_vot":"Save the table as VOTable (xml file) ",
        "save_as_ascii":"Save the current VOtable as an ASCII table",
        "close":"Close Current Document", 
        "close_session":"Close Current Session", 
        "close_all": "Close all opened documents", 
        "samp": "Register Samp", 
        "delete_set":"Delete the current Set",
        "delete_settable":"Delete the table from the Set",
        "rename" :"Change the name of the file", 
        'remove_fileAndChildren':"Remove the file and all output (its descendants)", 
        "remove":"Remove the file from the current session", 
        "quit":"Close the application", 
        

#SET EDITION MENU

        "Clip":"Clip", 
        "Combin":"Combin", 
        "Copy":"Copy", 
        "Decim":"Decim", 
        "Diminish":"Diminish", 
        "EditSet":"Editset", 
        "Extend":"Extend", 
        "Insert":"Insert", 
        "Mean":"Mean/Sum", 
        "MinBox":"MinBox", 
        "Regrid":"Regrid", 
        "Snapper":"Snapper", 
        "Transform":"Transform",
        "Transpose":"Transpose",  
        "Velsmo":"Velsmo", 
        "PyBlot":"PyBlot", 
        "ConDit":"ConDit", 
        "ConRem":"ConRem", 
        "FindGauss":"FindGauss", 
        "MFilter":"MFilter", 
        "Patch":"Patch", 
        "Smooth":"Smooth", 
        
#DISPLAY MENU
        "Maps":"Maps", 
        "Coords":"Coords", 
        "SkyCalq":"SkyCalq", 
        "Sliceview":"Sliceview", 
        "Render":"Render", 
        "VTKVolume":"VTKVolume", 
        "Visions":"Visions", 
        "Inspector":"Inspector", 
        "AllSkyPlot":"AllSkyPlot", 
        "CPlot":"CPlot",
        "Reproj":"Reproj", 
        "ReprojFits":"ReprojFits", 
        "WCSFlux":"WCSFlux", 
        
#ANALYSIS MENU
        "EllInt":"EllInt", 
        "GalMod":"GalMod", 
        "Moments":"Moments", 
        "Potential":"Potential", 
        "PPlot":"PPlot", 
        "Profil":"Profil", 
        "ResWri":"ResWri", 
        "RotCur":"RotCur",
        "Shuffle":"Shuffle",  
        "Slice":"Slice", 
        "VelFi":"VelFi", 
        "RotMas":"RotMas", 
        "XGauFit":"XGauFit", 
        "XGauProf":"XGauProf", 
        "GaussCube":"GaussCube", 
        "RotMod":"RotMod", 
        
#VO MENU
        "TOPCAT":"Download and launch TOPCAT tool", 
        "ALADIN":"Download and launch ALADIN tool", 
        "VOSPEC":"Download and launch VOSPEC tool", 
        "VOSearch":"VOSearch", 
        "Send_to":"Send to", 
#HELP MENU
        "About":"Show version info", 
        "Handbook":"User manual"
        
      }
ICONSLICENSE="http://openiconlibrary.sourceforge.net/LICENSES.html"
PYTHONCREDIT="http://www.python.org"
GUIPSY_VERSION="Version 0.1 - Abril 2013"
AUTHOR="Susana Sanchez sse@iaa.es"
INSTITUTION= "Instituto Astrofisica Andalucia, CSIC, Spain\n\
Kapteyn Astronomical Institute,\n\
University of Groningen, The Netherlands"


GIPSY_COORDS={
              "DEC":["DEGREE"], 
              "RA":["DEGREE"], 
              "FREQ":["HZ", "KHZ", "MHZ", "GHZ"], 
              "VELO":["KM/S", "M/S", "MM/S", "CM/S"], 
              "TIME":["SECOND", "MINUTE", "HOUR", "DAY", "YEAR"], 
              "LAMDA":["METER", "ANGSTROM", "MICRON", "MM", "CM", "INCH", "FOOT", "YARD", "M", "KM", "MILE", "PC","KPC", "MPC"], 
              "GLONG":["DEGREE"], 
              "GLAT":["DEGREE"], 
              "ELON":["DEGREE"], 
              "ELAT":["DEGREE"], 
              "SLONG":["DEGREE"], 
              "SLAT":["DEGREE"]
              }
ERROR_SETBROWSER={
                      'syntax': "BAD INPUT: syntax error", 
                      'overflow': "BAD INPUT: Output buffer overflow", 
                      'twovalues': "BAD INPUT: Exactly 2 items required"
                      
                      }
VOTOOLS={
         "TOPCAT": "http://www.star.bris.ac.uk/~mbt/topcat/topcat-full.jnlp", 
         "ALADIN":"http://aladin.u-strasbg.fr/java/nph-aladin.pl", 
         "VOSPEC":"http://esavo.esac.esa.int/webstart/VOSpec.jnlp"
         }
TASKS_CLASS={#Fclass, Fsubdim 
             "CLIP":(1, 0), 
             "COMBIN":(1, 0), 
             #"COPY":(-1, -1),  # Indeed it is (1,0)
             "COPY":(1, 0, -1), #Added a special class to avoid the control
             "DECIM":(1, 0), 
             "DIMINISH":(1, 0), #Diminish is not in $gip_tsk !??
             "EDITSET":(1, 0), 
             #"EXTEND":(1, 0), 
             "EXTEND":(-1, -1), 
             "INSERT":(1, 0), 
             "INSPECTOR":(1, 2), 
             "MEAN":(2, 0), 
             "MINBOX":(1, 0), 
             #"REGRID":(1, 0), 
             "REGRID":(-1, -1),
             "SNAPPER":(1, 2), 
             "TRANSFORM":(1, 2), 
             "TRANSPOSE":(-1, -1), 
             "VELSMO":(2, 1), 
             "ELLINT":(1, 2), 
              "GALMOD":(1, 2), 
             "MOMENTS":(2, 1), 
             "POTENTIAL":(1, 2), 
             "PPLOT":(-1, -1),  # PPLOT does not have classdim or class. (1,0)
             "PROFIL":(1, 0), 
             "RENDER":(2, 1), 
             "RESWRI":(1, 2), 
             "ROTCUR":(1, 2), 
             "SLICEVIEW":(1, 2), 
             "SHUFFLE":(2, 1), 
             "SLICE":(1, 2), 
             "VELFI":(1, 2) , 
             "VTKVOLUME":(-1, -1),  # VTKVOLUME does not have classdim or class.
             "VISIONS":(-1,-1), 
             "SKYCALQ":(-1, -1) # VTKVOLUME does not have classdim or class.
             }
ROTCURHEADER="!   radius    width systemic  error rotation  error expansion  error    pos.  error incli-  error x-pos.  error y-pos.  error npts   sigma\n\
!                   velocity        velocity         velocity          angle        nation        centre        centre             velocity\n\
! (arcsec) (arcsec)   (km/s) (km/s)   (km/s) (km/s)    (km/s) (km/s)  (deg.) (deg.) (deg.) (deg.) (grid) (grid) (grid) (grid)        (km/s)\n"
ELLINTHEADER="! radius radius    Msd-t   Mass-t Cum.Mass      Msd     Mass Cum.Mass      sum subpix     area  area-bl  segLO  segHI  width     pa   incl\n\
! arcsec    Kpc  Mo/pc^2  10^9 M0  10^9 M0  Mo/pc^2  10^9 M0  10^9 M0        ?      #   pixels   pixels   deg.   deg. arcsec   deg.   deg.\n\
"

DIRPYTHONTEMPLATE=":resources/python_templates/"
DIRCOLATEMPLATE=":resources/cola_templates/"
class counter ( object ):
    def __init__ ( self , ini =0 , *a ,** k ):
        super ( counter , self ). __init__ (* a ,** k )
        self . value = ini
    def __call__ ( self ):
        current = self . value
        self . value += 1
        return current
        

newId=counter()
taskCounter=counter()
ID_POLL=['TASKCOM0=', 'TASKCOM1=','TASKCOM2=']

def insetDefaultText(setname, axes, gdsClass, classDim):
     i=0
     boxtext=""
     subsetText=setname
     xbox=[]
     ybox=[]
    
     if gdsClass==-1: # TRANSPOSE
        subsetText=setname
        boxtext=""
     else:
        
     
         if gdsClass==1:
            limit=2 if classDim==0 else classDim
         else:
                dim=len(axes)
                if classDim!=0:
                    limit=dim-classDim
                else: # if required dim is 0, select one default axis , the last one
                    limit=dim-1
    
         for axe in axes:
             (axename, range)=axe
             axename=axename.split("-")[0].upper()
             if i<limit:
                 x, y=range.split()
                 xbox.append(x)
                 ybox.append(y)
             else:
                 subsetText=subsetText+" "+axename
             
             i +=1
     
    
         for x in xbox:
             boxtext=boxtext+" "+x
         for y in ybox:
             boxtext=boxtext+" "+y
    
     
     return (subsetText, boxtext)
        
