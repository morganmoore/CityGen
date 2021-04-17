import maya.cmds as cmds
import math as math
import functools
import random as rand
import os
import glob

# create UI function sets all features of the user interface. Controls include sliders to adjust Building width, height 
# and checkboxes to include or exclude certain features
def createUI(windowname):
    windowID = 'mainwindow'
    
    #Create Window
    if cmds.window( windowID, exists=True):
        cmds.deleteUI(windowID)
    cmds.window( windowID, title= windowname , sizeable=True, resizeToFitChildren=False)
    
    cmds.columnLayout( adjustableColumn=True )

    #Create UI Image
    current_project = cmds.workspace(q=True, rootDirectory=True) 
    cmds.image( w =10, h = 120, i= current_project+"images/cityGen")
    cmds.separator(h =10, style = 'none')
       
    cmds.text( label ='City Gen:',align='left', font = 'boldLabelFont')
    cmds.separator(h =5, style = 'none')

    #Building Types checkbox
    buildTypes = cmds.checkBoxGrp( numberOfCheckBoxes=4, label='Building Types', columnAlign=[1,'left'], labelArray4=['Square', 'Pointy', 'Hexagon', 'Square2'], valueArray4 = [True,True,True,True] )
    cmds.separator(h =10, style = 'none')

    #All slider controls
    numberBuildings = cmds.intSliderGrp(label='Number of Buildings:', minValue=1, maxValue=200, value=150, step=1, field=True, columnAlign=[1,'left'])
    mapWidth = cmds.floatSliderGrp(label='Map width:', minValue=20, maxValue=100, value=40, step=1, field=True, columnAlign=[1,'left'])
    minHeight = cmds.floatSliderGrp(label='Height min:', minValue=1, maxValue=5, value=3, step=0.1, field=True, columnAlign=[1,'left'])
    maxHeight = cmds.floatSliderGrp(label='Height max:', minValue=5, maxValue=12, value=8, step=0.1, field=True, columnAlign=[1,'left'])
    minWidth = cmds.floatSliderGrp(label='Width min:', minValue=1, maxValue=5, value=2, step=0.1, field=True, columnAlign=[1,'left'])
    maxWidth = cmds.floatSliderGrp(label='Width max:', minValue=3, maxValue=8, value=5, step=0.1, field=True, columnAlign=[1,'left'])
    minGapWidth =  cmds.floatSliderGrp(label='Gap Width min:', minValue=0, maxValue=5, value=0, step=0.1, field=True, columnAlign=[1,'left'])
    cmds.scriptJob( listJobs=True )
    cmds.separator(h =10, style = 'none')
    
    #control to enable or disable apples on the tree
    centreHeight = cmds.checkBoxGrp( numberOfCheckBoxes=1, label='Centre Height:  ',columnAlign=[1,'left'],  value1 =True  )
    centreWidth = cmds.checkBoxGrp( numberOfCheckBoxes=1, label='Centre Width:  ',columnAlign=[1,'left'],  value1 =True  )
    centreCluster = cmds.checkBoxGrp( numberOfCheckBoxes=1, label='Centre Cluster:  ',columnAlign=[1,'left'],  value1 =True  )
    cmds.separator(h =10, style = 'none')
    progressControl = cmds.progressBar( width = 300, bgc =[0.23,0.16,0.0] )
    
    cmds.separator(h =10, style = 'none')
    
    #when the apply button is pressed, the path names of the various controls are passed to the cityGen function
    cmds.button( label='Apply', backgroundColor=[0.9,0.9,0.9], command=functools.partial( cityGen, numberBuildings, mapWidth, minWidth, maxWidth, minHeight, maxHeight, minGapWidth, centreHeight,centreWidth, buildTypes, centreCluster, progressControl) )
             
    cmds.separator(h =10, style = 'none')
    
    #Save button calls the 'savemenu' fucntion 
    cmds.button( label = 'Save', command=functools.partial(savemenu), backgroundColor=[0.1,0.3,0.0])
    cmds.separator(h =10, style = 'none') 

    #Delete Button calls the 'deleteCity' function
    cmds.button( label = 'Delete', command=functools.partial(deleteCity), backgroundColor=[0.5,0.0,0.0])
    cmds.separator(h =10, style = 'none') 
    
    #Cancel button c
    cmds.button( label = 'Cancel', command=functools.partial( cancelCallback, windowID) )
    
    cmds.showWindow()
    cmds.window(windowID, e=True, width=640)   
    
def savemenu(*pArgs):
    '''creates a window for the user to enter a name and select the format of their generated tree''' 
      
    if cmds.window( 'savemenu', exists=True):
        cmds.deleteUI('savemenu')
    cmds.window( 'savemenu', title= 'Save Menu' , sizeable=False, resizeToFitChildren=True )
    cmds.columnLayout( adjustableColumn=True )
    cmds.text( label='Enter Filename: ',align='left')
    filename = cmds.textField( width=1, text='Filename?')
    fileformats = cmds.radioButtonGrp( numberOfRadioButtons=3, label='File Format:  ', labelArray3=['MayaAscii', 'OBJ', 'MayaBinary'], select = 1)
    
    #when the user clicks the save button the path names of the filename and fileformats controls are passed to the 'save' fucntion
    cmds.button( label='save', backgroundColor=[0.1,0.3,0.2], command=functools.partial( save, fileformats, filename))
    cmds.showWindow() 

def save(pfileformat, pfilename, *pArgs):
    saveDict = {
    1: "mayaAscii",
    2: "OBJexport",
    3: "mayaBinary",
    }

    fileformats = []
    filename = cmds.textField(pfilename, query=True, text=True)
    fileformat= cmds.radioButtonGrp(pfileformat, query=True, select=True) 
    workspace = cmds.workspace( q=True, dir=True )

    cmds.file(rename=workspace+ filename)
    if(saveDict[fileformat] != "OBJexport"):
        saved = cmds.file(save=True, type=saveDict[fileformat])
    else:
        cmds.select('City')
        cmds.file( exportSelected= True, type = "OBJexport")
    
    if glob.glob(workspace+ filename+".*"):
        print("Saved successfully!", workspace+ filename)
    else:
        print("Save unsuccessfull!", workspace+ filename+".*")

def deleteCity(*args):
    if cmds.objExists('City'):
        cmds.delete('City')
    else:
        print("Nothing to delete")

def cancelCallback(windowID,*pArgs):
    '''function to close UI window
       windowID        : The identification name of the window
    '''   
    if cmds.window( windowID, exists = True):
        cmds.deleteUI(windowID)



class Buildings:

    #static class variables
    mapWidth = 30
    minHeight = 1
    maxHeight = 5
    minWidth = 1
    maxWidth = 4
    minGapWidth = 0
    centreHeight = True
    centreWidth = True
    buildingTypeList = []
    centreCluster =True

    buildDict = {
    1: "Square",
    2: "Pointy",
    3: "Hexagon",
    4: "Square2"
    }
    
    #class constructor    
    def __init__(self, count, buildingList):
        self.recursionCount = 0
        self.buildingName = "Building_" + str(count) + "_"
        self.posX = self.posY = 0
        self.height = 2
        self.width = 2
        self.totalHeight = 0
        self.bOverlap = False
        
        self.createBuilding(buildingList)
        
     
    #Primary function to create buildings
    def createBuilding(self, buildingList):
        self.setBuildingPos(buildingList)
        if(not self.bOverlap):
            self.setBuildingHeight()
            x = self.create()
            self.moveBuilding(x)

    #randomly setting building location and checking for overlaps
    # if there is an overlap, the function recursively tries again for a maximum of 10 recursions
    def setBuildingPos(self, buildingList):
        self.bOverlap = False
        if(Buildings.centreCluster):
            tmp = pow(randrange_float(0,1,0.01), 0.5)
            x = -Buildings.mapWidth/2+(Buildings.mapWidth) * pow(randrange_float(0,1,0.01), 1.5) 
            y = -Buildings.mapWidth/2+(Buildings.mapWidth) * pow(randrange_float(0,1,0.01), 1.5)
        else:
            x = self.randrange_float(-Buildings.mapWidth/2, Buildings.mapWidth/2, 0.01)
            y = self.randrange_float(-Buildings.mapWidth/2, Buildings.mapWidth/2, 0.01)
        
        self.setBuildingWidth(x,y)
        
        for j in range(len(buildingList)):
            
            if(abs(buildingList[j].posX-x)<(buildingList[j].width+self.width+Buildings.minGapWidth)/2 and abs(buildingList[j].posY-y)<(buildingList[j].width+self.width+Buildings.minGapWidth)/2):
                self.bOverlap = True
                break
        
        if(self.bOverlap):
            self.recursionCount+=1
            if(self.recursionCount<10):
                self.setBuildingPos(buildingList)
            else:
                print("Couldn't find a spot")
        else:
            self.recursionCount = 0
            self.posX = x 
            self.posY = y

    #if 'centreWidth' checked by user, set height according to buildings distance from centre (0,0)
    def setBuildingWidth(self, x, y):
        if(Buildings.centreWidth):
            distanceFromCentre = math.sqrt(pow(x, 2)+pow(y, 2))
            tmp = randrange_float(0.8, 1.2, 0.1)
            self.width =  (((((Buildings.mapWidth/2)-distanceFromCentre)/(Buildings.mapWidth/2))*(Buildings.maxWidth-Buildings.minWidth))+Buildings.minWidth)*tmp
        else:
            self.width = randrange_float(Buildings.minWidth, Buildings.maxWidth, 0.1)
    
    #if 'centreHeight' checked by user, set height according to buildings distance from centre (0,0)
    def setBuildingHeight(self):
        if(Buildings.centreHeight):
            distanceFromCentre = math.sqrt(pow(self.posX, 2)+pow(self.posY, 2))
            tmp = randrange_float(0.8, 1.2, 0.1)
            self.height =  (((((Buildings.mapWidth/2)-distanceFromCentre)/(Buildings.mapWidth/2))*(Buildings.maxHeight-Buildings.minHeight))+Buildings.minHeight)*tmp
        else:
            self.height = randrange_float(Buildings.minHeight, Buildings.maxHeight, 0.1)

    # function to create each building floor by floor
    # Once built the building group is parented to its corresponding building type group
    def create(self):
        buildIter = rand.randint(0,len(Buildings.buildingTypeList)-1)
        buildnum = Buildings.buildingTypeList[buildIter]

        #get the scale-X of the original building geo
        buildingX = cmds.xform("type" +str(buildnum) + "Floor", q = True, bb = True)[3] - cmds.xform("type" +str(buildnum) + "Floor", q = True, bb = True)[0]

        #make copies of the original model
        floor = cmds.duplicate( "type" +str(buildnum) + "Floor" )
        top = cmds.duplicate("type" +str(buildnum) + "Top")
        
        #parent these models to the world (unparent)
        cmds.parent( floor, w=True )
        cmds.parent( top, w=True )
        
        # scale the models to the calculated width
        tmp = self.width/buildingX
        cmds.scale( tmp, tmp, tmp, floor, absolute=True )
        cmds.scale( tmp, tmp, tmp, top, absolute=True )
        buildingY = cmds.xform(floor, q = True, bb = True)[4] - cmds.xform(floor, q = True, bb = True)[1]

        #calculate number of floors required to match calculated height
        tmp2 = int(round(self.height/buildingY))
        cmds.group( floor, top, n=self.buildingName+Buildings.buildDict[buildnum])

        #create floors
        for i in range(tmp2-1):
            new2 = cmds.duplicate( floor )
            if(buildnum==1):
                r1 = rand.randint(0,1)*90
                cmds.rotate( 0, str(r1)+'deg', 0, new2)
            
            self.totalHeight+=buildingY
            cmds.move( 0, self.totalHeight, 0 , new2)

        #position top of building model
        if(not buildnum==3):
            r2 = rand.randint(0,4)*90
        else:
            r2 = rand.randint(0,1)*180
        cmds.rotate( 0, str(r2)+'deg', 0, top)
        self.totalHeight+=buildingY
        cmds.move( 0, self.totalHeight, 0 , top)  
        tester = cmds.parent(self.buildingName+Buildings.buildDict[buildnum], Buildings.buildDict[buildnum]+"_Buildings")

        return tester
       
    #move building to location  
    def moveBuilding(self, x):
        #print("moved", self.posX, self.posY)
        #cmds.select(x)
        cmds.move(self.posX, 0, self.posY, x)
        #cmds.select( cl = True)


def randrange_float( start, stop, step):
    return rand.randint(0, int((stop - start) / step)) * step + start

def setProgress(prog, numBuildings):
    cmds.progressBar(prog, edit=True, maxValue=numBuildings)
    cmds.progressBar(prog, edit=True, progress=0)

# Programs primary function
# 
def cityGen(numberBuildings, mapWidth, buildingMinWidth, buildingMaxWidth, buildingMinheight, buildingMaxheight, minGapWidth, centreHeight,centreWidth, buildTypes,centreCluster,progress,  *args): 
    
    cmds.group( em = True, n = "City")
    
    buildingList = []
    numBuildings = cmds.intSliderGrp(numberBuildings, query=True, value=True)

    #Setting Building Class variab;es
    Buildings.mapWidth = cmds.floatSliderGrp(mapWidth, query=True, value=True)
    Buildings.minWidth = cmds.floatSliderGrp(buildingMinWidth, query=True, value=True)
    Buildings.maxWidth = cmds.floatSliderGrp(buildingMaxWidth, query=True, value=True)
    Buildings.minHeight = cmds.floatSliderGrp(buildingMinheight, query=True, value=True)
    Buildings.maxHeight = cmds.floatSliderGrp(buildingMaxheight, query=True, value=True)
    Buildings.minGapWidth = cmds.floatSliderGrp(minGapWidth, query=True, value=True)
    Buildings.centreHeight = cmds.checkBoxGrp(centreHeight, query=True, value1=True)
    Buildings.centreWidth = cmds.checkBoxGrp(centreWidth, query=True, value1=True)
    Buildings.centreCluster = cmds.checkBoxGrp(centreCluster, query=True, value1=True)
    tmpList = cmds.checkBoxGrp(buildTypes, query=True, valueArray4=True)

    # initialise/reset the progress bar
    setProgress(progress, numBuildings)
    
    for i in range(len(tmpList)):
        if(tmpList[i]):
            Buildings.buildingTypeList.append(i+1)
            tmp = cmds.group( em=True, name=Buildings.buildDict[i+1]+"_Buildings")
            cmds.parent(tmp, "City")

    cmds.polyPlane( w=Buildings.mapWidth+Buildings.maxWidth, h=Buildings.mapWidth+Buildings.maxWidth  , n = "Ground")
    cmds.parent("Ground", "City")

    for i in range(numBuildings):
        cmds.progressBar(progress, edit=True, step=1)
        building = Buildings(i+1,buildingList)
        buildingList.append(building)

    

#Enter program and call create UI
if __name__ == "__main__":
    createUI('CityGen')