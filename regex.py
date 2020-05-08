import PyPDF2 ;
import pytesseract as pt
import pdf2image
import array 
import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize,regexp_tokenize

filename = "D:\Dropbox\TextMining\Scora\Sample Questions_TPO 2017 ( Public).pdf";

#using pdfReader does not produce good results, as it ignores the first sentence itself. THis seems to be a known issueas several users have said pdf reader , while the set up is easy, doesnt always render sentences easuly
#this is even more surprising as just a normal text select using Contrl+A is able to read the sentences easily
#so both user is provided the option of selecting any of the reader - tesseract or pdfreader or any other
import pytesseract as pt;
import pdf2image;
import textract;

    
class config:
#    reader= ""; #pdfReader or tesseract. Tesseract uses wand to convert into images
#    filename="";
    
    def __init__(self, file, reader):
        self.filename = file;
        self.reader = reader;
        self.data = self.callReader()
        
    def callReader(self):
        print(filename)
        if self.reader=="tesseract":
          data=self.pyTesseract()
        else:
          data=self.pdfReaderOutput()
        return data;
    
    def cleanDataFunc(self): #rmeoves only newline
        self.cleanData= self.data.replace('\n','')  
         
    def pyTesseract(self):
        from wand.image import Image as Img # have to install Imagemagick for converting pdf to images. R is much better here, with no additional installtion it can use tesseract seamlessly somehow
        with Img(filename=filename, resolution=300) as img:
            img.compression_quality = 99
            img.save(filename='image_name.jpg')
            numPages=len(img.sequence)
            

        data = [];
        for i in range (0, numPages): 
            data.append(pt.image_to_string('image_name-{i}.jpg'.format(i=i)))
        data = ' '.join(map(str, data))
        return(data)
    
    def pdfReaderOutput(self):
        pdfFileObj = open(filename, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj);
        data=[];
        for i in range (0, pdfReader.numPages): 
        #for i in range (0,1): 
            data.append(pdfReader.getPage(i).extractText())
        data = ' '.join(map(str, data))
        return(data)
       
    def chink(self,patternObj):
        removalPattern='|'.join(patternObj.remove)
        self.cleanData=re.sub(removalPattern,'',self.cleanData)        
           
class pattern:
    questionIndicator="Q\s*[0-9]+s*\)" # searches for the pattern Q1), to Q<any number>, \s adjusts for whitespaces
    questionIndicator_retain_delim="(Q\s*[0-9]+s*\))"  # this will retain the delimiter, not used for now in rest of the code
    answerIndicator =["\(\s*[a-zA-Z]\s*\)","[A-Z]\."]
    remove=["Marks:\s*[0-9]+","Middle\s*School\s*English\s*2016"]
    
    
class Item:
    def __init__(self, type, question):
        self.question = question;
        self.itemType = 'mcq'  if isinstance(question,McqQuestion) else 'others';
        self.data = self.callReader()
        
class McqQuestion:
    def __init__(self,question,options):
        self.question=question
        self.optionSet=options
        

myConfig= config(filename,"tesseract")
myPattern = pattern() #placeholder class for now, need to extend this class to build patterns for each question type


myConfig.cleanDataFunc() #removes all newlines
myConfig.chink(myPattern) #remove unwanted header footer etc. However this can be done by tesseract also.
#after_remove_n = [x.replace('\n','') for x in tokenized_sent_before_remove_n]
rawQnAList = re.split(myPattern.questionIndicator, myConfig.cleanData)



#tokenized_sent_before_remove_n = nltk.sent_tokenize(data)
#tokenized_sent_

#print(content)


itemSet=[];
for x in rawQnAList:
#    print(x)
    print("~~~~~~~~~Question~~~~~~~~~~~~~~~~~~~~~~~~~~~");
    QnAString =re.split('|'.join(myPattern.answerIndicator), x)
    qString=QnAString[0]
    QnAString.pop(0)
    optionString=QnAString
    itemSet.append(McqQuestion(qString,optionString))
 
    
def printItems(item):
    print("Question :\n")
    print(item.question)
    print("\n")
    for i in range(0,len(item.optionSet)-1):
        print("OPTION " + str(i+1) + ":"+ item.optionSet[i])
        print("\n")

printItems(itemSet[3])   # change number to view others     
    