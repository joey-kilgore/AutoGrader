from defs import *
import subprocess
import time
import os

class Student:
    # Student class contains all relevant information for each respective student

    def __init__(self):
        # intialize all key data
        self.name = ""
        self.pathToBinFolder = ""
        self.rawOutputDict = {}
        self.rawErrorDict = {}
        self.score = 0
        self.pathToGradeFile = ""
        self.gradeFile = None

    def createGradeFile(self):
        # open/create the student file and store the open file in self.gradeFile
        self.gradeFile = open(self.pathToGradeFile, "a+")

    def testStudent(self, input):
        # create a new dictionary entry for the student object
        #   mapping the input to the output and input to error

        # popen creates a subprocess that allows us to run the class file and then pass input and read output
        argsList = ['java', '-classpath', self.pathToBinFolder, 'ConnectFour']
        p = subprocess.Popen(argsList, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # test the given input using communicate
        try:
            # communicate lets us give a byte sequence (the encoded input)  and get a byte sequence out
            (out, err) = p.communicate(input.encode('ascii'), timeout=MAX_RUNTIME)
            p.kill()
        except TimeoutError:
            # if a timeout occurs we catch it here
            p.kill()
            (out, err) = p.communicate()

        # to save the output we need to do 3 things
        # we need to take the bytes and convert to a string (with decode)
        # we also need to do two replacements of null characters with spaces, and remove the carriage return
        #   the carriage return is removed because it creates extra new lines when writing to file
        self.rawOutputDict[input] = out.decode('ascii').replace("\0"," ").replace("\r","")
        self.rawErrorDict[input] = err.decode('ascii').replace("\0"," ").replace("\r","")


    def grade(self, gradingKey):
        self.gradeFile.write(self.name + "\n")
        self.gradeFile.write("AUTO GRADER SCORE : " + str(self.score) + "/" + str(1) + "\n")
        self.gradeFile.write("-----------------------------\n")

        for testInput in gradingKey.keys():
            # for each input, mark whether they got it correct or incorrect
            #   if there was an error we will output that
            #   if they got it incorrect, show all input, output, and solution
            if(self.rawOutputDict[testInput] == gradingKey[testInput]):
                self.gradeFile.write("\nCORRECT OUTPUT\n")
            else:
                self.gradeFile.write("\n***===INCORRECT OUTPUT===***\n")

            self.gradeFile.write("INPUT:\n")
            self.gradeFile.write(testInput + "\n")
            self.gradeFile.write("\nYOUR OUTPUT\n")
            self.gradeFile.write(self.rawOutputDict[testInput])
            self.gradeFile.write("\nSOLUTION\n")
            self.gradeFile.write(gradingKey[testInput])
            self.gradeFile.write("\nERROR\n")
            self.gradeFile.write(self.rawErrorDict[testInput])
            self.gradeFile.write("\n--------------------------\n")


def getInputs():
    # get the list of strings, each string being a set of inputs to test
    return ["0\n0\n1\n1\n2\n2\n3\n0"]

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
        student.pathToGradeFile = "./" + student.name + ".txt"
        student.pathToBinFolder = os.path.join(STUDENT_FOLDER_PARENT, studentFolder, PATH_TO_BIN)
        students.append(student) 

    return students

def gradeAllStudents():
    # grading all students will run through all necesary steps

    inputList = getInputs() # collect the list of inputs to test
    gradingKey = getGradingKey(inputList) # collect the list of respective outputs

    students = getAllStudents() # create list of student objects with names and pathToClassFile

    for student in students:
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

    print("done")

gradeAllStudents()