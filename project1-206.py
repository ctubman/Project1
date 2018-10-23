import os
import filecmp
import csv
from dateutil.relativedelta import *
from datetime import date


def getData(file):

	inFile = open(file,"r")
	lines = inFile.readlines()
	inFile.close()

	listOfDicts = []
	
	for line in lines:
	    # empty dict object for each student
	    dictObject = {}

	    values = line.split(',')
	    firstName = values[0]
	    lastName = values[1]
	    email = values[2]
	    schoolYear = values[3]

	    removeNewLineChar = values[4].split('\n')
	    DOB = removeNewLineChar[0]

	    dictObject['First'] = firstName
	    dictObject['Last'] = lastName
	    dictObject['Email'] = email
	    dictObject['Class'] = schoolYear
	    dictObject['DOB'] = DOB
	    listOfDicts.append(dictObject)

	# remove header bc it isn't a student
	listOfDicts.pop(0) 
	return listOfDicts


def mySort(data,col):
	# tell it what to sort dictionary on
	sortedList = sorted(data, key = lambda x: x[col])
	#return first and 2nd value of sorted list
	# sortedList is a list of dictionaries, get first dict out, format into string 
	firstDict = sortedList[0] 
	return firstDict['First'] + " " + firstDict['Last'] 


def classSizes(data): # data is list of Dicts
	classSizeDict = {}

	for studentDict in data: # now theres a dict
		studentClass = studentDict['Class'] # string
		classSizeDict[studentClass] = classSizeDict.get(studentClass, 0) + 1

	sortedTuples = sorted(classSizeDict.items(), key = lambda x: x[1], reverse = True)
	return sortedTuples 


def findMonth(data):  # data is list of dicts
	birthMonths = {}

	for studentDict in data:
		splitBirthday = studentDict['DOB'].split('/') # list of strings
		birthdayMonth = splitBirthday[0]
		birthMonths[birthdayMonth] = birthMonths.get(birthdayMonth, 0) + 1

	sortedBirths = sorted(birthMonths, key = lambda x: birthMonths[x], reverse = True)
	mostCommonMonth = int(sortedBirths[0])
	return mostCommonMonth


def mySortPrint(data,col,fileName): ######## FIX FIX FIX FIX 
	csvStudents = sorted(data, key = lambda x: x[col])
	with open(fileName, 'w') as c:
		filewriter = csv.writer(c, delimiter = ',') # separate by commas
		for student in csvStudents:
			filewriter.writerow([student['First'], student['Last'], student['Email']])
	c.close()


def findAge(data):
	currentAges = []
	for studentDict in data:
		DOB = studentDict['DOB'].split('/') # get bday
		birthYear = DOB[2] # get bday year
		age = 2018 - int(birthYear) # get age
		currentAges.append(age)
	overallAvgAge = sum(currentAges) / len(currentAges) # get total from list of nums and divide by # of students for avg
	return round(overallAvgAge)


################################################################
## DO NOT MODIFY ANY CODE BELOW THIS
################################################################

## We have provided simple test() function used in main() to print what each function returns vs. what it's supposed to return.
def test(got, expected, pts):
  score = 0;
  if got == expected:
    score = pts
    print(" OK ", end=" ")
  else:
    print (" XX ", end=" ")
  print("Got: ",got, "Expected: ",expected)
  return score


# Provided main() calls the above functions with interesting inputs, using test() to check if each result is correct or not.
def main():
	total = 0
	print("Read in Test data and store as a list of dictionaries")
	data = getData('P1DataA.csv')
	data2 = getData('P1DataB.csv')
	total += test(type(data),type([]),50)

	print()
	print("First student sorted by First name:")
	total += test(mySort(data,'First'),'Abbot Le',25)
	total += test(mySort(data2,'First'),'Adam Rocha',25)

	print("First student sorted by Last name:")
	total += test(mySort(data,'Last'),'Elijah Adams',25)
	total += test(mySort(data2,'Last'),'Elijah Adams',25)

	print("First student sorted by Email:")
	total += test(mySort(data,'Email'),'Hope Craft',25)
	total += test(mySort(data2,'Email'),'Orli Humphrey',25)

	print("\nEach grade ordered by size:")
	total += test(classSizes(data),[('Junior', 28), ('Senior', 27), ('Freshman', 23), ('Sophomore', 22)],25)
	total += test(classSizes(data2),[('Senior', 26), ('Junior', 25), ('Freshman', 21), ('Sophomore', 18)],25)

	print("\nThe most common month of the year to be born is:")
	total += test(findMonth(data),3,15)
	total += test(findMonth(data2),3,15)

	print("\nSuccessful sort and print to file:")
	mySortPrint(data,'Last','results.csv')
	if os.path.exists('results.csv'):
		total += test(filecmp.cmp('outfile.csv', 'results.csv'),True,20)

	print("\nTest of extra credit: Calcuate average age")
	total += test(findAge(data), 40, 5)
	total += test(findAge(data2), 42, 5)

	print("Your final score is " + str(total))

# Standard boilerplate to call the main() function that tests all your code
if __name__ == '__main__':
    main()
