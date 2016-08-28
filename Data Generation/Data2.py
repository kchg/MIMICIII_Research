# !usr/bin/env Python3

import os
import shutil
import sys
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as MP
from matplotlib.ticker import FormatStrFormatter


# Function to get the median of a list.
def median(L):
    print(len(L))
    print(type(len(L)))
    print (L)
    if len(L) < 1:
        return None
    
    if len(L) %2 == 1:
        return L[((len(L)+1)/2)-1]
    else:
        return float(sum(L[(len(L)/2)-1:(len(L)/2)+1]))/2.0


# Define a list to store all values of each measurement.
L = [[[],[]], # Albumin
     [[],[]], # ALP
     [[],[]], # ALT
     [[],[]], # AST
     [[],[]], # Bilirubin
     [[],[]], # BUN
     [[],[]], # Cholesterol
     [[],[]], # Creatinine
     [[],[]], # DiasABP
     [[],[]], # FiO2
     [[],[]], # GCS
     [[],[]], # Glucose
     [[],[]], # HCO3
     [[],[]], # HCT
     [[],[]], # HR
     [[],[]], # K
     [[],[]], # Lactate
     [[],[]], # Mg
     [[],[]], # MAP
     [[],[]], # MechVent
     [[],[]], # Na
     [[],[]], # NIDiasABP
     [[],[]], # NIMap
     [[],[]], # NISysABP
     [[],[]], # PaCO2
     [[],[]], # PaO2
     [[],[]], # pH
     [[],[]], # Platelets
     [[],[]], # RespRate
     [[],[]], # SaO2
     [[],[]], # SysABP
     [[],[]], # Temp
     [[],[]], # TropI
     [[],[]], # TropT
     [[],[]], # Urine
     [[],[]], # WBC
     [[],[]]] # Weight
Names = ['Albumin','ALP','ALT','AST','Bilirubin','BUN','Cholesterol','Creatinine',
         'DiasABP','FiO2','GCS','Glucose','HCO3','HCT','HR','K','Lactate','Mg',
         'MAP','MechVent','Na','NIDiasABP','NIMap','NISysABP','PaCO2','PaO2',
         'pH','Platelets','RespRate','SaO2','SysABP','Temp','TropI','TropT',
         'Urine','WBC','Weight']

# Store all patient's subject_id's and if they died or not.
Patients = {}
with open('Outcomes-a.txt', "r") as file:
    #print(file.name, file.tell())
    for line in file.readlines():
        #print('Hey')
        fields = line.split(',')
        Patients[str(fields[0])] = str(fields[5]).strip()

# Change directory to 'set-a'.
os.chdir("set-a")
path = "/Users/tvaughan94/Desktop/Research/Patient/set-a"

# Loop through all files in the directory 'set-a'.
files = os.listdir(os.getcwd())
numFiles = 0
sys.stderr.write("Starting Calculations\n")
for file in files:
    if(file != ".DS_Store"):
        Death = 0
        numFiles += 1
        f = open(file,'r')
        
        # Determine if the patient survived ICU stay or not.
        LINES = f.readlines()
        l = LINES[1]
        fields = l.split(',')
        if(Patients[str(fields[2]).strip()] == "1"):
            Death = 1
        
        
        # Loop through all lines in the file, formatting them as needed.
        for l in LINES[6:]:
            # Split each line into three fields.
            fields = l.split(',')
        
            if(float(fields[2]) >= 0):
                if(fields[1] == "Albumin"):
                    if(Death):
                        L[0][1].append(float(fields[2]))
                    else:
                        L[0][0].append(float(fields[2]))

                elif(fields[1] == "ALP"):
                    if(Death):
                        L[1][1].append(float(fields[2]))
                    else:
                        L[1][0].append(float(fields[2]))

                elif(fields[1] == "ALT"):
                    if(Death):
                        L[2][1].append(float(fields[2]))
                    else:
                        L[2][0].append(float(fields[2]))

                elif(fields[1] == "AST"):
                    if(Death):
                        L[3][1].append(float(fields[2]))
                    else:
                        L[3][0].append(float(fields[2]))

                elif(fields[1] == "Bilirubin"):
                    if(Death):
                        L[4][1].append(float(fields[2]))
                    else:
                        L[4][0].append(float(fields[2]))
                
                elif(fields[1] == "BUN"):
                    if(Death):
                        L[5][1].append(float(fields[2]))
                    else:
                        L[5][0].append(float(fields[2]))

                elif(fields[1] == "Cholesterol"):
                    if(Death):
                        L[6][1].append(float(fields[2]))
                    else:
                        L[6][0].append(float(fields[2]))

                elif(fields[1] == "Creatinine"):
                    if(Death):
                        L[7][1].append(float(fields[2]))
                    else:
                        L[7][0].append(float(fields[2]))

                elif(fields[1] == "DiasABP"):
                    if(Death):
                        L[8][1].append(float(fields[2]))
                    else:
                        L[8][0].append(float(fields[2]))

                elif(fields[1] == "FiO2"):
                    if(Death):
                        L[9][1].append(float(fields[2]))
                    else:
                        L[9][0].append(float(fields[2]))

                elif(fields[1] == "GCS"):
                    if(Death):
                        L[10][1].append(float(fields[2]))
                    else:
                        L[10][0].append(float(fields[2]))

                elif(fields[1] == "Glucose"):
                    if(Death):
                        L[11][1].append(float(fields[2]))
                    else:
                        L[11][0].append(float(fields[2]))

                elif(fields[1] == "HCO3"):
                    if(Death):
                        L[12][1].append(float(fields[2]))
                    else:
                        L[12][0].append(float(fields[2]))

                elif(fields[1] == "HCT"):
                    if(Death):
                        L[13][1].append(float(fields[2]))
                    else:
                        L[13][0].append(float(fields[2]))

                elif(fields[1] == "HR"):
                    if(Death):
                        L[14][1].append(float(fields[2]))
                    else:
                        L[14][0].append(float(fields[2]))

                elif(fields[1] == "K"):
                    if(Death):
                        L[15][1].append(float(fields[2]))
                    else:
                        L[15][0].append(float(fields[2]))

                elif(fields[1] == "Lactate"):
                    if(Death):
                        L[16][1].append(float(fields[2]))
                    else:
                        L[16][0].append(float(fields[2]))

                elif(fields[1] == "Mg"):
                    if(Death):
                        L[17][1].append(float(fields[2]))
                    else:
                        L[17][0].append(float(fields[2]))

                elif(fields[1] == "MAP"):
                    if(Death):
                        L[18][1].append(float(fields[2]))
                    else:
                        L[18][0].append(float(fields[2]))

                elif(fields[1] == "MechVent"):
                    if(Death):
                        L[19][1].append(float(fields[2]))
                    else:
                        L[19][0].append(float(fields[2]))

                elif(fields[1] == "Na"):
                    if(Death):
                        L[20][1].append(float(fields[2]))
                    else:
                        L[20][0].append(float(fields[2]))

                elif(fields[1] == "NIDiasABP"):
                    if(Death):
                        L[21][1].append(float(fields[2]))
                    else:
                        L[21][0].append(float(fields[2]))

                elif(fields[1] == "NIMap"):
                    if(Death):
                        L[22][1].append(float(fields[2]))
                    else:
                        L[22][0].append(float(fields[2]))

                elif(fields[1] == "NISysABP"):
                    if(Death):
                        L[23][1].append(float(fields[2]))
                    else:
                        L[23][0].append(float(fields[2]))

                elif(fields[1] == "PaCO2"):
                    if(Death):
                        L[24][1].append(float(fields[2]))
                    else:
                        L[24][0].append(float(fields[2]))
            
                elif(fields[1] == "PaO2"):
                    if(Death):
                        L[25][1].append(float(fields[2]))
                    else:
                        L[25][0].append(float(fields[2]))

                elif(fields[1] == "pH"):
                    if(Death):
                        L[26][1].append(float(fields[2]))
                    else:
                        L[26][0].append(float(fields[2]))

                elif(fields[1] == "Platelets"):
                    if(Death):
                        L[27][1].append(float(fields[2]))
                    else:
                        L[27][0].append(float(fields[2]))

                elif(fields[1] == "RespRate"):
                    if(Death):
                        L[28][1].append(float(fields[2]))
                    else:
                        L[28][0].append(float(fields[2]))

                elif(fields[1] == "SaO2"):
                    if(Death):
                        L[29][1].append(float(fields[2]))
                    else:
                        L[29][0].append(float(fields[2]))

                elif(fields[1] == "SysABP"):
                    if(Death):
                        L[30][1].append(float(fields[2]))
                    else:
                        L[30][0].append(float(fields[2]))

                elif(fields[1] == "Temp"):
                    if(Death):
                        L[31][1].append(float(fields[2]))
                    else:
                        L[31][0].append(float(fields[2]))

                elif(fields[1] == "TropI"):
                    if(Death):
                        L[32][1].append(float(fields[2]))
                    else:
                        L[32][0].append(float(fields[2]))

                elif(fields[1] == "TropT"):
                    if(Death):
                        L[33][1].append(float(fields[2]))
                    else:
                        L[33][0].append(float(fields[2]))

                elif(fields[1] == "Urine"):
                    if(Death):
                        L[34][1].append(float(fields[2]))
                    else:
                        L[34][0].append(float(fields[2]))

                elif(fields[1] == "WBC"):
                    if(Death):
                        L[35][1].append(float(fields[2]))
                    else:
                        L[35][0].append(float(fields[2]))

                elif(fields[1] == "Weight"):
                    if(Death):
                        L[36][1].append(float(fields[2]))
                    else:
                        L[36][0].append(float(fields[2]))
        f.close()
        if(numFiles%500 == 0):
            sys.stderr.write("Finished {} files.\n".format(numFiles))

# Display when finished with all files.
sys.stderr.write("Finished {} files.\n".format(numFiles))

print("Measurement,Min,Q1,Mean,Q3,Max,Median,StdDev,Death")

# Sort the lists, then calculate the Mean, Median, Std Deviation, and Quartiles.
plotNum = 1
for i in range(0,37):
    sys.stderr.write("On measurement {}:\n".format(i))
    if(i != 19 and (len(L[i][0]) > 0 or len(L[i][1]) > 0)):
        
        # Standardize the distribution.
        if(len(L[i][0]) > 0):
            sHi = np.percentile(L[i][0], 97.5)
            sLo = np.percentile(L[i][0], 2.5)
        else:
            sHi = None
        if(len(L[i][1]) > 0):
            dHi = np.percentile(L[i][1], 97.5)
            dLo = np.percentile(L[i][1], 2.5)
        else:
            dHi = None

        if(dHi is None):
            HI = sHi
            LO = sLo
        elif(sHi is None):
            HI = dHi
            LO = dLo
        else:
            LO = min(sLo, dLo)
            HI = max(sHi, dHi)

        for x in range(0,2):
            L[i][x].sort()
            if(len(L[i][x]) > 0):
                SD = np.std(L[i][x])
                MEAN = np.mean(L[i][x])
                MEDIAN = median(L[i][x])
                Q1 = np.percentile(L[i][x], 25)
                Q3 = np.percentile(L[i][x], 75)
        
                #HI = np.percentile(L[i][x], 97.5)
                #LO = np.percentile(L[i][x], 2.5)
                MIN = L[i][x][0]
                MAX = L[i][x][len(L[i][x])-1]

                # Print the statistics to the output file.
                print("{},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.5f},{}".format(Names[i],MIN,Q1,MEAN,Q3,MAX,MEDIAN,SD,x))
        
                # Calculate the bins for the histogram.
                step = (HI - LO)/30
                binTick = LO
                bins = []
                while(binTick <= HI):
                    bins.append(binTick)
                    binTick += step
        
                # Plot the histogram with the given data and bins.
                fig, ax = plt.subplots()
                counts, bins, patches = plt.hist(L[i][x], bins = bins)
        
                # Set the x ticks to match the histogram's bins.
                ax.set_xticks(bins)
                ax.set_xticklabels(bins,rotation=90)
                ax.xaxis.set_major_formatter(FormatStrFormatter('%0.1f'))
        
                # Color the bins according to their probability.
                for patch, rightside, leftside in zip(patches,bins[1:],bins[:-1]):
                    if rightside < Q1:
                        patch.set_facecolor('red')
                    elif leftside > Q3:
                        patch.set_facecolor('orange')
                    else:
                        patch.set_facecolor('yellow')
        
                # Set up the legend for the graph.
                #r_patch = MP.Patch(color='red',label='Below Q1')
                #y_patch = MP.Patch(color='yellow',label='Inner 50%')
                #o_patch = MP.Patch(color='orange',label='Above Q3')
                #plt.legend(handles = [r_patch,y_patch,o_patch])

                # Determine the subplot the graph belongs to.
                #if(x == 0):
                #    plt.subplot(211)
                #else:
                #    plt.subplot(212)
                
                # Set up the graph to be plotted.
                plt.xlim(LO, HI)
                plt.title('Measurement: {} - Distribution\nDeath: {}\n2.5%:{:.1f}  Q1:{:.1f}  Mean:{:.1f}  Q3:{:.1f}  97.5%:{:.1f}'.format(Names[i],x,LO,Q1,MEAN,Q3,HI))
                plt.xlabel('Distribution of {}'.format(Names[i]))
                plt.ylabel('Count')
                plt.subplots_adjust(bottom = 0.15)
                plt.show()
            else:
                print("{},No Values in List for Death:{}".format(Names[i],x))
    elif(i == 19):
        print("MechVent,Value is always 1.00")
    else:
        print("None,No measurements of given value type.")



os.chdir('..')
