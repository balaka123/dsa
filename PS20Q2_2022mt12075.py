# This is Python code for DSA Assignment # PS20 #Q2

# Pre-Req for running the code - Keep input file inputPS20Q2.txt in same directory where code is present.
# For running the code from command line execute following command: python PS20Q2_2022mt12075.py
# After running the code the output file outputPS20Q2.txt will be created in same location as input file.

import os
from operator import itemgetter

fpath=os.getcwd()
print("Current working directory is - ", fpath)
ifile = fpath + "\inputPS20Q2.txt"
ofile = fpath + "\outputPS20Q2.txt"

print("Input File:", ifile)
print("Output File:", ofile)

# Input file validation#1 : Check if number of rows is 3
with open(ifile, 'r') as fc:
    lineCnt = len(fc.readlines())
    if lineCnt != 3:
        print("Input file does not contain 3 rows")
        exit(1)

# Input file validation#2 : Check the lines contains correct tagging of data
with open(ifile, 'r') as ft:
    for rCnt in range(3):
        fline = ft.readline()
        ftyp = fline.split(":")
        # print(ftyp[0])
        if rCnt == 0:
            if ftyp[0] != "Products":
                print("1st row of input file should contain the list of products and should start with 'Products'")
                exit(1)
        elif rCnt == 1:
            if ftyp[0] != "Staging":
                print("2nd row of input file should start with 'Staging' as it contains the staging time for products")
                exit(1)
        elif rCnt == 2:
            if ftyp[0] != "Photo":
                print("3rd row of input file should start with 'Photo' as it contains the photoshoot time for products")
                exit(1)

# Read and parse the input file into list1
with open(ifile, "r") as file:
    data = file.readlines()
    list1 = []
    for line in data:
        word = line.split(":")
        list1.append(word[1])
    # print("list1 after parsing input file : " + str(list1))

# Cleanup list1 - remove \n and spaces
list2 = [x.replace('\n', '').replace(' ','').split('/') for x in list1]
# print("list2 after cleaning up list1 : " + str(list2))

# Input file validation#3 : Check if staging and photo timing is provided for all products
if len(list2[0]) != len(list2[1]) or len(list2[0]) != len(list2[2]) or len(list2[1]) != len(list2[2]):
    print("Each product should have related staging and photo timings")
    print("Number of products and number of timings are out of order")
    exit(1)

# Covert time value from string to int
for i in range(len(list2[1])):
    list2[1][i] = int(list2[1][i])
    list2[2][i] = int(list2[2][i])
#print("list2 after converting time to integer : " + str(list2))

# Transpose row to column
list3 = []
for i in range(len(list2[0])):
    # print(i)
    row = []
    for item in list2:
        # appending to new list with values and index positions
        # i contains index position and item contains values
        row.append(item[i])
    list3.append(row)
#print("list3 after transposing list2 : " + str(list3))
print("Working list : " + str(list3))

# Sort the list3 on staging time
stagelist=(sorted(list3, key=itemgetter(1)))
print("staging list after sorting on staging time : " + str(stagelist))

# n is the number of product to process
n = len(stagelist)
print("Number of product to process: " + str(n))

prodSeq = ''                                       # prodSeq will store the sequence of staging and photoshoot
for i in range(n):
    prodSeq = prodSeq + stagelist[i][0]+', '

finProdSeq = prodSeq[0:len(prodSeq)-2]
print("Product Sequence for Staging and Photoshoot : " + finProdSeq)

class ProductRecord:

    def __init__(self, prod, stageTm, photoTm):
        self.prod = prod
        self.stageTm = int(stageTm)
        self.photoTm = int(photoTm)
        self.stageSTm = 0
        self.stageETm = 0
        self.photoSTm = 0
        self.photoETm = 0

prodlist = []
XIdleTime = 0

# Create object of class ProductRecord with the provided data in input file
for i in range(len(stagelist)):
        prodlist.append(ProductRecord(stagelist[i][0], stagelist[i][1], stagelist[i][2]))

for obj in prodlist:
        print(obj.prod, obj.stageTm, obj.photoTm, sep=' ')

# Populating StageStartTime StageEndTime PhotoStartTime PhotoEndTime
for i in range(len(prodlist)):
    if i == 0:
        XIdleTime = prodlist[i].stageTm
        prodlist[i].stageSTm = 0
        prodlist[i].stageETm = prodlist[i].stageSTm + prodlist[i].stageTm
        prodlist[i].photoSTm = prodlist[i].stageETm
        prodlist[i].photoETm = prodlist[i].photoSTm + prodlist[i].photoTm
    else:
        prodlist[i].stageSTm = prodlist[i - 1].stageETm
        prodlist[i].stageETm = prodlist[i].stageSTm + prodlist[i].stageTm
        if prodlist[i-1].photoETm >= prodlist[i].stageETm:
            prodlist[i].photoSTm = prodlist[i - 1].photoETm
        else:
            XIdleTime = XIdleTime + (prodlist[i].stageETm - prodlist[i-1].photoETm)
            prodlist[i].photoSTm = prodlist[i].stageETm
        prodlist[i].photoETm = prodlist[i].photoSTm + prodlist[i].photoTm

print("Product information : ")
print("Product", "StageTime", "PhotoTime", "StageStartTime", "StageEndTime", "PhotoStartTime", "PhotoEndTime", sep="|")
for obj in prodlist:
    print(obj.prod, obj.stageTm, obj.photoTm, obj.stageSTm, obj.stageETm, obj.photoSTm, obj.photoETm, sep="|")

print("Product Sequence: " + finProdSeq)
print("Total time to complete photoshoot: " + str(prodlist[len(prodlist) - 1].photoETm))
print("Idle time for Xavier: " + str(XIdleTime))

f = open(ofile, "w")                                                # writing to output file
f.write("Product Sequence: " + finProdSeq + "\n")
f.write("Total time to complete photoshoot: " + str(prodlist[len(prodlist) - 1].photoETm) + "\n")
f.write("Idle time for Xavier: " + str(XIdleTime))
f.close()