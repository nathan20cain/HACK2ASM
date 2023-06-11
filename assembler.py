import re # for multi splitting


def isLabel(c):  # checks if label if it has ()
    if c == "":
        return False
    if str(c)[0] == '(' and str(c)[-1] == ')':
        return True
    else:
        return False


def positiveInteger(d): # checks if d is a positive int
    return d.isdigit()


def validSymbolChars(b, symbolTable): #checks if b is in the symbol tble
    return b in symbolTable

def isNotNumber(g): # checks if it is not a number
    return (not g.isdigit())

def isDigit(d): # checks if it is a digit
    return d.isdigit()

def isValidAInstruction(line, symbolTable): # checks if it is a valid A instruction
    if line == "":
        return False
    if line[0] != '@':
        return False
    dropAt = line[1:]
    if positiveInteger(dropAt):
        return True
    if isDigit(dropAt[0]):
        return False
    if validSymbolChars(dropAt, symbolTable):
        return True
    return True

def removeParenthesis(c): # removes parenthesis from labels
    return c[1:-1]

def removeCommentsAndWhitespace(l):  # removes comments and any spaces, tabs, \n
    retBurner = l.strip()
    ret = retBurner.replace(" ", "")
    for x in range(len(ret)):
        if ret[x] == '/':
            return ret[:x]
    return ret

def isInstruction(clean):   # checks if it either a c or a instruction
    if clean is None or clean == "":
        return False
    if clean[0] == '@':
        return True
    for let in str(clean):
        if let == '/':
            return False
        if let == '=':
            return True


def aInstruction(line):   # logic for A instruction
    dropAt = line[1:]
    if positiveInteger(dropAt):
        bin = format(int(dropAt), '015b')
        return '0' + bin
    addr = symbolTable[dropAt]
    bin = format(addr, '015b')
    return '0' + bin

def createSymbolTable(fileN):   # creates the symbol table
    symbolTable = {}
    symbolTable["SP"] = 0
    symbolTable["LCL"] = 1
    symbolTable["ARG"] = 2
    symbolTable["THIS"] = 3
    symbolTable["THAT"] = 4
    for r in range(16):
        symbolTable["R" + str(r) ] = r

    symbolTable["SCREEN"] = 16384
    symbolTable["KBD"] = 24576

    file = open(fileN)
    pc = 0

    for line in file:  # first pass through
        clean = removeCommentsAndWhitespace(line)
        if isLabel(clean):
            label = removeParenthesis(clean)
            if not label in symbolTable:
                symbolTable[label] = pc
        if isInstruction(clean):
            pc = pc + 1
    file.close()

    file = open(fileN)
    nextAddress = 16
    for line in file:  # second pass through
        clean = removeCommentsAndWhitespace(line)
        if (isValidAInstruction(clean, symbolTable)):
            AInstructionVal = clean.replace("@", "")
            if (isNotNumber(AInstructionVal) and AInstructionVal not in symbolTable):
                symbolTable[AInstructionVal] = nextAddress
                nextAddress = nextAddress + 1

    return symbolTable

def isCInstruction(line):  # checks if it is a C instruction
    if line.count('=') != 1 and line.count(';') != 1:
        return False
    #line.replace(";", "")
    tokens = re.split('=|;', line)
    if len(tokens) < 2 or len(tokens) > 3:
        return False
    if (len(tokens) == 2):
        if '=' in line: #dest and comp
            if tokens[0] not in destTable:
                return False
            if tokens[1] not in compTable:
                return False
        else: #comp and jump
            if tokens[0] not in compTable:
                return False
            if tokens[1] not in jumpTable:
                return False
    else: #dest, comp, jump present
        if tokens[0] not in destTable:
            return False
        if tokens[1] not in compTable:
            return False
        if tokens[2] not in jumpTable:
            return False
    return True


def aBot(cmp):   # sets a bit
    if 'M' in cmp:
        return '1'
    else:
        return "0"

def cInstruction(line):  # c instruction logic
    #line.replace(";", "")
    tokens = re.split('=|;', line)
    a = '0'
    dest = ""
    comp = ""
    jump = ""
    if len(tokens) == 2:
        if '=' in line:  #dest and comp
            a = aBot(tokens[1])
            dest = destTable[tokens[0]]
            comp = compTable[tokens[1]]
            jump = "000"
        else: # comp and jump
            a = aBot(tokens[0])
            dest = "000"
            comp = compTable[tokens[0]]
            jump = jumpTable[tokens[1]]
    else: # dest, comp, jump present
        a = aBot(tokens[1])
        dest = destTable[ tokens[0]]
        comp = compTable[ tokens[1]]
        jump = jumpTable[ tokens[2]]

    prefix = "111" + a
    return prefix + comp + dest + jump

def isEmptyLine(line):   # if its an empty line
    return line == ''


#File I/O
asmFileName = input("Enter asm file name:")
try:
    file = open(asmFileName)
except OSError:
    print("Error with opening file. ")
    quit()

file.close()
symbolTable = createSymbolTable(asmFileName)

compTable = {
    "0" : "101010",
    "1" : "111111",
    "-1" : "111010",
    "D" : "001100",
    "A" : "110000",
    "M" : "110000",
    "!D" : "001101",
    "!A" : "110001",
    "!M" : "110001",
    "-D" : "001111",
    "-A" : "110011",
    "-M" : "110011",
    "D+1" : "011111",
    "1+D" : "011111",
    "1+A" : "110111",
    "A+1" : "110111",
    "1+M" : "110111",
    "M+1" : "110111",
    "D-1" : "001110",
    "A-1" : "110010",
    "M-1" : "110010",
    "D+A" : "000010",
    "A+D" : "000010",
    "D+M" : "000010",
    "M+D" : "000010",
    "D-A" : "010011",
    "D-M" : "010011",
    "A-D" : "000111",
    "M-D" : "000111",
    "D&A" : "000000",
    "A&D" : "000000",
    "D&M" : "000000",
    "M&D" : "000000",
    "D|A" : "010101",
    "A|D" : "010101",
    "D|M" : "010101",
    "M|D": "010101"
}
destTable = {
    "null" : "000",
    "M" : "001",
    "D" : "010",
    "MD" : "011",
    "A" : "100",
    "AM" : "101",
    "AD" : "110",
    "AMD" : "111"
}
jumpTable = {"null": "000", "JGT": "001", "JEQ": "010", "JGE": "011", "JLT": "100", "JNE": "101", "JLE": "110",
             "JMP": "111"}

file = open(asmFileName)
fileNameRaw = asmFileName.replace(".asm", "")
binaryFileOut = open(fileNameRaw + ".hack", "w")
for line in file:
    line = removeCommentsAndWhitespace(line)
    if isEmptyLine(line):
        continue
    if '(' in line:
        continue
    if isValidAInstruction(line, symbolTable):
        bin = aInstruction(line)
        binaryFileOut.write(bin + '\n')
        continue
    if isCInstruction(line):
        bin = cInstruction(line)
        binaryFileOut.write(bin + '\n')
        continue
    if line in compTable:
        a = aBot(line)
        bin = "111" + a + compTable[line] + "000" + '000'
        binaryFileOut.write(bin + '\n')
        continue


binaryFileOut.close()
file.close()


