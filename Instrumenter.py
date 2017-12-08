import os
import re
import argparse
outputFileName = "SimpleC.nc"
declarations = ['int', 'uint8_t', 'uin16_t', 'bool', 'uint32_t', 'components']

METACHAR = "##"
#table that maps variables to ids
varIdTable = {}
varId = 0;
addLabelBlock = []

def setLabelCall(var, label):
    varid = varIdTable[var]
    callString = "call LabelServer.addLabel(" + str(varid) + ", "+str(label)\
                 +");\n"
    return callString

def addLabelCall(var, label):
    varid = varIdTable[var]
    callString = "call LabelServer.modifyLabel(" + str(varid) + ", "+str(label)\
                 +");\n"
    return callString


def checkTransferCall(src, dest):
    srcid = varIdTable[src]
    destid = varIdTable[dest]
    callString = "call LabelServer.checkTransfer("+str(srcid)+","\
                 +str(destid)+")"
    return callString


def checkTransferConditional(calls,line):
    cond = ""
    for call in calls:
        cond = cond + "("+ call + " == SUCCESS )&&"
    cond = cond.strip("&&")
    toadd = "if ("+cond+"){ "+line+";} else {dbg(\"Boot\",\"Cannot execute "+line+"\");}"
    return toadd

def startPass1(inFile):
    line = inFile.readline()
    if line.find("module")== -1 :
        print "Error: This is not a module file"
        exit(0)
    global outputFileName
    outf = open(outputFileName,"w")
    printandwrite(outf, line)
    pass1(inFile,outf)
    outf.close()

    
    
    
def isDeclaration(line):
    line = line.strip().strip(";")
    tokens = re.split("[\t ]+",line)
    if len(tokens)>0 and tokens[0] in declarations:
        return True
    else:
        return False
    
def isAssignment(line):
    if line.find("=") != -1:
       return True
    else:
       return False

def isInterfaceCall(line):
    if line.find("call") != -1:
        return True
    else:
        return False


def isBootEventDefinition(line):
    line = line.strip()
    if line.find('Boot.booted()') != -1:
        return True
    else:
        return False


def handleDeclaration(line):
    global varId;
    outputLine = line
    outputLine = re.sub(METACHAR+"[0-9,]+","",outputLine)
    #print outputLine
    line = line.strip().strip(';')
    tokens = re.split(" +",line)
    if(len(tokens) != 2):
        print "[Error] Multiple declarations in same line"
        exit(0)
    if line.find(METACHAR) == -1:
        return
    varName = tokens[1].split(METACHAR)[0]
    varLabels=tokens[1].split(METACHAR)[1]
    labelList = varLabels.split(",")
    varIdTable[varName] = varId;
    for varLabel in labelList:
        addLabelBlock.append(setLabelCall(varName,varLabel))
    varId = varId + 1
    return outputLine


    
def handleSpecification(file):
    global varId
    toret = ""
    line = file.readline()
    while line.find("implementation") == -1:
        outputLine = line
        outputLine = re.sub("##[0-9,]+","",outputLine);
        toret  = toret + outputLine
        if line.find("module") !=-1 :
            continue
        if line.find("uses interface") != -1 and line.find(METACHAR)!=-1:
            line = line.strip().strip(';')
            tokens = re.split("[ \t]+",line)
            interface = tokens[2].split(METACHAR)[0]
            labelstr = tokens[2].split(METACHAR)[1]
            labels = labelstr.split(",")
            varIdTable[interface] = varId
            varId = varId+1
            for label in labels:
                addLabelBlock.append(setLabelCall(interface,label))
        line = file.readline()
    toret = toret + line
    return toret
    
def handleBootEvent(line):
    toret = ""
    for addLabelCall in addLabelBlock:
        toret=toret + addLabelCall +"\n"
    toret = toret + "dbg(\"Boot\",\"labels setup for all variables\");"
    return toret

    

def handleAssignment(line):
    outputline = line
    line  = line.strip().strip(';')
    tokens = line.split("=")
    lhs = tokens[0].strip()
    toret = ""
    rhslist = tokens[1].strip().split(" ")
    for rhs in rhslist:
        rhs = rhs.strip()
        try:
            float(rhs)
        except ValueError:
            if (rhs in varIdTable):
                toret = toret + (addLabelCall(lhs, rhs))
    if toret == "":
        return ""
    else:
        return toret

def handleInterfaceCall(line):
    outputline = line
    line = line.strip().strip(';')
    call = line.split("call")[1].strip()
    interface = call.split(".")[0]
    params = call.split("(")[1].split(")")[0].split(", ")
    transferCalls = []
    for param in params:
        param = param.strip()
        if interface in varIdTable and param in varIdTable:
             transferCalls.append(checkTransferCall(param, interface))
    if len(transferCalls) != 0:
        return checkTransferConditional(transferCalls,line)
    else:
        return outputline
    

def printandwrite(outfile, str):
    print str
    outfile.write(str+os.linesep)
    
def pass1(inFile,outfile):
#    print "In Pass 1"
    specs =  handleSpecification(inFile)
    print specs
    outfile.write(specs)
    print specs
    global outputFileName
    outFile = open(outputFileName,"w")
    for line in inFile:
        if isAssignment(line):
            t =  handleAssignment(line)
            printandwrite(outfile,t)
            printandwrite(outfile, line)
            
        elif isInterfaceCall(line):
            printandwrite(outfile, handleInterfaceCall(line))
        elif isDeclaration(line):
            printandwrite(outfile, handleDeclaration(line)  )
        elif isBootEventDefinition(line):
            printandwrite(outfile, line)
            printandwrite(outfile, handleBootEvent(line))
        else:
            printandwrite(outfile, line )
        
        
if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument("input", help = "The input nesC file")
    argparser.add_argument("-o","--output-file",help = "Name of the output file")
    args = argparser.parse_args()
    if(args.output_file):
        outputFileName = args.output-file
    f = open(args.input, "r+")
    startPass1(f)
    print varIdTable
