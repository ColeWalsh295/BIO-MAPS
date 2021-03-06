library(dplyr)
library(data.table)

# the four primary functions included here read headers and full datasets for each of the
# Bio-MAPS assessments. Information in the header is binded with class data when data is
# downloaded, allowing instructors to better understand the data they download. We
# process column names to align with the dashboard labels.

Clean.GenBio <- function(df.file = 'GenBio-MAPS_MasterFile.csv', 
                         header.file = 'GenBioMAPS_Headers.csv'){
  
  header.df <- fread(header.file, header = TRUE)
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
  # need number of students in each class for summary statistics
  df <- data.table(df)[, N.Students := .N, by = .(Class_ID)]
  df <- Convert.ClassLevel(df)
  
  if(df.file != 'GenBio-MAPS_MasterFile.csv'){
    return(rbind(header.df, df))
  }
  
  return(list('dataFrame' = df, 'header' = header.df))
}

Clean.EcoEvo <- function(df.file = 'EcoEvo-MAPS_MasterFile.csv', 
                         header.file = 'EcoEvoMAPS_Headers.csv'){
  
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
  df <- Convert.ClassLevel(df)
  
  return(list('dataFrame' = df, 'header' = header.df))
}

Clean.Phys <- function(df.file = 'Phys-MAPS_MasterFile.csv',
                       header.file = 'PhysMAPS_Headers.csv'){
  
  header.df <- fread(header.file, header = TRUE)
  
  header.supplemental <- data.frame(SC_Total_Score = 'Total Phys-MAPS score',
                                    SC_VC_Evolution = 'Vision & Change Evolution subscore',
                                    SC_VC_Information_Flow = 'Vision & Change Information Flow 
                                    subscore',
                                    SC_VC_Structure_Function = 'Vision & Change Structure/Function 
                                    subscore',
                                    SC_VC_Transformations_of_Energy_and_Matter = 'Vision & Change 
                                    Transformations of energy and matter subscore',
                                    SC_VC_Systems = 'Vision & Change Systems subscore',
                                    SC_Phys_Homeostasis = 'Physiology homeostasis subscore',
                                    SC_Phys_CellCell_Communication = 'Physiology cell-cell 
                                    communication subscore',
                                    SC_Phys_Flowdown_Gradients = 'Physiology flow-down gradients 
                                    subscore',
                                    SC_Phys_Cell_Membrane = 'Physiology cell membrane subscore',
                                    SC_Phys_Interdependence = 'Physiology interdependence subscore',
                                    SC_Phys_Structure_Function = 'Physiology structure/function 
                                    subscore',
                                    SC_Phys_Evolution = 'Physiology evolution subscore')
  
  header.df <- cbind(header.df, header.supplemental)
  header.df <- Add.IDcols(header.df)
  
  names(header.df) = gsub(x = names(header.df), pattern = "1_", replacement = "B_")
  names(header.df) = gsub(x = names(header.df), pattern = "2_", replacement = "C_")
  names(header.df) = gsub(x = names(header.df), pattern = "3_", replacement = "E_")
  names(header.df) = gsub(x = names(header.df), pattern = "8_", replacement = "F_")
  names(header.df) = gsub(x = names(header.df), pattern = "4_", replacement = "G_")
  names(header.df) = gsub(x = names(header.df), pattern = "5_", replacement = "H_")
  names(header.df) = gsub(x = names(header.df), pattern = "21_", replacement = "J_")
  names(header.df) = gsub(x = names(header.df), pattern = "7_", replacement = "K_")
  names(header.df) = gsub(x = names(header.df), pattern = "38_", replacement = "V_")
  names(header.df) = gsub(x = names(header.df), pattern = "22_", replacement = "W_")
  names(header.df) = gsub(x = names(header.df), pattern = "40_", replacement = "Z_")
  
  # Get Complete dataset
  df <- fread(df.file)
  names(df) = gsub(x = names(df), pattern = "S$", replacement = "")
  
  df <- data.table(df)[, N.Students := .N, by = .(Class_ID)]
  df <- Convert.ClassLevel(df)
  
  return(list('dataFrame' = df, 'header' = header.df))
}

Clean.Cap <- function(df.file = 'Capstone_MasterFile.csv',
                       header.file = 'Capstone_Headers.csv'){
  
  header.df <- fread(header.file, header = TRUE)
  names(header.df) = gsub(x = names(header.df), pattern = "#1", replacement = "")
  
  header.supplemental <- data.frame(SC_Total_Score = 'Total Capstone score',
                                    SC_VC_Evolution = 'Vision & Change Evolution subscore',
                                    SC_VC_Information_Flow = 'Vision & Change Information Flow 
                                    subscore',
                                    SC_VC_Structure_Function = 'Vision & Change Structure/Function 
                                    subscore',
                                    SC_VC_Transformations_of_Energy_and_Matter = 'Vision & Change 
                                    Transformations of energy and matter subscore')
  
  header.df <- subset(cbind(header.df, header.supplemental), select = -ID)
  header.df <- Add.IDcols(header.df)
  
  # Get Complete dataset
  df <- fread(df.file)
  names(df) = gsub(x = names(df), pattern = "S$", replacement = "")
  
  df <- data.table(df)[, N.Students := .N, by = .(Class_ID)]
  df <- Convert.ClassLevel(df)
  
  return(list('dataFrame' = df, 'header' = header.df))
}

Add.IDcols <- function(df){
  # change names for student ID coloumns to be more descriptive
  ID.dataFrame <- data.frame(ID = 'Student ID',
                             First_Name = 'Student first name',
                             Last_Name = 'Student last name')
  
  
  new.df <- cbind(df, ID.dataFrame)
  
  return(new.df)
}

Convert.ClassLevel <- function(df){
  # collapse class level and class standing variables
  df <- df %>%
    mutate(Class_Level = case_when(
      Class_Level == 1 ~ 'Begin_Intro',
      Class_Level == 2 ~ 'End_Intro',
      Class_Level == 3 ~ 'Advanced'
    ),
    ClassStanding = factor(ClassStanding, levels = c('Freshman', 'Sophomore/Junior', 'Senior', 'Grad')))
  
  return(df)
}