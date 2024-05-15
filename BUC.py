# Author:	Ashokkumar Raja

import csv, math, itertools

# Reading the csv data set to perform BUC algorithm
file = open("Product_Sales_Data_Set.csv",'r')
allData = []
for row in file:
    row = row.replace("\n", "")
    allData.append(row.split(","))
file.close()
allData.pop(0)  # Removing the header

# Calculating the sales units
def calSalesUnits(list):
    Sales_Units = 0
    for row in allData:
        if set(list).issubset(set(row)):
            Sales_Units = Sales_Units + int(row[4])
    return Sales_Units

# Cardinality represents the size of each dimension
Cardinality = [0 for x in range(len(allData[0])-1)] # [0, 0, 0, 0] 
# allValue will store the value of each dimension
allValue = []

# Calculate the number of values ​​in each dimension and store it in the array allValue
def dimValue(): 
    for i in range(len(Cardinality)):
        Value = []
        for j in range(len(allData)):
            if (allData[j][i] not in Value):
                Value.append(allData[j][i])
        Cardinality[i] = len(Value)
        allValue.append(Value)

external_file = open("Iceberg-Cube-Results.txt", "w")

# Referred the link mentioned in the citations to understand the BUC function and its implementation.
# BUC is an recursive algorithm which filters out the data that meets the minimum support.
def BUC(list, min_sup, startDimension, maximumDimension):                                        
    for i in range(startDimension,maximumDimension):        # For each dimension i
        for j in range(Cardinality[i]):                     # Take the value j for each i dimension
            list.append(allValue[i][j])                     # From dimValue() we get the values ​​of each dimension and we move them and put it into a list which is passed to calSalesUnits() to get the sales units.
            Sales_Units = calSalesUnits(list)

            # Now we compare the sales units with the minimum support and if it is equal or greater than the
            # minimum support we pass the changed list, minimum support and the startDimesion to BUC to start recursion.
            if(Sales_Units >= min_sup):
                for x in range(len(list)-1):
                    external_file.write(str(list[x])+',')
                external_file.write(str(list[-1]+'\t'+str(Sales_Units)+"\n"))
                print(str(list)+''+str(Sales_Units))
                startDimension = i + 1     
                BUC(list,min_sup,startDimension,4)                    
            else:
                list.pop()
    if(len(list)>=1):
        list.pop()

# Prompting the user to enter the minimum support and passing the value to BUC function
min_sup = int(input("\nPlease enter the minimum support:"))
dimValue()
BUC([],min_sup,0,4)     
                         
