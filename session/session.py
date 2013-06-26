from PyQt4.QtCore import *
from PyQt4.QtGui import *

import networkx 
#import networkx.algorithms.traversal
import pickle

from general import *
from new_exceptions import *


class session(object):
    """This class represent the work session of a user. It stores the documents opened and the log gathered in the workflow area. 
        It also represents the relationship between the opened sets.
        A set B can be the result of an operation aplied to the set A, in this case the set A will be the parent of the set B. 
        This relationship graph is implemented by the networkx library. 
        The session is stored in a file using the pickle library. Before the user gives a pathfile to store the session,
        this class use the file  ./session<number>.ses.bkp, where number is got from a counter.
        When the user gives a name for the file session, the bakcup session is renamed to <filesession>.bkp.
        Whenever an action modifies the session, the backup file session  is updated with the  current  status of the session
        
         **Attributes**
        
        setTree : :class:`networkx.DiGraph`
            Graph which keeps the pathfiles of the sets opened during the session and the relation between them
        workflow : :class:`PyQt4.QtCore.QString`
            Current text in the workflow area.
        sessionfile :  String
            Path of the file where the session will be stored.
        sessionfileBkp : Stromg
            Path of the file where the session is stored, until the user does not give a name for the session
        docFiles : Dictionary
            Dictionary of lists. It contains 7 lists, one for each type of elements (TABLE, VOTABLE,IMAGE,PYFILE,TEXT,COLA,HELP). 
            The list contains the pathfiles or names of the document.

    """
        
    def __init__(self, n_session):
       
        self.setTree= networkx.DiGraph() #Directed graph
        self.workflow= QString()
        self.sessionfile= None
        self.sessionfileBkp="./session"+str(n_session)+".ses.bkp"

        self.docFiles={ # A list of pathfiles for each type of files
         "TABLE": [], 
         "VOTABLE":[], 
         "IMAGE":[], 
         "PYFILE":[], 
         "PYTEMP":[], 
         "TEXT":[], 
         "COLA":[], 
         "COLATEMP":[], 
         "HELP":[]
         } 
         
        if networkx.__version__[0]=='0':
            self.network_version=0
        else:
           self.network_version=1
    
        self.dirty=False
        
    def setToSession(self, pathfile, father=None ):
       
        self.setDirty()
        self.setTree.add_node(pathfile)
        if father !=None:
            self.setTree.add_edge(father, pathfile)
        self.saveSession(bkp=True)
        
    
    def docToSession(self, pathfile, type):
        
        self.setDirty()
        if pathfile not in self.docFiles[type]:
            self.docFiles[type].append(pathfile)
        self.saveSession(bkp=True)
        
 
    def saveSession(self, filename=None, bkp=False):
        #The sesionfile and the sesionfileBkp  pathfiles are updated suitably
        if filename is not None: 
            self.sessionfile=filename
            os.rename(self.sessionfileBkp, self.sessionfile+".bkp") 
            self.sessionfileBkp=filename+".bkp"
        
        #The bakcup session file always is updated
        try: 
                output = open(self.sessionfileBkp, 'wb')
        except:
                pass 
        else:
                pickle.dump(self, output)
                output.close()
        
        #The session file is updated when the user selects save the session
        if  not bkp and (self.sessionfile is not None): 
            try:
                output = open(self.sessionfile, 'wb')
            except:
                return
            else:
                pickle.dump(self, output)
                output.close()
            self.dirty=False

    
    def close(self):
        try:
            os.remove(self.sessionfileBkp)
        except:
            return
            
    def loadSession(self, sessionfile):
        if sessionfile is not None:
            try:
                read = open(sessionfile, 'rb')
            except IOError as e:
                raise e
                return
            try:
                tmp=pickle.load(read)
            except KeyError as k:
                raise k
                return
            
            #To avoid problems from renaming the filename of a session
            self.sessionfile=sessionfile
            self.sessionfileBkp=self.sessionfile+".bkp"
            self.setTree=tmp.setTree
            self.docFiles=tmp.docFiles
            self.workflow=tmp.workflow

            self.saveSession()
   
    
    def isDirty(self):
        return self.dirty
    
    def setDirty(self):
        self.dirty=True
        
    def has_sessionfile(self):
        if self.sessionfile is None:
            return False
        else:
            return True
    
    def setChildren(self,  parent):
        children=[]
        for key, val in self.setTree.iteritems():
            if val==parent:
                children.append(key)
        return children

    def getWorkflowText(self):
        return self.workflow
    
    def updateWorkflowText(self, text):
        self.workflow=QString(text)
        self.setDirty()
        self.saveSession(bkp=True)
        

    def orderedListOfSet(self):
        ordered=[]
        topological=networkx.algorithms.dag.topological_sort(self.setTree)
        
        for set in topological:
            pred=self.setTree.predecessors(set)
            if len(pred)>0:
                tmp=(set, pred[0])
            else:
                tmp=(set, "")
            ordered.append(tmp)
            
        return ordered
    
    def listOfSet(self):
        return self.setTree.nodes()
        
    def successors(self, setname):
        successors_graph=networkx.algorithms.traversal.dfs_tree(self.setTree,setname)
        successors=successors_graph.nodes()
        successors.remove(setname)
        return successors
        
        
        
    def prunSet(self, setname):
        #Delete the parent relation and the children relation of setname
        #The setname is not deleted. If it is neccesary it can be done by remove method
        #delete parent relation
        tmp=self.setTree.predecessors(setname)
        if len(tmp)>0:
            if self.network_version>0:
                self.setTree.remove_edge(tmp[0], setname)
            else:
                self.setTree.delete_edge(tmp[0], setname)
        #delete children relation
        tmp=self.setTree.successors(setname)
        for item in tmp:
            if self.network_version>0:
                self.setTree.remove_edge(setname, item)
            else:
                self.setTree.delete_edge(setname, item)
        self.setDirty()
        self.saveSession(bkp=True)
    
    def remove(self, fName, type):
        if type=="SET":
            
            if (self.network_version>0):
                self.setTree.remove_node(fName)
            else:
                self.setTree.delete_node(fName)
        else:
            list=self.docFiles[type]
            if fName in list:
                index=list.index(fName)
                del list[index]
        self.setDirty()
        self.saveSession(bkp=True)

    def removeFileAndChildren(self, fName):
        successors=self.successors(fName)
        for s in successors:
            if (self.network_version>0):
                    self.setTree.remove_node(s)
            else:   
                    self.setTree.delete_node(s)
        if (self.network_version>0):
                    self.setTree.remove_node(fName)
        else:   
                    self.setTree.delete_node(fName)
        self.setDirty()
        self.saveSession(bkp=True)
        return



