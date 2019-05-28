# importing modules
import requests
import webbrowser
import urllib
import os
import sys
import bs4
import collections
import require
import numpy
import scipy
import csv
import time
import re

# install 'requests' through comand prompt using 'pip install requests' in the path/Scripts
# cd.. helps you to go back and cd path goes further on cmd prompt
# C:\Users\Vikash Alex\AppData\Local\Programs\Python\Python37\Scripts

# defining variables
b = []
linkComplete = []
sleepCount1 = 0
pathFile = 'D:\\Clark University\\TA Work\\Prof Pankush\\Final\\Python\\'
fileName = 'uniqueIdfile.csv'
completePath = pathFile + fileName
countIncrGenreLink = 0
countGenre = 0
c = []
totalIds = 0
sleeptimeglobal = 180
# use following codes to get the 'path'
def getPythonPath():
          print ("path",os.path.dirname(sys.executable)) # the path we will get then add /Scripts into that path to install pip or any python packages
          deleteExistingFile()
          
# check for the existing files
def deleteExistingFile():
    from pathlib import Path
    filePath = Path(completePath)
    if filePath.is_file():
              os.remove(filePath)
              print("\nFile exist...Deleted uniqueIdfile")
    else:
              pass
    linkParameterPass()

def linkParameterPass():
          linkList = []
          # reading file line by line
          with open('D:\\Clark University\\TA Work\\Prof Pankush\\Final\\Python\\Link.txt') as file:
                    linkList.append(file.read().split("\n"))
          file.close()
          for linkGenre in linkList:
                    linkListLength = len(linkGenre)
                    for a in linkGenre:
                              global countGenre
                              countGenre = countGenre + 1
                              genre = getGenre(a)
                              linkChange(a, linkListLength, countGenre, genre)
          ########readLink(linkComplete)
          global totalIds
          print ("Total " + str(totalIds) + " Ids are generated.")

# create and change the link
def linkChange(linkGenre, linkListLength, countGenre, genre):
    k = linkGenre
    genre = getGenre(k)
    count = 0
    jj = []
    c = []
    linkcompleteGenre = []
    alphabetCount = 26  #This value is alphabates count..3 means it will go in the loop for A, B, and C...26 means it will go from A to Z
    print("\n*****" + str(genre) + " genre " + "****" + str(countGenre) + " of "+ str(linkListLength)+ " genre listed" +"*******")
    global sleeptimeglobal
    sleeptime1 = sleeptimeglobal
    for l in range(alphabetCount):
        m = str(chr(ord('a') + count))
        n = k + m
        o = "&letter="
        oo = m.upper()
        ooo = "&page="
        p = "#page"
        count1 = 0
        # for loop to generate link...range is to provide page number upto in navigational panel
        print ("Finding last page. Please wait......")
        for q in range(1,200000):
            count1 = count1 + 1
            global sleepCount1
            sleepCount1 = sleepCount1 + 1
            r = linkGenre + o + oo + ooo + str(q) + p
            stopPageEdit = findLastPage(r,q)
            if sleepCount1 == 200:
                      sleepCount1 = 0
                      print ("Sleeping for" + str(sleeptime1) + " sec since it reached interval of 200 links to find last page")
                      countdown(sleeptime1)
                      print ("Resuming scraping")
            if (stopPageEdit != 0):
                      jj.append(r)
            else:
                      jj.append(r)
                      break
        print ("-----" + str(genre) + " genre with page " + str(oo) + " has " + str(q) + " pages.")
        count = count + 1
    for j in jj:
                  linkComplete.append(j)
                  linkcompleteGenre.append(j)
    readLink(linkcompleteGenre, genre)
                
def findLastPage(link,q):
          site = urllib.request.urlopen(link).read().decode("utf-8")
          j = str(q+1) + "<"
          k = site.count("Next<")
          r = site.count(j)
          returnValue = 0
          if( k == 0):
                    if (r==0):
                              returnValue = 0
                    else:
                              returnValue = 1
          else:
                    if(r==0):
                              returnValue = 0
                    else:
                              returnValue = 1
                    
          return returnValue
          
def getGenre(k):
          countStartIndex = k.find('/ios')
          countEndIndex = k.find('/id')
          genre = k[countStartIndex + 5 : countEndIndex]
          return genre

def readLink(myList1, genre):
    myList1Length = 0
    myList1Length = len(myList1)
    count = 0
    sleepCount = 0
    global sleeptimeglobal
    sleeptime = sleeptimeglobal
    for line in myList1:
              count = count + 1
              sleepCount = sleepCount + 1
              print(str(count) + " of " + str(myList1Length) + " link started scraping")
              downloadingfile(line, genre)
              if sleepCount == 200:
                        sleepCount = 0
                        print ("Sleeping for " + str(sleeptime) + "sec since it reached interval of 200 links scraping")
                        countdown(sleeptime)
                        #time.sleep(60)
                        print ("******Resuming scraping********")
    print ("\nCompleted webscraping of " + str(genre), " genre")
    totalID = uniqueID(c, genre)
    global totalIds
    totalIds = totalIds + totalID
    print ("completed generating " + str(totalID) + " ids of " + str(genre) + " genre.")

def downloadingfile(line, genre):
          r = requests.get(line)
          data = bs4.BeautifulSoup(r.text, "html.parser")
          for l in data.find_all("a"): 
                    line = str(l.encode('utf8'))
                    if "https://itunes.apple.com/us/app/" in line:
                              if "/id" in line:
                                        countStartIndex = line.find('/id')
                                        countEndIndex = line.find('?')
                                        idValue = line[countStartIndex + 1:countEndIndex]
                                        b.append(idValue)
                                        c.append(idValue)

# get only uniqueID and writing into csv
def uniqueID(b, genre):
          savePath = pathFile + str(genre) + "Genre.csv"
          print("**********Writing IDs***********")
          from collections import OrderedDict
          d = list(OrderedDict.fromkeys(b))
          uId = []
          for line in d:
                    line = line.strip('id') # removing string-id from the idNumber
                    uId.append(line)
          # importing using numpy to csv which will store all the id in a single column.
          import numpy as np
          np.savetxt(savePath, uId, delimiter=",", fmt='%s')
          return len(uId)

def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        if (t%3 ==0):
                  print(timeformat, end='\t\r')
        time.sleep(1)
        t -= 1

# calling getPythonPath function to exexute the program
getPythonPath()
#linkParameterPass()

