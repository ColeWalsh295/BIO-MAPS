# -*- coding: utf-8 -*-
#!c:/Python/python3_6.exe -u

import os
import sys
import traceback
import csv
import pandas as pd
import re
import time
import sched
import datetime
import requests
try: import simplejson as json
except ImportError: import json
import zipfile
import pycurl
from urllib.request import Request, urlopen
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import numpy as np
import ReportGen_BIOMAPS

# Setting user Parameters
global apiToken, DataCenter, BIOMAPSEmail, UserEmail, ChangeURL
apiToken = 'NA'# Change token for different Qualtrics account
SharedJenny = 'NA'
SharedMindi = 'NA'
SharedEcoEvoMAPS = [SharedMindi]
SharedPhysMAPS = [SharedJenny]
SharedCapstone = [SharedJenny]
DataCenter = 'cornell'
baseURL = "https://{0}.qualtrics.com/API/v3/responseexports/".format(DataCenter)
ChangeURL = "https://{0}.qualtrics.com/jfe/form/SV_24b3m5CGBuWe08l".format(DataCenter)

BIOMAPSEmail = 'biomaps@cornell.edu' # Shared BIOMAPS email address
UserEmail = 'as-phy-edresearchlab@cornell.edu' # User email address
EmailPassword = 'NA' # User password
MainDirectory = "C:/BIOMAPS"

# Main Exceution body which repaets every hour
def main():
    InstructorSurveyControl()
    CourseChangesControl()
    SurveyControl()
    ReportControl()
    print("Waiting...")
    s = sched.scheduler(time.time, time.sleep)
    def runprogram(sc):
        try:
            print("Automation executed at: " + time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
            if(int(time.strftime("%H",time.localtime())) == 16):
                SendStatusEmail()
            InstructorSurveyControl()
            CourseChangesControl()
            SurveyControl()
            ReportControl()
            sc.enter(3600, 1, runprogram, (sc,))
            print("Waiting...")
        # If an error occurs somewhere in here, print to screen, but run again in one hour
        except Exception as e:
            print("Error at: " + time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            tb = traceback.extract_tb(exc_tb)[-1]
            print(exc_type, tb[2], tb[1])
            sc.enter(3600, 1, runprogram, (sc,))
            print("Waiting...")
    s.enter(3600, 1, runprogram, (s,))
    s.run()
    return 0

# Check information provided online by instructors
def InstructorSurveyControl():
    print("Checking CIS...")
    os.chdir(MainDirectory) # Main Survey Directory
    with open("MasterCourseData_BIOMAPS.csv", 'r', newline = '\n') as f: # Main Course Information Data
        MasterData = list(csv.reader(f))
        NumRows = len(MasterData)
        global LastAccess
        LastAccess = time.strftime("%d-%b-%Y %H:%M:%S %Z",time.localtime()) # Update last access time to current time
        MasterData[0][1] = LastAccess

    with open("MasterCourseData_BIOMAPS.csv",'w') as f: # Main Course Information Data
        FileWriter = csv.writer(f)
        FileWriter.writerows(MasterData)

    SurveyID = 'SV_79w7jYQmmFtzA0d' # Instructor survey ID
    DownloadResponses(SurveyID) # Course Information Survey downloaded as Course_Information_Survey.csv (or whatever name is used in qualtrics)

    InstructorsDF = pd.read_csv("CIS_BIOMAPS.csv", skiprows = [1, 2])
    InfoDummyDF = pd.read_csv('CIS_BIOMAPS.csv', skiprows = [2]) # Keep Header...we're only going to take one row from this to keep in the course's folder for specific info

    with open("MasterCourseData_BIOMAPS.csv",'a') as f0:
        MasterDataWriter = csv.writer(f0) # Write new entries in online Qualtrics survey to local Master Data file
        for Index, Instructor in InstructorsDF.iterrows():
            if(InstructorsDF.loc[Index, 'Finished'] == 0): # Check if they actually finished the online survey
                continue
            MasterDataRow = 2
            PreviouslyRecorded = False
            while(MasterDataRow < NumRows):
                if(InstructorsDF.loc[Index, 'ResponseID'] == MasterData[MasterDataRow][0]): # ResponseID stored in column zero in .csv file
                    PreviouslyRecorded = True
                    break
                else:
                    MasterDataRow += 1

            if(not PreviouslyRecorded):

                # Parse data from Course Information Survey to fill Master Data File
                # Use Regex to replace any non-alphanumeric characters with underscores...cause instructors fill forms with weird stuff
                ID = InstructorsDF.loc[Index, 'ResponseID']
                FirstName = re.sub('[^0-9a-zA-Z]+', '_', InstructorsDF.loc[Index, 'Q2'])
                LastName = re.sub('[^0-9a-zA-Z]+', '_', InstructorsDF.loc[Index, 'Q3'])
                Email = InstructorsDF.loc[Index, 'Q4']
                School = re.sub('[^0-9a-zA-Z]+', '_', InstructorsDF.loc[Index, 'Q5'])
                CourseYear = datetime.datetime.now().strftime('%Y')
                if(InstructorsDF.loc[Index, 'Q15'] == 1):
                    CreditOffered = True
                else:
                    CreditOffered = False
                SchoolType = int(InstructorsDF.loc[Index, 'Q16'])

                if(pd.notnull(InstructorsDF.loc[Index, 'EcoEvoD_v2'])):
                    EcoEvoType = int(InstructorsDF.loc[Index, 'EcoEvoA'])
                    EcoEvoCourseName = re.sub('[^0-9a-zA-Z]+', '_', InstructorsDF.loc[Index, 'EcoEvoB'])
                    EcoEvoCourseNumber = re.sub('[^0-9a-zA-Z]+', '_', str(InstructorsDF.loc[Index, 'EcoEvoC']))
                    EcoEvoClass = InstructorsDF.loc[Index, 'EcoEvo_Class']
                    EcoEvoCloseDate = datetime.datetime.strptime(InstructorsDF.loc[Index, 'EcoEvoD_v2'], "%m-%d-%Y")
                    if(EcoEvoCloseDate < datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())):
                        EcoEvoCloseDate = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time()) + datetime.timedelta(days = 14)
                    EcoEvoSurveyID = MakeSurvey(School, EcoEvoCourseNumber, CourseYear, LastName, 'EcoEvo-MAPS')
                    ActivateSurvey(EcoEvoSurveyID)
                    SurveyURL = "https://{0}.qualtrics.com/jfe/form/".format(DataCenter) + EcoEvoSurveyID
                    SendSurvey(ID, Email, FirstName, LastName, EcoEvoCourseName, EcoEvoCourseNumber, EcoEvoCloseDate, 'EcoEvo-MAPS', SurveyURL)
                    EcoEvoSent = time.strftime("%d-%b-%Y %H:%M:%S",time.localtime())
                    EcoEvoCloseDate = EcoEvoCloseDate.strftime("%d-%b-%Y")

                    for User in SharedEcoEvoMAPS: # Share surveys with other interested users
                        ShareSurvey(User, EcoEvoSurveyID)

                    # Create a directory for that term's files if it doesn't exist
                    TermDir = MainDirectory + "/EcoEvo-MAPS/" + str(CourseYear) + "Files"
                    if not os.path.exists(TermDir):
                        os.mkdir(TermDir, 755)

                    # Create a file for that course if it does not already exist
                    CourseDir = School + '_' + str(EcoEvoCourseNumber) + '_' + LastName
                    CourseDir = TermDir + "//" + CourseDir
                    if not os.path.exists(CourseDir):
                        os.mkdir(CourseDir, 755)

                    # Individual course info provided by instructor
                    InfoDummyDF.loc[[0, Index + 1], :].to_csv(CourseDir + '/EcoEvo-MAPS_' + str(CourseYear) + '_' + School + '_' + str(EcoEvoCourseNumber) + '_' + LastName + '_CourseInfo.csv', index = False)
                else:
                    EcoEvoSurveyID = np.nan
                    EcoEvoType = np.nan
                    EcoEvoCourseName = np.nan
                    EcoEvoCourseNumber = np.nan
                    EcoEvoClass = np.nan
                    EcoEvoCloseDate = np.nan
                    EcoEvoSent = np.nan

                if(pd.notnull(InstructorsDF.loc[Index, 'CapD_v2'])):
                    CapType = int(InstructorsDF.loc[Index, 'CapA'])
                    CapCourseName = re.sub('[^0-9a-zA-Z]+', '_', InstructorsDF.loc[Index, 'CapB'])
                    CapCourseNumber = re.sub('[^0-9a-zA-Z]+', '_', str(InstructorsDF.loc[Index, 'CapC']))
                    CapClass = InstructorsDF.loc[Index, 'Cap_Class']
                    CapCloseDate = datetime.datetime.strptime(InstructorsDF.loc[Index, 'CapD_v2'], "%m-%d-%Y")
                    if(CapCloseDate < datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())):
                        CapCloseDate = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time()) + datetime.timedelta(days = 14)
                    CapSurveyID = MakeSurvey(School, CapCourseNumber, CourseYear, LastName, 'Capstone')
                    ActivateSurvey(CapSurveyID)
                    SurveyURL = "https://{0}.qualtrics.com/jfe/form/".format(DataCenter) + CapSurveyID
                    SendSurvey(ID, Email, FirstName, LastName, CapCourseName, CapCourseNumber, CapCloseDate, 'Capstone', SurveyURL)
                    CapSent = time.strftime("%d-%b-%Y %H:%M:%S",time.localtime())
                    CapCloseDate = CapCloseDate.strftime("%d-%b-%Y")

                    for User in SharedCapstone: # Share surveys with other interested users
                        ShareSurvey(User, CapSurveyID)

                    # Create a directory for that term's files if it doesn't exist
                    TermDir = MainDirectory + "/Capstone/" + str(CourseYear) + "Files"
                    if not os.path.exists(TermDir):
                        os.mkdir(TermDir, 755)

                    # Create a file for that course if it does not already exist
                    CourseDir = School + '_' + str(CapCourseNumber) + '_' + LastName
                    CourseDir = TermDir + "//" + CourseDir
                    if not os.path.exists(CourseDir):
                        os.mkdir(CourseDir, 755)

                    # Individual course info provided by instructor
                    InfoDummyDF.loc[[0, Index + 1], :].to_csv(CourseDir + '/Capstone_' + str(CourseYear) + '_' + School + '_' + str(CapCourseNumber) + '_' + LastName + '_CourseInfo.csv', index = False)
                else:
                    CapSurveyID = np.nan
                    CapType = np.nan
                    CapCourseName = np.nan
                    CapCourseNumber = np.nan
                    CapClass = np.nan
                    CapCloseDate = np.nan
                    CapSent = np.nan

                if(pd.notnull(InstructorsDF.loc[Index, 'PhysD_v2'])):
                    PhysType = int(InstructorsDF.loc[Index, 'PhysA'])
                    PhysCourseName = re.sub('[^0-9a-zA-Z]+', '_', InstructorsDF.loc[Index, 'PhysB'])
                    PhysCourseNumber = re.sub('[^0-9a-zA-Z]+', '_', str(InstructorsDF.loc[Index, 'PhysC']))
                    PhysClass = InstructorsDF.loc[Index, 'Phys_Class']
                    PhysCloseDate = datetime.datetime.strptime(InstructorsDF.loc[Index, 'PhysD_v2'], "%m-%d-%Y")
                    if(PhysCloseDate < datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())):
                        PhysCloseDate = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time()) + datetime.timedelta(days = 14)
                    PhysSurveyID = MakeSurvey(School, PhysCourseNumber, CourseYear, LastName, 'Phys-MAPS')
                    ActivateSurvey(PhysSurveyID)
                    SurveyURL = "https://{0}.qualtrics.com/jfe/form/".format(DataCenter) + PhysSurveyID
                    SendSurvey(ID, Email, FirstName, LastName, PhysCourseName, PhysCourseNumber, PhysCloseDate, 'PhysMAPS', SurveyURL)
                    PhysSent = time.strftime("%d-%b-%Y %H:%M:%S",time.localtime())
                    PhysCloseDate = PhysCloseDate.strftime("%d-%b-%Y")

                    for User in SharedPhysMAPS: # Share surveys with other interested users
                        ShareSurvey(User, SharedPhysMAPS)

                    # Create a directory for that term's files if it doesn't exist
                    TermDir = MainDirectory + "/Phys-MAPS/" + str(CourseYear) + "Files"
                    if not os.path.exists(TermDir):
                        os.mkdir(TermDir, 755)

                    # Create a file for that course if it does not already exist
                    CourseDir = School + '_' + str(PhysCourseNumber) + '_' + LastName
                    CourseDir = TermDir + "//" + CourseDir
                    if not os.path.exists(CourseDir):
                        os.mkdir(CourseDir, 755)

                    # Individual course info provided by instructor
                    InfoDummyDF.loc[[0, Index + 1], :].to_csv(CourseDir + '/Phys-MAPS_' + str(CourseYear) + '_' + School + '_' + str(PhysCourseNumber) + '_' + LastName + '_CourseInfo.csv', index = False)
                else:
                    PhysSurveyID = np.nan
                    PhysType = np.nan
                    PhysCourseName = np.nan
                    PhysCourseNumber = np.nan
                    PhysClass = np.nan
                    PhysCloseDate = np.nan
                    PhysSent = np.nan

                if(pd.notnull(InstructorsDF.loc[Index, 'GenBioD_v2'])):
                    GenBioType = int(InstructorsDF.loc[Index, 'GenBioA'])
                    GenBioCourseName = re.sub('[^0-9a-zA-Z]+', '_', InstructorsDF.loc[Index, 'GenBioB'])
                    GenBioCourseNumber = re.sub('[^0-9a-zA-Z]+', '_', str(InstructorsDF.loc[Index, 'GenBioC']))
                    GenBioClass = InstructorsDF.loc[Index, 'GenBio_Class']
                    GenBioCloseDate = datetime.datetime.strptime(InstructorsDF.loc[Index, 'GenBioD_v2'], "%m-%d-%Y")
                    if(GenBioCloseDate < datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())):
                        GenBioCloseDate = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time()) + datetime.timedelta(days = 14)
                    GenBioSurveyID = MakeSurvey(School, GenBioCourseNumber, CourseYear, LastName, 'GenBio-MAPS')
                    ActivateSurvey(GenBioSurveyID)
                    SurveyURL = "https://{0}.qualtrics.com/jfe/form/".format(DataCenter) + GenBioSurveyID
                    SendSurvey(ID, Email, FirstName, LastName, GenBioCourseName, GenBioCourseNumber, GenBioCloseDate, 'GenBioMAPS', SurveyURL)
                    GenBioSent = time.strftime("%d-%b-%Y %H:%M:%S",time.localtime())
                    GenBioCloseDate = GenBioCloseDate.strftime("%d-%b-%Y")

                    # Create a directory for that term's files if it doesn't exist
                    TermDir = MainDirectory + "/GenBio-MAPS/" + str(CourseYear) + "Files"
                    if not os.path.exists(TermDir):
                        os.mkdir(TermDir, 755)

                    # Create a file for that course if it does not already exist
                    CourseDir = School + '_' + str(GenBioCourseNumber) + '_' + LastName
                    CourseDir = TermDir + "//" + CourseDir
                    if not os.path.exists(CourseDir):
                        os.mkdir(CourseDir, 755)

                    # Individual course info provided by instructor
                    InfoDummyDF.loc[[0, Index + 1], :].to_csv(CourseDir + '/GenBio-MAPS_' + str(CourseYear) + '_' + School + '_' + str(GenBioCourseNumber) + '_' + LastName + '_CourseInfo.csv', index = False)
                else:
                    GenBioSurveyID = np.nan
                    GenBioType = np.nan
                    GenBioCourseName = np.nan
                    GenBioCourseNumber = np.nan
                    GenBioClass = np.nan
                    GenBioCloseDate = np.nan
                    GenBioSent = np.nan

                # Write all data for new course to Master File for later reference
                csvUpdate = [ID, CourseYear, FirstName, LastName, Email, School, SchoolType, CreditOffered, EcoEvoSurveyID, EcoEvoType, EcoEvoCourseName, EcoEvoCourseNumber, EcoEvoClass, EcoEvoCloseDate, EcoEvoSent,'','','', CapSurveyID, CapType, CapCourseName,
                    CapCourseNumber, CapClass, CapCloseDate, CapSent,'','','', PhysSurveyID, PhysType, PhysCourseName, PhysCourseNumber, PhysClass, PhysCloseDate, PhysSent,'','','', GenBioSurveyID, GenBioType, GenBioCourseName, GenBioCourseNumber, GenBioClass, GenBioCloseDate, GenBioSent,'','','']
                MasterDataWriter.writerow(csvUpdate)

    os.remove('CIS_BIOMAPS.csv')

# Check the online form for changing dates and update the necessary dates in the Master file
def CourseChangesControl():
    print("Checking Changes...")
    MasterDF = pd.read_csv('MasterCourseData_BIOMAPS.csv', skiprows = [0], index_col = 'ID')

    ChangeDates_SurveyID = "SV_24b3m5CGBuWe08l"
    DownloadResponses(ChangeDates_SurveyID)
    ChangesDF = pd.read_csv("BIOMAPS_Date_Changes.csv", skiprows = [1, 2])

    NumChanges = len(ChangesDF)

    ChangeLogDF = pd.read_csv('BIOMAPS_ChangeLog.csv')
    ChangesDF = ChangesDF[((~ChangesDF[['ResponseID']].isin(ChangeLogDF[['ResponseID']])).as_matrix().flatten()) & ((ChangesDF[['Finished']] == 1).as_matrix().flatten())] # Get new changes to implement

    with open("BIOMAPS_ChangeLog.csv",'a') as f:
        ChangeLogWriter = csv.writer(f)

        for Index, Change in ChangesDF.iterrows():
            InstructorID = ChangesDF.loc[Index, 'Q1']
            # Log the online survey entries in the local copy of changes
            ChangeLogWriter.writerow([ChangesDF.loc[Index, 'ResponseID'], time.strftime("%d-%b-%Y %H:%M:%S", time.localtime()), ChangesDF.loc[Index, 'Q1'], ChangesDF.loc[Index, 'EcoEvo_Date'], ChangesDF.loc[Index, 'EcoEvo_R'], ChangesDF.loc[Index, 'Cap_Date'],
                                        ChangesDF.loc[Index, 'Cap_R'], ChangesDF.loc[Index, 'Phys_Date'], ChangesDF.loc[Index, 'Phys_R'], ChangesDF.loc[Index, 'GenBio_Date'], ChangesDF.loc[Index, 'GenBio_R']])
            # If any incorrect IDs or dates are entered...move on...otherwise update the Master dataframe
            if(InstructorID not in MasterDF.index):
                continue

            if(pd.notnull(MasterDF.loc[InstructorID, 'EcoEvo End']) & (pd.isnull(MasterDF.loc[InstructorID, 'EcoEvo Closed'])) & (pd.notnull(ChangesDF.loc[Index, 'EcoEvo_Date']))):
                try:
                    MasterDF.loc[InstructorID, 'EcoEvo End'] = datetime.datetime.strptime(ChangesDF.loc[Index, 'EcoEvo_Date'], "%m-%d-%Y").strftime("%d-%b-%Y")
                except ValueError:
                    continue

                # Reset reminder email statuses if requested
                if(ChangesDF.loc[Index, 'EcoEvo_R'] == 1):
                    MasterDF.loc[InstructorID, 'EcoEvo Reminder'] = np.nan
                elif((ChangesDF.loc[Index, 'EcoEvo_R'] == 2) and pd.isnull(MasterDF.loc[InstructorID, 'EcoEvo Reminder'])):
                    MasterDF.loc[InstructorID, 'EcoEvo Reminder'] = time.strftime("%d-%b-%Y %H:%M:%S", time.localtime())

                # Send email to instructor letting them know that the dates have been changed
                ChangesEmailSend(InstructorID, MasterDF.loc[InstructorID, 'Email'], MasterDF.loc[InstructorID, 'First Name'], MasterDF.loc[InstructorID, 'Last Name'], MasterDF.loc[InstructorID, 'EcoEvo Name'],
                                    MasterDF.loc[InstructorID, 'EcoEvo Number'], 'EcoEvo-MAPS', MasterDF.loc[InstructorID, 'EcoEvo End'])

            if(pd.notnull(MasterDF.loc[InstructorID, 'Capstone End']) & (pd.isnull(MasterDF.loc[InstructorID, 'Capstone Closed'])) & (pd.notnull(ChangesDF.loc[Index, 'Cap_Date']))):
                try:
                    MasterDF.loc[InstructorID, 'Capstone End'] = datetime.datetime.strptime(ChangesDF.loc[Index, 'Cap_Date'], "%m-%d-%Y").strftime("%d-%b-%Y")
                except ValueError:
                    continue

                # Reset reminder email statuses if requested
                if(ChangesDF.loc[Index, 'Cap_R'] == 1):
                    MasterDF.loc[InstructorID, 'Capstone Reminder'] = np.nan
                elif((ChangesDF.loc[Index, 'Cap_R'] == 2) and pd.isnull(MasterDF.loc[InstructorID, 'Capstone Reminder'])):
                    MasterDF.loc[InstructorID, 'Capstone Reminder'] = time.strftime("%d-%b-%Y %H:%M:%S", time.localtime())

                # Send email to instructor letting them know that the dates have been changed
                ChangesEmailSend(InstructorID, MasterDF.loc[InstructorID, 'Email'], MasterDF.loc[InstructorID, 'First Name'], MasterDF.loc[InstructorID, 'Last Name'], MasterDF.loc[InstructorID, 'Capstone Name'],
                                    MasterDF.loc[InstructorID, 'Capstone Number'], 'Capstone', MasterDF.loc[InstructorID, 'Capstone End'])

            if(pd.notnull(MasterDF.loc[InstructorID, 'Phys End']) & (pd.isnull(MasterDF.loc[InstructorID, 'Phys Closed'])) & (pd.notnull(ChangesDF.loc[Index, 'Phys_Date']))):
                try:
                    MasterDF.loc[InstructorID, 'Phys End'] = datetime.datetime.strptime(ChangesDF.loc[Index, 'Phys_Date'], "%m-%d-%Y").strftime("%d-%b-%Y")
                except ValueError:
                    continue

                # Reset reminder email statuses if requested
                if(ChangesDF.loc[Index, 'Phys_R'] == 1):
                    MasterDF.loc[InstructorID, 'Phys Reminder'] = np.nan
                elif((ChangesDF.loc[Index, 'Phys_R'] == 2) and pd.isnull(MasterDF.loc[InstructorID, 'Phys Reminder'])):
                    MasterDF.loc[InstructorID, 'Phys Reminder'] = time.strftime("%d-%b-%Y %H:%M:%S", time.localtime())

                # Send email to instructor letting them know that the dates have been changed
                ChangesEmailSend(InstructorID, MasterDF.loc[InstructorID, 'Email'], MasterDF.loc[InstructorID, 'First Name'], MasterDF.loc[InstructorID, 'Last Name'], MasterDF.loc[InstructorID, 'Phys Name'],
                                    MasterDF.loc[InstructorID, 'Phys Number'], 'Phys-MAPS', MasterDF.loc[InstructorID, 'Phys End'])

            if(pd.notnull(MasterDF.loc[InstructorID, 'GenBio End']) & (pd.isnull(MasterDF.loc[InstructorID, 'GenBio Closed'])) & (pd.notnull(ChangesDF.loc[Index, 'GenBio_Date']))):
                try:
                    MasterDF.loc[InstructorID, 'GenBio End'] = datetime.datetime.strptime(ChangesDF.loc[Index, 'GenBio_Date'], "%m-%d-%Y").strftime("%d-%b-%Y")
                except ValueError:
                    continue

                # Reset reminder email statuses if requested
                if(ChangesDF.loc[Index, 'GenBio_R'] == 1):
                    MasterDF.loc[InstructorID, 'GenBio Reminder'] = np.nan
                elif((ChangesDF.loc[Index, 'GenBio_R'] == 2) and pd.isnull(MasterDF.loc[InstructorID, 'GenBio Reminder'])):
                    MasterDF.loc[InstructorID, 'GenBio Reminder'] = time.strftime("%d-%b-%Y %H:%M:%S", time.localtime())

                # Send email to instructor letting them know that the dates have been changed
                ChangesEmailSend(InstructorID, MasterDF.loc[InstructorID, 'Email'], MasterDF.loc[InstructorID, 'First Name'], MasterDF.loc[InstructorID, 'Last Name'], MasterDF.loc[InstructorID, 'GenBio Name'],
                                    MasterDF.loc[InstructorID, 'GenBio Number'], 'GenBio-MAPS', MasterDF.loc[InstructorID, 'GenBio End'])

    # Write Master dataframe to file
    with open(MainDirectory + "/MasterCourseData_BIOMAPS.csv", 'w') as f:
        MasterDataWriter = csv.writer(f)
        MasterDataWriter.writerows([['Last Accessed:', LastAccess]])
    with open(MainDirectory + "/MasterCourseData_BIOMAPS.csv", 'a') as f:
        MasterDF.to_csv(f, index = True)

    os.remove('BIOMAPS_Date_Changes.csv')

def SurveyControl():
    # Send Pre survey, reminders, or close the pre-survey
    print("Checking survey reminders, end dates, etc...")
    CurrentTime = datetime.datetime.now()
    MasterDF = pd.read_csv(MainDirectory + "/MasterCourseData_BIOMAPS.csv", skiprows = [0])
    for Index, Course in MasterDF.iterrows():

        # EcoEvo-MAPS
        if(pd.notnull(MasterDF.loc[Index, 'EcoEvo ID']) & (pd.isnull(MasterDF.loc[Index, 'EcoEvo Closed']))):
            # If Survey not closed, check what time it is and what to do
            SurveyID = MasterDF.loc[Index, 'EcoEvo ID']
            SurveyURL = "https://{0}.qualtrics.com/jfe/form/".format(DataCenter) + SurveyID
            CloseDate = datetime.datetime.strptime(MasterDF.loc[Index, 'EcoEvo End'], "%d-%b-%Y")

            if(pd.isnull(MasterDF.loc[Index, 'EcoEvo Sent'])):
                # Send Pre-Survey if it hasn't been done so already
                SendSurvey(SurveyID, MasterDF.loc[Index, 'Email'], MasterDF.loc[Index, 'First Name'], MasterDF.loc[Index, 'Last Name'], MasterDF.loc[Index, 'EcoEvo Name'], MasterDF.loc[Index, 'EcoEvo Number'], CloseDate, 'EcoEvo-MAPS', SurveyURL)
                MasterDF.loc[Index, 'Pre-Survey Sent'] = time.strftime("%d-%b-%Y %H:%M:%S",time.localtime())

            elif((CurrentTime >= (CloseDate - datetime.timedelta(days = 4))) and pd.isnull(MasterDF.loc[Index, 'EcoEvo Reminder'])):
                # Send Pre-Survey reminder if we haven't already
                NumStudents = GetResponseData(MasterDF.loc[Index, 'School Name'], MasterDF.loc[Index, 'EcoEvo Number'], MasterDF.loc[Index, 'Last Name'], MasterDF.loc[Index, 'Course Year'], 'EcoEvo-MAPS', SurveyID)
                if(NumStudents == 0):
                    # If nobody has responded yet, give extra time and send a reminder
                    CloseDate = CloseDate + datetime.timedelta(days = 3)
                    MasterDF.loc[Index, 'EcoEvo End'] = CloseDate.strftime("%d-%b-%Y")
                    ZeroResponseEmail(MasterDF.loc[Index, 'ID'], MasterDF.loc[Index, 'Email'], MasterDF.loc[Index, 'First Name'], MasterDF.loc[Index, 'Last Name'], MasterDF.loc[Index, 'EcoEvo Name'], MasterDF.loc[Index, 'EcoEvo Number'], CloseDate, 'EcoEvo-MAPS', SurveyURL)
                    MasterDF.loc[Index, 'EcoEvo Reminder'] = time.strftime("%d-%b-%Y %H:%M:%S", time.localtime())
                else:
                    ReminderEmailSend(MasterDF.loc[Index, 'ID'], MasterDF.loc[Index, 'Email'], MasterDF.loc[Index, 'First Name'], MasterDF.loc[Index, 'Last Name'], MasterDF.loc[Index, 'EcoEvo Name'], MasterDF.loc[Index, 'EcoEvo Number'], CloseDate, 'EcoEvo-MAPS', SurveyURL, NumStudents)
                    MasterDF.loc[Index, 'EcoEvo Reminder'] = time.strftime("%d-%b-%Y %H:%M:%S", time.localtime())

            elif(CurrentTime >= (CloseDate + datetime.timedelta(hours = 23, minutes = 59, seconds = 59))):
                # Close the Pre-Survey
                CloseSurvey(SurveyID)
                MasterDF.loc[Index, 'EcoEvo Closed'] = time.strftime("%d-%b-%Y %H:%M:%S", time.localtime())

        # Capstone
        if(pd.notnull(MasterDF.loc[Index, 'Capstone ID']) & (pd.isnull(MasterDF.loc[Index, 'Capstone Closed']))):
            # If Survey not closed, check what time it is and what to do
            SurveyID = MasterDF.loc[Index, 'Capstone ID']
            SurveyURL = "https://{0}.qualtrics.com/jfe/form/".format(DataCenter) + SurveyID
            CloseDate = datetime.datetime.strptime(MasterDF.loc[Index, 'Capstone End'], "%d-%b-%Y")

            if(pd.isnull(MasterDF.loc[Index, 'Capstone Sent'])):
                # Send Pre-Survey if it hasn't been done so already
                SendSurvey(SurveyID, MasterDF.loc[Index, 'Email'], MasterDF.loc[Index, 'First Name'], MasterDF.loc[Index, 'Last Name'], MasterDF.loc[Index, 'Capstone Name'], MasterDF.loc[Index, 'Capstone Number'], CloseDate, 'Capstone', SurveyURL)
                MasterDF.loc[Index, 'Pre-Survey Sent'] = time.strftime("%d-%b-%Y %H:%M:%S",time.localtime())

            elif((CurrentTime >= (CloseDate - datetime.timedelta(days = 4))) and pd.isnull(MasterDF.loc[Index, 'Capstone Reminder'])):
                # Send Pre-Survey reminder if we haven't already
                NumStudents = GetResponseData(MasterDF.loc[Index, 'School Name'], MasterDF.loc[Index, 'Capstone Number'], MasterDF.loc[Index, 'Last Name'], MasterDF.loc[Index, 'Course Year'], 'Capstone', SurveyID)
                if(NumStudents == 0):
                    # If nobody has responded yet, give extra time and send a reminder
                    CloseDate = CloseDate + datetime.timedelta(days = 3)
                    MasterDF.loc[Index, 'Capstone End'] = CloseDate.strftime("%d-%b-%Y")
                    ZeroResponseEmail(MasterDF.loc[Index, 'ID'], MasterDF.loc[Index, 'Email'], MasterDF.loc[Index, 'First Name'], MasterDF.loc[Index, 'Last Name'], MasterDF.loc[Index, 'Capstone Name'], MasterDF.loc[Index, 'Capstone Number'], CloseDate, 'Capstone', SurveyURL)
                    MasterDF.loc[Index, 'Capstone Reminder'] = time.strftime("%d-%b-%Y %H:%M:%S", time.localtime())
                else:
                    ReminderEmailSend(MasterDF.loc[Index, 'ID'], MasterDF.loc[Index, 'Email'], MasterDF.loc[Index, 'First Name'], MasterDF.loc[Index, 'Last Name'], MasterDF.loc[Index, 'Capstone Name'], MasterDF.loc[Index, 'Capstone Number'], CloseDate, 'Capstone', SurveyURL, NumStudents)
                    MasterDF.loc[Index, 'Capstone Reminder'] = time.strftime("%d-%b-%Y %H:%M:%S", time.localtime())

            elif(CurrentTime >= (CloseDate + datetime.timedelta(hours = 23, minutes = 59, seconds = 59))):
                # Close the Pre-Survey
                CloseSurvey(SurveyID)
                MasterDF.loc[Index, 'Capstone Closed'] = time.strftime("%d-%b-%Y %H:%M:%S", time.localtime())

        # Phys-MAPS
        if(pd.notnull(MasterDF.loc[Index, 'Phys ID']) & (pd.isnull(MasterDF.loc[Index, 'Phys Closed']))):
            # If Survey not closed, check what time it is and what to do
            SurveyID = MasterDF.loc[Index, 'Phys ID']
            SurveyURL = "https://{0}.qualtrics.com/jfe/form/".format(DataCenter) + SurveyID
            CloseDate = datetime.datetime.strptime(MasterDF.loc[Index, 'Phys End'], "%d-%b-%Y")

            if(pd.isnull(MasterDF.loc[Index, 'Phys Sent'])):
                # Send Pre-Survey if it hasn't been done so already
                SendSurvey(SurveyID, MasterDF.loc[Index, 'Email'], MasterDF.loc[Index, 'First Name'], MasterDF.loc[Index, 'Last Name'], MasterDF.loc[Index, 'Phys Name'], MasterDF.loc[Index, 'Phys Number'], CloseDate, 'Phys-MAPS', SurveyURL)
                MasterDF.loc[Index, 'Pre-Survey Sent'] = time.strftime("%d-%b-%Y %H:%M:%S",time.localtime())

            elif((CurrentTime >= (CloseDate - datetime.timedelta(days = 4))) and pd.isnull(MasterDF.loc[Index, 'Phys Reminder'])):
                # Send Pre-Survey reminder if we haven't already
                NumStudents = GetResponseData(MasterDF.loc[Index, 'School Name'], MasterDF.loc[Index, 'Phys Number'], MasterDF.loc[Index, 'Last Name'], MasterDF.loc[Index, 'Course Year'], 'Phys-MAPS', SurveyID)
                if(NumStudents == 0):
                    # If nobody has responded yet, give extra time and send a reminder
                    CloseDate = CloseDate + datetime.timedelta(days = 3)
                    MasterDF.loc[Index, 'Phys End'] = CloseDate.strftime("%d-%b-%Y")
                    ZeroResponseEmail(MasterDF.loc[Index, 'ID'], MasterDF.loc[Index, 'Email'], MasterDF.loc[Index, 'First Name'], MasterDF.loc[Index, 'Last Name'], MasterDF.loc[Index, 'Phys Name'], MasterDF.loc[Index, 'Phys Number'], CloseDate, 'Phys-MAPS', SurveyURL)
                    MasterDF.loc[Index, 'Phys Reminder'] = time.strftime("%d-%b-%Y %H:%M:%S", time.localtime())
                else:
                    ReminderEmailSend(MasterDF.loc[Index, 'ID'], MasterDF.loc[Index, 'Email'], MasterDF.loc[Index, 'First Name'], MasterDF.loc[Index, 'Last Name'], MasterDF.loc[Index, 'Phys Name'], MasterDF.loc[Index, 'Phys Number'], CloseDate, 'Phys-MAPS', SurveyURL, NumStudents)
                    MasterDF.loc[Index, 'Phys Reminder'] = time.strftime("%d-%b-%Y %H:%M:%S", time.localtime())

            elif(CurrentTime >= (CloseDate + datetime.timedelta(hours = 23, minutes = 59, seconds = 59))):
                # Close the Pre-Survey
                CloseSurvey(SurveyID)
                MasterDF.loc[Index, 'Phys Closed'] = time.strftime("%d-%b-%Y %H:%M:%S", time.localtime())

        # GenBio-MAPS
        if(pd.notnull(MasterDF.loc[Index, 'GenBio ID']) & (pd.isnull(MasterDF.loc[Index, 'GenBio Closed']))):
            # If Survey not closed, check what time it is and what to do
            SurveyID = MasterDF.loc[Index, 'GenBio ID']
            SurveyURL = "https://{0}.qualtrics.com/jfe/form/".format(DataCenter) + SurveyID
            CloseDate = datetime.datetime.strptime(MasterDF.loc[Index, 'GenBio End'], "%d-%b-%Y")

            if(pd.isnull(MasterDF.loc[Index, 'GenBio Sent'])):
                # Send Pre-Survey if it hasn't been done so already
                SendSurvey(SurveyID, MasterDF.loc[Index, 'Email'], MasterDF.loc[Index, 'First Name'], MasterDF.loc[Index, 'Last Name'], MasterDF.loc[Index, 'GenBio Name'], MasterDF.loc[Index, 'GenBio Number'], CloseDate, 'GenBio-MAPS', SurveyURL)
                MasterDF.loc[Index, 'Pre-Survey Sent'] = time.strftime("%d-%b-%Y %H:%M:%S",time.localtime())

            elif((CurrentTime >= (CloseDate - datetime.timedelta(days = 4))) and pd.isnull(MasterDF.loc[Index, 'GenBio Reminder'])):
                # Send Pre-Survey reminder if we haven't already
                NumStudents = GetResponseData(MasterDF.loc[Index, 'School Name'], MasterDF.loc[Index, 'GenBio Number'], MasterDF.loc[Index, 'Last Name'], MasterDF.loc[Index, 'Course Year'], 'GenBio-MAPS', SurveyID)
                if(NumStudents == 0):
                    # If nobody has responded yet, give extra time and send a reminder
                    CloseDate = CloseDate + datetime.timedelta(days = 3)
                    MasterDF.loc[Index, 'GenBio End'] = CloseDate.strftime("%d-%b-%Y")
                    ZeroResponseEmail(MasterDF.loc[Index, 'ID'], MasterDF.loc[Index, 'Email'], MasterDF.loc[Index, 'First Name'], MasterDF.loc[Index, 'Last Name'], MasterDF.loc[Index, 'GenBio Name'], MasterDF.loc[Index, 'GenBio Number'], CloseDate, 'GenBio-MAPS', SurveyURL)
                    MasterDF.loc[Index, 'GenBio Reminder'] = time.strftime("%d-%b-%Y %H:%M:%S", time.localtime())
                else:
                    ReminderEmailSend(MasterDF.loc[Index, 'ID'], MasterDF.loc[Index, 'Email'], MasterDF.loc[Index, 'First Name'], MasterDF.loc[Index, 'Last Name'], MasterDF.loc[Index, 'GenBio Name'], MasterDF.loc[Index, 'GenBio Number'], CloseDate, 'GenBio-MAPS', SurveyURL, NumStudents)
                    MasterDF.loc[Index, 'GenBio Reminder'] = time.strftime("%d-%b-%Y %H:%M:%S", time.localtime())

            elif(CurrentTime >= (CloseDate + datetime.timedelta(hours = 23, minutes = 59, seconds = 59))):
                # Close the Pre-Survey
                CloseSurvey(SurveyID)
                MasterDF.loc[Index, 'GenBio Closed'] = time.strftime("%d-%b-%Y %H:%M:%S", time.localtime())

    with open(MainDirectory + "/MasterCourseData_BIOMAPS.csv", 'w') as f:
        MasterDataWriter = csv.writer(f)
        MasterDataWriter.writerows([['Last Accessed:', LastAccess]])
    with open(MainDirectory + "/MasterCourseData_BIOMAPS.csv", 'a') as f:
        MasterDF.to_csv(f, index = False)

# Score the surveys, construct the reports, and send them out
def ReportControl():
    print("Checking Report Data...")
    MasterDF = pd.read_csv(MainDirectory + "/MasterCourseData_BIOMAPS.csv", skiprows = [0])
    for Index, Course in MasterDF.iterrows():

        # EcoEvo-MAPS
        if(pd.isnull(MasterDF.loc[Index, 'EcoEvo Report']) and pd.notnull(MasterDF.loc[Index, 'EcoEvo Closed'])):
            Path = MainDirectory + "/EcoEvo-MAPS/" + str(MasterDF.loc[Index, 'Course Year']) + "Files/" + MasterDF.loc[Index, 'School Name'] + '_' + str(MasterDF.loc[Index, 'EcoEvo Number']) + '_' + MasterDF.loc[Index, 'Last Name']
            os.chdir(Path)
            DownloadResponses(MasterDF.loc[Index, 'EcoEvo ID'])
            SurveyName = GetSurveyName(MasterDF.loc[Index, 'EcoEvo ID'])
            df = pd.read_csv(SurveyName + '.csv', skiprows = [1, 2])
            df, NamesDF = ValidateResponses(df, 'EcoEvo-MAPS')
            if(len(df.index) > 4):
                PDFName = 'EcoEvo-MAPS' + str(MasterDF.loc[Index, 'Course Year']) + '_' + MasterDF.loc[Index, 'School Name'] + '_' + str(MasterDF.loc[Index, 'EcoEvo Number']) + '_' + MasterDF.loc[Index, 'Last Name'] + '_Report'
                print(PDFName)
                ReportGen_BIOMAPS.Generate_EcoEvoMAPS(Path + '/' + PDFName, r'\textwidth', DataFrame = df, NumReported = MasterDF.loc[Index, 'EcoEvo Class'], MainDirectory = MainDirectory, Where = 'Automation')

                if(MasterDF.loc[Index, 'Credit Offered']): # If the instructor is offering credit include a list of names and IDs of those who completed each of the surveys
                    NamesFileName = 'EcoEvo-MAPS' + str(MasterDF.loc[Index, 'Course Year']) + '_' + MasterDF.loc[Index, 'School Name'] + '_' + str(MasterDF.loc[Index, 'EcoEvo Number']) +'_' + MasterDF.loc[Index, 'Last Name'] + '_Names.csv'
                    NamesDF.to_csv(NamesFileName, index = False)
                    SendReport(MasterDF.loc[Index, 'Email'], MasterDF.loc[Index, 'First Name'], MasterDF.loc[Index, 'Last Name'], MasterDF.loc[Index, 'EcoEvo Name'], MasterDF.loc[Index, 'EcoEvo Number'], 'EcoEvo-MAPS', Path + '/' + PDFName + '.pdf', NamesFile = NamesFileName)
                else:
                    SendReport(MasterDF.loc[Index, 'Email'], MasterDF.loc[Index, 'First Name'], MasterDF.loc[Index, 'Last Name'], MasterDF.loc[Index, 'EcoEvo Name'], MasterDF.loc[Index, 'EcoEvo Number'], 'EcoEvo-MAPS', Path + '/' + PDFName + '.pdf')
            MasterDF.loc[Index, 'EcoEvo Report'] = time.strftime("%d-%b-%Y %H:%M:%S", time.localtime())

        # Capstone
        if(pd.isnull(MasterDF.loc[Index, 'Capstone Report']) and pd.notnull(MasterDF.loc[Index, 'Capstone Closed'])):
            Path = MainDirectory + "/Capstone/" + str(MasterDF.loc[Index, 'Course Year']) + "Files/" + MasterDF.loc[Index, 'School Name'] + '_' + str(MasterDF.loc[Index, 'Capstone Number']) + '_' + MasterDF.loc[Index, 'Last Name']
            os.chdir(Path)
            DownloadResponses(MasterDF.loc[Index, 'Capstone ID'])
            SurveyName = GetSurveyName(MasterDF.loc[Index, 'Capstone ID'])
            df = pd.read_csv(SurveyName + '.csv', skiprows = [1, 2])
            df, NamesDF = ValidateResponses(df, 'Capstone')
            if(len(df.index) > 4):
                PDFName = 'Capstone' + str(MasterDF.loc[Index, 'Course Year']) + '_' + MasterDF.loc[Index, 'School Name'] + '_' + str(MasterDF.loc[Index, 'Capstone Number']) + '_' + MasterDF.loc[Index, 'Last Name'] + '_Report'
                print(PDFName)
                ReportGen_BIOMAPS.Generate_Capstone(Path + '/' + PDFName, r'\textwidth', DataFrame = df, NumReported = MasterDF.loc[Index, 'Capstone Class'], MainDirectory = MainDirectory, Where = 'Automation')

                if(MasterDF.loc[Index, 'Credit Offered']): # If the instructor is offering credit include a list of names and IDs of those who completed each of the surveys
                    NamesFileName = 'Capstone' + str(MasterDF.loc[Index, 'Course Year']) + '_' + MasterDF.loc[Index, 'School Name'] + '_' + str(MasterDF.loc[Index, 'Capstone Number']) +'_' + MasterDF.loc[Index, 'Last Name'] + '_Names.csv'
                    NamesDF.to_csv(NamesFileName, index = False)
                    SendReport(MasterDF.loc[Index, 'Email'], MasterDF.loc[Index, 'First Name'], MasterDF.loc[Index, 'Last Name'], MasterDF.loc[Index, 'Capstone Name'], MasterDF.loc[Index, 'Capstone Number'], 'Capstone', Path + '/' + PDFName + '.pdf', NamesFile = NamesFileName)
                else:
                    SendReport(MasterDF.loc[Index, 'Email'], MasterDF.loc[Index, 'First Name'], MasterDF.loc[Index, 'Last Name'], MasterDF.loc[Index, 'Capstone Name'], MasterDF.loc[Index, 'Capstone Number'], 'Capstone', Path + '/' + PDFName + '.pdf')
            MasterDF.loc[Index, 'Capstone Report'] = time.strftime("%d-%b-%Y %H:%M:%S", time.localtime())
            ########## Remove plots here ############

        # Phys-MAPS
        if(pd.isnull(MasterDF.loc[Index, 'Phys Report']) and pd.notnull(MasterDF.loc[Index, 'Phys Closed'])):
            Path = MainDirectory + "/Phys-MAPS/" + str(MasterDF.loc[Index, 'Course Year']) + "Files/" + MasterDF.loc[Index, 'School Name'] + '_' + str(MasterDF.loc[Index, 'Phys Number']) + '_' + MasterDF.loc[Index, 'Last Name']
            os.chdir(Path)
            DownloadResponses(MasterDF.loc[Index, 'Phys ID'])
            SurveyName = GetSurveyName(MasterDF.loc[Index, 'Phys ID'])
            df = pd.read_csv(SurveyName + '.csv', skiprows = [1, 2])
            df, NamesDF = ValidateResponses(df, 'Phys-MAPS')
            if(len(df.index) > 4):
                PDFName = 'Phys-MAPS' + str(MasterDF.loc[Index, 'Course Year']) + '_' + MasterDF.loc[Index, 'School Name'] + '_' + str(MasterDF.loc[Index, 'Phys Number']) + '_' + MasterDF.loc[Index, 'Last Name'] + '_Report'
                print(PDFName)
                ReportGen_BIOMAPS.Generate_PhysMAPS(Path + '/' + PDFName, r'\textwidth', DataFrame = df, NumReported = MasterDF.loc[Index, 'Phys Class'], MainDirectory = MainDirectory, Where = 'Automation')

                if(MasterDF.loc[Index, 'Credit Offered']): # If the instructor is offering credit include a list of names and IDs of those who completed each of the surveys
                    NamesFileName = 'Phys-MAPS' + str(MasterDF.loc[Index, 'Course Year']) + '_' + MasterDF.loc[Index, 'School Name'] + '_' + str(MasterDF.loc[Index, 'Phys Number']) +'_' + MasterDF.loc[Index, 'Last Name'] + '_Names.csv'
                    NamesDF.to_csv(NamesFileName, index = False)
                    SendReport(MasterDF.loc[Index, 'Email'], MasterDF.loc[Index, 'First Name'], MasterDF.loc[Index, 'Last Name'], MasterDF.loc[Index, 'Phys Name'], MasterDF.loc[Index, 'Phys Number'], 'Phys-MAPS', Path + '/' + PDFName + '.pdf', NamesFile = NamesFileName)
                else:
                    SendReport(MasterDF.loc[Index, 'Email'], MasterDF.loc[Index, 'First Name'], MasterDF.loc[Index, 'Last Name'], MasterDF.loc[Index, 'Phys Name'], MasterDF.loc[Index, 'Phys Number'], 'Phys-MAPS', Path + '/' + PDFName + '.pdf')
            MasterDF.loc[Index, 'Phys Report'] = time.strftime("%d-%b-%Y %H:%M:%S", time.localtime())
            ########## Remove plots here ############

        # GenBio-MAPS
        if(pd.isnull(MasterDF.loc[Index, 'GenBio Report']) and pd.notnull(MasterDF.loc[Index, 'GenBio Closed'])):
            Path = MainDirectory + "/GenBio-MAPS/" + str(MasterDF.loc[Index, 'Course Year']) + "Files/" + MasterDF.loc[Index, 'School Name'] + '_' + str(MasterDF.loc[Index, 'GenBio Number']) + '_' + MasterDF.loc[Index, 'Last Name']
            os.chdir(Path)
            DownloadResponses(MasterDF.loc[Index, 'GenBio ID'])
            SurveyName = GetSurveyName(MasterDF.loc[Index, 'GenBio ID'])
            df = pd.read_csv(SurveyName + '.csv', skiprows = [1, 2])
            df, NamesDF = ValidateResponses(df, 'GenBio-MAPS')
            if(len(df.index) > 4):
                PDFName = 'GenBio-MAPS' + str(MasterDF.loc[Index, 'Course Year']) + '_' + MasterDF.loc[Index, 'School Name'] + '_' + str(MasterDF.loc[Index, 'GenBio Number']) + '_' + MasterDF.loc[Index, 'Last Name'] + '_Report'
                print(PDFName)
                ReportGen_BIOMAPS.Generate_GenBioMAPS(Path + '/' + PDFName, r'\textwidth', DataFrame = df, NumReported = MasterDF.loc[Index, 'GenBio Class'], MainDirectory = MainDirectory, Where = 'Automation')

                if(MasterDF.loc[Index, 'Credit Offered']): # If the instructor is offering credit include a list of names and IDs of those who completed each of the surveys
                    NamesFileName = 'GenBio-MAPS' + str(MasterDF.loc[Index, 'Course Year']) + '_' + MasterDF.loc[Index, 'School Name'] + '_' + str(MasterDF.loc[Index, 'GenBio Number']) +'_' + MasterDF.loc[Index, 'Last Name'] + '_Names.csv'
                    NamesDF.to_csv(NamesFileName, index = False)
                    SendReport(MasterDF.loc[Index, 'Email'], MasterDF.loc[Index, 'First Name'], MasterDF.loc[Index, 'Last Name'], MasterDF.loc[Index, 'GenBio Name'], MasterDF.loc[Index, 'GenBio Number'], 'GenBio-MAPS', Path + '/' + PDFName + '.pdf', NamesFile = NamesFileName)
                else:
                    SendReport(MasterDF.loc[Index, 'Email'], MasterDF.loc[Index, 'First Name'], MasterDF.loc[Index, 'Last Name'], MasterDF.loc[Index, 'GenBio Name'], MasterDF.loc[Index, 'GenBio Number'], 'GenBio-MAPS', Path + '/' + PDFName + '.pdf')
            MasterDF.loc[Index, 'GenBio Report'] = time.strftime("%d-%b-%Y %H:%M:%S", time.localtime())
            ########## Remove plots here ############

    with open(MainDirectory + "/MasterCourseData_BIOMAPS.csv", 'w') as f:
        MasterDataWriter = csv.writer(f)
        MasterDataWriter.writerows([['Last Accessed:', LastAccess]])
    with open(MainDirectory + "/MasterCourseData_BIOMAPS.csv", 'a') as f:
        MasterDF.to_csv(f, index = False)

def MakeSurvey(Institution, Number, Year, InstructorLast, SurveyType):
    baseURL = "https://{0}.qualtrics.com/API/v3/surveys".format(DataCenter)
    headers = {
        "x-api-token": apiToken,
        }

    files = {
        'file': (SurveyType + '.qsf', open(SurveyType + '.qsf', 'rb'), 'application/vnd.qualtrics.survey.qsf')
        }

    data = {
        "name": SurveyType + str(Year) + '_' + Institution + '_' + str(Number) +'_' + InstructorLast,
        }
    response = requests.post(baseURL, files=files, data=data, headers=headers)
    StringResponse = json.dumps(response.json())
    jsonResponse = json.loads(StringResponse)
    SurveyID = jsonResponse['result']['id']
    return SurveyID

def ActivateSurvey(SurveyID):
    baseUrl = "https://{0}.qualtrics.com/API/v3/surveys/{1}".format(DataCenter, SurveyID)
    headers = {
        "content-type": "application/json",
        "x-api-token": apiToken,
        }

    data = {
        "isActive": True,
        }

    response = requests.put(baseUrl, json=data, headers=headers)

def CloseSurvey(SurveyID):
    baseUrl = "https://{0}.qualtrics.com/API/v3/surveys/{1}".format(DataCenter, SurveyID)
    headers = {
        "content-type": "application/json",
        "x-api-token": apiToken,
        }

    data = {
        "isActive": False,
        }

    response = requests.put(baseUrl, json=data, headers=headers)

def SendSurvey(ID, InstructorEmail, InstructorFirst, InstructorLast, Course, Code, SurveyCloseDate, Survey, URL):
    msg = MIMEMultipart('alternative')
    msg['From'] = BIOMAPSEmail
    msg['To'] = InstructorEmail
    msg['Cc'] = BIOMAPSEmail
    msg['Subject'] = Survey + " Survey Link"

    SurveyCloseDate = (SurveyCloseDate + datetime.timedelta(hours = 23, minutes = 59, seconds = 59)).strftime("%d-%b-%Y %H:%M:%S")

    text = """
            Dear Dr. {First} {Last},\n \n

            Thank you again for completing the course information survey. Below is
            the link to the {Survey} survey for your course, {Course} ({Code}): \n \n
            {URL}\n \n
            Please share this link with your students. The date the survey is currently set to close is: \n
            {Close} EST\n
            If you would like to change the date that the {Survey} will stop accepting
            responses from students, please complete the form here with your unique ID({Identifier}):\n\n

            {ChangeURL}\n\n

            Let us know by replying to this email if you have any questions about
            this process. \n \n

            Thank you, \n
            BIOMAPS \n
            This message was sent by an automated system. \n
            """.format(Close = SurveyCloseDate, First = InstructorFirst, Last = InstructorLast, Survey = Survey, Course = Course.replace("_", " "), Code = Code, URL = URL, Identifier = ID, ChangeURL = ChangeURL)

    html = """\
	<html>
	  <head></head>
	  <body>
		<p>Dear Dr. {First} {Last},<br><br>

            Thank you again for completing the course information survey. Below is
            the link to the {Survey} survey for your course, {Course} ({Code}): <br><br>
            {URL}<br><br>
            Please share this link with your students. The date the survey is currently set to close is:<br>
            {Close} EST<br>
            If you would like to change the date that the {Survey} will stop accepting
            responses from students, please complete the form here with your unique ID({Identifier}):<br><br>

            {ChangeURL}<br><br>

            Let us know by replying to this email if you have any questions about
            this process.<br><br>

            Thank you,<br>
            BIOMAPS<br>
            This message was sent by an automated system.<br>
		</p>
	  </body>
	</html>
	""".format(Close = SurveyCloseDate, First = InstructorFirst, Last = InstructorLast, Survey = Survey, Course = Course.replace("_", " "), Code = Code, URL = URL, Identifier = ID, ChangeURL = ChangeURL)


    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    server = smtplib.SMTP(host = 'smtp.office365.com', port = 587)
    server.starttls()
    server.login(UserEmail,EmailPassword)
    server.sendmail(BIOMAPSEmail, [InstructorEmail, BIOMAPSEmail], msg.as_string())
    server.quit()

def ZeroResponseEmail(ID, InstructorEmail, InstructorFirst, InstructorLast, Course, Code, SurveyCloseDate, Survey, URL):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "There have been zero responses to the " + Survey
    msg['From'] = BIOMAPSEmail
    msg['To'] = InstructorEmail
    #msg['To'] = BIOMAPSEmail

    SurveyCloseDate = (SurveyCloseDate + datetime.timedelta(hours = 23, minutes = 59, seconds = 59)).strftime("%d-%b-%Y %H:%M:%S")

    # Create the body of the message (a plain-text and an HTML version).
    text = """
           Dear Dr. {First} {Last},\n \n

           This is a reminder from the BIOMAPS team about the {Survey} survey.
           Currently there are no responses to the survey for your course: {Course} ({Code}). \n \n
           We have extended the close date for the survey to: {Close} EST.\n \n
           If you have not already done so, please send out the link to your class. \n \n
           Here is another link to the survey: \n
           {Link} \n \n

           If you would like to change the date that the survey
           will stop accepting responses from students, please complete the form here
           with your unique ID({Identifier}):\n\n

           {ChangeURL}\n\n

           Let us know by replying to this email if you have any questions about
           this process. \n \n

           Thank you, \n
           BIOMAPS \n
           This message was sent by an automated system. \n
           """.format(First = InstructorFirst, Last = InstructorLast, Survey = Survey, Course = Course.replace("_", " "), Code = Code, Close = SurveyCloseDate, Link = URL, Identifier = ID, ChangeURL = ChangeURL)

    html = """\
    <html>
      <head></head>
      <body>
        Dear Dr. {First} {Last},<br> <br>

           This is a reminder from the BIOMAPS team about the {Survey} survey.
           Currently there are no responses to the survey for your course: {Course} ({Code}) <br> <br>
           We have extended the close date for the survey to: {Close} EST. <br> <br>
           If you have not already done so, please send out the link to your class. <br> <br>
           Here is another link to the survey: <br>
           {Link} <br> <br>

           If you would like to change the date that the survey
           will stop accepting responses from students, please complete the form here
           with your unique ID({Identifier}):<br><br>

           {ChangeURL}<br><br>

           Let us know by replying to this email if you have any questions about
           this process. <br><br>

           Thank you, <br>
           BIOMAPS <br> <br>
           This message was sent by an automated system. <br>
        </p>
      </body>
    </html>
    """.format(First = InstructorFirst, Last = InstructorLast, Survey = Survey, Course = Course.replace("_", " "), Code = Code, Close = SurveyCloseDate, Link = URL, Identifier = ID, ChangeURL = ChangeURL)

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    #Email Credentials


    # The actual mail send
    server = smtplib.SMTP(host = 'smtp.office365.com', port = 587)
    server.starttls()
    server.login(UserEmail, EmailPassword)
    server.sendmail(BIOMAPSEmail, InstructorEmail, msg.as_string())
    #server.sendmail(BIOMAPSEmail, BIOMAPSEmail, msg.as_string())
    server.quit()

def ReminderEmailSend(ID, InstructorEmail, InstructorFirst, InstructorLast, Course, Code, SurveyCloseDate, Survey, URL, NumResponses):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Reminder for the {} survey".format(Survey)
    msg['From'] = BIOMAPSEmail
    msg['To'] = InstructorEmail
    #msg['To'] = BIOMAPSEmail

    SurveyCloseDate = (SurveyCloseDate + datetime.timedelta(hours = 23, minutes = 59, seconds = 59)).strftime("%d-%b-%Y %H:%M:%S")

    # Create the body of the message (a plain-text and an HTML version).
    text = """
		   Dear Dr. {First} {Last},\n \n

           This is a reminder from the BIOMAPS team about the {Survey} survey for
           {Course} ({Code}) which will close on {Close} EST.\n \n
           So far there have been {Responses} responses to the survey.\n \n
           Here is another link to the survey: \n
		   {Link} \n \n

           If you would like to change the date that the survey
           will stop accepting responses from students, please complete the form here
           with your unique ID({Identifier}):\n\n

           {ChangeURL}\n\n

           Let us know by replying to this email if you have any questions about
           this process. \n \n

		   Thank you, \n
		   BIOMAPS \n \n
		   This message was sent by an automated system. \n
		   """.format(First = InstructorFirst, Last = InstructorLast, Survey = Survey, Close = SurveyCloseDate, Link = URL, Responses = NumResponses, Course = Course.replace("_", " "), Code = Code, Identifier = ID, ChangeURL = ChangeURL)

    html = """\
    <html>
	  <head></head>
	  <body>
        <p>Dear Dr. {First} {Last}, <br><br>

            This is a reminder from the BIOMAPS team about the {Survey} survey
            for {Course} ({Code}) which will close on {Close} EST.<br><br>
            So far there have been {Responses} responses to the survey. <br><br>
            Here is another link to the survey: <br>
			{Link} <br>

            If you would like to change the date that the survey
            will stop accepting responses from students, please complete the form here
            with your unique ID({Identifier}):<br><br>

            {ChangeURL}<br><br>


            Let us know by replying to this email if you have any questions about
            this process. <br><br>

		   Thank you, <br>
		   BIOMAPS <br><br>
		   This message was sent by an automated system.
		</p>
	  </body>
    </html>
    """.format(First = InstructorFirst, Last = InstructorLast, Survey = Survey, Close = SurveyCloseDate, Link = URL, Responses = NumResponses, Course = Course.replace("_", " "), Code = Code, Identifier = ID, ChangeURL = ChangeURL)

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # The actual mail send
    server = smtplib.SMTP(host = 'smtp.office365.com', port = 587)
    server.starttls()
    server.login(UserEmail,EmailPassword)
    server.sendmail(BIOMAPSEmail, InstructorEmail, msg.as_string())
    #server.sendmail(BIOMAPSEmail, BIOMAPSEmail, msg.as_string())
    server.quit()

def SendReport(InstructorEmail, InstructorFirst, InstructorLast, Course, Code, Survey, ReportFile, NamesFile = None):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = Survey + " Report"
    msg['From'] = BIOMAPSEmail
    msg['To'] = InstructorEmail
    msg['Cc'] = BIOMAPSEmail

	# Create the body of the message (a plain-text and an HTML version).
    text = """
		   Dear Dr. {First} {Last},\n \n

		   Thank you again for participating in the {Survey}. Please find attached a copy of the report summarizing the {Survey}
		   results for your course, {Course} ({Code}). Additionally, if you indicated to us that you are offering students credit
           for completing the survey we have included a CSV file with their names here.\n\n
		   We are continuing to test and improve our new report generation system, so please let us know by replying to this
		   email if you have any questions, comments, or suggestions regarding this new report format.\n \n

		   Thank you, \n
		   BIOMAPS \n \n
		   This message was sent by an automated system. \n
		   """.format(First = InstructorFirst, Last = InstructorLast, Survey = Survey, Course = Course.replace("_", " "), Code = Code)

    html = """\
	<html>
	  <head></head>
	  <body>
		<p>Dear Dr. {First} {Last},<br><br>
		   Thank you again for participating in the {Survey}. Please find attached a copy of the report summarizing the {Survey}
		   results for your course, {Course} ({Code}). Additionally, if you indicated to us that you are offering students credit
           for completing the survey we have included a CSV file with their names here.<br><br>
		   We are continuing to test and improve our new report generation system, so please let us know by replying to this
		   email if you have any questions, comments, or suggestions regarding this new report format. <br><br>

		   Thank you,<br>
		   BIOMAPS<br> <br>
		   This message was sent by an automated system.
		</p>
	  </body>
	</html>
	""".format(First = InstructorFirst, Last = InstructorLast, Survey = Survey, Course = Course.replace("_", " "), Code = Code)


    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    f_pdf = open(ReportFile, 'rb')
    att_pdf = MIMEApplication(f_pdf.read(), _subtype = "pdf")
    f_pdf.close()
    att_pdf.add_header('Content-Disposition', 'attachment', filename = ReportFile)
    msg.attach(att_pdf)

    if NamesFile is not None:
        f_csv = open(NamesFile, 'rb')
        att_csv = MIMEApplication(f_csv.read(), _subtype="csv")
        f_csv.close()
        att_csv.add_header('Content-Disposition', 'attachment', filename = NamesFile)
        msg.attach(att_csv)

    server = smtplib.SMTP(host = 'smtp.office365.com', port = 587)
    server.starttls()
    server.login(UserEmail, EmailPassword)
    server.sendmail(BIOMAPSEmail, [InstructorEmail, BIOMAPSEmail], msg.as_string())
    server.quit()

def ChangesEmailSend(ID, InstructorEmail, InstructorFirst, InstructorLast, CourseName, Code, Survey, CloseDate):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Changes to Survey Dates"
    msg['From'] = BIOMAPSEmail
    msg['To'] = InstructorEmail
    #msg['To'] = BIOMAPSEmail

	# Create the body of the message (a plain-text and an HTML version).
    text = """
		   Dear Dr. {First} {Last},\n \n

		   Thank you again for participating in the {Survey} survey. Changes were recently made to the close date
           for your class, {Course} ({Code}). This survey is currently set to close for students at the following time:\n\n

           {Close}\n

           If you would like to change this date again, please fill out the form again with your unique ResponseID ({Identifier}):\n\n
           {ChangeURL}\n\n


		   Thank you, \n
		   BIOMAPS \n \n
		   This message was sent by an automated system. \n
		   """.format(First = InstructorFirst, Last = InstructorLast, Survey = Survey, Course = CourseName.replace("_", " "), Code = Code, Close = CloseDate, Identifier = ID, ChangeURL = ChangeURL)

    html = """\
	<html>
	  <head></head>
	  <body>
		<p>Dear Dr. {First} {Last},<br><br>

		   Thank you again for participating in the {Survey} survey. Changes were recently made to the close date
           for your class, {Course} ({Code}). This survey is currently set to close for students at the following time:<br><br>

           {Close}<br>

           If you would like to change this date again, please fill out the form again with your unique ResponseID ({Identifier}):<br><br>
           {ChangeURL}<br><br>


		   Thank you, <br>
		   BIOMAPS <br><br>
		   This message was sent by an automated system. <br>
		</p>
	  </body>
	</html>
   """.format(First = InstructorFirst, Last = InstructorLast, Survey = Survey, Course = CourseName.replace("_", " "), Code = Code, Close = CloseDate, Identifier = ID, ChangeURL = ChangeURL)


    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    server = smtplib.SMTP(host = 'smtp.office365.com', port = 587)
    server.starttls()
    server.login(UserEmail, EmailPassword)
    server.sendmail(BIOMAPSEmail, InstructorEmail, msg.as_string())
    #server.sendmail(BIOMAPSEmail, BIOMAPSEmail, msg.as_string())
    server.quit()

def SendStatusEmail():
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "BIOMAPS Automation Status"
    msg['From'] = BIOMAPSEmail
    msg['To'] = BIOMAPSEmail

    StatusTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

    # Create the body of the message (a plain-text and an HTML version).
    text = """
		   Hey there,\n\n

           Everything's running nicely as of {CurrentTime}. \n\n

		   This message was sent by an automated system. \n
		   """.format(CurrentTime = StatusTime)

    html = """\
    <html>
	  <head></head>
	  <body>
        <p>Hey there,<br><br>

            Everything's running nicely as of {CurrentTime}.\n\n

		   This message was sent by an automated system.
        </p>
	  </body>
    </html>
    """.format(CurrentTime = StatusTime)

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # The actual mail send
    server = smtplib.SMTP(host = 'smtp.office365.com', port = 587)
    server.starttls()
    server.login(UserEmail, EmailPassword)
    server.sendmail(BIOMAPSEmail, BIOMAPSEmail, msg.as_string())
    server.quit()

def GetResponseData(SchoolName, CourseNumber, InstructorName, Year, Survey, SurveyID):

    # Move to the specific course directory to download responses
    path = MainDirectory + "/" + Survey + '/' + str(Year) + "Files/" + SchoolName + '_' + str(CourseNumber) + '_' + InstructorName

    os.chdir(path)
    DownloadResponses(SurveyID)
    Survey_Name = GetSurveyName(SurveyID)
    StudentDF = pd.read_csv(Survey_Name + '.csv', skiprows = [1, 2])

    NumStudents = len(StudentDF.index)

    return NumStudents

def ValidateResponses(df, Survey):
    def ProcessNames(df, ID = True):
        df['BackName'] = (df['Last Names'].apply(str).str.lower() + df['First Names'].apply(str).str.lower()).str.replace('\W', '') # Get full name in lower case with no white space
        df = df[df['BackName'].map(len) > 2] # Keep only full names with more than 2 characters
        df = df.drop_duplicates(subset = ['BackName'])
        df['BackName'] = df['BackName'].fillna('')
        df = df.sort_values(by = 'BackName')
        if(ID):
            df['IDs'] = df['IDs'].astype(str).str.split('@').str.get(0).str.lower() # Keep only first part of email addresses and take the lower case of all ids
            df = df.drop_duplicates(subset = ['IDs']) # Drop second entry if there are duplicate full names
            NamesDF = df.loc[:, ['IDs', 'Last Names', 'First Names']]
        else:
            NamesDF = df.loc[:, ['Last Names', 'First Names']]

        return df, NamesDF

    if(Survey == 'EcoEvo-MAPS'):
        df = df.loc[df['Finished'] == 1, :]
        df = df.rename(columns = {'PartInfo_3_TEXT':'IDs', 'PartInfo_2_TEXT':'Last Names', 'PartInfo_1_TEXT':'First Names'})
        df, Names = ProcessNames(df)

        df = df.loc[(df['Q55'] == 5) & (df['Q56'] == 5), :]
    if(Survey == 'Capstone'):
        df = df.loc[df['Finished'] == 1, :]
        df = df.rename(columns = {'ID_3_TEXT':'IDs', 'ID_2_TEXT':'Last Names', 'ID_1_TEXT':'First Names'})
        df, Names = ProcessNames(df)

        df = df.loc[(df['Q68'] == 5) & (df['Q69'] == 5), :]
    if(Survey == 'Phys-MAPS'):
        df = df.loc[df['Finished'] == 1, :]
        df = df.rename(columns = {'Q11_2_TEXT':'Last Names', 'Q11_1_TEXT':'First Names'})
        df, Names = ProcessNames(df, ID = False)

        df = df.loc[(df['Q46'] == 5) & (df['Q47'] == 5), :]
    if(Survey == 'GenBio-MAPS'):
        df = df.loc[df['Finished'] == 1, :] # &
        df = df.rename(columns = {'ID2_1_TEXT':'IDs', 'ID1_2_TEXT':'Last Names', 'ID1_1_TEXT':'First Names'})
        df, Names = ProcessNames(df)

        df = df.loc[(df['Q298'] == 5) & (df['Q299'] == 5), :]
    return df, Names

def GetSurveyName(SurveyID):
    baseUrl = "https://{0}.qualtrics.com/API/v3/surveys/{1}".format(DataCenter, SurveyID)
    headers = {
        "x-api-token": apiToken,
        }

    Req = Request(baseUrl, headers=headers)
    Response = urlopen(Req)
    SurveyName = json.load(Response)['result']['name']
    return SurveyName

def DownloadResponses(SurveyID):
    # Setting static parameters
    FileFormat = "csv"

    requestCheckProgress = 0
    headers = {
        "content-type": "application/json",
        "x-api-token": apiToken,
        }

    # Step 1: Creating Data Export
    downloadRequestUrl = baseURL
    downloadRequestPayload = '{"format":"' + FileFormat + '","surveyId":"' + SurveyID + '"}'
    downloadRequestResponse = requests.request("POST", downloadRequestUrl, data=downloadRequestPayload, headers=headers)
    progressId = downloadRequestResponse.json()["result"]["id"]

    # Step 2: Checking on Data Export Progress and waiting until export is ready
    while requestCheckProgress < 100:
      requestCheckUrl = baseURL + progressId
      requestCheckResponse = requests.request("GET", requestCheckUrl, headers=headers)
      requestCheckProgress = requestCheckResponse.json()["result"]["percentComplete"]

    # Step 3: Downloading file
    requestDownloadUrl = baseURL + progressId + '/file'
    requestDownload = requests.request("GET", requestDownloadUrl, headers=headers, stream=True)

    # Step 4: Unziping file
    with open("RequestFile.zip", "wb") as f:
        for chunk in requestDownload.iter_content(chunk_size=1024):
          f.write(chunk)
    try:
        zipfile.ZipFile("RequestFile.zip").extractall()
        os.remove("RequestFile.zip")
    except zipfile.BadZipfile:
        print("Bad Zip File, trying again...")
        os.remove("RequestFile.zip")
        DownloadResponses(SurveyID)

def ShareSurvey(UserID, SurveyID):
    headers = {
        'x-api-token': apiToken,
        'content-type': 'application/json',
        }

    data = {
        "userId" : UserID,
        "permissions" : {
            "surveyDefinitionManipulation" : {
                "copySurveyQuestions" : True,
                "editSurveyFlow" : True,
                "useBlocks" : True,
                "useSkipLogic" : True,
                "useConjoint" : True,
                "useTriggers" : True,
                "useQuotas" : True,
                "setSurveyOptions" : True,
                "editQuestions" : True,
                "deleteSurveyQuestions" : True
                },
            "surveyManagement" : {
                "editSurveys" : True,
                "activateSurveys" : True,
                "deactivateSurveys" : True,
                "copySurveys" : True,
                "distributeSurveys" : True,
                "deleteSurveys" : True,
                "translateSurveys" : True
                },
            "response" : {
                "editSurveyResponses" : True,
                "createResponseSets" : True,
                "viewResponseId" : True,
                "useCrossTabs" : True
                },
            "result" : {
                "downloadSurveyResults" : True,
                "viewSurveyResults" : True,
                "filterSurveyResults" : True,
                "viewPersonalData" : True
                }
            }
        }

    requests.post('https://{0}.qualtrics.com/API/v3/surveys/{1}/permissions/collaborations'.format(DataCenter, SurveyID), headers=headers, data=json.dumps(data))

if __name__ == '__main__':
	main()
