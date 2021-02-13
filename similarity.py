import math 
import string 
import sys 
from defs import *
import os

# reading the text file 
# This functio will return a  
# list of the lines of text  
# in the file. 
def read_file(filename):  
      
    try: 
        with open(filename, 'r') as f: 
            data = f.read() 
        return data 
      
    except IOError: 
        print("Error opening or reading input file: ", filename) 
        sys.exit() 
  
# splitting the text lines into words 
# translation table is a global variable 
# mapping upper case to lower case and 
# punctuation to spaces 
translation_table = str.maketrans(string.punctuation+string.ascii_uppercase, 
                                     " "*len(string.punctuation)+string.ascii_lowercase) 
       
# returns a list of the words 
# in the file 
def get_words_from_line_list(text):  
      
    text = text.translate(translation_table) 
    word_list = text.split() 
      
    return word_list 
  
  
# counts frequency of each word 
# returns a dictionary which maps 
# the words to  their frequency. 
def count_frequency(word_list):  
      
    D = {} 
      
    for new_word in word_list: 
          
        if new_word in D: 
            D[new_word] = D[new_word] + 1
              
        else: 
            D[new_word] = 1
              
    return D 
  
# returns dictionary of (word, frequency) 
# pairs from the previous dictionary. 
def word_frequencies_for_file(filename):  
      
    line_list = read_file(filename) 
    word_list = get_words_from_line_list(line_list) 
    freq_mapping = count_frequency(word_list) 
  
    # print("File", filename, ":", ) 
    # print(len(line_list), "lines, ", ) 
    # print(len(word_list), "words, ", ) 
    # print(len(freq_mapping), "distinct words") 
  
    return freq_mapping 
  
  
# returns the dot product of two documents 
def dotProduct(D1, D2):  
    Sum = 0.0
      
    for key in D1: 
          
        if key in D2: 
            Sum += (D1[key] * D2[key]) 
              
    return Sum
  
# returns the angle in radians  
# between document vectors 
def vector_angle(D1, D2):  
    numerator = dotProduct(D1, D2) 
    denominator = math.sqrt(dotProduct(D1, D1)*dotProduct(D2, D2)) 
      
    return math.acos(numerator / denominator) 
  
  
def documentSimilarity(filename_1, filename_2): 
   # filename_1 = sys.argv[1] 
   # filename_2 = sys.argv[2] 
    sorted_word_list_1 = word_frequencies_for_file(filename_1) 
    sorted_word_list_2 = word_frequencies_for_file(filename_2) 
    distance = vector_angle(sorted_word_list_1, sorted_word_list_2) 
      
    print("The distance between the documents is: % 0.6f (radians)"% distance) 
    return distance

def listdirs(path):
    # get a list of all directories in a given directory
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

def getStudentFolders():
    # return the list of all students folders in the parent folder
    return listdirs(STUDENT_FOLDER_PARENT)

def findFile(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

def main():
    studentFolders = getStudentFolders()

    javaFileDict = {}
    similarityMatrix = {}
    for studentFolder in studentFolders:
        similarityMatrix[studentFolder] = {}
    
    for studentFolder in studentFolders:
        javaFileDict[studentFolder] = findFile("ConnectFour.java", os.path.join(STUDENT_FOLDER_PARENT, studentFolder))
        
        for compareStudentFolder in javaFileDict.keys():
            num = documentSimilarity(javaFileDict[studentFolder], javaFileDict[compareStudentFolder])
            similarityMatrix[studentFolder][compareStudentFolder] = num
            similarityMatrix[compareStudentFolder][studentFolder] = num
    
    print(similarityMatrix)
    f = open("similarity.csv", "w")
    for studentFolder in studentFolders:
        f.write(studentFolder + ",")
        for compareStudentFolder in studentFolders:
            f.write(str(similarityMatrix[studentFolder][compareStudentFolder]) + ",")
        f.write("\n")

    f.close()

if __name__ == "__main__":
    main()