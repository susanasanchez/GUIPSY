#!/usr/bin/env python
import os
import sys
import getopt

def usage():
  print "Usage: packager.py -i --indir input_directory -o --outputfile path_name_output_file"
def main(argv):                         
                    
    try:                                
        opts, args = getopt.getopt(argv, "i:o:", ["indir=", "outputfile="]) 
    except getopt.GetoptError:           
        usage()                          
        sys.exit(2)
    if len(opts) !=2:
      usage()
      return
    
    for o, a in opts:
        if o in ("-i","--indir"):
            if(os.path.isdir(a)):
                indir=a
            else:
                usage()
                sys.exit(2)
        elif o in ("-o", "--outputfile"):
            outputname=a

    try:
        foutput=open(outputname,'w')
    except:
        print "Unable write in %s"%outputname
        sys.exit(2)
    foutput.write("\
#!/usr/bin/env python\n\
import gipsy\n\
from gipsy import *\n\
import sys\n\
import functools\n\
import os\n\
import re\n\
import matplotlib\n\
import glob\n\
import operator\n\
import decimal\n\
import time\n\
import pickle\n\
import webbrowser\n\
import math\n\
#import sampy\n\
#import astropy\n\
import numpy\n\
import numpy.ma as ma\n\
#from astropy.io.votable import parse_single_table\n\
#from astropy.table import Table as astroTable\n\
#from astropy.io.votable.tree import VOTableFile\n\
#import networkx as nx\n\
#import networkx.algorithms.traversal\n\
from types import *\n\
from xml.sax.saxutils import escape \n\
import xml.sax \n\
import xml.sax.handler \n\
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas\n\
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar\n\
from matplotlib.figure import Figure\n\
import PyQt4\n\
from PyQt4.QtCore import *\n\
from PyQt4.QtGui import *\n\
#from PIL import Image\n\
#from PIL.ImageQt import ImageQt\n\
\
")
    #First the resources
    f="./"+indir+"/resources_rc.py"
    print f
    try:
        tmp=open(f,"r")
    except:
        print "Unable to read %s"%f
        sys.exit(2)  
    start="####START %s\n"%f
    end="####END %s\n"%f
    foutput.write(start)
    for line in tmp:
        if line.strip().startswith("import") or line.strip().startswith("from"):
            line="#"+line
        foutput.write(line)
    tmp.close()

    #Second the exception
    f="./"+indir+"/new_exceptions.py"
    print f
    try:
        tmp=open(f,"r")
    except:
        print "Unable to read %s"%f
        sys.exit(2)  
    start="####START %s\n"%f
    end="####END %s\n"%f
    foutput.write(start)
    for line in tmp:
        if line.strip().startswith("import") or line.strip().startswith("from"):
            line="#"+line
        foutput.write(line)
    tmp.close()
    
    #Third the general
    f="./"+indir+"/general.py"
    print f
    try:
        tmp=open(f,"r")
    except:
        print "Unable to read %s"%f
        sys.exit(2)  
    start="####START %s\n"%f
    end="####END %s\n"%f
    foutput.write(start)
    
    for line in tmp:
        if line.strip().startswith("import") or line.strip().startswith("from"):
            line="#"+line
        foutput.write(line)
    tmp.close()

    #Fourth the compiled UI files 
    for item in os.listdir(indir):
        f="./"+indir+"/"+item
#        if os.path.isfile(f):
#            basename=str(os.path.basename(f))
#            if os.path.splitext(f)[1]==".py" and os.path.basename(f).startswith("Ui_"):
#                print f
#                try:
#                    tmp=open(f,"r")
#                except:
#                    print "Unable to read %s"%f
#                    sys.exit(2)
#                start="####START %s\n"%f
#                end="####END %s\n"%f
#                foutput.write(start)
#                for line in tmp:
#                    if line.strip().startswith("import") or not line.strip().startswith("from"):
#                        line="#"+line
#                foutput.write(line)
#                tmp.close()
#                foutput.write(end)
        if os.path.isdir(f): #Only two levels
            for item2 in os.listdir(f):
                g=f+"/"+item2
                if os.path.isfile(g):
                    basename=str(os.path.basename(g))
                    if os.path.splitext(g)[1]==".py" and basename.startswith("Ui_"):
                        print g
                        try:
                            tmp=open(g,"r")
                        except:
                            print "Unable to read %s"%f
                            sys.exit(2)
                        start="####START %s\n"%g
                        end="####END %s\n"%g
                        foutput.write(start)
                        for line in tmp:
                            if line.strip().startswith("import") or line.strip().startswith("from"):
                                line="#"+line
                            foutput.write(line)
                        tmp.close()
                        foutput.write(end)

    #Fourth the NOT compiled UI files 
    for item in os.listdir(indir):
        f="./"+indir+"/"+item
#        if os.path.isfile(f):
#            basename=str(os.path.basename(f))
#            if os.path.splitext(f)[1]==".py" and not basename.startswith("Ui_"):
#                print f
#                try:
#                    tmp=open(f,"r")
#                except:
#                    print "Unable to read %s"%f
#                    sys.exit(2)
#                start="####START %s\n"%f
#                end="####END %s\n"%f
#                foutput.write(start)
#                for line in tmp:
#                    if line.strip().startswith("import") or not line.strip().startswith("from"):
#                        line="#"+line
#                    foutput.write(line)
#                tmp.close()
#                foutput.write(end)
        if os.path.isdir(f): #Only two levels
            for item2 in os.listdir(f):
                g=f+"/"+item2
                if os.path.isfile(g):
                    basename=str(os.path.basename(g))
                    if os.path.splitext(g)[1]==".py" and not basename.startswith("Ui_"):
                        print g
                        try:
                            tmp=open(g,"r")
                        except:
                            print "Unable to read %s"%f
                            sys.exit(2)
                        start="####START %s\n"%g
                        end="####END %s\n"%g
                        foutput.write(start)
                        for line in tmp:
                            if line.strip().startswith("import") or line.strip().startswith("from"):
                                line="#"+line
                            foutput.write(line)
                        tmp.close()
                        foutput.write(end)

    #Last the main file
    f="./"+indir+"/guipsy.pyw"
    print f
    try:
        tmp=open(f,"r")
    except:
        print "Unable to read %s"%f
        sys.exit(2)  
    start="####START %s\n"%f
    end="####END %s\n"%f
    foutput.write(start)
    for line in tmp:
        if (line.strip().startswith("import") or line.strip().startswith("from")) and line.find('networkx')==-1 and line.find("sampy")==-1 and line.find("astropy")==-1 and line.find("PIL")==-1:
            
            line="#"+line
        foutput.write(line)
    tmp.close()

    foutput.close()  
    
    


if __name__ == "__main__":
    main(sys.argv[1:])
