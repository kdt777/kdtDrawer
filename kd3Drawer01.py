# Input parameters from csv file and draw graphics

import math
import time
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.close('all')
fig = plt.figure()    #plt.subplots(1)
ax = plt.axes(projection='3d')
#ax.set_aspect('equal')

varDict = {}                    #variable names and values
varDict["pi"] = 3.141592

def mainstream():
  print ("ptime =", time.process_time())
  stime = time.process_time()   # processor time
  print ("==="*18)

  with open('kD3sphereInPyr.txt', newline='') as csvfile:     # get drawing specs
    cpxDomReader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for kdRow in cpxDomReader:
      kdList = parse_csv_row(kdRow)
      #print("  L =", len(kdList))     #, kdList)

  print("\n   Vars:", varDict.items()) 

def parse_csv_row(csvRow):
    if csvRow[0] > "#Z":
      print(csvRow)
    kdLst = []
    for kdItem in csvRow:
      kdLst.append(kdItem.strip())
      
    if kdLst[0] == "ID":           #identifier
      print("   Iden:") 
      kdTitle = (kdLst[1])
      xLo = float(kdLst[2]); yLo = float(kdLst[3]); zLo = float(kdLst[4])
      xHi = float(kdLst[5]); yHi = float(kdLst[6]); zHi = float(kdLst[7])
      xCtr = (xLo+xHi)/2; yCtr = (yLo+yHi)/2
      print("  iden:  ", xLo, yLo, " to ", xHi, yHi)
      ax.set_xlim(xLo, xHi); ax.set_ylim(yLo, yHi); ax.set_zlim(yLo, yHi)
      '''ax.text(xCtr, yCtr, zHi*0.95, kdTitle, size="small",
                                style="italic", ha="center")''' 
      ax.set_title(kdTitle)
      if "noaxes" in kdLst[8]:
        plt.axis('off')       # <--- Hides both X and Y axes
      ax.text(xCtr, 0, -0.5, 'kd3Drawer', 
          fontsize=10, color='gray', alpha=0.20,
          ha='left', va='bottom', rotation=0)
        
    if kdLst[0] == "AV":           #variable assignment (eg x1:2.3)
      varNam = kdLst[1]
      varVal = float(kdLst[2]) 
      varDict[varNam] = varVal
      #print(varDict.items()) 
   
    if kdLst[0] == "SPH":           #circle
      #xCntr=1; yCntr = 1
      xval = kdLst[1]; yval = kdLst[2]; zval = kdLst[3]
      radS = float(kdLst[4])      
      xCntr = extract_value(xval)
      yCntr = extract_value(yval)
      zCntr = extract_value(zval)
      print("   sph:", xCntr, yCntr, zCntr, radS)
      lnWidth = float(kdLst[5]);
      lnColr = kdLst[6]

      nPts = 20            #generate coord grid
      phi, theta = np.mgrid[0.0:np.pi:complex(0, nPts), 
                            0.0:2.0*np.pi:complex(0, nPts)]
      Xmsh = radS * np.sin(phi) * np.cos(theta) + xCntr
      Ymsh = radS * np.sin(phi) * np.sin(theta) + yCntr
      Zmsh = radS * np.cos(phi) + zCntr
      sphere_surface = ax.plot_surface(Xmsh, Ymsh, Zmsh, cmap='viridis',
                                       edgecolor='none', alpha=0.2)
      ax.set_box_aspect([1, 1, 1])
      print("  sphr:  ", xCntr, yCntr, zCntr, radS, lnWidth, lnColr)
      
    if kdLst[0] == "LN":           #line (normal)
      x1 = extract_value(kdLst[1]); y1 = extract_value(kdLst[2]); z1 = extract_value(kdLst[3]);
      x2 = extract_value(kdLst[4]); y2 = extract_value(kdLst[5]); z2 = extract_value(kdLst[6]);
      #x1 = float(kdLst[1]); y1 = float(kdLst[2])
      #x2 = float(kdLst[3]); y2 = float(kdLst[4])
      XX = [x1, x2]; YY = [y1, y2]; ZZ = [z1, z2]
      lnWidth = float(kdLst[7]) 
      lnAttr = kdLst[8]
      ax.plot3D(XX, YY, ZZ, lnAttr, lw=lnWidth)
      print("  line:  ", XX, YY, ZZ)
    
    if kdLst[0] == "TX":           #text
      xT = float(kdLst[1]); yT = float(kdLst[2]); zT = float(kdLst[3])
      txtStrgRaw = kdLst[4]
      tsLth = len(txtStrgRaw) - 1
      if tsLth > 0:
        txtStrg = txtStrgRaw[1:tsLth]
      else:
        txtStrg = txtStrgRaw
      txtSize = float(kdLst[5])
      if txtStrgRaw[0] == "{":
        fStyle = "italic"
      else:
        fStyle = "normal"
      ax.text(xT, yT, zT, txtStrg, size=txtSize, style=fStyle)
                #style="italic", ha="center") 
    return(kdLst)
  
def extract_value(parm):
    if is_numeric(parm):
        pVal = float(parm)
    else:
        if parm in varDict: pVal = varDict[parm]
    return pVal

def is_numeric(val):
    try:
        float(val)
        return True
    except ValueError:
        return False

mainstream()

#ax.plot([2,3], [4,5], 'b-')
#plt.xticks(color='None')

plt.show()
