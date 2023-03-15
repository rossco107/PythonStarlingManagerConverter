
import csv
import re


class Model() :

  starlingName = "StarlingStatement"
  convertedname = "StarlingStatement_Converted"

  def __init__(self, outputter):
    self.label = outputter
    self.initialise()


  def initialise(self) :
    self.validArray = []
    self.printData  = ""
    self.sourceFile = ""
    self.sourcePath = ""
    self.label["text"] = ""
    

  def sourcePathCaptured(self) :
    return self.sourcePath != "" 


  def fileReadingConversionAndWritingProcess(self) :
    if self.sourcePathCaptured :
      convertedArray = self.convertCSVTo2DArray(self.sourceFile)
      self.validArray = self.analyseFile(convertedArray)
      
   
  def rowIsValid(self, row) :
    if len(row) != 8 :
      return False
    
    for i in range(0,3):
      if row[i] == "" :
        return False
    return True
  
  
  def sourcePathCaptured(self) : 
      return self.sourceFile is None
  

  def convert(self) :
    if self.validArray is not None :
      reformattedArray = self.reformatData(self.validArray)
      self.writeOut(reformattedArray)
      
      
  def convertCSVTo2DArray( self, csvFile ) : 
    sourceAs2DArray = []
    file = csv.reader(csvFile)
    for row in file :
        fields = row
        sourceAs2DArray.append(fields)
    return sourceAs2DArray
    
  
  def analyseFile(self, source) :  
    rowsCount = len(source)
    blankRows = 0
    hasHeaderRow = False
    dataRows = 0
    
    if not source :
      self.label["text"] = self.label["text"] + ("\n\nEmpty file")
      return None
    
    for  count, row  in enumerate(source) :
      if row == source[0] :
        if len(row) != 8:
          self.label["text"] = self.label["text"] + ("\n\nThere should be 8 columns")
          return None
        if self.rowIsAllText(row) :
          hasHeaderRow = True
          if rowsCount == 2 :
            self.label["text"] = self.label["text"] + ("\n\nNo data, only header row")
            return None
        else :
            self.label["text"] = self.label["text"] + ("\n\nFirst row should be a Header row")
            return None
      else :
        if self.rowIsBlank(row) :
          blankRows = blankRows + 1
        else :
          dataRows = dataRows + 1
          if not self.rowIsValid(row) :
            self.label["text"] = self.label["text"] + (f"\n\nRow {count + 1} has invalid data")
            return None
          
    self.label["text"] = self.label["text"] + (  f"\n\nFound : \n{rowsCount} rows \n{blankRows} blank row(s) \nhas header row = {hasHeaderRow} \n{dataRows} data rows \n8 columns" )
    
    return source
  
  
  def reformatData( self, source ) :
    
    output = []
    blankRowsRemoved = 0
    rowCount = 0
    
    for  row in source :
      newrow  = []
      if rowCount == 0 :
        newrow = [ "Date" , "Reference" , "Description" , "Amount"   ]
        rowCount = rowCount + 1
        output.append(newrow)
      else :
        if self.rowIsBlank(row) :
          blankRowsRemoved = blankRowsRemoved + 1
        else :
          newrow = [ row[0] , row[2] , row[1] , row[4]    ]
          rowCount = rowCount + 1
          output.append(newrow)
        
    self.label["text"] = self.label["text"] +  (f"\n\n{blankRowsRemoved} blank rows removed" )
    self.label["text"] = self.label["text"] +  ("\n4 columns removed")
    self.label["text"] = self.label["text"] +  ("\n2 columns reordered")
    self.label["text"] = self.label["text"] +  ("\n4 column headings renamed")
    
    return output
  
  
  def writeOut(self, output) :
    
    with open( self.saveFileFullPath()  , 'w') as f:
      writer = csv.writer(f)
      writer.writerows(output)

    self.label["text"] = self.label["text"] + ( f"\n\nWritten {len(output)} rows to file \n" + self.saveFileName() )


  def saveFileFullPath(self) :
    return self.saveFilePath() + self.saveFileName()

  def saveFilePath(self) : 
    path =  self.sourcePath
    stringToFindInSourceFileName = self.starlingName
    found = re.search(stringToFindInSourceFileName, path)
    folderPath = path[0:found.start()]
    return folderPath
  

  def saveFileName(self) :
    path =  self.sourcePath
    stringToFindInSourceFileName = self.starlingName
    found = re.search(stringToFindInSourceFileName, path)
    fileNameSecondPart = self.convertedname + path[found.end():found.lastindex]
    fileName = fileNameSecondPart
    return fileName

  
  def rowIsAllText(self, row) :
    for cell in row :
      if not cell.isnumeric :
        return False
    return True
  
  
  def rowIsBlank(self, row) :
    for cell in row :
      if cell != "" :
        return False
    return True
    
  
  
  
