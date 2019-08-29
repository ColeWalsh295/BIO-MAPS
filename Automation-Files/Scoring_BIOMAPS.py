import os
import numpy as np
import pandas as pd

def Score_EcoEvoMAPS(df, CorrectAnswers_File):
    CorrectAnswers_Series = pd.read_csv(CorrectAnswers_File)

    df[CorrectAnswers_Series.index.values] = df[CorrectAnswers_Series.index.values] == CorrectAnswers_Series

    Answers = pd.read_csv(CorrectAnswers_File)

    df = df.astype(int)

    ### Get Total Score and scores on Ecology and Evolution sub-groups ###

    df['SC_Total Score'] = df.sum(axis = 1) / len(df.columns)

    EC_Questions = ['Q1_1S', 'Q1_2S', 'Q1_3S', 'Q1_4S', 'Q1_5S', 'Q1_6S', 'Q1_7S', 'Q2_9S', 'Q3_1S', 'Q3_2S', 'Q3_3S', 'Q3_4S', 'Q3_5S', 'Q5_5S', 'Q7_1S', 'Q7_2S', 'Q7_3S', 'Q7_7S', 'Q8_1S',
                    'Q8_2S', 'Q8_3S', 'Q8_5S', 'Q8_6S', 'Q8_7S', 'Q9_1S', 'Q9_2S', 'Q9_4S', 'Q9_5S', 'Q9_6S', 'Q9_7S']
    EV_Questions = ['Q2_1S', 'Q2_2S', 'Q2_3S', 'Q2_4S', 'Q2_5S', 'Q2_6S', 'Q2_7S', 'Q2_8S', 'Q4_1S', 'Q4_2S', 'Q4_3S', 'Q4_4S', 'Q4_5S', 'Q4_6S', 'Q4_7S', 'Q5_1S', 'Q5_2S', 'Q5_3S', 'Q5_4S',
                    'Q5_6S', 'Q5_7S', 'Q6_1S', 'Q6_2S', 'Q6_3S', 'Q6_4S', 'Q6_5S', 'Q6_6S', 'Q6_7S', 'Q7_4S', 'Q7_5S', 'Q7_6S', 'Q8_4S', 'Q9_3S']

    df['SC_T_Ecology'] = df[EC_Questions].sum(axis = 1) / len(EC_Questions)
    df['SC_T_Evolution'] = df[EV_Questions].sum(axis = 1) /len(EV_Questions)

    ### Get vision and change scores ###

    VC_Evo_Questions = ['Q2_2S', 'Q2_3S', 'Q2_7S', 'Q2_8S', 'Q4_1S', 'Q4_2S', 'Q4_3S', 'Q4_4S', 'Q4_5S', 'Q4_6S', 'Q4_7S', 'Q5_2S', 'Q5_3S', 'Q5_7S', 'Q6_1S', 'Q6_2S', 'Q6_3S', 'Q6_4S', 'Q6_5S',
                        'Q6_6S', 'Q7_4S', 'Q7_5S', 'Q7_6S', 'Q8_4S']
    VC_IF_Questions =  ['Q2_1S', 'Q2_4S', 'Q2_5S', 'Q2_6S', 'Q5_1S', 'Q5_4S', 'Q5_6S', 'Q6_7S']
    VC_SF_Questions = ['Q7_1S', 'Q7_7S', 'Q9_3S']
    VC_TEM_Questions = ['Q1_4S', 'Q1_5S', 'Q7_2S', 'Q7_3S', 'Q8_2S', 'Q8_5S', 'Q8_7S', 'Q9_4S', 'Q9_5S', 'Q9_6S', 'Q9_7S']
    VC_S_Questions = ['Q1_1S', 'Q1_2S', 'Q1_3S', 'Q1_6S', 'Q1_7S', 'Q2_9S', 'Q3_1S', 'Q3_2S', 'Q3_3S', 'Q3_4S', 'Q3_5S', 'Q5_5S', 'Q8_1S', 'Q8_3S', 'Q8_6S', 'Q9_1S', 'Q9_2S']

    df['SC_VC_Evolution'] = df[VC_Evo_Questions].sum(axis = 1) / len(VC_Evo_Questions)
    df['SC_VC_Information Flow'] = df[VC_IF_Questions].sum(axis = 1) / len(VC_IF_Questions)
    df['SC_VC_Structure Function'] = df[VC_SF_Questions].sum(axis = 1) / len(VC_SF_Questions)
    df['SC_VC_Transformations of Energy and Matter'] = df[VC_TEM_Questions].sum(axis = 1) / len(VC_TEM_Questions)
    df['SC_VC_Systems'] = df[VC_S_Questions].sum(axis = 1) / len(VC_S_Questions)

    ### Get Ecology and Evolution sub-group scores

    EE_HV_Questions = ['Q2_1S', 'Q2_4S', 'Q2_5S', 'Q2_6S', 'Q5_1S', 'Q5_4S', 'Q5_6S', 'Q6_7S']
    EE_MC_Questions = ['Q2_3S', 'Q2_7S', 'Q2_8S', 'Q5_2S', 'Q5_3S', 'Q5_7S', 'Q6_6S', 'Q7_4S', 'Q7_5S', 'Q7_6S', 'Q8_4S']
    EE_PEH_Questions = ['Q2_2S', 'Q4_1S', 'Q4_2S', 'Q4_3S', 'Q4_4S', 'Q4_5S', 'Q4_6S', 'Q4_7S', 'Q6_1S', 'Q6_2S', 'Q6_3S', 'Q6_4S', 'Q6_5S', 'Q9_3S']
    EE_BD_Questions = ['Q8_1S', 'Q8_3S', 'Q9_1S']
    EE_P_Questions = ['Q1_3S', 'Q1_6S', 'Q3_1S', 'Q3_2S', 'Q3_4S', 'Q3_5S', 'Q7_7S']
    EE_EM_Questions = ['Q1_4S', 'Q1_5S', 'Q7_2S', 'Q7_3S', 'Q8_2S', 'Q8_5S', 'Q8_7S', 'Q9_4S', 'Q9_5S', 'Q9_6S', 'Q9_7S']
    EE_IE_Questions = ['Q1_1S', 'Q1_2S', 'Q1_7S', 'Q3_3S', 'Q7_1S', 'Q9_2S']
    EE_HI_Questions = ['Q2_9S', 'Q5_5S', 'Q8_6S']

    df['SC_EE_Heritable Variation'] = df[EE_HV_Questions].sum(axis = 1) / len(EE_HV_Questions)
    df['SC_EE_Modes of Change'] = df[EE_MC_Questions].sum(axis = 1) / len(EE_MC_Questions)
    df['SC_EE_Phylogeny and Evolutionary History'] = df[EE_PEH_Questions].sum(axis = 1) / len(EE_PEH_Questions)
    df['SC_EE_Biological Diversity'] = df[EE_BD_Questions].sum(axis = 1) / len(EE_BD_Questions)
    df['SC_EE_Populations'] = df[EE_P_Questions].sum(axis = 1) / len(EE_P_Questions)
    df['SC_EE_Energy and Matter'] = df[EE_EM_Questions].sum(axis = 1) / len(EE_EM_Questions)
    df['SC_EE_Interactions with Ecosystems'] = df[EE_IE_Questions].sum(axis = 1) / len(EE_IE_Questions)
    df['SC_EE_Human Impact'] = df[EE_HI_Questions].sum(axis = 1) / len(EE_HI_Questions)

    ### Get 4DEE scores ###

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
    FDEE_SpaceTime_Questions = ['Q2_1S', 'Q2_2S', 'Q2_3S', 'Q2_4S', 'Q2_5S', 'Q2_6S', 'Q2_7S', 'Q2_8S', 'Q3_4S', 'Q4_1S', 'Q4_2S', 'Q4_3S', 'Q4_4S', 'Q4_5S', 'Q4_6S', 'Q4_7S', 'Q5_1S', 'Q5_2S', 'Q5_3S', 'Q5_4S', 'Q5_6S', 'Q5_7S', 'Q6_1S', 'Q6_2S', 'Q6_3S', 'Q6_4S', 'Q6_5S', 'Q6_6S', 'Q6_7S', 'Q7_4S', 'Q7_5S', 'Q7_6S', 'Q8_3S', 'Q8_4S', 'Q9_3S']

    df['SC_FDEE_Populations'] = df[FDEE_Pop_Questions].sum(axis = 1) / len(FDEE_Pop_Questions)
    df['SC_FDEE_Communities'] = df[FDEE_Com_Questions].sum(axis = 1) / len(FDEE_Com_Questions)
    df['SC_FDEE_Ecosystems'] = df[FDEE_Eco_Questions].sum(axis = 1) / len(FDEE_Eco_Questions)
    df['SC_FDEE_Biomes'] = df[FDEE_Biomes_Questions].sum(axis = 1) / len(FDEE_Biomes_Questions)
    df['SC_FDEE_Biosphere'] = df[FDEE_Biosphere_Questions].sum(axis = 1) / len(FDEE_Biosphere_Questions)
    df['SC_FDEE_Quantitative Reasoning'] = df[FDEE_Quant_Questions].sum(axis = 1) / len(FDEE_Quant_Questions)
    df['SC_FDEE_Designing and Critiquing'] = df[FDEE_Design_Questions].sum(axis = 1) / len(FDEE_Design_Questions)
    df['SC_FDEE_Human Change'] = df[FDEE_HumanAcc_Questions].sum(axis = 1) / len(FDEE_HumanAcc_Questions)
    df['SC_FDEE_Human Shape'] = df[FDEE_HumanShape_Questions].sum(axis = 1) / len(FDEE_HumanShape_Questions)
    df['SC_FDEE_Matter and Energy'] = df[FDEE_TME_Questions].sum(axis = 1) / len(FDEE_TME_Questions)
    df['SC_FDEE_Systems'] = df[FDEE_Systems_Questions].sum(axis = 1) / len(FDEE_Systems_Questions)
    df['SC_FDEE_Space and Time'] = df[FDEE_SpaceTime_Questions].sum(axis = 1) / len(FDEE_SpaceTime_Questions)

    df['SC_FDEE_Core Ecology'] = df[FDEE_CoreEcology].sum(axis = 1) / len(FDEE_CoreEcology)
    df['SC_FDEE_FDEE_Ecology Practices'] = df[FDEE_EcologyPractices].sum(axis = 1) / len(FDEE_EcologyPractices)
    df['SC_FDEE_Human Environment'] = df[FDEE_HumanEnvironment].sum(axis = 1) / len(FDEE_HumanEnvironment)
    df['SC_FDEE_Cross-Cutting'] = df[FDEE_CrossCutting].sum(axis = 1) / len(FDEE_CrossCutting)

    return df
