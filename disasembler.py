
def isEmptyLine(line):  # removes empty line
    return line == ''

def btd(n): # converts binary to decimal
    return int(n,2)


def cinstruction(line):   # logic for c instruction
    a = line[0]
    comp = ""
    dest = ""
    jump = ""

    compTable = {
        "101010": "0",
        "111111": "1",
        "111010": "-1",
        "001100": "D",
        "001101": "!D",
        "001111": "-D",
        "011111": "D+1",
        "001110": "D-1"
    }
    destTable = {
        "000": "null",
        "001": "M",
        "010": "D",
        "011": "MD",
        "100": "A",
        "101": "AM",
        "110": "AD",
        "111": "AMD"
    }
    jumpTable = {"000": "null",
                 "001": "JGT",
                 "010": "JEQ",
                 "011": "JGE",
                 "100": "JLT",
                 "101": "JNE",
                 "110": "JLE",
                 "111": "JMP"
    }
    if(a == '0'): # each one is different so a dictionary is unoptimal
        if line[1:7] == '110000':
            comp = "A"
        if line[1:7] == "110001":
            comp = "!A"
        if line[1:7] == "110011":
            comp = "-A"
        if line[1:7] == "110111":
            comp = "A+1"
        if line[1:7] == "110010":
            comp = "A-1"
        if line[1:7] == "000010":
            comp = "D+A"
        if line[1:7] == "010011":
            comp = "D-A"
        if line[1:7] == "000111":
            comp = "A-D"
        if line[1:7] == "000000":
            comp = "D&A"
        if line[1:7] == "010101":
            comp = "D|A"
    elif(a == '1'):   # logic for if the a bit is set to 1
        if line[1:7] == '110000':
            comp = "M"
        if line[1:7] == "110001":
            comp = "!M"
        if line[1:7] == "110011":
            comp = "-M"
        if line[1:7] == "110111":
            comp = "M+1"
        if line[1:7] == "110010":
            comp = "M-1"
        if line[1:7] == "000010":
            comp = "D+M"
        if line[1:7] == "010011":
            comp = "D-M"
        if line[1:7] == "000111":
            comp = "M-D"
        if line[1:7] == "000000":
            comp = "D&M"
        if line[1:7] == "010101":
            comp = "D|M"
    if comp == '':
        comp = compTable[line[1:7]]

    dest = destTable[line[7:10]]
    jump = jumpTable[line[10:]]

    if(jump =='null') and (dest == 'null'):
        return comp
    if(jump =='null'):
        return dest + '=' + comp
    if(dest == 'null'):
        return comp + ';' + jump
    return dest + '=' + comp + ';' + jump

# File I/O
hackFileName = input("Enter .hack file name: ") 
try:
    file = open(hackFileName)
except OSError:
    print("Error with opening file. ")
    quit()

file.close()
file = open(hackFileName)

fileNameRaw = hackFileName.replace(".hack", "")
asmOUT = open(fileNameRaw + ".asm", "w")

for line in file:
    line = line.strip()
    if isEmptyLine(line):
        continue
    if line[0] == '0':
        bin = '@' + str(btd(line[1:]))
        asmOUT.write(bin + '\n')
        continue
    if line[1] == '1':
        bin = cinstruction(line[3:])
        asmOUT.write(bin + '\n')
        continue


asmOUT.close()
file.close()
