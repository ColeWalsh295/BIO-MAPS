import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
from matplotlib import gridspec
matplotlib.rcParams.update({'font.size': 20})
import matplotlib.pyplot as plt
plt.style.use('seaborn-white')
GradientYour = matplotlib.cm.get_cmap('PiYG')
GradientOther = matplotlib.cm.get_cmap('PiYG')
C = 50

def GenerateGraphs_EcoEvoMAPS(df):
    df_Correct = pd.DataFrame()

    df_Correct['Q1_1S'] = df['Q1_1'] == 2
    df_Correct['Q1_2S'] = df['Q1_2'] == 1
    df_Correct['Q1_3S'] = df['Q1_3'] == 2
    df_Correct['Q1_4S'] = df['Q1_5'] == 2
    df_Correct['Q1_5S'] = df['Q1_6'] == 2
    df_Correct['Q1_6S'] = df['Q1_10'] == 2
    df_Correct['Q1_7S'] = df['Q1_11'] == 2

    df_Correct['Q2_1S'] = df['Q2_1'] == 1
    df_Correct['Q2_2S'] = df['Q2_3'] == 2
    df_Correct['Q2_3S'] = df['Q2_5'] == 2
    df_Correct['Q2_4S'] = df['Q2_12'] == 2
    df_Correct['Q2_5S'] = df['Q2_11'] == 2
    df_Correct['Q2_6S'] = df['Q2_15'] == 2
    df_Correct['Q2_7S'] = df['Q2_13'] == 2
    df_Correct['Q2_8S'] = df['Q2_18'] == 1
    df_Correct['Q2_9S'] = df['Q2_10'] == 2

    df_Correct['Q3_1S'] = df['Q3_2'] == 1
    df_Correct['Q3_2S'] = df['Q3_4'] == 2
    df_Correct['Q3_3S'] = df['Q3_8'] == 2
    df_Correct['Q3_4S'] = df['Q3_13'] == 1
    df_Correct['Q3_5S'] = df['Q3_14'] == 2

    df_Correct['Q4_1S'] = df['Q4_1'] == 2
    df_Correct['Q4_2S'] = df['Q4_2'] == 1
    df_Correct['Q4_3S'] = df['Q4_5'] == 1
    df_Correct['Q4_4S'] = df['Q4_12'] == 1
    df_Correct['Q4_5S'] = df['Q4_6'] == 1
    df_Correct['Q4_6S'] = df['Q4_7'] == 1
    df_Correct['Q4_7S'] = df['Q4_11'] == 2

    df_Correct['Q5_1S'] = df['Q5_7'] == 2
    df_Correct['Q5_2S'] = df['Q5_10'] == 2
    df_Correct['Q5_3S'] = df['Q5_23'] == 1
    df_Correct['Q5_4S'] = df['Q5_24'] == 2
    df_Correct['Q5_5S'] = df['Q5_13'] == 2
    df_Correct['Q5_6S'] = df['Q5_15'] == 2
    df_Correct['Q5_7S'] = df['Q5_18'] == 2

    df_Correct['Q6_1S'] = df['Q6_1'] == 2
    df_Correct['Q6_2S'] = df['Q6_2'] == 2
    df_Correct['Q6_3S'] = df['Q6_3'] == 1
    df_Correct['Q6_4S'] = df['Q6_5'] == 2
    df_Correct['Q6_5S'] = df['Q6_6'] == 1
    df_Correct['Q6_6S'] = df['Q6_10'] == 2
    df_Correct['Q6_7S'] = df['Q6_9'] == 2

    df_Correct['Q7_1S'] = df['Q7_2'] == 1
    df_Correct['Q7_2S'] = df['Q7_3'] == 2
    df_Correct['Q7_3S'] = df['Q7_5'] == 2
    df_Correct['Q7_4S'] = df['Q7_17'] == 1
    df_Correct['Q7_5S'] = df['Q7_18'] == 1
    df_Correct['Q7_6S'] = df['Q7_19'] == 2
    df_Correct['Q7_7S'] = df['Q7_7'] == 1

    df_Correct['Q8_1S'] = df['Q8_1'] == 1
    df_Correct['Q8_2S'] = df['Q8_2'] == 2
    df_Correct['Q8_3S'] = df['Q8_3'] == 1
    df_Correct['Q8_4S'] = df['Q8_4'] == 1
    df_Correct['Q8_5S'] = df['Q8_6'] == 1
    df_Correct['Q8_6S'] = df['Q8_12'] == 1
    df_Correct['Q8_7S'] = df['Q8_16'] == 2

    df_Correct['Q9_1S'] = df['Q9_2'] == 1
    df_Correct['Q9_2S'] = df['Q9_12'] == 1
    df_Correct['Q9_3S'] = df['Q9_13'] == 1
    df_Correct['Q9_4S'] = df['Q9_14'] == 2
    df_Correct['Q9_5S'] = df['Q9_19'] == 2
    df_Correct['Q9_6S'] = df['Q9_17'] == 1
    df_Correct['Q9_7S'] = df['Q9_23'] == 2

    df_Correct = df_Correct.astype(int)
    StatementsList = []
    StatementsList.append(len(df_Correct.columns))

    df_Correct['SC_Total_Score'] = df_Correct.sum(axis = 1) / len(df_Correct.columns)

    EC_Questions = ['Q1_1S', 'Q1_2S', 'Q1_3S', 'Q1_4S', 'Q1_5S', 'Q1_6S', 'Q1_7S', 'Q2_9S', 'Q3_1S', 'Q3_2S', 'Q3_3S', 'Q3_4S', 'Q3_5S', 'Q5_5S', 'Q7_1S', 'Q7_2S', 'Q7_3S', 'Q7_7S', 'Q8_1S',
                    'Q8_2S', 'Q8_3S', 'Q8_5S', 'Q8_6S', 'Q8_7S', 'Q9_1S', 'Q9_2S', 'Q9_4S', 'Q9_5S', 'Q9_6S', 'Q9_7S']
    EV_Questions = ['Q2_1S', 'Q2_2S', 'Q2_3S', 'Q2_4S', 'Q2_5S', 'Q2_6S', 'Q2_7S', 'Q2_8S', 'Q4_1S', 'Q4_2S', 'Q4_3S', 'Q4_4S', 'Q4_5S', 'Q4_6S', 'Q4_7S', 'Q5_1S', 'Q5_2S', 'Q5_3S', 'Q5_4S',
                    'Q5_6S', 'Q5_7S', 'Q6_1S', 'Q6_2S', 'Q6_3S', 'Q6_4S', 'Q6_5S', 'Q6_6S', 'Q6_7S', 'Q7_4S', 'Q7_5S', 'Q7_6S', 'Q8_4S', 'Q9_3S']

    StatementsList.append(len(EC_Questions))
    StatementsList.append(len(EV_Questions))

    df_Correct['SC_T_Ecology'] = df_Correct[EC_Questions].sum(axis = 1) / len(EC_Questions)
    df_Correct['SC_T_Evolution'] = df_Correct[EV_Questions].sum(axis = 1) /len(EV_Questions)

    plt.figure(figsize = (12, 9))
    sns.boxplot(data = df_Correct[['SC_Total_Score', 'SC_T_Ecology', 'SC_T_Evolution']], color = 'w', showfliers = False)
    sns.stripplot(data = df_Correct[['SC_Total_Score', 'SC_T_Ecology', 'SC_T_Evolution']], jitter = 0.25, alpha = min(1, C * 30/(3 * len(df.index))), size = 10, edgecolor = None)
    plt.xticks((0, 1, 2), ('Total Score', 'Ecology', 'Evolution'))
    plt.yticks((0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1), ('0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'))
    plt.text(1, 1.05, 'Total Scores', ha = 'center', va = 'center')
    plt.subplots_adjust(left = 0.1)
    plt.savefig('EcoEvoMAPS_TotalScores.png')
    plt.close()
    plt.clf()

    VC_Evo_Questions = ['Q2_2S', 'Q2_3S', 'Q2_7S', 'Q2_8S', 'Q4_1S', 'Q4_2S', 'Q4_3S', 'Q4_4S', 'Q4_5S', 'Q4_6S', 'Q4_7S', 'Q5_2S', 'Q5_3S', 'Q5_7S', 'Q6_1S', 'Q6_2S', 'Q6_3S', 'Q6_4S', 'Q6_5S',
                        'Q6_6S', 'Q7_4S', 'Q7_5S', 'Q7_6S', 'Q8_4S']
    VC_IF_Questions = ['Q2_1S', 'Q2_4S', 'Q2_5S', 'Q2_6S', 'Q5_1S', 'Q5_4S', 'Q5_6S', 'Q6_7S']
    VC_SF_Questions = ['Q7_1S', 'Q7_7S', 'Q9_3S']
    VC_TEM_Questions = ['Q1_4S', 'Q1_5S', 'Q7_2S', 'Q7_3S', 'Q8_2S', 'Q8_5S', 'Q8_7S', 'Q9_4S', 'Q9_5S', 'Q9_6S', 'Q9_7S']
    VC_S_Questions = ['Q1_1S', 'Q1_2S', 'Q1_3S', 'Q1_6S', 'Q1_7S', 'Q2_9S', 'Q3_1S', 'Q3_2S', 'Q3_3S', 'Q3_4S', 'Q3_5S', 'Q5_5S', 'Q8_1S', 'Q8_3S', 'Q8_6S', 'Q9_1S', 'Q9_2S']

    StatementsList.append(len(VC_Evo_Questions))
    StatementsList.append(len(VC_IF_Questions))
    StatementsList.append(len(VC_SF_Questions))
    StatementsList.append(len(VC_TEM_Questions))
    StatementsList.append(len(VC_S_Questions))

    df_Correct['SC_VC_Evolution'] = df_Correct[VC_Evo_Questions].sum(axis = 1) / len(VC_Evo_Questions)
    df_Correct['SC_VC_Information_Flow'] = df_Correct[VC_IF_Questions].sum(axis = 1) / len(VC_IF_Questions)
    df_Correct['SC_VC_Structure_Function'] = df_Correct[VC_SF_Questions].sum(axis = 1) / len(VC_SF_Questions)
    df_Correct['SC_VC_Transformations_of_Energy_and_Matter'] = df_Correct[VC_TEM_Questions].sum(axis = 1) / len(VC_TEM_Questions)
    df_Correct['SC_VC_Systems'] = df_Correct[VC_S_Questions].sum(axis = 1) / len(VC_S_Questions)

    plt.figure(figsize = (12, 9))
    sns.boxplot(data = df_Correct[['SC_VC_Evolution', 'SC_VC_Information_Flow', 'SC_VC_Structure_Function', 'SC_VC_Transformations_of_Energy_and_Matter', 'SC_VC_Systems']], color = 'w', showfliers = False)
    sns.stripplot(data = df_Correct[['SC_VC_Evolution', 'SC_VC_Information_Flow', 'SC_VC_Structure_Function', 'SC_VC_Transformations_of_Energy_and_Matter', 'SC_VC_Systems']], jitter = 0.25, alpha = min(1, C * 3/(5 * len(df.index))), size = 10, edgecolor = None)
    plt.xticks((0, 1, 2, 3, 4), ('Evolution', 'Information Flow', 'Structure Function', u'Transformations of\nEnergy and Matter', 'Systems'), rotation = 40)
    plt.yticks((0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1), ('0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'))
    plt.text(2, 1.1, 'Vision and Change Core Concepts', ha = 'center', va = 'center')
    plt.subplots_adjust(left = 0.1, bottom = 0.22)
    plt.savefig('EcoEvoMAPS_VisionChange_Scores.png')
    plt.close()
    plt.clf()

    EE_HV_Questions = ['Q2_1S', 'Q2_4S', 'Q2_5S', 'Q2_6S', 'Q5_1S', 'Q5_4S', 'Q5_6S', 'Q6_7S']
    EE_MC_Questions = ['Q2_3S', 'Q2_7S', 'Q2_8S', 'Q5_2S', 'Q5_3S', 'Q5_7S', 'Q6_6S', 'Q7_4S', 'Q7_5S', 'Q7_6S', 'Q8_4S']
    EE_PEH_Questions = ['Q2_2S', 'Q4_1S', 'Q4_2S', 'Q4_3S', 'Q4_4S', 'Q4_5S', 'Q4_6S', 'Q4_7S', 'Q6_1S', 'Q6_2S', 'Q6_3S', 'Q6_4S', 'Q6_5S', 'Q9_3S']
    EE_BD_Questions = ['Q8_1S', 'Q8_3S', 'Q9_1S']
    EE_P_Questions = ['Q1_3S', 'Q1_6S', 'Q3_1S', 'Q3_2S', 'Q3_4S', 'Q3_5S', 'Q7_7S']
    EE_EM_Questions = ['Q1_4S', 'Q1_5S', 'Q7_2S', 'Q7_3S', 'Q8_2S', 'Q8_5S', 'Q8_7S', 'Q9_4S', 'Q9_5S', 'Q9_6S', 'Q9_7S']
    EE_IE_Questions = ['Q1_1S', 'Q1_2S', 'Q1_7S', 'Q3_3S', 'Q7_1S', 'Q9_2S']
    EE_HI_Questions = ['Q2_9S', 'Q5_5S', 'Q8_6S']

    StatementsList.append(len(EE_HV_Questions))
    StatementsList.append(len(EE_MC_Questions))
    StatementsList.append(len(EE_PEH_Questions))
    StatementsList.append(len(EE_BD_Questions))
    StatementsList.append(len(EE_P_Questions))
    StatementsList.append(len(EE_EM_Questions))
    StatementsList.append(len(EE_IE_Questions))
    StatementsList.append(len(EE_HI_Questions))

    df_Correct['SC_EE_Heritable_Variation'] = df_Correct[EE_HV_Questions].sum(axis = 1) / len(EE_HV_Questions)
    df_Correct['SC_EE_Modes_of_Change'] = df_Correct[EE_MC_Questions].sum(axis = 1) / len(EE_MC_Questions)
    df_Correct['SC_EE_Phylogeny_and_Evolutionary_History'] = df_Correct[EE_PEH_Questions].sum(axis = 1) / len(EE_PEH_Questions)
    df_Correct['SC_EE_Biological_Diversity'] = df_Correct[EE_BD_Questions].sum(axis = 1) / len(EE_BD_Questions)
    df_Correct['SC_EE_Populations'] = df_Correct[EE_P_Questions].sum(axis = 1) / len(EE_P_Questions)
    df_Correct['SC_EE_Energy_and_Matter'] = df_Correct[EE_EM_Questions].sum(axis = 1) / len(EE_EM_Questions)
    df_Correct['SC_EE_Interactions_with_Ecosystems'] = df_Correct[EE_IE_Questions].sum(axis = 1) / len(EE_IE_Questions)
    df_Correct['SC_EE_Human_Impact'] = df_Correct[EE_HI_Questions].sum(axis = 1) / len(EE_HI_Questions)

    matplotlib.rcParams.update({'font.size': 16})
    plt.figure(figsize = (12, 9))
    sns.boxplot(data = df_Correct[['SC_EE_Heritable_Variation', 'SC_EE_Modes_of_Change', 'SC_EE_Phylogeny_and_Evolutionary_History', 'SC_EE_Biological_Diversity', 'SC_EE_Populations', 'SC_EE_Energy_and_Matter',
                                    'SC_EE_Interactions_with_Ecosystems', 'SC_EE_Human_Impact']], color = 'w', showfliers = False)
    sns.stripplot(data = df_Correct[['SC_EE_Heritable_Variation', 'SC_EE_Modes_of_Change', 'SC_EE_Phylogeny_and_Evolutionary_History', 'SC_EE_Biological_Diversity', 'SC_EE_Populations', 'SC_EE_Energy_and_Matter',
                                    'SC_EE_Interactions_with_Ecosystems', 'SC_EE_Human_Impact']], jitter = 0.25, alpha = min(1, C * 3/(8 * len(df.index))), size = 10, edgecolor = None)
    plt.xticks((0, 1, 2, 3, 4, 5, 6, 7), ('Heritable Variation', 'Modes of Change', u'Phylogeny and\nEvolutionary History', 'Biological Diversity', 'Populations', 'Energy and Matter', u'Interactions\nwith Ecosystems', 'Human Impact'), rotation = 60)
    plt.yticks((0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1), ('0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'))
    plt.text(3.5, 1.1, 'Ecology and Evolution Conceptual Themes', ha = 'center', va = 'center')
    plt.subplots_adjust(left = 0.1, bottom = 0.25)
    plt.savefig('EcoEvoMAPS_EcologyEvolution_Scores.png')
    plt.close()
    plt.clf()

    FDEE_Pop_Questions = ['Q1_6S', 'Q2_9S', 'Q3_2S', 'Q3_3S', 'Q3_5S', 'Q5_5S', 'Q7_7S']
    FDEE_Com_Questions = ['Q1_2S', 'Q1_3S', 'Q3_1S', 'Q3_4S', 'Q7_1S', 'Q9_1S', 'Q9_2S']
    FDEE_Eco_Questions = ['Q1_1S', 'Q1_4S', 'Q1_5S', 'Q1_7S', 'Q7_2S', 'Q7_3S', 'Q8_7S', 'Q9_4S', 'Q9_6S', 'Q9_7S']
    FDEE_Biomes_Questions = ['Q8_1S', 'Q8_2S', 'Q8_5S']
    FDEE_Biosphere_Questions = ['Q8_3S', 'Q8_6S', 'Q9_5S']
    FDEE_Quant_Questions = ['Q1_4S', 'Q1_6S', 'Q3_2S', 'Q3_5S', 'Q5_5S']
    FDEE_Design_Questions = ['Q1_1S', 'Q1_2S', 'Q1_3S', 'Q1_5S', 'Q1_7S', 'Q3_1S', 'Q8_1S', 'Q8_2S', 'Q8_3S', 'Q8_5S', 'Q9_1S']
    FDEE_HumanAcc_Questions = ['Q1_5S', 'Q8_6S']
    FDEE_HumanShape_Questions = ['Q1_1S', 'Q1_2S', 'Q1_3S', 'Q1_4S', 'Q1_6S', 'Q1_7S', 'Q2_9S', 'Q5_5S', 'Q8_7S']
    FDEE_TME_Questions = ['Q1_4S', 'Q1_5S', 'Q7_2S', 'Q7_3S', 'Q8_2S', 'Q8_5S', 'Q8_7S', 'Q9_4S', 'Q9_5S', 'Q9_6S', 'Q9_7S']
    FDEE_Systems_Questions = ['Q1_1S', 'Q1_2S', 'Q1_3S', 'Q1_6S', 'Q1_7S', 'Q2_9S', 'Q3_1S', 'Q3_2S', 'Q3_3S', 'Q3_5S', 'Q5_5S', 'Q7_1S', 'Q7_7S', 'Q8_1S', 'Q8_6S', 'Q9_1S', 'Q9_2S']
    FDEE_SpaceTime_Questions = ['Q2_1S', 'Q2_2S', 'Q2_3S', 'Q2_4S', 'Q2_5S', 'Q2_6S', 'Q2_7S', 'Q2_8S', 'Q3_4S', 'Q4_1S', 'Q4_2S', 'Q4_3S', 'Q4_4S', 'Q4_5S', 'Q4_6S', 'Q4_7S', 'Q5_1S', 'Q5_2S', 'Q5_3S', 'Q5_4S', 'Q5_6S', 'Q5_7S', 'Q6_1S',
    'Q6_2S', 'Q6_3S', 'Q6_4S', 'Q6_5S', 'Q6_6S', 'Q6_7S', 'Q7_4S', 'Q7_5S', 'Q7_6S', 'Q8_3S', 'Q8_4S', 'Q9_3S']

    FDEE_CoreEcology = FDEE_Pop_Questions + FDEE_Com_Questions + FDEE_Eco_Questions + FDEE_Biomes_Questions + FDEE_Biosphere_Questions
    FDEE_EcologyPractices = FDEE_Quant_Questions + FDEE_Design_Questions
    FDEE_HumanEnvironment = FDEE_HumanAcc_Questions + FDEE_HumanShape_Questions
    FDEE_CrossCutting = FDEE_TME_Questions + FDEE_Systems_Questions + FDEE_SpaceTime_Questions

    StatementsList.append(len(FDEE_CoreEcology))
    StatementsList.append(len(FDEE_EcologyPractices))
    StatementsList.append(len(FDEE_HumanEnvironment))
    StatementsList.append(len(FDEE_CrossCutting))

    df_Correct['SC_FDEE_Populations'] = df_Correct[FDEE_Pop_Questions].sum(axis = 1) / len(FDEE_Pop_Questions)
    df_Correct['SC_FDEE_Communities'] = df_Correct[FDEE_Com_Questions].sum(axis = 1) / len(FDEE_Com_Questions)
    df_Correct['SC_FDEE_Ecosystems'] = df_Correct[FDEE_Eco_Questions].sum(axis = 1) / len(FDEE_Eco_Questions)
    df_Correct['SC_FDEE_Biomes'] = df_Correct[FDEE_Biomes_Questions].sum(axis = 1) / len(FDEE_Biomes_Questions)
    df_Correct['SC_FDEE_Biosphere'] = df_Correct[FDEE_Biosphere_Questions].sum(axis = 1) / len(FDEE_Biosphere_Questions)
    df_Correct['SC_FDEE_Quantitative_Reasoning'] = df_Correct[FDEE_Quant_Questions].sum(axis = 1) / len(FDEE_Quant_Questions)
    df_Correct['SC_FDEE_Designing_and_Critiquing'] = df_Correct[FDEE_Design_Questions].sum(axis = 1) / len(FDEE_Design_Questions)
    df_Correct['SC_FDEE_Human_Change'] = df_Correct[FDEE_HumanAcc_Questions].sum(axis = 1) / len(FDEE_HumanAcc_Questions)
    df_Correct['SC_FDEE_Human_Shape'] = df_Correct[FDEE_HumanShape_Questions].sum(axis = 1) / len(FDEE_HumanShape_Questions)
    df_Correct['SC_FDEE_Matter_and_Energy'] = df_Correct[FDEE_TME_Questions].sum(axis = 1) / len(FDEE_TME_Questions)
    df_Correct['SC_FDEE_Systems'] = df_Correct[FDEE_Systems_Questions].sum(axis = 1) / len(FDEE_Systems_Questions)
    df_Correct['SC_FDEE_Space_and_Time'] = df_Correct[FDEE_SpaceTime_Questions].sum(axis = 1) / len(FDEE_SpaceTime_Questions)

    df_Correct['SC_FDEE_Core_Ecology'] = df_Correct[FDEE_CoreEcology].sum(axis = 1) / len(FDEE_CoreEcology)
    df_Correct['SC_FDEE_FDEE_Ecology_Practices'] = df_Correct[FDEE_EcologyPractices].sum(axis = 1) / len(FDEE_EcologyPractices)
    df_Correct['SC_FDEE_Human_Environment'] = df_Correct[FDEE_HumanEnvironment].sum(axis = 1) / len(FDEE_HumanEnvironment)
    df_Correct['SC_FDEE_CrossCutting'] = df_Correct[FDEE_CrossCutting].sum(axis = 1) / len(FDEE_CrossCutting)

    matplotlib.rcParams.update({'font.size': 16})
    fig, axes = plt.subplots(2, 2, figsize = (12, 9))

    plt.sca(axes[0, 0])
    sns.boxplot(data = df_Correct[['SC_FDEE_Populations', 'SC_FDEE_Communities', 'SC_FDEE_Ecosystems', 'SC_FDEE_Biomes', 'SC_FDEE_Biosphere']], color = 'w', showfliers = False)
    sns.stripplot(data = df_Correct[['SC_FDEE_Populations', 'SC_FDEE_Communities', 'SC_FDEE_Ecosystems', 'SC_FDEE_Biomes', 'SC_FDEE_Biosphere']], jitter = 0.25, alpha = min(1, C * 3/(8 * len(df.index))), size = 10, edgecolor = None, color = sns.color_palette()[0])
    plt.xticks((0, 1, 2, 3, 4), ('Populations', 'Communities', 'Ecosystems', 'Biomes', 'Biosphere'), rotation = 40)
    plt.ylabel('Percent Correct')
    plt.yticks((0, 0.2, 0.4, 0.6, 0.8, 1), ('0', '20', '40', '60', '80', '100'))
    plt.text(2, 1.15, 'Dimension 1: Core Ecology Concepts', ha = 'center', va = 'center')

    plt.sca(axes[0, 1])
    sns.boxplot(data = df_Correct[['SC_FDEE_Quantitative_Reasoning', 'SC_FDEE_Designing_and_Critiquing']], color = 'w', showfliers = False)
    sns.stripplot(data = df_Correct[['SC_FDEE_Quantitative_Reasoning', 'SC_FDEE_Designing_and_Critiquing']], jitter = 0.25, alpha = min(1, C * 3/(8 * len(df.index))), size = 10, edgecolor = None, color = sns.color_palette()[1])
    plt.xticks((0, 1), (u'Quant. Reasoning\n& Comp. Thinking', u'Designing & Critiquing\nInvestigations'), rotation = 20)
    plt.ylabel('Percent Correct')
    plt.yticks((0, 0.2, 0.4, 0.6, 0.8, 1), ('0', '20', '40', '60', '80', '100'))
    plt.text(0.5, 1.15, 'Dimension 2: Ecology Practices', ha = 'center', va = 'center')

    plt.sca(axes[1, 0])
    sns.boxplot(data = df_Correct[['SC_FDEE_Human_Change', 'SC_FDEE_Human_Shape']], color = 'w', showfliers = False)
    sns.stripplot(data = df_Correct[['SC_FDEE_Human_Change', 'SC_FDEE_Human_Shape']], jitter = 0.25, alpha = min(1, C * 3/(8 * len(df.index))), size = 10, edgecolor = None, color = sns.color_palette()[2])
    plt.xticks((0, 1), (u'Human Accelerated\nEnvironmental Change', u'Humans shape resources\n/ecosystems/environment'), rotation = 20)
    plt.ylabel('Percent Correct')
    plt.yticks((0, 0.2, 0.4, 0.6, 0.8, 1), ('0', '20', '40', '60', '80', '100'))
    plt.text(0.5, 1.15, 'Dimension 3: Human-Environment Interactions', ha = 'center', va = 'center')

    plt.sca(axes[1, 1])
    sns.boxplot(data = df_Correct[['SC_FDEE_Matter_and_Energy', 'SC_FDEE_Systems', 'SC_FDEE_Space_and_Time']], color = 'w', showfliers = False)
    sns.stripplot(data = df_Correct[['SC_FDEE_Matter_and_Energy', 'SC_FDEE_Systems', 'SC_FDEE_Space_and_Time']], jitter = 0.25, alpha = min(1, C * 3/(8 * len(df.index))), size = 10, edgecolor = None, color = sns.color_palette()[3])
    plt.xticks((0, 1, 2), (u'Transformations of\nmatter & energy', 'Systems', 'Space & time'), rotation = 30)
    plt.ylabel('Percent Correct')
    plt.yticks((0, 0.2, 0.4, 0.6, 0.8, 1), ('0', '20', '40', '60', '80', '100'))
    plt.text(1, 1.15, 'Dimension 4:Cross-Cutting Themes', ha = 'center', va = 'center')

    plt.subplots_adjust(hspace = 0.6, bottom = 0.2)
    fig.savefig('EcoEvoMAPS_4DEE_Scores.png')
    plt.close()
    plt.clf()

    df = pd.concat([df, df_Correct], axis = 1)

    return df, StatementsList

def GenerateGraphs_GenBioMAPS(df):
    df_Correct = pd.DataFrame()

    df_Correct['BM-01_1S'] = (df['BM-01#1_1'] == 2) * (pd.notnull(df['T-BM-01_1']).replace(False, np.nan))
    df_Correct['BM-01_2S'] = (df['BM-01#1_2'] == 1) * (pd.notnull(df['T-BM-01_1']).replace(False, np.nan))
    df_Correct['BM-01_3S'] = (df['BM-01#1_3'] == 2) * (pd.notnull(df['T-BM-01_1']).replace(False, np.nan))
    df_Correct['BM-01_4S'] = (df['BM-01#1_4'] == 1) * (pd.notnull(df['T-BM-01_1']).replace(False, np.nan))
    df_Correct['BM-01_5S'] = (df['BM-01#1_5'] == 1) * (pd.notnull(df['T-BM-01_1']).replace(False, np.nan))

    df_Correct['BM-02_1S'] = (df['BM-02#1_1'] == 1) * (pd.notnull(df['T-BM-02_1']).replace(False, np.nan))
    df_Correct['BM-02_2S'] = (df['BM-02#1_2'] == 1) * (pd.notnull(df['T-BM-02_1']).replace(False, np.nan))
    df_Correct['BM-02_3S'] = (df['BM-02#1_3'] == 2) * (pd.notnull(df['T-BM-02_1']).replace(False, np.nan))
    df_Correct['BM-02_4S'] = (df['BM-02#1_4'] == 1) * (pd.notnull(df['T-BM-02_1']).replace(False, np.nan))

    df_Correct['BM-03_1S'] = (df['BM-03#1_1'] == 1) * (pd.notnull(df['T-BM-03_1']).replace(False, np.nan))
    df_Correct['BM-03_2S'] = (df['BM-03#1_2'] == 1) * (pd.notnull(df['T-BM-03_1']).replace(False, np.nan))
    df_Correct['BM-03_3S'] = (df['BM-03#1_3'] == 1) * (pd.notnull(df['T-BM-03_1']).replace(False, np.nan))
    df_Correct['BM-03_4S'] = (df['BM-03#1_4'] == 1) * (pd.notnull(df['T-BM-03_1']).replace(False, np.nan))
    df_Correct['BM-03_5S'] = (df['BM-03#1_5'] == 2) * (pd.notnull(df['T-BM-03_1']).replace(False, np.nan))

    df_Correct['BM-04_1S'] = (df['BM-04#1_1'] == 2) * (pd.notnull(df['T-BM-04_1']).replace(False, np.nan))
    df_Correct['BM-04_2S'] = (df['BM-04#1_2'] == 2) * (pd.notnull(df['T-BM-04_1']).replace(False, np.nan))
    df_Correct['BM-04_3S'] = (df['BM-04#1_3'] == 1) * (pd.notnull(df['T-BM-04_1']).replace(False, np.nan))
    df_Correct['BM-04_4S'] = (df['BM-04#1_4'] == 1) * (pd.notnull(df['T-BM-04_1']).replace(False, np.nan))

    df_Correct['BM-07_1S'] = (df['BM-07#1_1'] == 1) * (pd.notnull(df['T-BM-07_1']).replace(False, np.nan))
    df_Correct['BM-07_2S'] = (df['BM-07#1_2'] == 2) * (pd.notnull(df['T-BM-07_1']).replace(False, np.nan))
    df_Correct['BM-07_3S'] = (df['BM-07#1_3'] == 1) * (pd.notnull(df['T-BM-07_1']).replace(False, np.nan))
    df_Correct['BM-07_4S'] = (df['BM-07#1_4'] == 1) * (pd.notnull(df['T-BM-07_1']).replace(False, np.nan))
    df_Correct['BM-07_5S'] = (df['BM-07#1_5'] == 1) * (pd.notnull(df['T-BM-07_1']).replace(False, np.nan))

    df_Correct['BM-08_1S'] = (df['BM-08#1_1'] == 1) * (pd.notnull(df['T-BM-08_1']).replace(False, np.nan))
    df_Correct['BM-08_2S'] = (df['BM-08#1_2'] == 2) * (pd.notnull(df['T-BM-08_1']).replace(False, np.nan))
    df_Correct['BM-08_3S'] = (df['BM-08#1_3'] == 1) * (pd.notnull(df['T-BM-08_1']).replace(False, np.nan))
    df_Correct['BM-08_4S'] = (df['BM-08#1_4'] == 1) * (pd.notnull(df['T-BM-08_1']).replace(False, np.nan))

    df_Correct['BM-12_1S'] = (df['BM-12#1_1'] == 1) * (pd.notnull(df['T-BM-12_1']).replace(False, np.nan))
    df_Correct['BM-12_2S'] = (df['BM-12#1_2'] == 2) * (pd.notnull(df['T-BM-12_1']).replace(False, np.nan))
    df_Correct['BM-12_3S'] = (df['BM-12#1_3'] == 1) * (pd.notnull(df['T-BM-12_1']).replace(False, np.nan))
    df_Correct['BM-12_4S'] = (df['BM-12#1_4'] == 1) * (pd.notnull(df['T-BM-12_1']).replace(False, np.nan))
    df_Correct['BM-12_5S'] = (df['BM-12#1_5'] == 1) * (pd.notnull(df['T-BM-12_1']).replace(False, np.nan))

    df_Correct['BM-13_1S'] = (df['BM-13#1_1'] == 1) * (pd.notnull(df['T-BM-13_1']).replace(False, np.nan))
    df_Correct['BM-13_2S'] = (df['BM-13#1_2'] == 2) * (pd.notnull(df['T-BM-13_1']).replace(False, np.nan))
    df_Correct['BM-13_3S'] = (df['BM-13#1_3'] == 1) * (pd.notnull(df['T-BM-13_1']).replace(False, np.nan))
    df_Correct['BM-13_4S'] = (df['BM-13#1_4'] == 2) * (pd.notnull(df['T-BM-13_1']).replace(False, np.nan))

    df_Correct['BM-14_1S'] = (df['BM-14#1_1'] == 2) * (pd.notnull(df['T-BM-14_1']).replace(False, np.nan))
    df_Correct['BM-14_2S'] = (df['BM-14#1_2'] == 2) * (pd.notnull(df['T-BM-14_1']).replace(False, np.nan))
    df_Correct['BM-14_3S'] = (df['BM-14#1_3'] == 1) * (pd.notnull(df['T-BM-14_1']).replace(False, np.nan))
    df_Correct['BM-14_4S'] = (df['BM-14#1_4'] == 1) * (pd.notnull(df['T-BM-14_1']).replace(False, np.nan))

    df_Correct['BM-15_1S'] = (df['BM-15#1_1'] == 1) * (pd.notnull(df['T-BM-15_1']).replace(False, np.nan))
    df_Correct['BM-15_2S'] = (df['BM-15#1_2'] == 2) * (pd.notnull(df['T-BM-15_1']).replace(False, np.nan))
    df_Correct['BM-15_3S'] = (df['BM-15#1_3'] == 1) * (pd.notnull(df['T-BM-15_1']).replace(False, np.nan))
    df_Correct['BM-15_4S'] = (df['BM-15#1_4'] == 2) * (pd.notnull(df['T-BM-15_1']).replace(False, np.nan))

    df_Correct['BM-16_1S'] = (df['BM-16#1_1'] == 1) * (pd.notnull(df['T-BM-16_1']).replace(False, np.nan))
    df_Correct['BM-16_2S'] = (df['BM-16#1_2'] == 1) * (pd.notnull(df['T-BM-16_1']).replace(False, np.nan))
    df_Correct['BM-16_3S'] = (df['BM-16#1_3'] == 2) * (pd.notnull(df['T-BM-16_1']).replace(False, np.nan))
    df_Correct['BM-16_4S'] = (df['BM-16#1_4'] == 1) * (pd.notnull(df['T-BM-16_1']).replace(False, np.nan))

    df_Correct['BM-18_1S'] = (df['BM-18#1_1'] == 1) * (pd.notnull(df['T-BM-18_1']).replace(False, np.nan))
    df_Correct['BM-18_2S'] = (df['BM-18#1_2'] == 2) * (pd.notnull(df['T-BM-18_1']).replace(False, np.nan))
    df_Correct['BM-18_3S'] = (df['BM-18#1_3'] == 2) * (pd.notnull(df['T-BM-18_1']).replace(False, np.nan))
    df_Correct['BM-18_4S'] = (df['BM-18#1_4'] == 2) * (pd.notnull(df['T-BM-18_1']).replace(False, np.nan))

    df_Correct['BM-19_1S'] = (df['BM-19#1_1'] == 2) * (pd.notnull(df['T-BM-19_1']).replace(False, np.nan))
    df_Correct['BM-19_2S'] = (df['BM-19#1_2'] == 2) * (pd.notnull(df['T-BM-19_1']).replace(False, np.nan))
    df_Correct['BM-19_3S'] = (df['BM-19#1_3'] == 1) * (pd.notnull(df['T-BM-19_1']).replace(False, np.nan))
    df_Correct['BM-19_4S'] = (df['BM-19#1_4'] == 1) * (pd.notnull(df['T-BM-19_1']).replace(False, np.nan))

    df_Correct['BM-20_1S'] = (df['BM-20#1_1'] == 1) * (pd.notnull(df['T-BM-20_1']).replace(False, np.nan))
    df_Correct['BM-20_2S'] = (df['BM-20#1_2'] == 2) * (pd.notnull(df['T-BM-20_1']).replace(False, np.nan))
    df_Correct['BM-20_3S'] = (df['BM-20#1_3'] == 2) * (pd.notnull(df['T-BM-20_1']).replace(False, np.nan))
    df_Correct['BM-20_4S'] = (df['BM-20#1_4'] == 2) * (pd.notnull(df['T-BM-20_1']).replace(False, np.nan))
    df_Correct['BM-20_5S'] = (df['BM-20#1_5'] == 1) * (pd.notnull(df['T-BM-20_1']).replace(False, np.nan))

    df_Correct['BM-21_1S'] = (df['BM-21#1_1'] == 2) * (pd.notnull(df['T-BM-21_1']).replace(False, np.nan))
    df_Correct['BM-21_2S'] = (df['BM-21#1_2'] == 2) * (pd.notnull(df['T-BM-21_1']).replace(False, np.nan))
    df_Correct['BM-21_3S'] = (df['BM-21#1_3'] == 1) * (pd.notnull(df['T-BM-21_1']).replace(False, np.nan))
    df_Correct['BM-21_4S'] = (df['BM-21#1_4'] == 2) * (pd.notnull(df['T-BM-21_1']).replace(False, np.nan))

    df_Correct['BM-22_1S'] = (df['BM-22#1_1'] == 1) * (pd.notnull(df['T-BM-22_1']).replace(False, np.nan))
    df_Correct['BM-22_2S'] = (df['BM-22#1_2'] == 2) * (pd.notnull(df['T-BM-22_1']).replace(False, np.nan))
    df_Correct['BM-22_3S'] = (df['BM-22#1_3'] == 1) * (pd.notnull(df['T-BM-22_1']).replace(False, np.nan))
    df_Correct['BM-22_4S'] = (df['BM-22#1_4'] == 2) * (pd.notnull(df['T-BM-22_1']).replace(False, np.nan))

    df_Correct['BM-23_1S'] = (df['BM-23#1_1'] == 1) * (pd.notnull(df['T-BM-23_1']).replace(False, np.nan))
    df_Correct['BM-23_2S'] = (df['BM-23#1_2'] == 2) * (pd.notnull(df['T-BM-23_1']).replace(False, np.nan))
    df_Correct['BM-23_3S'] = (df['BM-23#1_3'] == 1) * (pd.notnull(df['T-BM-23_1']).replace(False, np.nan))
    df_Correct['BM-23_4S'] = (df['BM-23#1_4'] == 2) * (pd.notnull(df['T-BM-23_1']).replace(False, np.nan))

    df_Correct['BM-24_1S'] = (df['BM-24#1_1'] == 2) * (pd.notnull(df['T-BM-24_1']).replace(False, np.nan))
    df_Correct['BM-24_2S'] = (df['BM-24#1_2'] == 2) * (pd.notnull(df['T-BM-24_1']).replace(False, np.nan))
    df_Correct['BM-24_3S'] = (df['BM-24#1_3'] == 1) * (pd.notnull(df['T-BM-24_1']).replace(False, np.nan))
    df_Correct['BM-24_4S'] = (df['BM-24#1_4'] == 2) * (pd.notnull(df['T-BM-24_1']).replace(False, np.nan))
    df_Correct['BM-24_5S'] = (df['BM-24#1_5'] == 2) * (pd.notnull(df['T-BM-24_1']).replace(False, np.nan))

    df_Correct['BM-27_1S'] = (df['BM-27#1_1'] == 2) * (pd.notnull(df['T-BM-27_1']).replace(False, np.nan))
    df_Correct['BM-27_2S'] = (df['BM-27#1_2'] == 1) * (pd.notnull(df['T-BM-27_1']).replace(False, np.nan))
    df_Correct['BM-27_3S'] = (df['BM-27#1_3'] == 1) * (pd.notnull(df['T-BM-27_1']).replace(False, np.nan))
    df_Correct['BM-27_4S'] = (df['BM-27#1_4'] == 2) * (pd.notnull(df['T-BM-27_1']).replace(False, np.nan))
    df_Correct['BM-27_5S'] = (df['BM-27#1_5'] == 2) * (pd.notnull(df['T-BM-27_1']).replace(False, np.nan))

    df_Correct['BM-28_1S'] = (df['BM-28#1_1'] == 2) * (pd.notnull(df['T-BM-28_1']).replace(False, np.nan))
    df_Correct['BM-28_2S'] = (df['BM-28#1_2'] == 1) * (pd.notnull(df['T-BM-28_1']).replace(False, np.nan))
    df_Correct['BM-28_3S'] = (df['BM-28#1_3'] == 1) * (pd.notnull(df['T-BM-28_1']).replace(False, np.nan))
    df_Correct['BM-28_4S'] = (df['BM-28#1_4'] == 2) * (pd.notnull(df['T-BM-28_1']).replace(False, np.nan))
    df_Correct['BM-28_5S'] = (df['BM-28#1_5'] == 1) * (pd.notnull(df['T-BM-28_1']).replace(False, np.nan))

    df_Correct['BM-30_1S'] = (df['BM-30#1_1'] == 1) * (pd.notnull(df['T-BM-30_1']).replace(False, np.nan))
    df_Correct['BM-30_2S'] = (df['BM-30#1_2'] == 2) * (pd.notnull(df['T-BM-30_1']).replace(False, np.nan))
    df_Correct['BM-30_3S'] = (df['BM-30#1_3'] == 2) * (pd.notnull(df['T-BM-30_1']).replace(False, np.nan))
    df_Correct['BM-30_4S'] = (df['BM-30#1_4'] == 1) * (pd.notnull(df['T-BM-30_1']).replace(False, np.nan))

    df_Correct['BM-31_1S'] = (df['BM-31#1_1'] == 1) * (pd.notnull(df['T-BM-31_1']).replace(False, np.nan))
    df_Correct['BM-31_2S'] = (df['BM-31#1_2'] == 1) * (pd.notnull(df['T-BM-31_1']).replace(False, np.nan))
    df_Correct['BM-31_3S'] = (df['BM-31#1_3'] == 1) * (pd.notnull(df['T-BM-31_1']).replace(False, np.nan))
    df_Correct['BM-31_4S'] = (df['BM-31#1_4'] == 2) * (pd.notnull(df['T-BM-31_1']).replace(False, np.nan))

    df_Correct['BM-32_1S'] = (df['BM-32#1_1'] == 2) * (pd.notnull(df['T-BM-32_1']).replace(False, np.nan))
    df_Correct['BM-32_2S'] = (df['BM-32#1_2'] == 2) * (pd.notnull(df['T-BM-32_1']).replace(False, np.nan))
    df_Correct['BM-32_3S'] = (df['BM-32#1_3'] == 1) * (pd.notnull(df['T-BM-32_1']).replace(False, np.nan))
    df_Correct['BM-32_4S'] = (df['BM-32#1_4'] == 2) * (pd.notnull(df['T-BM-32_1']).replace(False, np.nan))
    df_Correct['BM-32_5S'] = (df['BM-32#1_5'] == 2) * (pd.notnull(df['T-BM-32_1']).replace(False, np.nan))

    df_Correct['BM-33_1S'] = (df['BM-33#1_1'] == 1) * (pd.notnull(df['T-BM-33_1']).replace(False, np.nan))
    df_Correct['BM-33_2S'] = (df['BM-33#1_2'] == 1) * (pd.notnull(df['T-BM-33_1']).replace(False, np.nan))
    df_Correct['BM-33_3S'] = (df['BM-33#1_3'] == 2) * (pd.notnull(df['T-BM-33_1']).replace(False, np.nan))
    df_Correct['BM-33_4S'] = (df['BM-33#1_4'] == 1) * (pd.notnull(df['T-BM-33_1']).replace(False, np.nan))
    df_Correct['BM-33_5S'] = (df['BM-33#1_5'] == 1) * (pd.notnull(df['T-BM-33_1']).replace(False, np.nan))

    df_Correct['BM-35_1S'] = (df['BM-35#1_1'] == 2) * (pd.notnull(df['T-BM-35_1']).replace(False, np.nan))
    df_Correct['BM-35_2S'] = (df['BM-35#1_2'] == 1) * (pd.notnull(df['T-BM-35_1']).replace(False, np.nan))
    df_Correct['BM-35_3S'] = (df['BM-35#1_3'] == 1) * (pd.notnull(df['T-BM-35_1']).replace(False, np.nan))
    df_Correct['BM-35_4S'] = (df['BM-35#1_4'] == 1) * (pd.notnull(df['T-BM-35_1']).replace(False, np.nan))

    df_Correct['BM-36_1S'] = (df['BM-36#1_1'] == 1) * (pd.notnull(df['T-BM-36_1']).replace(False, np.nan))
    df_Correct['BM-36_2S'] = (df['BM-36#1_2'] == 2) * (pd.notnull(df['T-BM-36_1']).replace(False, np.nan))
    df_Correct['BM-36_3S'] = (df['BM-36#1_3'] == 2) * (pd.notnull(df['T-BM-36_1']).replace(False, np.nan))
    df_Correct['BM-36_4S'] = (df['BM-36#1_4'] == 2) * (pd.notnull(df['T-BM-36_1']).replace(False, np.nan))
    df_Correct['BM-36_5S'] = (df['BM-36#1_5'] == 2) * (pd.notnull(df['T-BM-36_1']).replace(False, np.nan))

    df_Correct['BM-37_1S'] = (df['BM-37#1_1'] == 1) * (pd.notnull(df['T-BM-37_1']).replace(False, np.nan))
    df_Correct['BM-37_2S'] = (df['BM-37#1_2'] == 2) * (pd.notnull(df['T-BM-37_1']).replace(False, np.nan))
    df_Correct['BM-37_3S'] = (df['BM-37#1_3'] == 1) * (pd.notnull(df['T-BM-37_1']).replace(False, np.nan))
    df_Correct['BM-37_4S'] = (df['BM-37#1_4'] == 2) * (pd.notnull(df['T-BM-37_1']).replace(False, np.nan))
    df_Correct['BM-37_5S'] = (df['BM-37#1_5'] == 2) * (pd.notnull(df['T-BM-37_1']).replace(False, np.nan))

    df_Correct['BM-38_1S'] = (df['BM-38#1_1'] == 2) * (pd.notnull(df['T-BM-38_1']).replace(False, np.nan))
    df_Correct['BM-38_2S'] = (df['BM-38#1_2'] == 1) * (pd.notnull(df['T-BM-38_1']).replace(False, np.nan))
    df_Correct['BM-38_3S'] = (df['BM-38#1_3'] == 1) * (pd.notnull(df['T-BM-38_1']).replace(False, np.nan))
    df_Correct['BM-38_4S'] = (df['BM-38#1_4'] == 1) * (pd.notnull(df['T-BM-38_1']).replace(False, np.nan))
    df_Correct['BM-38_5S'] = (df['BM-38#1_5'] == 2) * (pd.notnull(df['T-BM-38_1']).replace(False, np.nan))

    df_Correct['BM-40_1S'] = (df['BM-40#1_1'] == 2) * (pd.notnull(df['T-BM-40_1']).replace(False, np.nan))
    df_Correct['BM-40_2S'] = (df['BM-40#1_2'] == 1) * (pd.notnull(df['T-BM-40_1']).replace(False, np.nan))
    df_Correct['BM-40_3S'] = (df['BM-40#1_3'] == 1) * (pd.notnull(df['T-BM-40_1']).replace(False, np.nan))
    df_Correct['BM-40_4S'] = (df['BM-40#1_4'] == 2) * (pd.notnull(df['T-BM-40_1']).replace(False, np.nan))

    df_Correct['BM-43_1S'] = (df['BM-43#1_1'] == 2) * (pd.notnull(df['T-BM-43_1']).replace(False, np.nan))
    df_Correct['BM-43_2S'] = (df['BM-43#1_2'] == 1) * (pd.notnull(df['T-BM-43_1']).replace(False, np.nan))
    df_Correct['BM-43_3S'] = (df['BM-43#1_3'] == 2) * (pd.notnull(df['T-BM-43_1']).replace(False, np.nan))
    df_Correct['BM-43_4S'] = (df['BM-43#1_4'] == 2) * (pd.notnull(df['T-BM-43_1']).replace(False, np.nan))
    df_Correct['BM-43_5S'] = (df['BM-43#1_5'] == 1) * (pd.notnull(df['T-BM-43_1']).replace(False, np.nan))

    df_Correct['BM-44_1S'] = (df['BM-44#1_1'] == 1) * (pd.notnull(df['T-BM-44_1']).replace(False, np.nan))
    df_Correct['BM-44_2S'] = (df['BM-44#1_2'] == 2) * (pd.notnull(df['T-BM-44_1']).replace(False, np.nan))
    df_Correct['BM-44_3S'] = (df['BM-44#1_3'] == 2) * (pd.notnull(df['T-BM-44_1']).replace(False, np.nan))
    df_Correct['BM-44_4S'] = (df['BM-44#1_4'] == 1) * (pd.notnull(df['T-BM-44_1']).replace(False, np.nan))
    df_Correct['BM-44_5S'] = (df['BM-44#1_5'] == 2) * (pd.notnull(df['T-BM-44_1']).replace(False, np.nan))

    df_Correct['BM-45_1S'] = (df['BM-45#1_1'] == 2) * (pd.notnull(df['T-BM-45_1']).replace(False, np.nan))
    df_Correct['BM-45_2S'] = (df['BM-45#1_2'] == 1) * (pd.notnull(df['T-BM-45_1']).replace(False, np.nan))
    df_Correct['BM-45_3S'] = (df['BM-45#1_3'] == 1) * (pd.notnull(df['T-BM-45_1']).replace(False, np.nan))
    df_Correct['BM-45_4S'] = (df['BM-45#1_4'] == 1) * (pd.notnull(df['T-BM-45_1']).replace(False, np.nan))
    df_Correct['BM-45_5S'] = (df['BM-45#1_5'] == 2) * (pd.notnull(df['T-BM-45_1']).replace(False, np.nan))

    df_Correct['BM-49_1S'] = (df['BM-49#1_1'] == 2) * (pd.notnull(df['T-BM-49_1']).replace(False, np.nan))
    df_Correct['BM-49_2S'] = (df['BM-49#1_2'] == 1) * (pd.notnull(df['T-BM-49_1']).replace(False, np.nan))
    df_Correct['BM-49_3S'] = (df['BM-49#1_3'] == 2) * (pd.notnull(df['T-BM-49_1']).replace(False, np.nan))
    df_Correct['BM-49_4S'] = (df['BM-49#1_4'] == 2) * (pd.notnull(df['T-BM-49_1']).replace(False, np.nan))

    df_Correct['BM-50_1S'] = (df['BM-50#1_1'] == 1) * (pd.notnull(df['T-BM-50_1']).replace(False, np.nan))
    df_Correct['BM-50_2S'] = (df['BM-50#1_2'] == 2) * (pd.notnull(df['T-BM-50_1']).replace(False, np.nan))
    df_Correct['BM-50_3S'] = (df['BM-50#1_3'] == 1) * (pd.notnull(df['T-BM-50_1']).replace(False, np.nan))
    df_Correct['BM-50_4S'] = (df['BM-50#1_4'] == 1) * (pd.notnull(df['T-BM-50_1']).replace(False, np.nan))
    df_Correct['BM-50_5S'] = (df['BM-50#1_5'] == 2) * (pd.notnull(df['T-BM-50_1']).replace(False, np.nan))

    df_Correct['BM-54_1S'] = (df['BM-54#1_1'] == 2) * (pd.notnull(df['T-BM-54_1']).replace(False, np.nan))
    df_Correct['BM-54_2S'] = (df['BM-54#1_2'] == 1) * (pd.notnull(df['T-BM-54_1']).replace(False, np.nan))
    df_Correct['BM-54_3S'] = (df['BM-54#1_3'] == 2) * (pd.notnull(df['T-BM-54_1']).replace(False, np.nan))
    df_Correct['BM-54_4S'] = (df['BM-54#1_4'] == 1) * (pd.notnull(df['T-BM-54_1']).replace(False, np.nan))

    df_Correct['BM-55_1S'] = (df['BM-55#1_1'] == 1) * (pd.notnull(df['T-BM-55_1']).replace(False, np.nan))
    df_Correct['BM-55_2S'] = (df['BM-55#1_2'] == 1) * (pd.notnull(df['T-BM-55_1']).replace(False, np.nan))
    df_Correct['BM-55_3S'] = (df['BM-55#1_3'] == 2) * (pd.notnull(df['T-BM-55_1']).replace(False, np.nan))
    df_Correct['BM-55_4S'] = (df['BM-55#1_4'] == 1) * (pd.notnull(df['T-BM-55_1']).replace(False, np.nan))
    df_Correct['BM-55_5S'] = (df['BM-55#1_5'] == 1) * (pd.notnull(df['T-BM-55_1']).replace(False, np.nan))

    df_Correct['BM-59_1S'] = (df['BM-59#1_1'] == 2) * (pd.notnull(df['T-BM-59_1']).replace(False, np.nan))
    df_Correct['BM-59_2S'] = (df['BM-59#1_2'] == 1) * (pd.notnull(df['T-BM-59_1']).replace(False, np.nan))
    df_Correct['BM-59_3S'] = (df['BM-59#1_3'] == 2) * (pd.notnull(df['T-BM-59_1']).replace(False, np.nan))
    df_Correct['BM-59_4S'] = (df['BM-59#1_4'] == 1) * (pd.notnull(df['T-BM-59_1']).replace(False, np.nan))

    df_Correct['BM-60_1S'] = (df['BM-60#1_1'] == 2) * (pd.notnull(df['T-BM-60_1']).replace(False, np.nan))
    df_Correct['BM-60_2S'] = (df['BM-60#1_2'] == 1) * (pd.notnull(df['T-BM-60_1']).replace(False, np.nan))
    df_Correct['BM-60_3S'] = (df['BM-60#1_3'] == 1) * (pd.notnull(df['T-BM-60_1']).replace(False, np.nan))
    df_Correct['BM-60_4S'] = (df['BM-60#1_4'] == 1) * (pd.notnull(df['T-BM-60_1']).replace(False, np.nan))
    df_Correct['BM-60_5S'] = (df['BM-60#1_5'] == 1) * (pd.notnull(df['T-BM-60_1']).replace(False, np.nan))

    df_Correct['BM-61_1S'] = (df['BM-61#1_1'] == 2) * (pd.notnull(df['T-BM-61_1']).replace(False, np.nan))
    df_Correct['BM-61_2S'] = (df['BM-61#1_2'] == 1) * (pd.notnull(df['T-BM-61_1']).replace(False, np.nan))
    df_Correct['BM-61_3S'] = (df['BM-61#1_3'] == 2) * (pd.notnull(df['T-BM-61_1']).replace(False, np.nan))
    df_Correct['BM-61_4S'] = (df['BM-61#1_4'] == 1) * (pd.notnull(df['T-BM-61_1']).replace(False, np.nan))

    StatementsList = []
    StatementsList.append(len(df_Correct.columns))

    df_Correct['SC_Total_Score'] = df_Correct.sum(axis = 1) / df_Correct.count(axis = 1)

    plt.figure(figsize = (12, 9))
    sns.boxplot(data = df_Correct['SC_Total_Score'], color = 'w', showfliers = False)
    sns.stripplot(data = df_Correct['SC_Total_Score'], jitter = 0.25, alpha = min(1, C * 67/len(df.index)), size = 10, edgecolor = None)
    plt.tick_params(bottom = False, labelbottom = False)
    plt.yticks((0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1), ('0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'))
    plt.text(0, 1.05, 'Total Scores', ha = 'center', va = 'center')
    plt.subplots_adjust(left = 0.1)
    plt.savefig('GenBioMAPS_TotalScores.png')
    plt.close()
    plt.clf()

    VC_Evo_Questions = ['BM-01_5S', 'BM-02_4S', 'BM-03_1S', 'BM-04_3S', 'BM-07_1S', 'BM-07_2S', 'BM-07_3S', 'BM-07_4S', 'BM-07_5S', 'BM-08_1S', 'BM-08_2S', 'BM-08_4S', 'BM-14_1S', 'BM-14_2S', 'BM-14_3S', 'BM-14_4S', 'BM-15_2S', 'BM-15_4S', 'BM-20_5S',
                        'BM-24_2S', 'BM-24_4S', 'BM-24_5S', 'BM-28_1S', 'BM-30_2S', 'BM-30_4S', 'BM-36_1S', 'BM-36_2S', 'BM-36_3S', 'BM-37_1S', 'BM-37_2S', 'BM-37_5S', 'BM-38_1S', 'BM-40_1S', 'BM-40_2S', 'BM-43_4S', 'BM-54_1S', 'BM-55_3S', 'BM-55_4S', 'BM-59_3S']
    VC_IF_Questions = ['BM-01_4S', 'BM-02_2S', 'BM-03_5S', 'BM-04_1S', 'BM-04_2S', 'BM-04_4S', 'BM-08_3S', 'BM-12_3S', 'BM-13_3S', 'BM-13_4S', 'BM-18_3S', 'BM-18_4S', 'BM-19_1S', 'BM-19_2S', 'BM-21_4S', 'BM-22_1S', 'BM-22_2S', 'BM-22_3S', 'BM-22_4S',
                        'BM-24_1S', 'BM-24_3S', 'BM-27_5S', 'BM-32_4S', 'BM-33_3S', 'BM-36_4S', 'BM-36_5S', 'BM-37_4S', 'BM-38_2S', 'BM-38_3S', 'BM-38_4S', 'BM-38_5S', 'BM-40_4S', 'BM-43_2S', 'BM-43_3S', 'BM-43_5S', 'BM-54_2S', 'BM-55_5S', 'BM-61_1S', 'BM-61_2S',
                        'BM-61_3S', 'BM-61_4S']
    VC_SF_Questions = ['BM-01_1S', 'BM-01_2S', 'BM-01_3S', 'BM-03_2S', 'BM-03_3S', 'BM-03_4S', 'BM-12_4S', 'BM-18_1S', 'BM-18_2S', 'BM-19_3S', 'BM-19_4S', 'BM-20_1S', 'BM-20_2S', 'BM-20_3S', 'BM-20_4S', 'BM-21_1S', 'BM-21_2S', 'BM-21_3S', 'BM-28_4S',
                        'BM-30_1S', 'BM-33_1S', 'BM-40_3S', 'BM-43_1S', 'BM-44_1S', 'BM-44_4S', 'BM-44_5S', 'BM-45_3S', 'BM-45_4S', 'BM-45_5S', 'BM-59_2S', 'BM-60_4S']
    VC_TEM_Questions = ['BM-02_1S', 'BM-02_3S', 'BM-12_5S', 'BM-16_3S', 'BM-16_4S', 'BM-23_1S', 'BM-23_2S', 'BM-23_3S', 'BM-23_4S', 'BM-27_1S', 'BM-27_2S', 'BM-27_3S', 'BM-27_4S', 'BM-28_2S', 'BM-28_5S', 'BM-31_1S', 'BM-31_2S', 'BM-31_3S', 'BM-31_4S',
                        'BM-33_4S', 'BM-35_3S', 'BM-37_3S', 'BM-44_2S', 'BM-44_3S', 'BM-45_1S', 'BM-45_2S', 'BM-49_1S', 'BM-49_2S', 'BM-49_3S', 'BM-49_4S', 'BM-50_1S', 'BM-50_2S', 'BM-50_5S', 'BM-54_3S', 'BM-54_4S', 'BM-55_1S', 'BM-60_3S']
    VC_S_Questions = ['BM-12_1S', 'BM-12_2S', 'BM-13_1S', 'BM-13_2S', 'BM-15_1S', 'BM-15_3S', 'BM-16_1S', 'BM-16_2S', 'BM-28_3S', 'BM-30_3S', 'BM-32_1S', 'BM-32_2S', 'BM-32_3S', 'BM-32_5S', 'BM-33_2S', 'BM-33_5S', 'BM-35_1S', 'BM-35_2S', 'BM-35_4S',
                        'BM-50_3S', 'BM-50_4S', 'BM-55_2S', 'BM-59_1S', 'BM-59_4S', 'BM-60_1S', 'BM-60_2S', 'BM-60_5S']

    StatementsList.append(len(VC_Evo_Questions))
    StatementsList.append(len(VC_IF_Questions))
    StatementsList.append(len(VC_SF_Questions))
    StatementsList.append(len(VC_TEM_Questions))
    StatementsList.append(len(VC_S_Questions))

    df_Correct['SC_VC_Evolution'] = df_Correct[VC_Evo_Questions].sum(axis = 1) / df_Correct[VC_Evo_Questions].count(axis = 1)
    df_Correct['SC_VC_Information_Flow'] = df_Correct[VC_IF_Questions].sum(axis = 1) / df_Correct[VC_IF_Questions].count(axis = 1)
    df_Correct['SC_VC_Structure_Function'] = df_Correct[VC_SF_Questions].sum(axis = 1) / df_Correct[VC_SF_Questions].count(axis = 1)
    df_Correct['SC_VC_Transformations_of_Energy_and_Matter'] = df_Correct[VC_TEM_Questions].sum(axis = 1) / df_Correct[VC_TEM_Questions].count(axis = 1)
    df_Correct['SC_VC_Systems'] = df_Correct[VC_S_Questions].sum(axis = 1) / df_Correct[VC_S_Questions].count(axis = 1)

    plt.figure(figsize = (12, 9))
    sns.boxplot(data = df_Correct[['SC_VC_Evolution', 'SC_VC_Information_Flow', 'SC_VC_Structure_Function', 'SC_VC_Transformations_of_Energy_and_Matter', 'SC_VC_Systems']], color = 'w', showfliers = False)
    sns.stripplot(data = df_Correct[['SC_VC_Evolution', 'SC_VC_Information_Flow', 'SC_VC_Structure_Function', 'SC_VC_Transformations_of_Energy_and_Matter', 'SC_VC_Systems']], jitter = 0.25, alpha = min(1, C * 10/(5 * len(df.index))), size = 10, edgecolor = None)
    plt.xticks((0, 1, 2, 3, 4), ('Evolution', 'Information Flow', 'Structure Function', u'Transformations of\nEnergy and Matter', 'Systems'), rotation = 40)
    #plt.yticks((0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1), ('0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'))
    plt.yticks((0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1), ('0', '10', '20', '30', '40', '50', '60', '70', '80', '90', '100'))
    plt.ylabel('Percent Correct')
    #plt.text(2, 1.1, 'Vision and Change Core Concepts', ha = 'center', va = 'center')
    plt.subplots_adjust(left = 0.1, bottom = 0.22)
    plt.savefig('GenBioMAPS_VisionChange_Scores.png')
    plt.close()
    plt.clf()

    CellMol_Questions = ['BM-01_1S', 'BM-01_2S', 'BM-01_3S', 'BM-01_4S', 'BM-01_5S', 'BM-02_1S', 'BM-02_3S', 'BM-03_1S', 'BM-03_2S', 'BM-03_3S', 'BM-03_4S', 'BM-03_5S', 'BM-04_1S', 'BM-04_2S', 'BM-04_3S', 'BM-04_4S', 'BM-07_1S', 'BM-07_4S', 'BM-07_5S',
                            'BM-12_1S', 'BM-12_2S', 'BM-12_3S', 'BM-12_4S', 'BM-12_5S', 'BM-13_1S', 'BM-13_2S', 'BM-13_3S', 'BM-18_1S', 'BM-18_2S', 'BM-18_3S', 'BM-18_4S', 'BM-19_1S', 'BM-19_2S', 'BM-19_3S', 'BM-19_4S', 'BM-20_1S', 'BM-20_2S', 'BM-20_3S', 'BM-20_4S',
                            'BM-21_1S', 'BM-21_2S', 'BM-21_3S', 'BM-21_4S', 'BM-22_3S', 'BM-22_4S', 'BM-24_1S', 'BM-24_2S', 'BM-24_3S', 'BM-24_4S', 'BM-24_5S', 'BM-27_1S', 'BM-27_2S', 'BM-27_3S', 'BM-27_4S', 'BM-28_1S', 'BM-28_4S', 'BM-31_4S', 'BM-33_1S', 'BM-33_3S',
                            'BM-33_4S', 'BM-36_1S', 'BM-36_2S', 'BM-36_4S', 'BM-36_5S', 'BM-37_1S', 'BM-37_3S', 'BM-37_4S', 'BM-37_5S', 'BM-38_1S', 'BM-38_2S', 'BM-38_3S', 'BM-38_4S', 'BM-38_5S', 'BM-40_1S', 'BM-40_2S', 'BM-40_3S', 'BM-40_4S', 'BM-44_1S', 'BM-44_2S',
                            'BM-44_3S', 'BM-44_4S', 'BM-44_5S', 'BM-49_2S', 'BM-49_4S', 'BM-54_3S', 'BM-54_4S']
    Phys_Questions = ['BM-02_2S', 'BM-02_4S', 'BM-07_2S', 'BM-07_3S', 'BM-13_4S', 'BM-20_5S', 'BM-22_1S', 'BM-22_2S', 'BM-23_2S', 'BM-23_3S', 'BM-27_5S', 'BM-28_2S', 'BM-28_3S', 'BM-28_5S', 'BM-30_1S', 'BM-30_3S', 'BM-30_4S', 'BM-31_1S', 'BM-31_3S',
                        'BM-32_1S', 'BM-32_2S', 'BM-32_3S', 'BM-32_4S', 'BM-32_5S', 'BM-33_2S', 'BM-33_5S', 'BM-43_1S', 'BM-43_4S', 'BM-45_1S', 'BM-45_2S', 'BM-45_3S', 'BM-49_1S', 'BM-49_3S', 'BM-54_1S', 'BM-54_2S', 'BM-55_3S', 'BM-55_5S', 'BM-60_3S', 'BM-61_1S',
                        'BM-61_2S', 'BM-61_3S', 'BM-61_4S']
    EcoEvo_Questions = ['BM-08_1S', 'BM-08_2S', 'BM-08_3S', 'BM-08_4S', 'BM-14_1S', 'BM-14_2S', 'BM-14_3S', 'BM-14_4S', 'BM-15_1S', 'BM-15_2S', 'BM-15_3S', 'BM-15_4S', 'BM-16_1S', 'BM-16_2S', 'BM-16_3S', 'BM-16_4S', 'BM-23_1S', 'BM-23_4S', 'BM-30_2S',
                        'BM-31_2S', 'BM-35_1S', 'BM-35_2S', 'BM-35_3S', 'BM-35_4S', 'BM-36_3S', 'BM-37_2S', 'BM-43_2S', 'BM-43_3S', 'BM-43_5S', 'BM-45_4S', 'BM-45_5S', 'BM-50_1S', 'BM-50_2S', 'BM-50_3S', 'BM-50_4S', 'BM-50_5S', 'BM-55_1S', 'BM-55_2S', 'BM-55_4S',
                        'BM-59_1S', 'BM-59_2S', 'BM-59_3S', 'BM-59_4S', 'BM-60_1S', 'BM-60_2S', 'BM-60_4S', 'BM-60_5S']

    StatementsList.append(len(CellMol_Questions))
    StatementsList.append(len(Phys_Questions))
    StatementsList.append(len(EcoEvo_Questions))

    df_Correct['SC_T_Cellular_and_Molecular'] = df_Correct[CellMol_Questions].sum(axis = 1) / df_Correct[CellMol_Questions].count(axis = 1)
    df_Correct['SC_T_Physiology'] = df_Correct[Phys_Questions].sum(axis = 1) / df_Correct[Phys_Questions].count(axis = 1)
    df_Correct['SC_T_Ecology_and_Evolution'] = df_Correct[EcoEvo_Questions].sum(axis = 1) / df_Correct[EcoEvo_Questions].count(axis = 1)

    plt.figure(figsize = (12, 9))
    sns.boxplot(data = df_Correct[['SC_T_Cellular_and_Molecular', 'SC_T_Physiology', 'SC_T_Ecology_and_Evolution']], color = 'w', showfliers = False)
    sns.stripplot(data = df_Correct[['SC_T_Cellular_and_Molecular', 'SC_T_Physiology', 'SC_T_Ecology_and_Evolution']], jitter = 0.25, alpha = min(1, C * 16/(3 * len(df.index))), size = 10, edgecolor = None)
    plt.xticks((0, 1, 2), (u'Cellular and\nMolecular', 'Physiology', u'Ecology and\nEvolution'), rotation = 60)
    plt.yticks((0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1), ('0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'))
    plt.text(3.5, 1.1, 'Subdisciplines', ha = 'center', va = 'center')
    plt.subplots_adjust(left = 0.1, bottom = 0.25)
    plt.savefig('GenBioMAPS_Subdiscipline_Scores.png')
    plt.close()
    plt.clf()

    df = pd.concat([df, df_Correct], axis = 1)

    return df, StatementsList

def GenerateGraphs_Capstone(df):
    df_Correct = pd.DataFrame()

    df_Correct['Q1_1S'] = df['Q1#1_1'] == 2
    df_Correct['Q1_2S'] = df['Q1#1_2'] == 2
    df_Correct['Q1_3S'] = df['Q1#1_3'] == 1
    df_Correct['Q1_4S'] = df['Q1#1_4'] == 1

    df_Correct['Q2_1S'] = df['Q2#1_1'] == 2
    df_Correct['Q2_2S'] = df['Q2#1_2'] == 2
    df_Correct['Q2_3S'] = df['Q2#1_3'] == 1
    df_Correct['Q2_4S'] = df['Q2#1_4'] == 1

    df_Correct['Q3_1S'] = df['Q3#1_1'] == 1
    df_Correct['Q3_2S'] = df['Q3#1_2'] == 2
    df_Correct['Q3_3S'] = df['Q3#1_3'] == 1
    df_Correct['Q3_4S'] = df['Q3#1_4'] == 1

    df_Correct['Q4_1S'] = df['Q4#1_1'] == 2
    df_Correct['Q4_2S'] = df['Q4#1_2'] == 1
    df_Correct['Q4_3S'] = df['Q4#1_3'] == 1
    df_Correct['Q4_4S'] = df['Q4#1_4'] == 1

    df_Correct['Q5_1S'] = df['Q5#1_1'] == 2
    df_Correct['Q5_2S'] = df['Q5#1_2'] == 1
    df_Correct['Q5_3S'] = df['Q5#1_3'] == 1
    df_Correct['Q5_4S'] = df['Q5#1_4'] == 1

    df_Correct['Q6_1S'] = df['Q6#1_1'] == 2
    df_Correct['Q6_2S'] = df['Q6#1_2'] == 1
    df_Correct['Q6_3S'] = df['Q6#1_3'] == 1
    df_Correct['Q6_4S'] = df['Q6#1_4'] == 1

    df_Correct['Q7_1S'] = df['Q7#1_1'] == 2
    df_Correct['Q7_2S'] = df['Q7#1_2'] == 1
    df_Correct['Q7_3S'] = df['Q7#1_3'] == 1
    df_Correct['Q7_4S'] = df['Q7#1_4'] == 2

    df_Correct['Q8_1S'] = df['Q8#1_1'] == 2
    df_Correct['Q8_2S'] = df['Q8#1_2'] == 2
    df_Correct['Q8_3S'] = df['Q8#1_3'] == 2
    df_Correct['Q8_4S'] = df['Q8#1_4'] == 1

    df_Correct['Q9_1S'] = df['Q9#1_1'] == 2
    df_Correct['Q9_2S'] = df['Q9#1_2'] == 1
    df_Correct['Q9_3S'] = df['Q9#1_3'] == 1
    df_Correct['Q9_4S'] = df['Q9#1_4'] == 2

    df_Correct['Q10_1S'] = df['Q10#1_1'] == 1
    df_Correct['Q10_2S'] = df['Q10#1_2'] == 2
    df_Correct['Q10_3S'] = df['Q10#1_3'] == 1
    df_Correct['Q10_4S'] = df['Q10#1_4'] == 1

    df_Correct['Q11_1S'] = df['Q11#1_1'] == 1
    df_Correct['Q11_2S'] = df['Q11#1_2'] == 1
    df_Correct['Q11_3S'] = df['Q11#1_3'] == 2
    df_Correct['Q11_4S'] = df['Q11#1_4'] == 2

    df_Correct['Q12_1S'] = df['Q12#1_1'] == 2
    df_Correct['Q12_2S'] = df['Q12#1_2'] == 2
    df_Correct['Q12_3S'] = df['Q12#1_3'] == 2
    df_Correct['Q12_4S'] = df['Q12#1_4'] == 1

    df_Correct['Q13_1S'] = df['Q13#1_1'] == 2
    df_Correct['Q13_2S'] = df['Q13#1_2'] == 1
    df_Correct['Q13_3S'] = df['Q13#1_3'] == 1
    df_Correct['Q13_4S'] = df['Q13#1_4'] == 2

    df_Correct['Q14_1S'] = df['Q14#1_1'] == 1
    df_Correct['Q14_2S'] = df['Q14#1_2'] == 1
    df_Correct['Q14_3S'] = df['Q14#1_3'] == 2
    df_Correct['Q14_4S'] = df['Q14#1_4'] == 2

    df_Correct['Q15_1S'] = df['Q15#1_1'] == 1
    df_Correct['Q15_2S'] = df['Q15#1_2'] == 2
    df_Correct['Q15_3S'] = df['Q15#1_3'] == 2
    df_Correct['Q15_4S'] = df['Q15#1_4'] == 2

    df_Correct['Q16_1S'] = df['Q16#1_1'] == 2
    df_Correct['Q16_2S'] = df['Q16#1_2'] == 2
    df_Correct['Q16_3S'] = df['Q16#1_3'] == 2
    df_Correct['Q16_4S'] = df['Q16#1_4'] == 2

    df_Correct['Q17_1S'] = df['Q17#1_1'] == 1
    df_Correct['Q17_2S'] = df['Q17#1_2'] == 1
    df_Correct['Q17_3S'] = df['Q17#1_3'] == 1
    df_Correct['Q17_4S'] = df['Q17#1_4'] == 1

    df_Correct['Q18_1S'] = df['Q18#1_1'] == 2
    df_Correct['Q18_2S'] = df['Q18#1_2'] == 2
    df_Correct['Q18_3S'] = df['Q18#1_3'] == 1
    df_Correct['Q18_4S'] = df['Q18#1_4'] == 1

    df_Correct = df_Correct.astype(int)
    StatementsList = []
    StatementsList.append(len(df_Correct.columns))

    df_Correct['SC_Total Score'] = df_Correct.sum(axis = 1) / len(df_Correct.columns)

    plt.figure(figsize = (12, 9))
    sns.boxplot(data = df_Correct['SC_Total Score'], color = 'w', showfliers = False)
    sns.stripplot(data = df_Correct['SC_Total Score'], jitter = 0.25, alpha = min(1, C * 72/len(df.index)), size = 10, edgecolor = None)
    plt.tick_params(bottom = False, labelbottom = False)
    plt.yticks((0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1), ('0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'))
    plt.text(0, 1.05, 'Total Scores', ha = 'center', va = 'center')
    plt.subplots_adjust(left = 0.1)
    plt.savefig('Capstone_TotalScores.png')
    plt.close()
    plt.clf()

    VC_Evo_Questions = [col for col in df_Correct.columns if 'Q1_' in col or 'Q2' in col or 'Q3' in col]
    VC_IF_Questions = [col for col in df_Correct.columns if 'Q4' in col or 'Q5' in col or 'Q6' in col or 'Q8' in col or 'Q9' in col or 'Q10' in col or 'Q11' in col or 'Q17' in col or 'Q18' in col]
    VC_SF_Questions = [col for col in df_Correct.columns if 'Q7' in col or 'Q15' in col or 'Q16' in col or 'Q9' in col or 'Q11' in col or 'Q12' in col or 'Q13' in col]
    VC_TEM_Questions = [col for col in df_Correct.columns if 'Q12' in col or 'Q13' in col or 'Q14' in col or 'Q2' in col or 'Q15' in col]
    VC_S_Questions = [col for col in df_Correct.columns if 'Q6' in col or 'Q10' in col]

    StatementsList.append(len(VC_Evo_Questions))
    StatementsList.append(len(VC_IF_Questions))
    StatementsList.append(len(VC_SF_Questions))
    StatementsList.append(len(VC_TEM_Questions))
    StatementsList.append(len(VC_S_Questions))

    df_Correct['SC_VC_Evolution'] = df_Correct[VC_Evo_Questions].sum(axis = 1) / len(VC_Evo_Questions)
    df_Correct['SC_VC_Information Flow'] = df_Correct[VC_IF_Questions].sum(axis = 1) / len(VC_IF_Questions)
    df_Correct['SC_VC_Structure/Function'] = df_Correct[VC_SF_Questions].sum(axis = 1) / len(VC_SF_Questions)
    df_Correct['SC_VC_Transformations of Energy and Matter'] = df_Correct[VC_TEM_Questions].sum(axis = 1) / len(VC_TEM_Questions)
    df_Correct['SC_VC_Systems'] = df_Correct[VC_S_Questions].sum(axis = 1) / len(VC_S_Questions)

    plt.figure(figsize = (12, 9))
    sns.boxplot(data = df_Correct[['SC_VC_Evolution', 'SC_VC_Information Flow', 'SC_VC_Structure/Function', 'SC_VC_Transformations of Energy and Matter', 'SC_VC_Systems']], color = 'w', showfliers = False)
    sns.stripplot(data = df_Correct[['SC_VC_Evolution', 'SC_VC_Information Flow', 'SC_VC_Structure/Function', 'SC_VC_Transformations of Energy and Matter', 'SC_VC_Systems']], jitter = 0.25, alpha = min(1, C * 8/(5 * len(df.index))), size = 10, edgecolor = None)
    plt.xticks((0, 1, 2, 3, 4), ('Evolution', 'Information Flow', 'Structure/Function', u'Transformations of\nEnergy and Matter', 'Systems'), rotation = 40)
    plt.yticks((0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1), ('0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'))
    plt.text(2, 1.1, 'Vision and Change Core Concepts', ha = 'center', va = 'center')
    plt.subplots_adjust(left = 0.1, bottom = 0.22)
    plt.savefig('Capstone_VisionChange_Scores.png')
    plt.close()
    plt.clf()

    df = pd.concat([df, df_Correct], axis = 1)

    return df, StatementsList

def GenerateGraphs_PhysMAPS(df):
    # df = df.iloc[:40, :]

    # df.loc[:, 'Q1_1':'Q40_7'] = df.loc[:, 'Q1_1':'Q40_7'].apply(lambda x: x.map({1:1, 2:2, 3:2}))

    df_Correct = pd.DataFrame()

    df_Correct['QB_1S'] = df['Q1_1'] == 1
    df_Correct['QB_2S'] = df['Q1_2'] == 1
    df_Correct['QB_3S'] = df['Q1_3'] == 1
    df_Correct['QB_4S'] = df['Q1_4'] == 1
    df_Correct['QB_5S'] = df['Q1_5'] == 2
    df_Correct['QB_6S'] = df['Q1_6'] == 1

    df_Correct['QC_1S'] = df['Q2_1'] == 1
    df_Correct['QC_2S'] = df['Q2_2'] == 2
    df_Correct['QC_3S'] = df['Q2_4'] == 1
    df_Correct['QC_4S'] = df['Q2_6'] == 1
    df_Correct['QC_5S'] = df['Q2_7'] == 2
    df_Correct['QC_6S'] = df['Q2_8'] == 2

    df_Correct['QE_1S'] = df['Q3_1'] == 1
    df_Correct['QE_2S'] = df['Q3_2'] == 2
    df_Correct['QE_3S'] = df['Q3_3'] == 1
    df_Correct['QE_4S'] = df['Q3_4'] == 1
    df_Correct['QE_5S'] = df['Q3_5'] == 1
    df_Correct['QE_6S'] = df['Q3_6'] == 2

    df_Correct['QF_1S'] = df['Q8_6'] == 2
    df_Correct['QF_2S'] = df['Q8_2'] == 1
    df_Correct['QF_3S'] = df['Q8_4'] == 1
    df_Correct['QF_4S'] = df['Q8_5'] == 2
    df_Correct['QF_5S'] = df['Q8_7'] == 1

    df_Correct['QG_1S'] = df['Q4_1'] == 2
    df_Correct['QG_2S'] = df['Q4_3'] == 1
    df_Correct['QG_3S'] = df['Q4_4'] == 1
    df_Correct['QG_4S'] = df['Q4_5'] == 1
    df_Correct['QG_5S'] = df['Q4_6'] == 2

    df_Correct['QH_1S'] = df['Q5_8'] == 1
    df_Correct['QH_2S'] = df['Q5_2'] == 1
    df_Correct['QH_3S'] = df['Q5_3'] == 1
    df_Correct['QH_4S'] = df['Q5_4'] == 2
    df_Correct['QH_5S'] = df['Q5_6'] == 2
    df_Correct['QH_6S'] = df['Q5_7'] == 2

    df_Correct['QI_1S'] = df['Q6_2'] == 2
    df_Correct['QI_2S'] = df['Q6_3'] == 1
    df_Correct['QI_3S'] = df['Q6_4'] == 2
    df_Correct['QI_4S'] = df['Q6_5'] == 1
    df_Correct['QI_5S'] = df['Q6_7'] == 2
    df_Correct['QI_6S'] = df['Q6_10'] == 2

    df_Correct['QJ_1S'] = df['Q21_1'] == 1
    df_Correct['QJ_2S'] = df['Q21_2'] == 2
    df_Correct['QJ_3S'] = df['Q21_3'] == 1
    df_Correct['QJ_4S'] = df['Q21_4'] == 2
    df_Correct['QJ_5S'] = df['Q21_5'] == 1
    df_Correct['QJ_6S'] = df['Q21_6'] == 1

    df_Correct['QK_1S'] = df['Q7_1'] == 2
    df_Correct['QK_2S'] = df['Q7_2'] == 1
    df_Correct['QK_3S'] = df['Q7_3'] == 1
    df_Correct['QK_4S'] = df['Q7_8'] == 2
    df_Correct['QK_5S'] = df['Q7_7'] == 1

    df_Correct['QV_1S'] = df['Q38_1'] == 1
    df_Correct['QV_2S'] = df['Q38_2'] == 2
    df_Correct['QV_3S'] = df['Q38_3'] == 2
    df_Correct['QV_4S'] = df['Q38_4'] == 1
    df_Correct['QV_5S'] = df['Q38_5'] == 2

    df_Correct['QW_1S'] = df['Q22_1'] == 2
    df_Correct['QW_2S'] = df['Q22_2'] == 1
    df_Correct['QW_3S'] = df['Q22_3'] == 2
    df_Correct['QW_4S'] = df['Q22_4'] == 1
    df_Correct['QW_5S'] = df['Q22_5'] == 1
    df_Correct['QW_6S'] = df['Q22_7'] == 2

    df_Correct['QZ_1S'] = df['Q40_1'] == 2
    df_Correct['QZ_2S'] = df['Q40_2'] == 1
    df_Correct['QZ_3S'] = df['Q40_3'] == 1
    df_Correct['QZ_4S'] = df['Q40_4'] == 2
    df_Correct['QZ_5S'] = df['Q40_6'] == 1
    df_Correct['QZ_6S'] = df['Q40_7'] == 1

    df_Correct = df_Correct.astype(int)
    StatementsList = []
    StatementsList.append(len(df_Correct.columns))

    df_Correct['SC_Total_Score'] = df_Correct.sum(axis = 1) / len(df_Correct.columns)

    plt.figure(figsize = (12, 9))
    sns.boxplot(data = df_Correct['SC_Total_Score'], color = 'w', showfliers = False)
    sns.stripplot(data = df_Correct['SC_Total_Score'], jitter = 0.25, alpha = min(1, C * 68/len(df.index)), size = 10, edgecolor = None)
    plt.tick_params(bottom = False, labelbottom = False)
    plt.yticks((0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1), ('0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'))
    plt.text(0, 1.05, 'Total Scores', ha = 'center', va = 'center')
    plt.subplots_adjust(left = 0.1)
    plt.savefig('PhysMAPS_TotalScores.png')
    plt.close()
    plt.clf()

    VC_Evo_Questions = ['QW_2S', 'QW_3S', 'QW_4S', 'QW_5S']
    VC_IF_Questions = ['QB_1S', 'QB_2S', 'QB_3S', 'QB_4S', 'QB_5S', 'QB_6S', 'QE_3S', 'QF_3S', 'QF_4S', 'QF_5S', 'QG_2S', 'QI_1S', 'QI_2S', 'QI_3S', 'QI_4S', 'QI_5S', 'QI_6S', 'QV_1S', 'QV_2S',
                        'QV_3S', 'QV_5S', 'QZ_5S']
    VC_SF_Questions = ['QC_4S', 'QC_5S', 'QC_6S', 'QE_1S', 'QE_2S', 'QE_6S', 'QG_3S', 'QG_4S', 'QG_5S', 'QH_1S', 'QH_6S', 'QI_5S', 'QJ_6S', 'QK_5S', 'QV_1S', 'QV_5S', 'QW_1S', 'QW_6S', 'QZ_5S']
    VC_TEM_Questions = ['QC_1S', 'QC_2S', 'QC_3S', 'QC_4S', 'QC_5S', 'QC_6S', 'QE_1S', 'QE_2S', 'QE_6S', 'QH_1S', 'QH_2S', 'QH_3S', 'QH_4S', 'QJ_1S', 'QJ_2S', 'QJ_3S', 'QJ_4S', 'QJ_5S', 'QK_3S',
                        'QZ_3S', 'QZ_6S']
    VC_S_Questions = ['QB_1S', 'QB_2S', 'QB_3S', 'QB_4S', 'QB_5S', 'QB_6S', 'QE_4S', 'QE_5S', 'QF_1S', 'QF_2S', 'QG_1S', 'QK_1S', 'QK_2S', 'QK_4S', 'QZ_1S', 'QZ_2S', 'QZ_4S']

    StatementsList.append(len(VC_Evo_Questions))
    StatementsList.append(len(VC_IF_Questions))
    StatementsList.append(len(VC_SF_Questions))
    StatementsList.append(len(VC_TEM_Questions))
    StatementsList.append(len(VC_S_Questions))

    df_Correct['SC_VC_Evolution'] = df_Correct[VC_Evo_Questions].sum(axis = 1) / len(VC_Evo_Questions)
    df_Correct['SC_VC_Information_Flow'] = df_Correct[VC_IF_Questions].sum(axis = 1) / len(VC_IF_Questions)
    df_Correct['SC_VC_Structure_Function'] = df_Correct[VC_SF_Questions].sum(axis = 1) / len(VC_SF_Questions)
    df_Correct['SC_VC_Transformations_of_Energy_and_Matter'] = df_Correct[VC_TEM_Questions].sum(axis = 1) / len(VC_TEM_Questions)
    df_Correct['SC_VC_Systems'] = df_Correct[VC_S_Questions].sum(axis = 1) / len(VC_S_Questions)

    plt.figure(figsize = (12, 9))
    sns.boxplot(data = df_Correct[['SC_VC_Evolution', 'SC_VC_Information_Flow', 'SC_VC_Structure_Function', 'SC_VC_Transformations_of_Energy_and_Matter', 'SC_VC_Systems']], color = 'w', showfliers = False)
    sns.stripplot(data = df_Correct[['SC_VC_Evolution', 'SC_VC_Information_Flow', 'SC_VC_Structure_Function', 'SC_VC_Transformations_of_Energy_and_Matter', 'SC_VC_Systems']], jitter = 0.25, alpha = min(1, C * 4/(5 * len(df.index))), size = 10, edgecolor = None)
    plt.xticks((0, 1, 2, 3, 4), ('Evolution', 'Information Flow', 'Structure/Function', u'Transformations of\nEnergy and Matter', 'Systems'), rotation = 40)
    plt.yticks((0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1), ('0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'))
    plt.text(2, 1.05, 'Vision and Change Core Concepts', ha = 'center', va = 'center')
    plt.subplots_adjust(left = 0.1, bottom = 0.22)
    plt.savefig('PhysMAPS_VisionChange_Scores.png')
    plt.close()
    plt.clf()

    Phys_Hom_Questions = ['QE_5S', 'QF_1S', 'QF_2S', 'QG_1S', 'QK_1S', 'QK_2S', 'QK_4S', 'QZ_1S', 'QZ_2S', 'QZ_4S']
    Phys_CCC_Questions = ['QF_3S', 'QF_4S', 'QG_2S', 'QI_1S', 'QI_2S', 'QI_3S', 'QI_4S', 'QI_5S', 'QI_6S', 'QV_1S', 'QV_2S', 'QV_3S', 'QV_4S', 'QV_5S', 'QZ_5S']
    Phys_FDG_Questions = ['QC_1S', 'QC_2S', 'QC_3S', 'QE_2S', 'QH_2S', 'QH_3S', 'QH_4S', 'QJ_1S', 'QJ_3S', 'QJ_4S', 'QJ_5S', 'QK_3S', 'QZ_3S', 'QZ_6S']
    Phys_CM_Questions = ['QC_4S', 'QC_5S', 'QC_6S', 'QE_6S', 'QH_1S', 'QH_2S', 'QH_4S', 'QH_5S', 'QJ_1S', 'QJ_2S', 'QJ_3S', 'QJ_4S', 'QJ_5S', 'QJ_6S']
    Phys_Int_Questions = ['QB_1S', 'QB_2S', 'QB_3S', 'QB_4S', 'QB_5S', 'QB_6S', 'QE_4S', 'QJ_3S', 'QK_1S', 'QK_4S', 'QV_4S']
    Phys_SF_Questions = ['QC_4S', 'QC_5S', 'QC_6S', 'QE_1S', 'QE_6S', 'QG_3S', 'QG_4S', 'QG_5S', 'QH_5S', 'QH_6S', 'QI_5S', 'QJ_6S', 'QK_5S', 'QV_1S', 'QV_5S', 'QW_1S', 'QW_6S', 'QZ_5S']
    Phys_Evo_Questions = ['QW_2S', 'QW_3S', 'QW_4S', 'QW_5S']

    StatementsList.append(len(Phys_Hom_Questions))
    StatementsList.append(len(Phys_CCC_Questions))
    StatementsList.append(len(Phys_FDG_Questions))
    StatementsList.append(len(Phys_CM_Questions))
    StatementsList.append(len(Phys_Int_Questions))
    StatementsList.append(len(Phys_SF_Questions))
    StatementsList.append(len(Phys_Evo_Questions))

    df_Correct['SC_Phys_Homeostasis'] = df_Correct[Phys_Hom_Questions].sum(axis = 1) / len(Phys_Hom_Questions)
    df_Correct['SC_Phys_CellCell_Communication'] = df_Correct[Phys_CCC_Questions].sum(axis = 1) / len(Phys_CCC_Questions)
    df_Correct['SC_Phys_Flowdown_Gradients'] = df_Correct[Phys_FDG_Questions].sum(axis = 1) / len(Phys_FDG_Questions)
    df_Correct['SC_Phys_Cell_Membrane'] = df_Correct[Phys_CM_Questions].sum(axis = 1) / len(Phys_CM_Questions)
    df_Correct['SC_Phys_Interdependence'] = df_Correct[Phys_Int_Questions].sum(axis = 1) / len(Phys_Int_Questions)
    df_Correct['SC_Phys_Structure_Function'] = df_Correct[Phys_SF_Questions].sum(axis = 1) / len(Phys_SF_Questions)
    df_Correct['SC_Phys_Evolution'] = df_Correct[Phys_Evo_Questions].sum(axis = 1) / len(Phys_Evo_Questions)

    plt.figure(figsize = (12, 9))
    sns.boxplot(data = df_Correct[['SC_Phys_Homeostasis', 'SC_Phys_CellCell_Communication', 'SC_Phys_Flowdown_Gradients', 'SC_Phys_Cell_Membrane', 'SC_Phys_Interdependence', 'SC_Phys_Structure_Function', 'SC_Phys_Evolution']], color = 'w', showfliers = False)
    sns.stripplot(data = df_Correct[['SC_Phys_Homeostasis', 'SC_Phys_CellCell_Communication', 'SC_Phys_Flowdown_Gradients', 'SC_Phys_Cell_Membrane', 'SC_Phys_Interdependence', 'SC_Phys_Structure_Function', 'SC_Phys_Evolution']], jitter = 0.25, alpha = min(1, C * 4/(7 * len(df.index))), size = 10, edgecolor = None)
    plt.xticks((0, 1, 2, 3, 4, 5, 6, 7), ('Homeostasis', u'Cell-Cell\nCommunication', u'Flow-down\nGradients', 'Cell Membrane', 'Interdependence', 'Structure/Function', 'Evolution'), rotation = 75)
    plt.yticks((0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1), ('0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'))
    plt.text(3.5, 1.1, 'Physiology Conceptual Themes', ha = 'center', va = 'center')
    plt.subplots_adjust(left = 0.1, bottom = 0.26)
    plt.savefig('PhysMAPS_Physiology_Scores.png')
    plt.close()
    plt.clf()

    df = pd.concat([df, df_Correct], axis = 1)

    return df, StatementsList
