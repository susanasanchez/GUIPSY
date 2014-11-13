import gipsy
from gipsy import *

import sys
import time
import re
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from gipsyClasses.gipsySet import *
from new_exceptions import *
from general import *


class dynamicalForm(QDialog):
    """
    This is a dialog which is showed when a task is launched to HERMES. This dialog allow the user insert 
    the values for the parameters task. The dialog grows dinamically, adding a new field for each required parameter
    """
    def __init__(self, taskname,parent=None):
        super(dynamicalForm,self).__init__(parent)
       
        self.setModal(True)
        
        self.keys = []
        self.log=""
        #taskname=taskname.upper()
        cmd='Running '+taskname
        cmd_inlines=re.sub("(.{64})", "\\1\n", cmd, re.DOTALL)
        cmdlab = QLabel(cmd_inlines)
        #self.lineedit = QLineEdit()
        layout = QHBoxLayout() 
        layout.addWidget(cmdlab)
        #layout.addWidget(self.lineedit)
        self.statusLabel = QLabel('Ready')
        self.errorLabel = QLabel()
        self.errorLabel.setStyleSheet('QLabel {color: red}')
        self.layout = QVBoxLayout()
        self.layout.addLayout(layout)
        self.layout.addWidget(self.statusLabel)
        self.layout.addWidget(self.errorLabel)
        self.setLayout(self.layout)
        self.setWindowTitle('Task launcher')
        
        
   
    def addkey(self, key):
        statusLabel = QLabel(key)
        lineedit = QLineEdit()
        lineedit.setFocus()
        gipsy.QtLink(key, lineedit, 'returnPressed()', compare=False)
        layout = QHBoxLayout()
        layout.addWidget(statusLabel)
        layout.addWidget(lineedit)
        lineedit.setFocus(Qt.TabFocusReason)
        self.layout.addLayout(layout)
        
        self.keys.append(key)

    def addCloseButton(self):
        button = QPushButton("Close this form")
        layout = QHBoxLayout()
        layout.addWidget(button)
        self.layout.addLayout(layout)
        self.connect(button, SIGNAL("clicked()"), self.closeForm)
        
    def showError(self, error):
        error_inlines=re.sub("(.{64})", "\\1\n", error, re.DOTALL)
        self.errorLabel.setText(error_inlines)
    
    def showStatus(self, status):
        status_inlines=re.sub("(.{64})", "\\1\n", status, re.DOTALL)
        self.statusLabel.setText(status_inlines)
        
    def closeForm(self):
        
        self.done(0)
        
class gipsyDynamicalTask(QObject):
    """
    This class implements the interaction between GUIpsy and HERMES in a more dynamical way. The differences between the custom 
    interface (see gipsyTask class) and this dynamical interface, is that the former try to gather all the parameters needed to run a task
    in HERMES and if an error value is inserted, the task is aborted and the user is warning about the error and asked to solve it. 
    The dynamical interface imitates the interactivity of HERMES: it gets all the messages and requests of HERMES and show them in a 
    dynamical form. 
    In this way, for example, if the user inserts a wrong value, the task is not aborted, the dynamical form will show the message of HERMES and the user can correct t
    he value in order to continue with inserting values of parameters.

    **Attributes**

    flagFinished : Boolean
        This flag is on when the task has finished. If the user close the dynamical form, and this flag is off, the task running on HERMES 
        will be aborted.
    form : :class:`gipsyClasses.gipsyTask.dinamicalForm`
        It is an instance of the dynamicalForm class, which implements a QDialog. This instance is the dynamical dialog form 
        to gather the parameters and show the messages from HERMES.
    log : String
        It contains the messages of log indicating the actions performed.
    taskname : String
        It is the whole command which is launched/is going to be launched to HERMES. It could be a string containing a gipsy task, 
        or the path of a python or cola script. 
        
    """
  #This class is used to launch COLA files and PYTHON files
    
    def __init__(self, parent):
        super(QObject, self).__init__(parent)
        self.flagFinished=False
        return
        

    def finished(self,cb):
        self.flagFinished=True
        self.form.addCloseButton()
        self.emit(SIGNAL("taskExecuted"), self.log)
        cb.deschedule()                                          # deregister
  


    def writekey(self,cb):
        gipsy.wkey(cb.key+gipsy.usertext(cb.key, default=2, defval=''), cb.task)
        self.form.errorLabel.setText('')
        

    def show_status(self,cb):
        self.form.statusLabel.setText(gipsy.usertext(cb.key))
       

    def taskrequest(self,cb):
        taskkey = gipsy.usertext(cb.key)
        if taskkey not in self.form.keys:
            self.form.addkey(taskkey)
            self.form.keys.append(taskkey)
            gipsy.KeyCallback(self.writekey, taskkey, task=cb.task)
            taskmsg = gipsy.usertext('M_'+cb.notifykey, default=2)
        self.form.errorLabel.setText(gipsy.usertext('R_'+cb.notifykey, default=2, defval=''))
        

    def launchTask(self,task):
        self.form = dynamicalForm(task)
        self.connect(self.form, SIGNAL("finished(int)"), self.abort)
        self.form.show()
        
        self.taskname = task
        
        if not self.taskname:                                          # empty input:
            return                                                 # ignore
        notifykey = 'TASKCOM='
        
        self.log="#The next task might have been executed from two places: \n#1)From the task help tab, in this case the keywords used have not been recovered in this log\n#2)From python/cola tab\n gipsy.xeq(\"%s\",\"%s\")\n"%(self.taskname, notifykey)
        
        try:
            gipsy.xeq(self.taskname, notifykey)                         # start task
            gipsy.KeyCallback(self.finished, notifykey, task=self.taskname)  # register callback
            gipsy.KeyCallback(self.taskrequest, 'K_'+notifykey,task=self.taskname, notifykey=notifykey)
            gipsy.KeyCallback(self.show_status, 'S_'+notifykey)
            self.form.lineedit.setDisabled(True)
        except:
            self.form.statusLabel.setText('Cannot run %s' % self.taskname)        # failed to start 
    
    def abort(self):
        
        if not self.flagFinished:
            task_upper=self.taskname.split()[0].upper()
            try:            
                gipsy.aborttask( task_upper)
            except:
                return
            self.log=self.log+"\ngipsy.aborttask(\"%s\")\n"%task_upper
        

            
class gipsyDirectTask(object):
    """This class is used to open those GIPSY task which have their own graphical interface. The method sendTask, 
    gathers the information about the set needed for the task, in case there was a default set, and launches the corresponding 
    task to HERMES, which will open the corresponding task interface.
    
    **Attributes**
    
    InsetAxesInfo : List
        A list, where, in case it exists a default set,  each item will correspond to one axis of the set, containing a 
        tuple with the name and the range of the axes
    InsetAxesList : List 
        A list which, in case it exists a default set, will contain the names of the set axes
    newTaskId : Integer
        The identifier of the task.
        
    """
    
    def __init__(self):
        self.newTaskId=counter()
        return
        
    
    def sendTask(self, task,  setname=None):
        if setname!=None:
            inset=gipsySet()
            inset.loadSetRO(setname)
            self.insetAxesInfo=inset.getInfoAxes()
            self.insetAxesList=inset.getAxes()
            inset.closeSet()
        
            (subsetText, boxText)=insetDefaultText(setname, self.insetAxesInfo,*TASKS_CLASS[task.upper()])
            command=task+" INSET=%s BOX=%s"%(subsetText, boxText)
        else:
            command=task
        key="SVKEY="
        output="xeq(%s,%s)"%(command, key)
        try:
            xeq(command, key)
        except XeqError as e:
            raise gipsyException(unicode(e))
            return
        return output

class gipsyTask(QObject):
    """
        This class implements the relation between Hermes and the static task views/forms which build a task command 
        with the values for all the parameters of the task (the views implemented in view_task.py). 
        
        This class has methods for:
            - launching task commands to HERMES,
            - receiving the status/error messages from HERMES and communicating these messages to the corresponding view/form, 
            - aborting a task running in HERMES. If the user close the view of the task, before the task finishes, gipsyTask will execute 
              the gipsy.abort method to abort the task.
            - receiving request parameter messages from HERMES. This is a special case. It could happen the source of a task changed, 
              and requested as obligatory one of the parameters. If the form/view, does not gather the value of this parameter, HERMES will request it. 
              This class will communicate this request to the form, and the form, dynamically will build a new field (QtextField) to gather the value from 
              the user and give it back to HERMES through gipsyTask class. The RFITS view uses this functionality a lot. When a fits file are being 
              converted to a gipsy SET with the RFITS, it is common RFITS request the value for some header parameters "on-the-fly", so in this case, 
              the RFITS form builds dynamically the text field to gather the value.
            
        Indeed, the communication gipsyTask-Form/View is stronger, since the gipsyTask class receive the form itself as a parameter, and stores it in
        one of its attributes, so on, the gipsyClass can use the form methods through this attribute.
        The communication between gipsyTask and HERMES through the xeq and KeyCallback methods needs a "notifykey" parameter. This notifykey
        has to be unique. In GUIpsy, an user could launch several tasks at the same time (through several views), so it is necessary to assure the 
        notifikey is unique. A list of 4 string is used to assure this. There are 4 strings because the default number of simultaneously tasks is 4 
        for the terminal hermes, thermes, and 8 and for the non-interactive hermes, nhermes. This number can be changed in the Hermes 
        defaults file, see http://www.astro.rug.nl/~gipsy/hermes/hermesdef.html.  If the user try to run too many tasks, xeq() will raise 
        an XeqError exception "Cannot execute".

        **Attributes**

        flagFinished : Boolean
            It is a flag to avoid send an abort signal to a task which is already finished.
        form : view
            This attribute is set with the form/view which is using the gipsyTask class. Through this attribute, methods of the form can be used. 
            The methods of the form used are related to show messages from HERMES in the form, or to create a new field dynamically to gather 
            the value of a new parameter
        log : String
            It is used to store the logs which have to be in the workflow log of GUIpsy.
        task :  String
            Task name (just the name) of the task command which is going to be launched to HERMES
    
    """
    
    def __init__(self):
       
        #self.newTaskId=counter()
        self.flagFinished=False
        self.log=""
        return
        

    def finished(self,cb):
        self.flagFinished=True
        for othercb in cb.others:
            othercb.deschedule()
        cb.deschedule()                                          # deregister
        
#        if gipsy.usertext(cb.key) =="1":
        if gipsy.userint(cb.key)==1: # successful execution
            ID_POLL.append(cb.notifykey)
            self.form.finished(self.log)
            #In which other cases  would I have to append the notifykey to the poll?
        if gipsy.userint(cb.key)==0:
            self.form.showError("Command executed")
        if gipsy.userint(cb.key)==-1:
            self.form.showError("Hermes refused to execute command because of syntax error.")
        if gipsy.userint(cb.key)==-2:
            self.form.showError("Task exited before calling INIT")
        if gipsy.userint(cb.key)==-3:
            self.form.showError("Fatal execution error (i.e. CALL ERROR with a level at or above current error level)")
        if gipsy.userint(cb.key)==-4:
            self.form.showError("Task crashed")
        if gipsy.userint(cb.key)==-5: #User abort
            #This is the case when the gipsy.abort is executed
            ID_POLL.append(cb.notifykey)
            
   
    def writekey(self, cb):
        gipsy.wkey(cb.key+gipsy.usertext(cb.key, default=2, defval=''), cb.task)
        
   
    def taskrequest(self, cb):
        taskkey = gipsy.usertext(cb.key)
        
        if taskkey not in self.form.keys:
            self.form.addkey(taskkey)
            gipsy.KeyCallback(self.writekey, taskkey, task=cb.task)
            self.form.showError(gipsy.usertext('R_'+cb.notifykey, default=1, defval=''))
        else:
                
            self.form.showError(gipsy.usertext('R_'+cb.notifykey, default=1, defval=''))
            self.form.showStatus(gipsy.usertext('S_'+cb.notifykey, default=1, defval=''), wi="error")
            gipsy.aborttask( self.task)
           
            
        
    def show_status(self, cb):
        msg=gipsy.usertext('S_'+cb.notifykey, default=1, defval='') 
        
        if not "ABORT" in msg:
            self.form.showStatus(msg, wi="error")
         
    def launchTask(self,taskcommand, form):
        self.form=form
        self.connect(self.form, SIGNAL("finished(int)"), self.abort)
        self.task=taskcommand.split()[0].upper()

        if not taskcommand:                                          # empty input:
            return                                                 # ignore
            
        
        #Initially ID_POLL=['TASKCOM0=', 'TASKCOM1=','TASKCOM2=']
        if len(ID_POLL)==0:
            self.form.showStatus('Cannot run %s. Maximum 3 GUIpsy tasks simultaneously'%self.task)
            return
        else:
            notifykey=ID_POLL.pop()
        #self.log="gipsy.xeq(\"%s\",\"%s\")\n"%(taskcommand, notifykey)
        self.log="gipsy.xeq(\"%s\")\n"%(taskcommand)
        dcb=[]
        
        try:
            gipsy.xeq(taskcommand, notifykey)                         # start task
            gipsy.KeyCallback(self.finished, notifykey, task=taskcommand, notifykey=notifykey, others=dcb)  # register callback
            #gipsy.KeyCallback(self.finished, notifykey=notifykey, task=taskcommand, others=dcb)  # register callback
            dcb.append(gipsy.KeyCallback(self.taskrequest, 'K_'+notifykey,task=self.task, notifykey=notifykey))
            dcb.append(gipsy.KeyCallback(self.show_status, 'S_'+notifykey ,  notifykey=notifykey))
            
        except XeqError as e:
            self.form.showStatus('Cannot run %s. Probably Hermes has not a free task slot' % self.task)  # failed to start
            
    
    
    def abort(self):
       
        if not self.flagFinished:
            #It is NOT possible return the log, since the form is already closed when this task is executed.
            self.log=self.log+"\ngipsy.aborttask(\"%s\")\n"%self.task
            try: 
                #The method gipsy.aborttask, also trigger the method finished,due to that the notifikeys are appended to the ID_POLL
                gipsy.aborttask(self.task)
            except:
                return
            









