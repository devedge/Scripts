import sys
import csvGenerator

dirPath = ""
csvName = ""
csvFile = ""

def main():
    import parserAPI
    global dirPath
    global csvName
    global csvFile

    # Get the path to the data folder and the name of the CSV file to write to
    if (sys.version_info[0] >= 3):
        dirPath = input('Enter the absolute path to the folder with the dataset: ')
        csvName = input('Enter a name for the csv file that will be created: ')
    else:
        dirPath = eval(input('Enter the absolute path to the folder with the dataset: '))
        csvName = eval(input('Enter a name for the csv file that will be created: '))

    # check the file location of the csv file
    # checkFileLocation(csvName)

    # create the blank csv file

    # open the csv file
    # with open(csvName, 'w', newline='') as csvfile:
    csvFile = csv.writer(open(csvName, "wb"))

    # call the parserAPI.py file that starts parsing
    parserAPI.scanDirectory(dirPath)