import os
os.chdir('C:/Users/Cole/Documents/GitHub/BIO-MAPS/Automation-Files')
from PythonAutomation_BIOMAPS import GetResponseData, GetSurveyName, DownloadResponses, ValidateResponses
import ReportGraph_BIOMAPS
import pandas as pd
import numpy as np
from glob import glob
import datetime

def GetAllData(df, test, mainDirectory, startDate = None, endDate = None):
    """Download and validate all surveys within a given date range.

    Keyword arguments:
    df -- pandas dataframe of master Bio-MAPS data file with instructor responses
    test -- either Capstone, EcoEvo, GenBio, Phys
    mainDirectory -- directory to download Bio-MAPS data
    startDate -- beginning of date range of survey close dates to download (format = %m/%d/%Y)
    endDate -- end of date range of survey close dates to download (format = %m/%d/%Y)
    """

    df[test + ' Closed'] = pd.to_datetime(df[test + ' Closed'])
    if(startDate is not None):
        df = df.loc[df[test + ' Closed'] > datetime.datetime.strptime(startDate, '%m/%d/%Y')]
    if(endDate is not None):
        df = df.loc[df[test + ' Closed'] < datetime.datetime.strptime(endDate, '%m/%d/%Y')]

    df = df.reset_index(drop = True)
    for Index, Class in df.iterrows():
        TermDir = mainDirectory + "/" + test + "/" + str(Class['Course Year']) + "Files"
        if not os.path.exists(TermDir):
            os.mkdir(TermDir, 755)

        CourseDir = Class['School Name'] + '_' + str(Class[test + ' Number']) + '_' + Class['Last Name'] + '_' + Class['ID']
        CourseDir = TermDir + "//" + CourseDir
        if not os.path.exists(CourseDir):
            os.mkdir(CourseDir, 755)

        os.chdir(CourseDir)
        DownloadResponses(Class[test + ' ID'])

        SurveyName = GetSurveyName(Class[test + ' ID'])
        df = pd.read_csv(SurveyName + '.csv', skiprows = [1, 2])
        if(test == 'Capstone'):
            df, Namesdf = ValidateResponses(df, 'Capstone')
        else:
            try:
                df, Namesdf = ValidateResponses(df, test + '-MAPS')
            except:
                print(SurveyName)
        try: # there's some issue writing particular files, that I think has to do with length
            df.to_csv(SurveyName + '_' + Class['ID'] + '.csv', index = False)
            Class.T.to_frame().T.to_csv(SurveyName + '_' + Class['ID'] + '_CourseInfo.csv', index = False)
        except:
            print(SurveyName)
        os.remove(SurveyName + '.csv')

    return 0

def LabelDemographics(df, test):
    """Convert demographic columns to readable labels.

    Keyword arguments:
    df -- pandas dataframe of student responses
    test -- either Capstone, EcoEvo, GenBio, Phys
    """

    def LabelGen(row, test):
        if(test == 'Capstone'):
            if((row['Gender'] == 1) | (row['Gender_1'] == 1)):
                return 'Male'
            elif((row['Gender'] == 2) | (row['Gender_2'] == 1)):
                return 'Female'
            else:
                return ''
        elif(test == 'EcoEvo'):
            if((row['D.12'] == 1) | (row['D.12_1'] == 1)):
                return 'Female'
            elif((row['D.12'] == 2) | (row['D.12_2'] == 1)):
                return 'Male'
            else:
                return ''
        elif(test == 'GenBio'):
            if((row['Gen'] == 1) | (row['Gen_1'] == 1)):
                return 'Female'
            elif((row['Gen'] == 2) | (row['Gen_2'] == 1)):
                return 'Male'
            else:
                return ''
        else:
            if((row['Q30'] == 1) | (row['Q30_1'] == 1)):
                return 'Female'
            elif((row['Q30'] == 2) | (row['Q30_2'] == 1)):
                return 'Male'
            else:
                return ''

    def SetURM(df, test):
        # white and asian/asian american students are coded as 'Majority', all others are coded as 'URM'
        if(test == 'Capstone'):
            conditions = [
                df['Race_1'] == 1,
                df['Race_2'] == 1,
                df['Race_3'] == 1,
                df['Race_4'] == 1,
                df['Race_5'] == 1,
                df['Race_6'] == 1,
                df['Race_7'] == 1
            ]

            output = ['URM', 'Majority', 'URM', 'URM', 'URM', 'Majority', 'URM']
        elif(test == 'EcoEvo'):
            conditions = [
                df['D.13_3'] == 1,
                df['D.13_4'] == 1,
                df['D.13_5'] == 1,
                df['D.13_6'] == 1,
                df['D.13_7'] == 1,
                df['D.13_8'] == 1,
                df['D.13_9'] == 1,
                df['D.13_1'] == 1,
                df['D.13_2'] == 1
            ]

            output = ['URM'] * 7 + ['Majority'] * 2
        elif(test == 'GenBio'):
            conditions = [
                df['Ethn_1'] == 1,
                df['Ethn_2'] == 1,
                df['Ethn_3'] == 1,
                df['Ethn_4'] == 1,
                df['Ethn_5'] == 1,
                df['Ethn_6'] == 1,
                df['Ethn_7'] == 1
            ]

            output = ['URM', 'Majority', 'Majority', 'URM', 'URM', 'URM', 'URM']
        else:
            conditions = [
                df['Q16_1'] == 1,
                df['Q16_4'] == 1,
                df['Q16_5'] == 1,
                df['Q16_6'] == 1,
                df['Q16_7'] == 1,
                df['Q16_8'] == 1,
                df['Q16_9'] == 1,
                df['Q16_2'] == 1,
                df['Q16_3'] == 1
            ]

            output = ['URM'] * 7 + ['Majority'] * 2

        df['Ethn'] = np.select(conditions, output, None)
        return df

    df['Gen'] = df.apply(lambda x: LabelGen(x, test = test), axis = 1)
    df = SetURM(df, test)

    if(test == 'Capstone'):
        df['Class'] = df['CY'].map({1:'Freshman', 2:'Sophomore/Junior', 3:'Sophomore/Junior', 4:'Senior', 5:'Grad'})
    elif(test == 'EcoEvo'):
        df['Class'] = df['D.2'].map({1:'Freshman', 2:'Sophomore/Junior', 3:'Sophomore/Junior', 4:'Senior', 6:'Grad'})
        df['Maj'] = df['D.9'].map({1:'Biology', 2:'Other'})
        df['Trans'] = df['D.3'].map({1:'Transfer student', 2:'Not a transfer student'})
        df['Eng'] = df['D.14'].map({1:'English', 2:'Other'})
        df['Educ'] = df['D.17'].map({1:'First Gen', 2:'First Gen', 3:'First Gen', 4:'Continuing Gen', 5:'Continuing Gen',
                                     6:'Continuing Gen', 7:'Continuing Gen'})
    elif(test == 'GenBio'):
        df['Class'] = df['Class'].map({1:'Freshman', 2:'Sophomore/Junior', 3:'Sophomore/Junior', 4:'Senior', 6:'Grad'})
        df['Trans'] = df['Trans'].map({1:'Transfer student', 2:'Not a transfer student'})
        df['Maj'] = df['Maj'].map({1:'Life Sciences', 2:'Other'})
        df['Eng'] = df['Eng'].map({1:'English', 2:'Other Language'})
        df['Educ'] = df['Educ'].map({1:'First Gen', 2:'First Gen', 3:'First Gen', 4:'Continuing Gen', 5:'Continuing Gen',
                                     6:'Continuing Gen', 7:'Continuing Gen'})
    else:
        df['Class'] = df['Q19'].map({1:'Freshamn', 2:'Sophomore/Junior', 3:'Sophomore/Junior', 4:'Senior', 6:'Grad'})
        df['Maj'] = (1 * ((df['Q27'] == 1) | (df['Q42'] == 1))).map({1:'Biology', 0:'Other'})
        df['Trans'] = df['Q21'].map({1:'Transfer student', 2:'Not a transfer student'})
        df['Eng'] = df['Q31'].map({1:'English', 2:'Other'})
        df['Educ'] = df['Q33'].map({1:'First Gen', 2:'First Gen', 3:'First Gen', 4:'Continuing Gen', 5:'Continuing Gen',
                                    6:'Continuing Gen', 7:'Continuing Gen'})

    return df

def WriteFile(df, test, directory, EndDate):
    """Write to master file. Only surveys that have closed prior to EndDate are included.

    Keyword arguments:
    df -- pandas dataframe of student responses
    test -- either Capstone, EcoEvo, GenBio, Phys
    directory -- file path to write file to
    EndDate -- only include surveys with close dates prior to end date in file (format = %m/%d/%Y)
    """

    df['EndDate'] = pd.to_datetime(df['EndDate'])
    df = df[df['EndDate'] < datetime.datetime.strptime(EndDate, '%m/%d/%Y')]

    if(test == 'Capstone'):
        df = df.loc[:, [c for c in df.columns if ('Q' in c and 'S' in c) or 'SC' in c] +
                            ['Class_ID', 'Class_Level', 'ID', 'First Names', 'Last Names', 'FullName', 'BackName', 'Class',
                             'Gen', 'Ethn']].rename(columns = {'First Names':'First_Name', 'Last Names':'Last_Name',
                                                               'Class':'ClassStanding', 'Gen':'SexGender', 'Ethn':'URMStatus',
                                                               'SC_Total Score':'SC_Total_Score',
                                                               'SC_VC_Information Flow':'SC_VC_Information_Flow',
                                                               'SC_VC_Structure/Function':'SC_VC_Structure_Function',
                                                               'SC_VC_Transformations of Energy and Matter':'SC_VC_Transformations_of_Energy_and_Matter'})
        df.to_csv(directory + '/Capstone_MasterFile.csv', index = False)
    elif(test == 'EcoEvo'):
        df = df[[c for c in df.columns if (('Q' in c and 'S' in c) or 'SC' in c) and '58' not in c] +
                ['Class_ID', 'Class_Level', 'ID', 'First Names', 'Last Names', 'FullName', 'BackName', 'Class', 'Maj', 'Gen',
                 'Ethn', 'Educ', 'Eng', 'Trans']].rename(columns = {'First Names':'First_Name', 'Last Names':'Last_Name',
                                                                    'Class':'ClassStanding', 'Trans':'TransferStatus',
                                                                    'Maj':'Major', 'Gen':'SexGender', 'Ethn':'URMStatus',
                                                                    'Eng':'ELL', 'Educ':'ParentEducation'})
        df.to_csv(directory + '/EcoEvo-MAPS_MasterFile.csv', index = False)
    elif(test == 'GenBio'):
        df = df.loc[:, [c for c in df.columns if ('BM' in c and 'S' in c) or 'SC' in c] +
                    ['Class_ID', 'Class_Level', 'ID', 'First Names', 'Last Names', 'FullName', 'BackName', 'Class', 'Trans',
                     'Maj', 'Gen', 'Ethn', 'Eng', 'Educ']].rename(columns = {'First Names':'First_Name',
                                                                             'Last Names':'Last_Name',
                                                                             'Class':'ClassStanding', 'Trans':'TransferStatus',
                                                                             'Maj':'Major', 'Gen':'SexGender',
                                                                             'Ethn':'URMStatus', 'Eng':'ELL',
                                                                             'Educ':'ParentEducation'})
        df.to_csv(directory + '/GenBio-MAPS_MasterFile.csv', index = False)
    else:
        df = df[[c for c in df.columns if ('Q' in c and 'S' in c) or 'SC' in c] +
                ['Class_ID', 'Class_Level', 'ID', 'First Names', 'Last Names', 'FullName', 'BackName', 'Class', 'Maj', 'Gen',
                 'Ethn', 'Educ', 'Eng', 'Trans']].rename(columns = {'First Names':'First_Name', 'Last Names':'Last_Name',
                                                                    'Class':'ClassStanding', 'Trans':'TransferStatus',
                                                                    'Maj':'Major', 'Gen':'SexGender', 'Ethn':'URMStatus',
                                                                    'Eng':'ELL', 'Educ':'ParentEducation'})
        df.to_csv(directory + '/Phys-MAPS_MasterFile.csv', index = False)


    return df

def BuildMasterFile(test, mainDirectory, EndDate, Admin_ID):
    """Construct master dataframe of student responses to Bio-MAPS assessments.

    Keyword arguments:
    test -- either Capstone, EcoEvo, GenBio, Phys
    mainDirectory -- directory to download Bio-MAPS data
    EndDate -- only include surveys with close dates prior to end date in file (format = %m/%d/%Y)
    """

    test_directory = mainDirectory + '/' + test + '/'
    os.chdir(test_directory)
    Files_Data = [f for f in glob('./*/**/*.csv', recursive = True) if 'CourseInfo' not in f]

    dfs = []
    for f in Files_Data:
        Course_Info = pd.read_csv(f[:-4] + '_CourseInfo.csv')
        df = pd.read_csv(f).assign(Class_ID = Course_Info.loc[0, 'ID'],
                                                      Class_Level = Course_Info.loc[0, test + ' Level'])

        dfs.append(df)
    df = pd.concat(dfs).reset_index(drop = True)
    if(test == 'Capstone'):
        df_out, Statements = ReportGraph_BIOMAPS.GenerateGraphs_Capstone(df)
    elif(test == 'EcoEvo'):
        df_out, Statements = ReportGraph_BIOMAPS.GenerateGraphs_EcoEvoMAPS(df)
    elif(test == 'GenBio'):
        df_out, Statements = ReportGraph_BIOMAPS.GenerateGraphs_GenBioMAPS(df)
    else:
        df_out, Statements = ReportGraph_BIOMAPS.GenerateGraphs_PhysMAPS(df)

    df_out['FullName'] = (df_out['First Names'].apply(str).str.lower() +
                          df_out['Last Names'].apply(str).str.lower()).str.replace('\W', '')
    df_out['BackName'] = (df_out['Last Names'].apply(str).str.lower() +
                          df_out['First Names'].apply(str).str.lower()).str.replace('\W', '')
    if(test != 'Phys'): # Phys-MAPS doesn't ask for IDs so we fill the ID column with fullname
        df_out['ID'] = df_out['IDs'].astype(str).str.split('@').str.get(0).str.lower()
    else:
        df_out['ID'] = df_out['FullName']

    df_out = pd.concat([df_out, pd.DataFrame({'Class_ID': [Admin_ID], 'EndDate': ['03/04/2020']})], join = 'outer').reset_index(drop = True)
    df_out = LabelDemographics(df_out, test)
    df_out = WriteFile(df_out, test, test_directory, EndDate)

    return df_out
