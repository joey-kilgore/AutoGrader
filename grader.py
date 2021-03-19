from defs import *
import subprocess
import time
import os
from student import *
import time
import math
from multiprocessing import Pool
from multiprocessing import freeze_support
from functools import partial

def findFile(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

def getInputs():
    # get the list of strings, each string being a set of inputs to test
    inputList = []
    with open(INPUT_FILE_PATH) as inputFile:
        while True:
            # loop until we run out of lines to read
            # the first line of each set of inputs should be in the form "inputs:#"
            numInputsLine = inputFile.readline()
            if not numInputsLine:
                break # we have run out of inputs 

            # we have another test case, so we will loop through the number of inputs
            #   and build the input string
            numInputs = int(numInputsLine.replace("inputs:",""))
            testInput = ""
            for i in range(numInputs):
                testInput += inputFile.readline()

            # add each new testInput to the list of inputs
            inputList.append(testInput)
    
    return inputList

def getGradingKey(inputList):
    # get the dictionary mapping inputs to the correct ouptut
    # This is done by running a known correct program through all inputs
    solution = Student()
    solution.name = "solution"
    solution.pathToBinFolder =  SOLUTION_BIN_FOLDER

    for testInput in inputList:
        solution.testStudent(testInput)
    
    # the solution 'student' has run all input, which means the output dictionary is the gradingKey
    return solution.rawOutputDict

def listdirs(path):
    # get a list of all directories in a given directory
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

def getAllStudents():
    # return the list of all students as student objects
    #   and populate the student objects with the relevant initial information
    studentFolders = listdirs(STUDENT_FOLDER_PARENT)

    students = []
    for studentFolder in studentFolders:
        student = Student() # create a new student
        student.name = studentFolder    # we are just going to assume that the folders are named after the students
        student.pathToGradeFile = os.path.join(PATH_TO_OUTPUT, student.name + ".txt")

        # We find the first instance of the class file in the student workspace
        try:
            student.pathToBinFolder = os.path.dirname(findFile(CLASS_FILE, os.path.join(STUDENT_FOLDER_PARENT, studentFolder)))
            students.append(student) 
        except:
            # unable to find the class file for the student
            print("NO CLASS FILE AVAILABLE " + student.name)

    return students

def run_multiprocessing(studentList, inputList, gradingKey):
    global NUM_PROCESSORS
    with Pool(processes=NUM_PROCESSORS) as pool:
       pool.map(partial(gradeIndividualStudent, inputList=inputList, gradingKey=gradingKey) , studentList)
    #  for student in studentList:
    #      gradeIndividualStudent(student,inputList,gradingKey)

def gradeIndividualStudent(student, inputList, gradingKey):
    student.createGradeFile()
    print("grading student : " + student.name)

    for testInput in inputList:
        # use each input case to load output and error dictionaries
        student.testStudent(testInput)

        if(student.rawOutputDict[testInput] == gradingKey[testInput]):
            # if the student got the question right we can increase their score
            student.score += 1
    
    student.grade(gradingKey)
    student.gradeFile.close()

def gradeAllStudents():
    # grading all students will run through all necesary steps

    inputList = getInputs() # collect the list of inputs to test
    gradingKey = getGradingKey(inputList) # collect the list of respective outputs

    students = getAllStudents() # create list of student objects with names and pathToClassFile
    run_multiprocessing(list(students), inputList, gradingKey)

    print("done")

if __name__ == "__main__":
    freeze_support()
    gradeAllStudents()