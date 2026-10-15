# Input parameters from csv file and draw graphics - 2D

import math
import time
import csv
import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.close('all')
fig, ax = plt.subplots(1)
ax.set_aspect('equal')

varDict = {}                    #variable names and values
varDict["pi"] = 3.141592

def mainstream():
  print ("ptime =", time.process_time())
  stime = time.process_time()   # processor time
  print ("==="*18)

  with open('kd2Dxmpl.txt', newline='') as csvfile:     # get drawing specs
    cpxDomReader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for kdRow in cpxDomReader:
      if len(kdRow) < 2:
        continue
      kdList = parse_csv_row(kdRow)
      #print("  L =", len(kdList))     #, kdList)

  print("\nVars:", varDict.items())

def parse_csv_row(csvRow):
    
    if csvRow[0] > "#Z":
      print(csvRow)
    kdLst = []
    for kdItem in csvRow:
      #print("    ", item)
      kdLst.append(kdItem.strip())
      #print("  ", cdLst)
      
    if kdLst[0] == "ID":           #identifier
      print("IDEN") 
      kdTitle = (kdLst[1])
      xLo = float(kdLst[2]); yLo = float(kdLst[3])
      xHi = float(kdLst[4]); yHi = float(kdLst[5])
      print("  iden:  ", xLo, yLo, " to ", xHi, yHi)
      ax.set_xlim(xLo, xHi); ax.set_ylim(yLo, yHi)
      xCtr = (xLo+xHi)/2; yCtr = (yLo+yHi)/2
      ax.text((xLo+xHi)/2, yHi*0.95, kdTitle, size="small",
                                style="italic", ha="center")

      if "noaxes" in kdLst[6]:
        plt.axis('off')       # <--- Hides both X and Y axes
      ax.text(xCtr,-0.2, 'kd2Drawer',     #transform=ax.transAxes,
          fontsize=10, color='gray', alpha=0.120,
          ha='left', va='bottom', rotation=0)
        
    if kdLst[0] == "AV":           #variable assignment (eg x1:2.3)
      varNam = kdLst[1]
      varVal = float(kdLst[2]) 
      varDict[varNam] = varVal
      #print(varDict.items()) 
   
    if kdLst[0] == "CL":           #circle
      #xCntr=1; yCntr = 1
      xval = kdLst[1]; yval = kdLst[2]
      radC = float(kdLst[3])      
      xCntr = extract_value(xval)
      yCntr = extract_value(yval)
      #print("   CL:", xCntr, yCntr, radC)
      
      lnWidth = float(kdLst[4]);
      lnColr = kdLst[5]
      kdCircle = plt.Circle((xCntr,yCntr), radC, fill=False,
                            lw=lnWidth, edgecolor=lnColr)
      ax.add_patch(kdCircle)
      print("  circ:  ", xCntr, yCntr, radC, lnWidth, lnColr)
      
    if kdLst[0] == "LN":           #line (normal)
      x1 = extract_value(kdLst[1]); y1 = extract_value(kdLst[2])
      x2 = extract_value(kdLst[3]); y2 = extract_value(kdLst[4])
      #x1 = float(kdLst[1]); y1 = float(kdLst[2])
      #x2 = float(kdLst[3]); y2 = float(kdLst[4])
      XX = [x1, x2]; YY = [y1, y2]
      lnWidth = float(kdLst[5]) 
      lnAttr = kdLst[6]
      ax.plot(XX, YY, lnAttr, lw=lnWidth)
      print("  line:  ", XX, YY)
    
    if kdLst[0] == "TX":           #text
      xT = float(kdLst[1]); yT = float(kdLst[2])
      txtStrgRaw = kdLst[3]
      tsLth = len(txtStrgRaw) - 1
      if tsLth > 0:
        txtStrg = txtStrgRaw[1:tsLth]
      else:
        txtStrg = txtStrgRaw
      txtSize = float(kdLst[4])
      if txtStrgRaw[0] == "{":
        fStyle = "italic"
      else:
        fStyle = "normal"
      ax.text(xT, yT, txtStrg, size=txtSize, style=fStyle)
              #  style="italic", ha="center") 
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
