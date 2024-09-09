import os
import boto3
AnswerKey = input("Answers:")
Filepath = input("Input Filepath:")
Filepath = os.path.normpath(Filepath)
AnswerArray = AnswerKey.split(" ")
def CreateAnswerDict(AnswerArray):
    ExpectedAnswers = {}
    for index in range(len(AnswerArray)):
        ExpectedAnswers[index+1] = AnswerArray[index]
    return ExpectedAnswers

def pdfToString(Filepath):
    pdfString = ''
    textract = boto3.client('textract')

    with open(Filepath, 'rb') as document:
        imageBytes = document.read()

    response = textract.detect_document_text(
        Document = {'Bytes': imageBytes}
    )

    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            pdfString += item['Text']
    return pdfString

def ExtractAnswers(PdfString):
    ExtractedAnswers = []
    CurrentAnswer = ""
    inAnswer = False

    for char in PdfString:
        if char == '[':
            inAnswer = True
        elif char == ']':
            inAnswer = False
            if CurrentAnswer:
                ExtractedAnswers.append(CurrentAnswer)
                CurrentAnswer = ""
        elif inAnswer:
            CurrentAnswer += char
    return ExtractedAnswers
def StripExtractedAnswers(extractedAnswers):
    finalArray = []
    for string in extractedAnswers:
        addstring = ""
        for char in string:
            if char == "-" or char.isdigit():
                addstring += char
        finalArray.append(addstring)
    return finalArray
def GradeTest(AnswerArray, expectedAnswers):
    Questions = len(expectedAnswers)
    WrongAnswers = 0
    for value in expectedAnswers:
        if sorted(expectedAnswers[value]) != sorted(AnswerArray[value-1]):
                WrongAnswers += 1
    return (Questions - WrongAnswers)/Questions

expectedAnswers = CreateAnswerDict(AnswerArray)
String = pdfToString(Filepath)
ExtractedAnswers = ExtractAnswers(String)
ParsedAnswers = StripExtractedAnswers(ExtractedAnswers)
FinalGrade = GradeTest(ParsedAnswers,expectedAnswers)
print("Your Final Grade is : " + str(round(FinalGrade,2)*100) + " %")