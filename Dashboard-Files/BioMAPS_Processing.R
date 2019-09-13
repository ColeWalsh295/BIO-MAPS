library(dplyr)
library(data.table)

Clean.GenBio <- function(df.file = 'C:/Users/Cole/Documents/GRA_Fall2019/BIO-MAPS/GenBio-MAPS/GenBio-MAPS_MasterFile.csv', 
                         header.file = 'C:/Users/Cole/Documents/GRA_Fall2019/BIO-MAPS/GenBio-MAPS/GenBioMAPS_Headers.csv'){
  
  header.df <- fread(header.file, header = TRUE) %>%
    select(-c('Class', 'Trans', 'Maj','Eng', 'Educ'))
  names(header.df) = gsub(x = names(header.df), pattern = "#1", replacement = "")
  
  header.supplemental <- data.frame(SC_Total_Score = 'Total GenBio-MAPS score',
                           SC_VC_Evolution = 'Vision & Change Evolution subscore',
                           SC_VC_Information_Flow = 'Vision & Change Information Flow subscore',
                           SC_VC_Structure_Function = 'Vision & Change Structure/Function subscore',
                           SC_VC_Transformations_of_Energy_and_Matter = 'Vision & Change 
                         Transformations of energy and matter subscore',
                           SC_VC_Systems = 'Vision & Change Systems subscore',
                           SC_T_Cellular_and_Molecular = 'Cellular and Molecular biology subscore',
                           SC_T_Physiology = 'Physiology subscore',
                           SC_T_Ecology_and_Evolution = 'Ecology and Evolution subscore')
  
  header.df <- cbind(header.df, header.supplemental)
  header.df <- Add.IDcols(header.df)
  
  # Get Complete dataset
  df <- fread(df.file)
  names(df) = gsub(x = names(df), pattern = "S$", replacement = "")
  
  df <- data.table(df)[, N.Students := .N, by = .(Class_ID)]
  df <- Rename.cols(df)
  
  return(list('dataFrame' = df, 'header' = header.df))
}

Clean.EcoEvo <- function(df.file = 'C:/Users/Cole/Documents/GRA_Fall2019/BIO-MAPS/EcoEvo-MAPS/EcoEvo-MAPS_MasterFile.csv', 
                         header.file = 'C:/Users/Cole/Documents/GRA_Fall2019/BIO-MAPS/EcoEvo-MAPS/EcoEvoMAPS_Headers.csv'){
  
  header.df <- fread(header.file, header = TRUE)
  
  header.supplemental <- data.frame(SC_Total_Score = 'Total EcoEvo-MAPS score',
                                    SC_T_Ecology = 'Ecology suscore',
                                    SC_T_Evolution = 'Evolution subscore',
                                    SC_VC_Evolution = 'Vision & Change Evolution subscore',
                                    SC_VC_Information_Flow = 'Vision & Change Information Flow 
                                    subscore',
                                    SC_VC_Structure_Function = 'Vision & Change Structure/Function 
                                    subscore',
                                    SC_VC_Transformations_of_Energy_and_Matter = 'Vision & Change 
                         Transformations of energy and matter subscore',
                                    SC_VC_Systems = 'Vision & Change Systems subscore',
                                    SC_T_Cellular_and_Molecular = 'Cellular and Molecular biology 
                                    subscore',
                                    SC_T_Physiology = 'Physiology subscore',
                                    SC_T_Ecology_and_Evolution = 'Ecology and Evolution subscore',
                                    SC_EE_Heritable_Variation = 'Ecology and Evolution Heritable 
                                    Variations subscore',
                                    SC_EE_Modes_of_Change = 'Ecology and Evolution Modes of Change 
                                    subscore',
                                    SC_EE_Phylogeny_and_Evolutionary_History = 'Ecology and 
                                    Evolution Phylogeny and Evolutionary History subscore',
                                    SC_EE_Biological_Diversity = 'Ecology and Evolution Biological 
                                    Diversity subscore',
                                    SC_EE_Populations = 'Ecology and Evolution Populations subscore',
                                    SC_EE_Energy_and_Matter	 = 'Ecology and Evolution Energy and 
                                    Matter subscore',
                                    SC_EE_Interactions_with_Ecosystems = 'Ecology and Evolution 
                                    Interactions within Ecosystems subscore',
                                    SC_EE_Human_Impact = 'Ecology and Evolution Human Impact 
                                    subscore',
                                    SC_FDEE_Populations = '4DEE Populations subscore',
                                    SC_FDEE_Communities = '4DEE Communities subscore',
                                    SC_FDEE_Ecosystems = '4DEE Ecosystems subscore',
                                    SC_FDEE_Biomes = '4DEE Biomes subscore',
                                    SC_FDEE_Biosphere = '4DEE Biosphere subscore',
                                    SC_FDEE_Quantitative_Reasoning = '4DEE Quantitative Reasoning 
                                    and Computational Thinking subscore',
                                    SC_FDEE_Designing_and_Critiquing = '4DEE Designing and 
                                    Critiquing Investigations subscore',
                                    SC_FDEE_Human_Change = '4DEE Human Accelerated Environmental 
                                    Change subscore',
                                    SC_FDEE_Human_Shape = '4DEE How Humans Shape and Manage 
                                    Resources/Ecosystems/the Environment subscore',
                                    SC_FDEE_Matter_and_Energy = '4DEE Transformations of Matter and 
                                    Energy subscore',
                                    SC_FDEE_Systems = '4DEE Systems subscore',
                                    SC_FDEE_Space_and_Time = '4DEE Space and Time subscore',
                                    SC_FDEE_Core_Ecology = '4DEE Dimension 1: Core Ecology Concepts 
                                    subscore',
                                    SC_FDEE_FDEE_Ecology_Practices = '4DEE Dimension 2: Ecology 
                                    Practices subscore',
                                    SC_FDEE_Human_Environment = '4DEE Dimension 3: Human-Environment 
                                    Interactions subscore',
                                    SC_FDEE_CrossCutting = '4DEE Dimension 4: Cross-Cutting 
                                    Themes subscore')
  
  header.df <- cbind(header.df, header.supplemental)
  header.df <- Add.IDcols(header.df)
  
  # Get Complete dataset
  df <- fread(df.file)
  names(df) = gsub(x = names(df), pattern = "S$", replacement = "")
  
  df <- data.table(df)[, N.Students := .N, by = .(Class_ID)]
  #df <- Rename.cols(df)
  
  return(list('dataFrame' = df, 'header' = header.df))
}

Add.IDcols <- function(df){
  ID.dataFrame <- data.frame(ID = 'Encoded student ID',
                             FullName = 'Encoded student full name',
                             BackName = 'Encoded student name with first and last name reversed',
                             Class = 'Class Standing',
                             Trans = 'Transfer Status',
                             Maj = 'Intended Major',
                             Gen = 'Sex/Gender',
                             Eng = 'English Language Learner Status',
                             Educ = 'First Generation Status',
                             Ethn = 'URM Status')
  
  new.df <- cbind(df, ID.dataFrame)
  
  return(new.df)
}

Rename.cols <- function(df){
  colnames(df)[colnames(df) == "Class"] <- "Class_Standing"
  colnames(df)[colnames(df) == "Trans"] <- "Transfer_Status"
  colnames(df)[colnames(df) == "Maj"] <- "Intended_Major"
  colnames(df)[colnames(df) == "Gen"] <- "Self-Declared_Sex/Gender"
  colnames(df)[colnames(df) == "Eng"] <- "English_Language_Learner_Status"
  colnames(df)[colnames(df) == "Educ"] <- "First_Generation_Status"
  colnames(df)[colnames(df) == "Class"] <- "URM_Status"
  
  df <- df %>%
    mutate(Class_Level = case_when(
      Class_Level == 1 ~ 'Begin_Intro',
      Class_Level == 2 ~ 'End_Intro',
      Class_Level == 3 ~ 'Advanced'
    ))
  
  return(df)
}