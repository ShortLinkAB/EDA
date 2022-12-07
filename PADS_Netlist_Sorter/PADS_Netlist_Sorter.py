from datetime import datetime
from collections import OrderedDict

import re,subprocess,sys
now = datetime.now()

dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

infile = sys.argv[1] #argument input: file to be sorted
script = sys.argv[0] #argument input: script name (to be able to print svn revision of script)

print("PADS Netlist Sorter")
print("Read file: " + infile)
print("Only sorts between *NET* and *MISC*")

file1 = open(infile, 'r')
Lines = file1.readlines()

inNetSection = False #Are we currently in the section of the file listing nets?
currentNet = "" #Will contain the current net that has its nodes listed.

nodeList = dict();

# Build nodelist
for line in Lines:
    line = line.strip() #remove trailing endline
    #If we are not currently in the part of the file defining nets, all we need to do is check if we should enter that state.
    if inNetSection == False:
        if ("*NET*" in line):
            inNetSection = True
        continue        
    
    #Check if we should exit the section defining nets
    if ("*MISC*" in line) and ("MISCELLANEOUS PARAMETERS" in line):
        inNetSection = False
        continue
    
    if ("*END*" in line):
        inNetSection = False
        continue
    
    #Check if the row represents a new net name
    if "*SIGNAL*" in line:
        currentNet = line[9:] 
        #Check that the signal does not already exist. If it does, something is wrong with the parsing.
        if currentNet in nodeList:            
            print("Error! Signal already created!")
            exit()
        nodeList[currentNet] = []
        continue
    
    #If none of the above is true, the row contains new nodes to be added.
    nodeList[currentNet].extend(line.split())
    nodeList[currentNet].sort()
    
    #print(line)
    
# Print nodelist


with open('sorted_'+infile, 'w') as f:
    print("Sorted netlist from PADS", file=f)
    print("Input file: " + infile, file=f)
    print("Script run at: ", dt_string, file=f)
    print ("SVN version of " + script + ": " + subprocess.check_output(["svnversion", script]).decode(),end="", file=f)
    print ("SVN version of netlist file: "+ subprocess.check_output(["svnversion", infile]).decode(),end="", file=f)
    
    #Order by value (e.g. nodelist), not by net name.    
    sortedNodeList = OrderedDict(sorted(nodeList.items(), key=lambda t: t[1]))

    for net in sortedNodeList:        
        print(net + " - ", end='', file=f)
        print(sortedNodeList[net], file=f)


print("Script execution complete")
