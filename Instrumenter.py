import argparse
outputFile = ""
declarations = ['int', 'uint8_t', 'uin16_t', 'bool', 'uint32_t', 'components']

#table that maps variables to ids
varIdTable = {}
varIdTable['a'] = 10


def setLabelCall(var, label):
    varid = varIdTable[var]
    callString = "LabelServer.addLabel(" + str(varid) + ", "+str(label)\
                 +")"
    return callString

def checkTransferCall(src, dest):
    srcid = varIdTable[src]
    destid = varIdTable[dest]
    callString = "LabelServer.checkTransfer("+str(srcid)+","\
                 +str(destid)+")"
    return callString

def startPass1(inFile):
    line = inFile.readline()
    if line.find("module")== -1 :
        print "Error: This is not a module file"
        exit(0)
    pass1(inFile)
    
def isDeclaration(line):
    isdeclaration = False
    for k in declarations:
        if line.find(k) != -1:
            isdeclaration = True
            break
    return isdeclaration

def isAssignment(line):
    return True

def isInterfaceCall(line):
    return True



def pass1(inFile):
    print "In Pass 1"
    for line in inFile:
        
if __name__ == '__main__':
    global outputFile
    argparser = argparse.ArgumentParser()
    argparser.add_argument("input", help = "The input nesC file")
    argparser.add_argument("-o","--output-file",help = "Name of the output file")
    args = argparser.parse_args()
    if(args.output_file):
        outputFile = args.output-file
    f = open(args.input, "r+")
    startPass1(f)
