# This is Python code for DSA Assignment # PS20 #1

import os
import random

fpath=os.getcwd()
print("Current working directory is - ", fpath)
ifile = fpath + "\inputPS20Q1.txt"
pfile = fpath + "\promptsPS20Q1.txt"
ofile = fpath + "\outputPS20Q1.txt"

print("Input File:", ifile)
print("Prompt File:", pfile)
print("Output File:", ofile)


class PatientRecord:

    def __init__(self, age, name, Pid):             # Patient Record structure
        self.Patid = str(Pid) + str(age)
        self.name = name
        self.age = int(age)
        self.left = None
        self.right = None


plist = []                                          # list of objects to hold patient records
TestingQueue = []                                   # Queue to maintain the order of patients for testing
lc = 0                                              # Line count of prompt file - needed in error handling message


def left(k):                                        # function to calculate left child position of a node
    return 2 * k + 1


def right(k):                                       # function to calculate right child position of a node
    return 2 * k + 2


# function to max heapify the TestingQueue data - Key is age part of the Patid
# Patid - First 4 bytes contain Pid followed by the age of the patient
def max_heapify(TestingQueue, k, pl):
    l = left(k)
    # print("l: " + str(l))
    r = right(k)
    # print("r: " + str(r))
    # compare key value of kth node with that of left child if left child exists and set largest value accordingly
    if l < pl and int(TestingQueue[l][4:]) > int(TestingQueue[k][4:]):
        largest = l
    else:
        largest = k
    # compare largest key value with right child if right child exists
    if r < pl and int(TestingQueue[r][4:]) > int(TestingQueue[largest][4:]):
        # print("if r <")
        largest = r
    # if kth node is not largest, then swap the kth node with the largest and repeat the process
    if largest != k:
        # print("if largest")
        TestingQueue[k], TestingQueue[largest] = TestingQueue[largest], TestingQueue[k]
        max_heapify(TestingQueue, largest, pl)


# function to build max heap with the TestingQueue data: it will call max_heapify for (TestingQueue length)/2 -1 times
def build_max_heap(TestingQueue):
    n = int((len(TestingQueue) // 2) - 1)
    pl = int(len(TestingQueue))
    for k in range(n, -1, -1):
        max_heapify(TestingQueue, k, pl)


# function to do max heap sort with the TestingQueue data
# it will recursively call max_heapify with heap size decreased by 1 until heap size became 1 i.e.
# it will call max_heapify for as many times as the number of nodes
def max_heap_sort(TestingQueue):
    build_max_heap(TestingQueue)
    m = int(len(TestingQueue)) - 1
    pl = int(len(TestingQueue))
    for k in range(m, 0, -1):
        TestingQueue[0], TestingQueue[k] = TestingQueue[k], TestingQueue[0]
        pl = pl - 1
        # print("pl: " + str(pl))
        max_heapify(TestingQueue, 0, pl)


"""
def upheap(k):
    parent = (k - 1) // 2
    if k > 0 and plist[k].age > plist[parent].age:
        plist[k], plist[parent] = plist[parent], plist[k]
        upheap(parent)
"""


# populate the object of PatientRecord with input file; also push the related Patid to TestingQueue
def registerPatient(name, age):
    plist.append(PatientRecord(age, name, random.randrange(1000, 9999)))
    TestingQueue.append(plist[-1].Patid)


# push the Patid to TestingQueue for prompt file new PatientRecord
# then sort the TestingQueue to maintain the sorting order and write the refreshed queue in output file
def enqueuePatient(PatId):
    TestingQueue.append(PatId)

    # upheap(pl)

    max_heap_sort(TestingQueue)

    f = open(ofile, "a")
    f.write("Refreshed queue: " + "\n")
    for i in range(len(TestingQueue) - 1, -1, -1):
        for obj in plist:
            if obj.Patid == TestingQueue[i]:
                pname = obj.name
        f.write(TestingQueue[i] + ", " + pname + "\n")
    f.write("----------------------------------------------" + "\n\n")
    f.close()


# Delete the Patid from TestingQueue once the patient details is written in output as nextPatient for testing
def dequeuePatient(PatId):
    TestingQueue.remove(PatId)


# Write the patient details to output file in sorted order of age from TestingQueue as requested in the prompt file
def nextPatient():
    nxp = word[1]
    f = open(ofile, "a")
    f.write("---- next patient: " + str(nxp).strip() + " ---------------" + "\n")
    if len(TestingQueue) == 0:
        f.write("No patient is waiting for the testing" + "\n")
        f.write("----------------------------------------------" + "\n\n")
        f.close()
    else:
        if int(nxp) <= int(len(TestingQueue)):
            dplcnt = int(nxp)
        elif int(nxp) > len(TestingQueue):
            dplcnt = int(len(TestingQueue))
            f.write("---- patient waiting is only: " + str(dplcnt) + "\n")
        for k in range(dplcnt):
            ixdel = len(TestingQueue) - 1
            f.write("Next patient for testing is: ")
            for obj in plist:
                if obj.Patid == TestingQueue[ixdel]:
                    pname = obj.name
            f.write(TestingQueue[ixdel] + ", " + pname + "\n")
            dequeuePatient(TestingQueue[ixdel])
        f.write("----------------------------------------------" + "\n\n")
        f.close()


# ############################# Driving Method ###############################

# Parse the input file
with open(ifile, 'r') as f1:
    initList = [line for line in f1]
# print("initList after parsing input file : " + str(initList))

# Cleanup initList - remove \n and spaces
initList2 = [x.replace('\n', '').replace(' ', '').split(",") for x in initList]
print("List from Input File : " + str(initList2))

# Input File Validation: All rows should have 2 values separated by ",".
for i in range(len(initList2)):
    if len(initList2[i]) != 2:
        print("Error! All rows of Input File should have 2 values separated by ','")
        print("Row# " + str(i + 1) + " does not have 2 values")
        exit(1)

# For each record in input file, call registerPatient function to insert it to the PatientRecord and TestingQueue
for i in range(len(initList2)):
    registerPatient(initList2[i][0], initList2[i][1])

# Call max_heap_sort to keep the initial patients queue in sorted order with age
max_heap_sort(TestingQueue)

# Write the initial list of Patient in output file
f = open(ofile, "w")
f.write("---- registered Patient ---------------" + "\n")
f.write("No of patients added: " + str(len(TestingQueue)) + "\n")
f.write("Refreshed queue:" + "\n")

for i in range(len(TestingQueue) - 1, -1, -1):
    for obj in plist:
        if obj.Patid == TestingQueue[i]:
            pname = obj.name
    f.write(TestingQueue[i] + ", " + pname + "\n")

f.write("----------------------------------------------" + "\n\n")
f.close()

# Parse prompt file
with open(pfile, 'r') as promptf:
    for line in promptf:
        lc = lc + 1
        print("Processing prompt file line# " + str(lc) + ": " + str(line))
        word = line.split(":")

        # New Patient processing
        if word[0] == "newPatient":
            tmplist = [word[1].replace('\n', '').replace(' ', '').split(",")]
            # New Patient record validation
            if len(tmplist[0]) != 2:
                print("Error! newPatient record should have 2 values name and age separated by ','")
                print("Row# " + str(lc) + " does not have 2 values for newPatient")
                exit(1)
            # populate the object of PatientRecord with new patient from prompt file and call enqueuePatient
            plist.append(PatientRecord(tmplist[0][1], tmplist[0][0], random.randrange(1000, 9999)))
            pl = int(len(plist)) - 1
            f = open(ofile, "a")
            f.write("---- new patient entered---------------" + "\n")
            f.write("Patient details: ")
            f.write(plist[pl].name + ", " + str(plist[pl].age) + ", " + plist[pl].Patid + "\n")
            f.close()

            enqueuePatient(plist[-1].Patid)
        # For nextPatient in prompt file, call nextPatient function
        elif word[0] == "nextPatient":
            nextPatient()
        # prompt file validation
        else:
            print("Error! The prompt file should always start with 'newPatient' or 'nextPatient' ")
            print("Error! Line# " + str(lc) + " starts with '" + str(word[0] + "'"))
            exit(1)
# ############################## Driving Method End ################################################
