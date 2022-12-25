# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import xml.etree.ElementTree as et
import json

# function 
# return node text or None 
def getValueOfNode(node):
    return node.text if node is not None else None

# function read xml file
# limitations - should have single leaf or singe node
"""
sample xml record structure
<?xml version = "1.0"?>
<Friends>
	<Record>
		<Display>Tanmay Patil</Display>
		<Name>
			<FirstName>Tanmay</FirstName>
			<LastName>Patil</LastName>
		</Name>	
		<Age>25</Age>
		<Contact>
			<Mobile>9876543210</Mobile>
			<Email>tanmaypatil@xyz.com</Email>
		</Contact>
		<Address>
			<City>Bangalore</City>
			<State>Karnataka</State>
			<Pin>560212</Pin>
		</Address>
	</Record>
</Friends>
"""
def read_xml(fileName):
    #fileName = './data/Friends.xml'
    # create empty data frame
    df = pd.DataFrame()
    # filename with math from cwd
    oTree = et.parse(fileName)
    # get root
    oRoot = oTree.getroot()
    #print(oRoot.tag)
    # get records from root
    for oRecord in oRoot:
        #print(oRecord.tag)
        recDict={}
        for oField in oRecord:
            #print(oField.tag)
            vFieldValue = getValueOfNode(oField)
            #print(type(vFieldValue))
            if (vFieldValue.strip() != ''):
                recDict[oField.tag] = vFieldValue
            else:
                fldDict={}
                for oSubField in oField:
                    #print(oSubField.tag,':',getvalueofnode(oSubField))
                    fldDict[oSubField.tag] = getValueOfNode(oSubField)
                #print(fldDict)    
                recDict.update(fldDict)
        print(recDict)
        dft= pd.DataFrame(recDict, index=[0])
        df = df.append(dft, ignore_index=True)
    # return
    return(df)    

# function read json file 
# limitations - should have single leaf or singe node
"""
sample json record structure
{
"Friends":[
   {
	  "Display":"Tanmay Patil",
      "Name": {
         "FirstName": "Tanmay",
         "LastName": "Patil"
      },
	  "Age":"25",
      "Contact": {
         "Mobile": "9876543210",
         "Email": "tanmaypatil@xyz.com"
      },
      "Address": {
         "City": "Bangalore",
         "State": "Karnataka",
         "Pin": "560212"
      }
   }
]}
"""
def read_json(fileName):
    #fileName = './data/Friends.json'
    # create empty dataframe
    df = pd.DataFrame()
    # read json file
    with open(fileName, 'rb') as jsonFile:  
        data = json.load(jsonFile)
        #print(data)
        #print(data.keys())
        # get json Name (top level name / table name)
        for jsonName in data.keys():
            #print(jsonName)
            # get record dict
            for recData in data[jsonName]:
                recDict = {}
                for k, v in recData.items():
                    if not isinstance(v, dict):
                        recDict[k] = v
                    else:
                        recDict.update(v)
                print("\n"+str(recDict))        
                dft= pd.DataFrame(recDict, index=[0])
                df = df.append(dft, ignore_index=True)
    # return
    return(df)



# space count per coulmn
"""
returns: 
    number of rows which contain <blank>
usage: 
    colSpaceCount(colName)
""" 
def colSpaceCount(colName):
    return (colName.str.strip().values == '').sum()


# space count for data frame
"""
returns:  
    number of rows which contain <blank> iterating through each col of df
usage: 
    SpaceCount(df)
"""
def SpaceCount(df): 
    colNames = df.columns
    dsRetValue = pd.Series() 
    for colName in colNames:
        if df[colName].dtype == "object": 
            dsRetValue[colName] = colSpaceCount(df[colName])
    return(dsRetValue)


# outlier limits
"""
returns: 
    upper boud & lower bound for array values or df[col] 
usage: 
    OutlierLimits(df[col]): 
"""
def colOutlierLimits(colValues, pMul=3): 
    if (pMul != 3 and pMul != 2.5 and pMul != 2 and pMul != 1.5):
        pMul = 3
    pMul = float(pMul)    
    q1, q3 = np.percentile(colValues, [25, 75])
    iqr = q3 - q1
    ll = q1 - (iqr * pMul)
    ul = q3 + (iqr * pMul)
    return ll, ul


# outlier count for column
"""
returns: 
    count of outliers in the colName
usage: 
    colOutCount(colValues)
"""
def colOutlierCount(colValues, pMul):
    ll, ul = colOutlierLimits(colValues, pMul)
    ndOutData = np.where((colValues > ul) | (colValues < ll))
    ndOutData = np.array(ndOutData)
    return ndOutData.size


# outlier count for dataframe
"""
returns: 
    count of outliers in each column of dataframe
usage: 
    OutlierCount(df): 
"""
def OutlierCount(df, pMul=3): 
    if (pMul != 3 and pMul != 2.5 and pMul != 2 and pMul != 1.5):
        pMul = 3
    pMul = float(pMul)    
    colNames = df.columns
    dsRetValue = pd.Series() 
    for colName in colNames:
        if (df[colName].dtypes == 'object'):
            continue
        #print(colName)
        colValues = df[colName].values
        #print(colValues)
        #outCount = colOutCount(colValues)
        #print(outCount)
        dsRetValue[colName] = colOutlierCount(colValues, pMul)
    return(dsRetValue)


# oulier index for column
"""
returns: 
    row index in the colName
usage: 
    colOutIndex(colValues)
"""
def colOutlierIndex(colValues, pMul):
    ll, ul = colOutlierLimits(colValues, pMul)
    ndOutData = np.where((colValues > ul) | (colValues < ll))
    ndOutData = np.array(ndOutData)
    return ndOutData


# oulier index for data frame
"""
returns: 
    row index of outliers in each column of dataframe
usage: 
    OutlierIndex(df): 
"""
def OutlierIndex(df, pMul=3): 
    if (pMul != 3 and pMul != 2.5 and pMul != 2 and pMul != 1.5):
        pMul = 3
    pMul = float(pMul)    
    colNames = df.columns
    dsRetValue = pd.Series() 
    for colName in colNames:
        if (df[colName].dtypes == 'object'):
            continue
        colValues = df[colName].values
        dsRetValue[colName] = str(colOutlierIndex(colValues, pMul))
    return(dsRetValue)


# outlier values for column 
"""
returns: 
    actual outliers values in the colName
usage: 
    colOutValues(colValues)
"""
def colOutlierValues(colValues, pMul):
    ll, ul = colOutlierLimits(colValues, pMul)
    ndOutData = np.where((colValues > ul) | (colValues < ll))
    ndOutData = np.array(colValues[ndOutData])
    return ndOutData


# outlier values for dataframe 
"""
returns: 
    actual of outliers in each column of dataframe
usage: 
    OutlierValues(df): 
"""
def OutlierValues(df, pMul=3): 
    if (pMul != 3 and pMul != 2.5 and pMul != 2 and pMul != 1.5):
        pMul = 3
    pMul = float(pMul)    
    colNames = df.columns
    dsRetValue = pd.Series() 
    for colName in colNames:
        if (df[colName].dtypes == 'object'):
            continue
        colValues = df[colName].values
        dsRetValue[colName] = str(colOutlierValues(colValues, pMul))
    return(dsRetValue)


# column level handle outlier by capping
# at lower limit & upper timit respectively
"""
returns: 
    array values or df[col].values without any outliers
usage: 
    HandleOutlier(df[col].values): 
"""
def colHandleOutliers(colValues, pMul=3):
    ll, ul = colOutlierLimits(colValues, pMul)
    colValues = np.where(colValues < ll, ll, colValues)
    colValues = np.where(colValues > ul, ul, colValues)
    return (colValues)


# data frame level handline outliers
"""
desc:
    HandleOutliers - removes Outliers from all cols in df except exclCols 
usage: 
    HandleOutliers(df, colClass) 
params:
    df datarame, exclCols - col to ignore while transformation, Multiplier  
"""
def HandleOutliers(df,  lExclCols=[], pMul=3):
    #lExclCols = depVars
    # preparing for standadrising
    # orig col names
    colNames = df.columns.tolist()
    # if not list convert to list
    if not isinstance(lExclCols, list):
        lExclCols = [lExclCols]
    #print(lExclCols)
    # if not empty, create a dataframe of ExclCols
    if lExclCols != []:
        for vExclCol in lExclCols:
            colNames.remove(vExclCol)
    # handle outlier for each col
    for colName in colNames:
        colType =  df[colName].dtype  
        df[colName] = colHandleOutliers(df[colName], pMul)
        if df[colName].isnull().sum() > 0:
            df[colName] = df[colName].astype(np.float64)
        else:
            df[colName] = df[colName].astype(colType)    
    return df


# data frame handle zeros replace with null
"""
desc:
    HandleZeros - removes Outliers from all cols in df except exclCols 
usage: 
    HandleZeros(df, colClass) 
params:
    df datarame, exclCols - col to ignore while transformation, Multiplier  
"""
def HandleZeros(df, lExclCols=[]):
    #lExclCols = depVars
    # preparing for standadrising
    # orig col names
    colNames = df.columns.tolist()
    # if not list convert to list
    if not isinstance(lExclCols, list):
        lExclCols = [lExclCols]
    #print(lExclCols)
    # if not empty, create a dataframe of ExclCols
    if lExclCols != []:
        for vExclCol in lExclCols:
            colNames.remove(vExclCol)
    # handle outlier for each col
    for colName in colNames:
        if ((df[colName]==0).sum() > 0):
            df[colName] = np.where(df[colName] == 0, None, df[colName])
    return df


# data frame handle nulls replace with ReplVals of the columns as per replBy vars
"""
desc:
    HandleNulls - removes Outliers from all cols in df except exclCols 
usage: 
    HandleNulls(df, replBy, colClass) 
params:
    df datarame, 
    replBy - mean, median, minimum (of mean & median), maximum (of mean & median) 
    exclCols - col to ignore while transformation, Multiplier  
"""
def HandleNulls(df, replBy, lExclCols=[]):
    #lExclCols = depVars
    # preparing for standadrising
    # orig col names
    colNames = df.columns.tolist()
    # if not list convert to list
    if not isinstance(lExclCols, list):
        lExclCols = [lExclCols]
    #print(lExclCols)
    # if not empty, create a dataframe of ExclCols
    if lExclCols != []:
        for vExclCol in lExclCols:
            colNames.remove(vExclCol)
    # handle outlier for each col
    for colName in colNames:
        if ((df[colName].isnull()).sum() > 0):
            if (replBy == "mean"):
                replVals = df[colName].mean()
            elif (replBy == "median"):
                replVals = df[colName].median()
            elif (replBy == "minimum"):
                replVals = min(df[colName].mean(),df[colName].median())
            elif (replBy == "maximum"):
                replVals = max(df[colName].mean(),df[colName].median())
            # replace
            df[colName] = df[colName].fillna(replVals)
    return df

