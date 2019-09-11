# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd
import pylatex.config as cf
from pylatex import Document, Package, Center, NewPage, Section, Subsection, MiniPage, FootnoteText, Figure, Tabular, Table, Tabu, LongTable, NoEscape, Itemize
import ReportGraph_BIOMAPS
cwd = os.getcwd()

def StdErr(Series):
    return Series.std()/np.sqrt(len(Series))

def Tablefy(Series, func, **kwargs):
    try:
        Input = str(int(func(Series, **kwargs))) + '%'
    except ValueError:
        Input = 0
    return Input

def Generate_EcoEvoMAPS(fname, width, DataFrame, NumReported, MainDirectory = cwd, Where = 'Local'):

    df, Statements = ReportGraph_BIOMAPS.GenerateGraphs_EcoEvoMAPS(DataFrame)
    df_info = pd.read_excel(MainDirectory + '/EcoEvo_Supplemental.xlsx', index_col = 0)

    cf.active = cf.Version1(indent = False)
    geometry_options = {"right": "1.5cm", "left": "1.5cm", "top": "2.5cm", "bottom": "2.5cm"}
    doc = Document(fname, geometry_options = geometry_options)
    doc.packages.append(Package('graphicx'))
    doc.packages.append(Package('caption'))
    doc.packages.append(Package('array'))
    doc.packages.append(Package('makecell'))

    df.loc[:, 'Q1_1S':] = (df.loc[:, 'Q1_1S':] * 100)

    with doc.create(Section('Ecology and Evolution (EcoEvo-MAPS)', numbering = False)):

        doc.append(NoEscape("Summary of class participation in EcoEvo-MAPS:"))
        with doc.create(Center()) as centered:
            with centered.create(Table(position = 'h!')) as Tab_Class:
                with doc.create(Tabular('| l | c |')) as Tab:
                    Tab.add_hline()
                    Tab.add_row(("Reported number of students in class", int(NumReported)))
                    Tab.add_hline()
                    Tab.add_row(("Number of valid responses", len(df.index)))
                    Tab.add_hline()
                    Tab.add_row(("Estimated fraction of class participating in survey", str(int(len(df.index)/NumReported * 100)) + '%'))
                    Tab.add_hline()

        doc.append(NoEscape("""
                            Box-and-whisker plots show the median and variation between students' scores. The line in the middle of the box represents the median score and boxes represent the interquartile range.
                            Points overlaying the box plots represent averages for individual students on that subset of questions:
                            """))

        with doc.create(Center()) as centered:
            doc.append(NoEscape(r"\includegraphics[width = 0.5\linewidth]{C:/BIOMAPS/Example_Box.png}"))
            # doc.append(NoEscape(r"\captionof{figure}{Data presented below is summarized using box and whisker plots.}"))

        with doc.create(Subsection('Total score and total score subdivided by questions focused on Ecology and Evolutionary Biology', numbering = False)):

            with doc.create(Center()) as centered:
                doc.append(NoEscape(r"\includegraphics[width = \linewidth]{EcoEvoMAPS_TotalScores.png}"))
                doc.append(NoEscape(r"\captionof{figure}{Boxplots of total score and total score subdivided by questions focused on Ecology and Evolutionary Biology}"))

            with doc.create(Center()) as centered:
                with centered.create(Table(position = 'h!')) as Tab:
                    with doc.create(Tabular('l c c c')) as Tab1:
                        Tab1.add_row(("", "Total Score", "Ecology", "Evolution"))
                        Tab1.add_hline()

                        Tab1.add_row(("No. Statements", Statements[0], Statements[1], Statements[2]))

                        Tab1.add_row(("Average", Tablefy(df['SC_Total_Score'], np.mean), Tablefy(df['SC_T_Ecology'], np.mean), Tablefy(df['SC_T_Evolution'], np.mean)))

                        Tab1.add_row(("Std. Error", Tablefy(df['SC_Total_Score'], StdErr), Tablefy(df['SC_T_Ecology'], StdErr), Tablefy(df['SC_T_Evolution'], StdErr)))

                        Tab1.add_row(("Minimum", Tablefy(df['SC_Total_Score'], np.min), Tablefy(df['SC_T_Ecology'], np.min), Tablefy(df['SC_T_Evolution'], np.min)))

                        Tab1.add_row(("1st Quartile", Tablefy(df['SC_Total_Score'], np.percentile, q = 25), Tablefy(df['SC_T_Ecology'], np.percentile, q = 25), Tablefy(df['SC_T_Evolution'], np.percentile, q = 25)))

                        Tab1.add_row(("Median", Tablefy(df['SC_Total_Score'], np.median), Tablefy(df['SC_T_Ecology'], np.median), Tablefy(df['SC_T_Evolution'], np.median)))

                        Tab1.add_row(("3rd Quartile", Tablefy(df['SC_Total_Score'], np.percentile, q = 75), Tablefy(df['SC_T_Ecology'], np.percentile, q = 75), Tablefy(df['SC_T_Evolution'], np.percentile, q = 75)))

                        Tab1.add_row(("Maximum", Tablefy(df['SC_Total_Score'], np.max), Tablefy(df['SC_T_Ecology'], np.max), Tablefy(df['SC_T_Evolution'], np.max)))

                        Tab1.add_hline()

                    Tab.add_caption(NoEscape("Summary statistics of total score and total score subdivided by questions focused on Ecology and Evolutionary Biology."))

        doc.append(NewPage())

        with doc.create(Subsection(NoEscape("""Scores subdivided by the Vision and Change Core Concepts (American Association for the Advancement of Science 2011. Vision and change in undergraduate biology education: A call to
                                            action. American Association for the Advancement of Science, Washington, D.C.)
                                            """), numbering = False)):

            with doc.create(Center()) as centered:
                doc.append(NoEscape(r"\includegraphics[width = \linewidth]{EcoEvoMAPS_VisionChange_Scores.png}"))
                doc.append(NoEscape(r"\captionof{figure}{Boxplots of scores subdivided by the Vision and Change core concepts.}"))

            with doc.create(Center()) as centered:
                with centered.create(Table(position = 'h!')) as Tab:
                    with doc.create(Tabular('l c c c c c')) as Tab2:
                        Tab2.add_row(("", 'Evolution', 'Information Flow', 'Structure Function', u'Transformations of Energy and Matter', 'Systems'))
                        Tab2.add_hline()

                        Tab2.add_row(("No. Statements", Statements[3], Statements[4], Statements[5], Statements[6], Statements[7]))

                        Tab2.add_row(("Average", Tablefy(df['SC_VC_Evolution'], np.mean), Tablefy(df['SC_VC_Information_Flow'], np.mean), Tablefy(df['SC_VC_Structure_Function'], np.mean), Tablefy(df['SC_VC_Transformations_of_Energy_and_Matter'], np.mean), Tablefy(df['SC_VC_Systems'], np.mean)))

                        Tab2.add_row(("Std. Error", Tablefy(df['SC_VC_Evolution'], StdErr), Tablefy(df['SC_VC_Information_Flow'], StdErr), Tablefy(df['SC_VC_Structure_Function'], StdErr), Tablefy(df['SC_VC_Transformations_of_Energy_and_Matter'], StdErr), Tablefy(df['SC_VC_Systems'], StdErr)))

                        Tab2.add_row(("Minimum", Tablefy(df['SC_VC_Evolution'], np.min), Tablefy(df['SC_VC_Information_Flow'], np.min), Tablefy(df['SC_VC_Structure_Function'], np.min), Tablefy(df['SC_VC_Transformations_of_Energy_and_Matter'], np.min), Tablefy(df['SC_VC_Systems'], np.min)))

                        Tab2.add_row(("1st Quartile", Tablefy(df['SC_VC_Evolution'], np.percentile, q = 25), Tablefy(df['SC_VC_Information_Flow'], np.percentile, q = 25), Tablefy(df['SC_VC_Structure_Function'], np.percentile, q = 25), Tablefy(df['SC_VC_Transformations_of_Energy_and_Matter'], np.percentile, q = 25),
                                        Tablefy(df['SC_VC_Systems'], np.percentile, q = 25)))

                        Tab2.add_row(("Median", Tablefy(df['SC_VC_Evolution'], np.median), Tablefy(df['SC_VC_Information_Flow'], np.median), Tablefy(df['SC_VC_Structure_Function'], np.median), Tablefy(df['SC_VC_Transformations_of_Energy_and_Matter'], np.median), Tablefy(df['SC_VC_Systems'], np.median)))

                        Tab2.add_row(("3rd Quartile", Tablefy(df['SC_VC_Evolution'], np.percentile, q = 75), Tablefy(df['SC_VC_Information_Flow'], np.percentile, q = 75), Tablefy(df['SC_VC_Structure_Function'], np.percentile, q = 75), Tablefy(df['SC_VC_Transformations_of_Energy_and_Matter'], np.percentile, q = 75),
                                        Tablefy(df['SC_VC_Systems'], np.percentile, q = 75)))

                        Tab2.add_row(("Maximum", Tablefy(df['SC_VC_Evolution'], np.max), Tablefy(df['SC_VC_Information_Flow'], np.max), Tablefy(df['SC_VC_Structure_Function'], np.max), Tablefy(df['SC_VC_Transformations_of_Energy_and_Matter'], np.max), Tablefy(df['SC_VC_Systems'], np.max)))

                        Tab2.add_hline()

                    Tab.add_caption(NoEscape("Summary statistics of scores subdivided by the Vision and Change core concepts."))

        doc.append(NewPage())

        with doc.create(Subsection('Scores divided by Ecology and Evolution Conceptual Themes (based on those identified by a CourseSource working group www.coursesource.org/courses/ecology)', numbering = False)):

            with doc.create(Center()) as centered:
                doc.append(NoEscape(r"\includegraphics[width = \linewidth]{EcoEvoMAPS_EcologyEvolution_Scores.png}"))
                doc.append(NoEscape(r"\captionof{figure}{Boxplots of scores on Ecology and Evolution conceptual themes.}"))

            with doc.create(Center()) as centered:
                with centered.create(Table(position = 'h!')) as Tab:
                    with doc.create(Tabu('>{\RaggedRight}p{0.14\linewidth} >{\centering}p{0.08\linewidth} >{\centering}p{0.06\linewidth} >{\centering}p{0.08\linewidth} >{\centering}p{0.08\linewidth} >{\centering}p{0.08\linewidth} >{\centering}p{0.06\linewidth} >{\centering}p{0.1\linewidth} >{\centering}p{0.06\linewidth}')) as Tab3:
                        Tab3.add_row(("", 'Heritable Variation', 'Modes of Change', u'Phylogeny\nand\nEvolutionary\nHistory', 'Biological Diversity', 'Populations', 'Energy and Matter', 'Interactions with Ecosystems', 'Human Impact'))
                        Tab3.add_hline()

                        Tab3.add_row("No. Statements", Statements[8], Statements[9], Statements[10], Statements[11], Statements[12], Statements[13], Statements[14], Statements[15])

                        Tab3.add_row(("Average", Tablefy(df['SC_EE_Heritable_Variation'], np.mean), Tablefy(df['SC_EE_Modes_of_Change'], np.mean), Tablefy(df['SC_EE_Phylogeny_and_Evolutionary_History'], np.mean), Tablefy(df['SC_EE_Biological_Diversity'], np.mean), Tablefy(df['SC_EE_Populations'], np.mean),
                                        Tablefy(df['SC_EE_Energy_and_Matter'], np.mean), Tablefy(df['SC_EE_Interactions_with_Ecosystems'], np.mean), Tablefy(df['SC_EE_Human_Impact'], np.mean)))

                        Tab3.add_row(("Std. Error", Tablefy(df['SC_EE_Heritable_Variation'], StdErr), Tablefy(df['SC_EE_Modes_of_Change'], StdErr), Tablefy(df['SC_EE_Phylogeny_and_Evolutionary_History'], StdErr), Tablefy(df['SC_EE_Biological_Diversity'], StdErr), Tablefy(df['SC_EE_Populations'], StdErr),
                                        Tablefy(df['SC_EE_Energy_and_Matter'], StdErr), Tablefy(df['SC_EE_Interactions_with_Ecosystems'], StdErr), Tablefy(df['SC_EE_Human_Impact'], StdErr)))

                        Tab3.add_row(("Minimum", Tablefy(df['SC_EE_Heritable_Variation'], np.min), Tablefy(df['SC_EE_Modes_of_Change'], np.min), Tablefy(df['SC_EE_Phylogeny_and_Evolutionary_History'], np.min), Tablefy(df['SC_EE_Biological_Diversity'], np.min), Tablefy(df['SC_EE_Populations'], np.min),
                                        Tablefy(df['SC_EE_Energy_and_Matter'], np.min), Tablefy(df['SC_EE_Interactions_with_Ecosystems'], np.min), Tablefy(df['SC_EE_Human_Impact'], np.min)))

                        Tab3.add_row(("1st Quartile", Tablefy(df['SC_EE_Heritable_Variation'], np.percentile, q = 25), Tablefy(df['SC_EE_Modes_of_Change'], np.percentile, q = 25), Tablefy(df['SC_EE_Phylogeny_and_Evolutionary_History'], np.percentile, q = 25), Tablefy(df['SC_EE_Biological_Diversity'], np.percentile, q = 25),
                                        Tablefy(df['SC_EE_Populations'], np.percentile, q = 25), Tablefy(df['SC_EE_Energy_and_Matter'], np.percentile, q = 25), Tablefy(df['SC_EE_Interactions_with_Ecosystems'], np.percentile, q = 25), Tablefy(df['SC_EE_Human_Impact'], np.percentile, q = 25)))

                        Tab3.add_row(("Median", Tablefy(df['SC_EE_Heritable_Variation'], np.median), Tablefy(df['SC_EE_Modes_of_Change'], np.median), Tablefy(df['SC_EE_Phylogeny_and_Evolutionary_History'], np.median), Tablefy(df['SC_EE_Biological_Diversity'], np.median), Tablefy(df['SC_EE_Populations'], np.median),
                                        Tablefy(df['SC_EE_Energy_and_Matter'], np.median), Tablefy(df['SC_EE_Interactions_with_Ecosystems'], np.median), Tablefy(df['SC_EE_Human_Impact'], np.median)))

                        Tab3.add_row(("3rd Quartile", Tablefy(df['SC_EE_Heritable_Variation'], np.percentile, q = 75), Tablefy(df['SC_EE_Modes_of_Change'], np.percentile, q = 75), Tablefy(df['SC_EE_Phylogeny_and_Evolutionary_History'], np.percentile, q = 75), Tablefy(df['SC_EE_Biological_Diversity'], np.percentile, q = 75),
                                        Tablefy(df['SC_EE_Populations'], np.percentile, q = 75), Tablefy(df['SC_EE_Energy_and_Matter'], np.percentile, q = 75), Tablefy(df['SC_EE_Interactions_with_Ecosystems'], np.percentile, q = 75), Tablefy(df['SC_EE_Human_Impact'], np.percentile, q = 75)))

                        Tab3.add_row(("Maximum", Tablefy(df['SC_EE_Heritable_Variation'], np.max), Tablefy(df['SC_EE_Modes_of_Change'], np.max), Tablefy(df['SC_EE_Phylogeny_and_Evolutionary_History'], np.max), Tablefy(df['SC_EE_Biological_Diversity'], np.max), Tablefy(df['SC_EE_Populations'], np.max),
                                        Tablefy(df['SC_EE_Energy_and_Matter'], np.max), Tablefy(df['SC_EE_Interactions_with_Ecosystems'], np.max), Tablefy(df['SC_EE_Human_Impact'], np.max)))

                        Tab3.add_hline()

                    Tab.add_caption(NoEscape("Summary statistics of scores on Ecology and Evolution conceptual themes."))

        doc.append(NewPage())

        with doc.create(Subsection('Scores divided by 4DEE framework alignment.', numbering = False)):

            with doc.create(Center()) as centered:
                doc.append(NoEscape(r"\includegraphics[width = \linewidth]{EcoEvoMAPS_4DEE_Scores.png}"))
                doc.append(NoEscape(r"\captionof{figure}{Boxplots of scores based on 4DEE framework alignment.}"))

            with doc.create(Center()) as centered:
                with centered.create(Table(position = 'h!')) as Tab:
                    with doc.create(Tabular('l c c c c')) as Tab2:
                        Tab2.add_row(("", 'Core Ecology Concepts', 'Ecology Practices', 'Human-Environment Interactions', 'Cross-Cutting Themes'))
                        Tab2.add_hline()

                        Tab2.add_row(("No. Statements", Statements[16], Statements[17], Statements[18], Statements[19]))

                        Tab2.add_row(("Average", Tablefy(df['SC_FDEE_Core_Ecology'], np.mean), Tablefy(df['SC_FDEE_FDEE_Ecology_Practices'], np.mean), Tablefy(df['SC_FDEE_Human_Environment'], np.mean), Tablefy(df['SC_FDEE_CrossCutting'], np.mean)))

                        Tab2.add_row(("Std. Error", Tablefy(df['SC_FDEE_Core_Ecology'], StdErr), Tablefy(df['SC_FDEE_FDEE_Ecology_Practices'], StdErr), Tablefy(df['SC_FDEE_Human_Environment'], StdErr), Tablefy(df['SC_FDEE_CrossCutting'], StdErr)))

                        Tab2.add_row(("Minimum", Tablefy(df['SC_FDEE_Core_Ecology'], np.min), Tablefy(df['SC_FDEE_FDEE_Ecology_Practices'], np.min), Tablefy(df['SC_FDEE_Human_Environment'], np.min), Tablefy(df['SC_FDEE_CrossCutting'], np.min)))

                        Tab2.add_row(("1st Quartile", Tablefy(df['SC_FDEE_Core_Ecology'], np.percentile, q = 25), Tablefy(df['SC_FDEE_FDEE_Ecology_Practices'], np.percentile, q = 25), Tablefy(df['SC_FDEE_Human_Environment'], np.percentile, q = 25), Tablefy(df['SC_FDEE_CrossCutting'], np.percentile, q = 25)))

                        Tab2.add_row(("Median", Tablefy(df['SC_FDEE_Core_Ecology'], np.median), Tablefy(df['SC_FDEE_FDEE_Ecology_Practices'], np.median), Tablefy(df['SC_FDEE_Human_Environment'], np.median), Tablefy(df['SC_FDEE_CrossCutting'], np.median)))

                        Tab2.add_row(("3rd Quartile", Tablefy(df['SC_FDEE_Core_Ecology'], np.percentile, q = 75), Tablefy(df['SC_FDEE_FDEE_Ecology_Practices'], np.percentile, q = 75), Tablefy(df['SC_FDEE_Human_Environment'], np.percentile, q = 75), Tablefy(df['SC_FDEE_CrossCutting'], np.percentile, q = 75)))

                        Tab2.add_row(("Maximum", Tablefy(df['SC_FDEE_Core_Ecology'], np.max), Tablefy(df['SC_FDEE_FDEE_Ecology_Practices'], np.max), Tablefy(df['SC_FDEE_Human_Environment'], np.max), Tablefy(df['SC_FDEE_CrossCutting'], np.max)))

                        Tab2.add_hline()

                    Tab.add_caption(NoEscape("Summary statistics of scores subdivided by 4DEE framework dimensions."))

        doc.append(NewPage())

        with doc.create(Subsection('Student Performance on Individual Statements', numbering = False)):

            with doc.create(Center()) as centered:
                with centered.create(LongTable('>{\RaggedRight}p{0.06\linewidth} >{\centering}p{0.06\linewidth} p{0.24\linewidth} >{\centering}p{0.06\linewidth} >{\centering}p{0.08\linewidth} >{\centering}p{0.14\linewidth} >{\RaggedRight}p{0.22\linewidth}', pos = 'h!')) as Tab4:
                    doc.append(NoEscape('\small'))
                    Tab4.add_row(("Statement No.", 'Percent Correct', 'Statement', 'Correct Answer', 'Vision and Change', 'Ecology and Evolution "Big Ideas"', '4DEE Framework'), Tabular = True)
                    Tab4.add_hline()

                    for Statement, Sup in df_info.iterrows():

                        Tab4.add_row((Statement, str(int(df.loc[:, 'Q' + Statement + 'S'].mean(axis = 0))) + '%', df_info.loc[Statement, 'Statement'],
                                        df_info.loc[Statement, 'Correct Answer'], NoEscape(df_info.loc[Statement, 'Vision and Change']),
                                        NoEscape(df_info.loc[Statement, 'Ecology and Evolution "Big Ideas" (i.e., concepts)']), NoEscape(df_info.loc[Statement, '4DEE Framework Dimensions'])), Tabular = True)
                        Tab4.add_hline()

                    Tab4.add_hline()

    Compiled = False
    Tries = 0
    while not Compiled:
        try:
            Tries += 1
            doc.generate_pdf(clean_tex = False, compiler_args = ['-quiet'])
            Compiled = True
        except:
            pass
        if(Tries > 5):
            break

    return df

def Generate_GenBioMAPS(fname, width, DataFrame, NumReported, MainDirectory = cwd, Where = 'Local'):

    df, Statements = ReportGraph_BIOMAPS.GenerateGraphs_GenBioMAPS(DataFrame)
    df_info = pd.read_excel(MainDirectory + '/GenBio_Supplemental.xlsx', index_col = 0)

    cf.active = cf.Version1(indent = False)
    geometry_options = {"right": "1.5cm", "left": "1.5cm", "top": "2.5cm", "bottom": "2.5cm"}
    doc = Document(fname, geometry_options = geometry_options)
    doc.packages.append(Package('graphicx'))
    doc.packages.append(Package('caption'))
    doc.packages.append(Package('array'))
    doc.packages.append(Package('makecell'))

    df.loc[:, 'BM-01_1S':] = (df.loc[:, 'BM-01_1S':] * 100)

    with doc.create(Section('General Biology (GenBio-MAPS)', numbering = False)):

        doc.append(NoEscape("Summary of class participation in GenBio-MAPS:"))
        with doc.create(Center()) as centered:
            with centered.create(Table(position = 'h!')) as Tab_Class:
                with doc.create(Tabular('| l | c |')) as Tab:
                    Tab.add_hline()
                    Tab.add_row(("Reported number of students in class", int(NumReported)))
                    Tab.add_hline()
                    Tab.add_row(("Number of valid responses", len(df.index)))
                    Tab.add_hline()
                    Tab.add_row(("Estimated fraction of class participating in survey", str(int(len(df.index)/NumReported * 100)) + '%'))
                    Tab.add_hline()

        doc.append(NoEscape("""
                            Box-and-whisker plots show the median and variation between students' scores. The line in the middle of the box represents the median score and boxes represent the interquartile range.
                            Points overlaying the box plots represent averages for individual students on that subset of questions:
                            """))

        with doc.create(Center()) as centered:
            doc.append(NoEscape(r"\includegraphics[width = 0.5\linewidth]{" + MainDirectory + "/Example_Box.png}"))
            # doc.append(NoEscape(r"\captionof{figure}{Data presented below is summarized using box and whisker plots.}"))

        with doc.create(Subsection('Total score', numbering = False)):

            with doc.create(Center()) as centered:
                doc.append(NoEscape(r"\includegraphics[width = \linewidth]{GenBioMAPS_TotalScores.png}"))
                doc.append(NoEscape(r"\captionof{figure}{Boxplots of total scores.}"))

            with doc.create(Center()) as centered:
                with centered.create(Table(position = 'h!')) as Tab:
                    with doc.create(Tabular('l c')) as Tab1:
                        Tab1.add_row(("", "Total Score"))
                        Tab1.add_hline()

                        Tab1.add_row(("No. Statements", Statements[0]))

                        Tab1.add_row(("Average", Tablefy(df['SC_Total_Score'], np.mean)))

                        Tab1.add_row(("Std. Error", Tablefy(df['SC_Total_Score'], StdErr)))

                        Tab1.add_row(("Minimum", Tablefy(df['SC_Total_Score'], np.min)))

                        Tab1.add_row(("1st Quartile", Tablefy(df['SC_Total_Score'], np.percentile, q = 25)))

                        Tab1.add_row(("Median", Tablefy(df['SC_Total_Score'], np.median)))

                        Tab1.add_row(("3rd Quartile", Tablefy(df['SC_Total_Score'], np.percentile, q = 75)))

                        Tab1.add_row(("Maximum", Tablefy(df['SC_Total_Score'], np.max)))

                        Tab1.add_hline()

                    Tab.add_caption(NoEscape("Summary statistics of total scores."))

        doc.append(NewPage())

        with doc.create(Subsection(NoEscape("""Scores subdivided by the Vision and Change Core Concepts (American Association for the Advancement of Science 2011. Vision and change in undergraduate biology education: A call to
                                            action. American Association for the Advancement of Science, Washington, D.C.)
                                            """), numbering = False)):

            with doc.create(Center()) as centered:
                doc.append(NoEscape(r"\includegraphics[width = \linewidth]{GenBioMAPS_VisionChange_Scores.png}"))
                doc.append(NoEscape(r"\captionof{figure}{Boxplots of scores subdivided by the Vision and Change core concepts.}"))

            with doc.create(Center()) as centered:
                with centered.create(Table(position = 'h!')) as Tab:
                    with doc.create(Tabular('l c c c c c')) as Tab2:
                        Tab2.add_row(("", 'Evolution', 'Information Flow', 'Structure Function', u'Transformations of Energy and Matter', 'Systems'))
                        Tab2.add_hline()

                        Tab2.add_row(("No. Statements", Statements[1], Statements[2], Statements[3], Statements[4], Statements[5]))

                        Tab2.add_row(("Average", Tablefy(df['SC_VC_Evolution'], np.mean), Tablefy(df['SC_VC_Information_Flow'], np.mean), Tablefy(df['SC_VC_Structure_Function'], np.mean), Tablefy(df['SC_VC_Transformations_of_Energy_and_Matter'], np.mean), Tablefy(df['SC_VC_Systems'], np.mean)))

                        Tab2.add_row(("Std. Error", Tablefy(df['SC_VC_Evolution'], StdErr), Tablefy(df['SC_VC_Information_Flow'], StdErr), Tablefy(df['SC_VC_Structure_Function'], StdErr), Tablefy(df['SC_VC_Transformations_of_Energy_and_Matter'], StdErr), Tablefy(df['SC_VC_Systems'], StdErr)))

                        Tab2.add_row(("Minimum", Tablefy(df['SC_VC_Evolution'], np.min), Tablefy(df['SC_VC_Information_Flow'], np.min), Tablefy(df['SC_VC_Structure_Function'], np.min), Tablefy(df['SC_VC_Transformations_of_Energy_and_Matter'], np.min), Tablefy(df['SC_VC_Systems'], np.min)))

                        Tab2.add_row(("1st Quartile", Tablefy(df['SC_VC_Evolution'], np.nanpercentile, q = 25), Tablefy(df['SC_VC_Information_Flow'], np.nanpercentile, q = 25), Tablefy(df['SC_VC_Structure_Function'], np.nanpercentile, q = 25), Tablefy(df['SC_VC_Transformations_of_Energy_and_Matter'], np.nanpercentile, q = 25),
                                        Tablefy(df['SC_VC_Systems'], np.nanpercentile, q = 25)))

                        Tab2.add_row(("Median", Tablefy(df['SC_VC_Evolution'], np.nanmedian), Tablefy(df['SC_VC_Information_Flow'], np.nanmedian), Tablefy(df['SC_VC_Structure_Function'], np.nanmedian), Tablefy(df['SC_VC_Transformations_of_Energy_and_Matter'], np.nanmedian), Tablefy(df['SC_VC_Systems'], np.nanmedian)))

                        Tab2.add_row(("3rd Quartile", Tablefy(df['SC_VC_Evolution'], np.nanpercentile, q = 75), Tablefy(df['SC_VC_Information_Flow'], np.nanpercentile, q = 75), Tablefy(df['SC_VC_Structure_Function'], np.nanpercentile, q = 75), Tablefy(df['SC_VC_Transformations_of_Energy_and_Matter'], np.nanpercentile, q = 75),
                                        Tablefy(df['SC_VC_Systems'], np.nanpercentile, q = 75)))

                        Tab2.add_row(("Maximum", Tablefy(df['SC_VC_Evolution'], np.max), Tablefy(df['SC_VC_Information_Flow'], np.max), Tablefy(df['SC_VC_Structure_Function'], np.max), Tablefy(df['SC_VC_Transformations_of_Energy_and_Matter'], np.max), Tablefy(df['SC_VC_Systems'], np.max)))

                        Tab2.add_hline()

                    Tab.add_caption(NoEscape("Summary statistics of scores subdivided by the Vision and Change core concepts."))

        doc.append(NewPage())

        with doc.create(Subsection('Scores divided by subdiscipline', numbering = False)):

            with doc.create(Center()) as centered:
                doc.append(NoEscape(r"\includegraphics[width = \linewidth]{GenBIOMAPS_Subdiscipline_Scores.png}"))
                doc.append(NoEscape(r"\captionof{figure}{Boxplots of scores on subdisciplines.}"))

            with doc.create(Center()) as centered:
                with centered.create(Table(position = 'h!')) as Tab:
                    with doc.create(Tabular('l c c c')) as Tab3:
                        Tab3.add_row(("", 'Cellular and Molecular', 'Physiology', 'Ecology and Evolution'))
                        Tab3.add_hline()

                        Tab3.add_row("No. Statements", Statements[6], Statements[7], Statements[8])

                        Tab3.add_row(("Average", Tablefy(df['SC_T_Cellular_and_Molecular'], np.mean), Tablefy(df['SC_T_Physiology'], np.mean), Tablefy(df['SC_T_Ecology_and_Evolution'], np.mean)))

                        Tab3.add_row(("Std. Error", Tablefy(df['SC_T_Cellular_and_Molecular'], StdErr), Tablefy(df['SC_T_Physiology'], StdErr), Tablefy(df['SC_T_Ecology_and_Evolution'], StdErr)))

                        Tab3.add_row(("Minimum", Tablefy(df['SC_T_Cellular_and_Molecular'], np.min), Tablefy(df['SC_T_Physiology'], np.min), Tablefy(df['SC_T_Ecology_and_Evolution'], np.min)))

                        Tab3.add_row(("1st Quartile", Tablefy(df['SC_T_Cellular_and_Molecular'], np.nanpercentile, q = 25), Tablefy(df['SC_T_Physiology'], np.nanpercentile, q = 25), Tablefy(df['SC_T_Ecology_and_Evolution'], np.nanpercentile, q = 25)))

                        Tab3.add_row(("Median", Tablefy(df['SC_T_Cellular_and_Molecular'], np.nanmedian), Tablefy(df['SC_T_Physiology'], np.nanmedian), Tablefy(df['SC_T_Ecology_and_Evolution'], np.nanmedian)))

                        Tab3.add_row(("3rd Quartile", Tablefy(df['SC_T_Cellular_and_Molecular'], np.nanpercentile, q = 75), Tablefy(df['SC_T_Physiology'], np.nanpercentile, q = 75), Tablefy(df['SC_T_Ecology_and_Evolution'], np.nanpercentile, q = 75)))

                        Tab3.add_row(("Maximim", Tablefy(df['SC_T_Cellular_and_Molecular'], np.max), Tablefy(df['SC_T_Physiology'], np.max), Tablefy(df['SC_T_Ecology_and_Evolution'], np.max)))

                        Tab3.add_hline()

                    Tab.add_caption(NoEscape("Summary statistics of scores on subdisciplines."))

        doc.append(NewPage())

        with doc.create(Subsection('Student Performance on Individual Statements', numbering = False)):

            with doc.create(Center()) as centered:
                with centered.create(LongTable('>{\RaggedRight}p{0.08\linewidth} >{\centering}p{0.08\linewidth} p{0.35\linewidth} >{\centering}p{0.08\linewidth} >{\centering}p{0.1\linewidth} >{\centering}p{0.18\linewidth}', pos = 'h!')) as Tab4:
                    Tab4.add_row(("Statement No.", 'Percent Correct', 'Statement', 'Correct Answer', 'Vision and Change', 'Subdiscipline'), Tabular = True)
                    Tab4.add_hline()
                    #Tab4.append(NoEscape(r"\tabularnewline"))

                    for Statement, Sup in df_info.iterrows():

                        Tab4.add_row(('BM-' + Statement, str(int(df.loc[:, 'BM-' + Statement[:2] + '_' + str(ord(Statement[2]) - 96) + 'S'].mean(axis = 0))) + '%', NoEscape(df_info.loc[Statement, 'Statement']),
                                        df_info.loc[Statement, 'Correct Answer'], NoEscape(df_info.loc[Statement, 'Vision and Change']),
                                        NoEscape(df_info.loc[Statement, 'Subdiscipline'])), Tabular = True)
                        Tab4.add_hline()
                        #Tab4.append(NoEscape(r"\tabularnewline"))

                    Tab4.add_hline()

    Compiled = False
    Tries = 0
    while not Compiled:
        try:
            Tries += 1
            doc.generate_pdf(clean_tex = False, compiler_args = ['-quiet'])
            Compiled = True
        except:
            pass
        if(Tries > 5):
            break

    return df

def Generate_Capstone(fname, width, DataFrame, NumReported, MainDirectory = cwd, Where = 'Local'):

    df, Statements = ReportGraph_BIOMAPS.GenerateGraphs_Capstone(DataFrame)
    df_info = pd.read_excel(MainDirectory + '/Capstone_Supplemental.xlsx', index_col = 0)

    cf.active = cf.Version1(indent = False)
    geometry_options = {"right": "1.5cm", "left": "1.5cm", "top": "2.5cm", "bottom": "2.5cm"}
    doc = Document(fname, geometry_options = geometry_options)
    doc.packages.append(Package('graphicx'))
    doc.packages.append(Package('caption'))
    doc.packages.append(Package('array'))
    doc.packages.append(Package('makecell'))

    df.loc[:, 'Q1_1S':] = (df.loc[:, 'Q1_1S':] * 100)

    with doc.create(Section('Molecular Biology Capstone', numbering = False)):

        doc.append(NoEscape("Summary of class participation in Capstone:"))
        with doc.create(Center()) as centered:
            with centered.create(Table(position = 'h!')) as Tab_Class:
                with doc.create(Tabular('| l | c |')) as Tab:
                    Tab.add_hline()
                    Tab.add_row(("Reported number of students in class", int(NumReported)))
                    Tab.add_hline()
                    Tab.add_row(("Number of valid responses", len(df.index)))
                    Tab.add_hline()
                    Tab.add_row(("Estimated fraction of class participating in survey", str(int(len(df.index)/NumReported * 100)) + '%'))
                    Tab.add_hline()

        doc.append(NoEscape("""
                            Box-and-whisker plots show the median and variation between students' scores. The line in the middle of the box represents the median score and boxes represent the interquartile range.
                            Points overlaying the box plots represent averages for individual students on that subset of questions:
                            """))

        with doc.create(Center()) as centered:
            doc.append(NoEscape(r"\includegraphics[width = 0.5\linewidth]{" + MainDirectory + "/Example_Box.png}"))
            # doc.append(NoEscape(r"\captionof{figure}{Data presented below is summarized using box and whisker plots.}"))

        with doc.create(Subsection('Total score', numbering = False)):

            with doc.create(Center()) as centered:
                doc.append(NoEscape(r"\includegraphics[width = \linewidth]{Capstone_TotalScores.png}"))
                doc.append(NoEscape(r"\captionof{figure}{Boxplot of total scores.}"))

            with doc.create(Center()) as centered:
                with centered.create(Table(position = 'h!')) as Tab:
                    with doc.create(Tabular('l c')) as Tab1:
                        Tab1.add_row(("", "Total Score"))
                        Tab1.add_hline()

                        Tab1.add_row(("No. Statements", Statements[0]))

                        Tab1.add_row(("Average", Tablefy(df['SC_Total Score'], np.mean)))

                        Tab1.add_row(("Std. Error", Tablefy(df['SC_Total Score'], StdErr)))

                        Tab1.add_row(("Minimum", Tablefy(df['SC_Total Score'], np.min)))

                        Tab1.add_row(("1st Quartile", Tablefy(df['SC_Total Score'], np.percentile, q = 25)))

                        Tab1.add_row(("Median", Tablefy(df['SC_Total Score'], np.median)))

                        Tab1.add_row(("3rd Quartile", Tablefy(df['SC_Total Score'], np.percentile, q = 75)))

                        Tab1.add_row(("Maximum", Tablefy(df['SC_Total Score'], np.max)))

                        Tab1.add_hline()

                    Tab.add_caption(NoEscape("Summary statistics of students' total scores."))

        doc.append(NewPage())

        with doc.create(Subsection(NoEscape("""Scores subdivided by the Vision and Change Core Concepts (American Association for the Advancement of Science 2011. Vision and change in undergraduate biology education: A call to
                                            action. American Association for the Advancement of Science, Washington, D.C.)
                                            """), numbering = False)):

            with doc.create(Center()) as centered:
                doc.append(NoEscape(r"\includegraphics[width = \linewidth]{Capstone_VisionChange_Scores.png}"))
                doc.append(NoEscape(r"\captionof{figure}{Boxplots of scores subdivided by the Vision and Change core concepts.}"))

            with doc.create(Center()) as centered:
                with centered.create(Table(position = 'h!')) as Tab:
                    with doc.create(Tabular('l c c c c c')) as Tab2:
                        Tab2.add_row(("", 'Evolution', 'Information Flow', 'Structure Function', 'Transformations of Energy and Matter', 'Systems'))
                        Tab2.add_hline()

                        Tab2.add_row(("No. Statements", Statements[1], Statements[2], Statements[3], Statements[4], Statements[5]))

                        Tab2.add_row(("Average", Tablefy(df['SC_VC_Evolution'], np.mean), Tablefy(df['SC_VC_Information Flow'], np.mean), Tablefy(df['SC_VC_Structure/Function'], np.mean), Tablefy(df['SC_VC_Transformations of Energy and Matter'], np.mean), Tablefy(df['SC_VC_Systems'], np.mean)))

                        Tab2.add_row(("Std. Error", Tablefy(df['SC_VC_Evolution'], StdErr), Tablefy(df['SC_VC_Information Flow'], StdErr), Tablefy(df['SC_VC_Structure/Function'], StdErr), Tablefy(df['SC_VC_Transformations of Energy and Matter'], StdErr), Tablefy(df['SC_VC_Systems'], StdErr)))

                        Tab2.add_row(("Minimum", Tablefy(df['SC_VC_Evolution'], np.min), Tablefy(df['SC_VC_Information Flow'], np.min), Tablefy(df['SC_VC_Structure/Function'], np.min), Tablefy(df['SC_VC_Transformations of Energy and Matter'], np.min), Tablefy(df['SC_VC_Systems'], np.min)))

                        Tab2.add_row(("1st Quartile", Tablefy(df['SC_VC_Evolution'], np.percentile, q = 25), Tablefy(df['SC_VC_Information Flow'], np.percentile, q = 25), Tablefy(df['SC_VC_Structure/Function'], np.percentile, q = 25), Tablefy(df['SC_VC_Transformations of Energy and Matter'], np.percentile, q = 25),
                                        Tablefy(df['SC_VC_Systems'], np.percentile, q = 25)))

                        Tab2.add_row(("Median", Tablefy(df['SC_VC_Evolution'], np.median), Tablefy(df['SC_VC_Information Flow'], np.median), Tablefy(df['SC_VC_Structure/Function'], np.median), Tablefy(df['SC_VC_Transformations of Energy and Matter'], np.median), Tablefy(df['SC_VC_Systems'], np.median)))

                        Tab2.add_row(("3rd Quartile", Tablefy(df['SC_VC_Evolution'], np.percentile, q = 75), Tablefy(df['SC_VC_Information Flow'], np.percentile, q = 75), Tablefy(df['SC_VC_Structure/Function'], np.percentile, q = 75), Tablefy(df['SC_VC_Transformations of Energy and Matter'], np.percentile, q = 75),
                                        Tablefy(df['SC_VC_Systems'], np.percentile, q = 75)))

                        Tab2.add_row(("Maximum", Tablefy(df['SC_VC_Evolution'], np.max), Tablefy(df['SC_VC_Information Flow'], np.max), Tablefy(df['SC_VC_Structure/Function'], np.max), Tablefy(df['SC_VC_Transformations of Energy and Matter'], np.max), Tablefy(df['SC_VC_Systems'], np.max)))

                        Tab2.add_hline()

                    Tab.add_caption(NoEscape("Summary statistics of scores subdivided by the Vision and Change core concepts."))

        doc.append(NewPage())

        with doc.create(Subsection('Student Performance on Individual Statements', numbering = False)):

            with doc.create(Center()) as centered:
                with centered.create(LongTable('>{\RaggedRight}p{0.08\linewidth} >{\centering}p{0.08\linewidth} p{0.4\linewidth} >{\centering}p{0.08\linewidth} >{\RaggedRight}p{0.2\linewidth}', pos = 'h!')) as Tab4:
                    Tab4.add_row(("Statement No.", 'Percent Correct', 'Statement', 'Correct Answer', 'Vision and Change'))
                    Tab4.add_hline()

                    for Statement, Sup in df_info.iterrows():

                        Statement_Split = Statement.split('_')
                        Statement_No = 4 * (int(Statement_Split[0]) - 1) + int(Statement_Split[1])

                        Tab4.add_row((Statement_No, str(int(df.loc[:, 'Q' + Statement + 'S'].mean(axis = 0))) + '%', NoEscape(df_info.loc[Statement, 'Statement']),
                                        df_info.loc[Statement, 'Correct Answer'], NoEscape(str(df_info.loc[Statement, 'Vision and Change']))))
                        Tab4.add_hline()

                    Tab4.add_hline()

    Compiled = False
    Tries = 0
    while not Compiled:
        try:
            Tries += 1
            doc.generate_pdf(clean_tex = False, compiler_args = ['-quiet'])
            Compiled = True
        except:
            pass
        if(Tries > 5):
            break

    doc.generate_pdf(clean_tex = False)

    return df

def Generate_PhysMAPS(fname, width, DataFrame, NumReported, MainDirectory = cwd, Where = 'Local'):

    df, Statements = ReportGraph_BIOMAPS.GenerateGraphs_PhysMAPS(DataFrame)
    df_info = pd.read_excel(MainDirectory + '/Phys_Supplemental.xlsx', index_col = 0).fillna('')

    cf.active = cf.Version1(indent = False)
    geometry_options = {"right": "1.5cm", "left": "1.5cm", "top": "2.5cm", "bottom": "2.5cm"}
    doc = Document(fname, geometry_options = geometry_options)
    doc.packages.append(Package('graphicx'))
    doc.packages.append(Package('caption'))
    doc.packages.append(Package('array'))
    doc.packages.append(Package('makecell'))

    df.loc[:, 'QB_1S':] = (df.loc[:, 'QB_1S':] * 100)

    with doc.create(Section('Physiology (Phys-MAPS)', numbering = False)):

        doc.append(NoEscape("Summary of class participation in Phys-MAPS:"))
        with doc.create(Center()) as centered:
            with centered.create(Table(position = 'h!')) as Tab_Class:
                with doc.create(Tabular('| l | c |')) as Tab:
                    Tab.add_hline()
                    Tab.add_row(("Reported number of students in class", int(NumReported)))
                    Tab.add_hline()
                    Tab.add_row(("Number of valid responses", len(df.index)))
                    Tab.add_hline()
                    Tab.add_row(("Estimated fraction of class participating in survey", str(int(len(df.index)/NumReported * 100)) + '%'))
                    Tab.add_hline()

        doc.append(NoEscape("""
                            Box-and-whisker plots show the median and variation between students' scores. The line in the middle of the box represents the median score and boxes represent the interquartile range.
                            Points overlaying the box plots represent averages for individual students on that subset of questions:
                            """))

        with doc.create(Center()) as centered:
            doc.append(NoEscape(r"\includegraphics[width = 0.5\linewidth]{C:/BIOMAPS/Example_Box.png}"))
            # doc.append(NoEscape(r"\captionof{figure}{Data presented below is summarized using box and whisker plots.}"))

        with doc.create(Subsection('Total score', numbering = False)):

            with doc.create(Center()) as centered:
                doc.append(NoEscape(r"\includegraphics[width = \linewidth]{PhysMAPS_TotalScores.png}"))
                doc.append(NoEscape(r"\captionof{figure}{Boxplot of total scores.}"))

            with doc.create(Center()) as centered:
                with centered.create(Table(position = 'h!')) as Tab:
                    with doc.create(Tabular('l c')) as Tab1:
                        Tab1.add_row(("", "Total Score"))
                        Tab1.add_hline()

                        Tab1.add_row(("No. Statements", Statements[0]))

                        Tab1.add_row(("Average", Tablefy(df['SC_Total Score'], np.mean)))

                        Tab1.add_row(("Std. Error", Tablefy(df['SC_Total Score'], StdErr)))

                        Tab1.add_row(("Minimum", Tablefy(df['SC_Total Score'], np.min)))

                        Tab1.add_row(("1st Quartile", Tablefy(df['SC_Total Score'], np.percentile, q = 25)))

                        Tab1.add_row(("Median", Tablefy(df['SC_Total Score'], np.median)))

                        Tab1.add_row(("3rd Quartile", Tablefy(df['SC_Total Score'], np.percentile, q = 75)))

                        Tab1.add_row(("Maximum", Tablefy(df['SC_Total Score'], np.max)))

                        Tab1.add_hline()

                    Tab.add_caption(NoEscape("Summary statistics of students' total scores."))

        doc.append(NewPage())

        with doc.create(Subsection(NoEscape("""Scores subdivided by the Vision and Change Core Concepts (American Association for the Advancement of Science 2011. Vision and change in undergraduate biology education: A call to
                                            action. American Association for the Advancement of Science, Washington, D.C.)
                                            """), numbering = False)):

            with doc.create(Center()) as centered:
                doc.append(NoEscape(r"\includegraphics[width = \linewidth]{PhysMAPS_VisionChange_Scores.png}"))
                doc.append(NoEscape(r"\captionof{figure}{Boxplots of scores subdivided by the Vision and Change core concepts.}"))

            with doc.create(Center()) as centered:
                with centered.create(Table(position = 'h!')) as Tab:
                    with doc.create(Tabular('l c c c c c')) as Tab2:
                        Tab2.add_row(("", 'Evolution', 'Information Flow', 'Structure Function', 'Transformations of Energy and Matter', 'Systems'))
                        Tab2.add_hline()

                        Tab2.add_row(("No. Statements", Statements[1], Statements[2], Statements[3], Statements[4], Statements[5]))

                        Tab2.add_row(("Average", Tablefy(df['SC_VC_Evolution'], np.mean), Tablefy(df['SC_VC_Information Flow'], np.mean), Tablefy(df['SC_VC_Structure/Function'], np.mean), Tablefy(df['SC_VC_Transformations of Energy and Matter'], np.mean), Tablefy(df['SC_VC_Systems'], np.mean)))

                        Tab2.add_row(("Std. Error", Tablefy(df['SC_VC_Evolution'], StdErr), Tablefy(df['SC_VC_Information Flow'], StdErr), Tablefy(df['SC_VC_Structure/Function'], StdErr), Tablefy(df['SC_VC_Transformations of Energy and Matter'], StdErr), Tablefy(df['SC_VC_Systems'], StdErr)))

                        Tab2.add_row(("Minimum", Tablefy(df['SC_VC_Evolution'], np.min), Tablefy(df['SC_VC_Information Flow'], np.min), Tablefy(df['SC_VC_Structure/Function'], np.min), Tablefy(df['SC_VC_Transformations of Energy and Matter'], np.min), Tablefy(df['SC_VC_Systems'], np.min)))

                        Tab2.add_row(("1st Quartile", Tablefy(df['SC_VC_Evolution'], np.percentile, q = 25), Tablefy(df['SC_VC_Information Flow'], np.percentile, q = 25), Tablefy(df['SC_VC_Structure/Function'], np.percentile, q = 25), Tablefy(df['SC_VC_Transformations of Energy and Matter'], np.percentile, q = 25),
                                        Tablefy(df['SC_VC_Systems'], np.percentile, q = 25)))

                        Tab2.add_row(("Median", Tablefy(df['SC_VC_Evolution'], np.median), Tablefy(df['SC_VC_Information Flow'], np.median), Tablefy(df['SC_VC_Structure/Function'], np.median), Tablefy(df['SC_VC_Transformations of Energy and Matter'], np.median), Tablefy(df['SC_VC_Systems'], np.median)))

                        Tab2.add_row(("3rd Quartile", Tablefy(df['SC_VC_Evolution'], np.percentile, q = 75), Tablefy(df['SC_VC_Information Flow'], np.percentile, q = 75), Tablefy(df['SC_VC_Structure/Function'], np.percentile, q = 75), Tablefy(df['SC_VC_Transformations of Energy and Matter'], np.percentile, q = 75),
                                        Tablefy(df['SC_VC_Systems'], np.percentile, q = 75)))

                        Tab2.add_row(("Maximum", Tablefy(df['SC_VC_Evolution'], np.max), Tablefy(df['SC_VC_Information Flow'], np.max), Tablefy(df['SC_VC_Structure/Function'], np.max), Tablefy(df['SC_VC_Transformations of Energy and Matter'], np.max), Tablefy(df['SC_VC_Systems'], np.max)))

                        Tab2.add_hline()

                    Tab.add_caption(NoEscape("Summary statistics of scores subdivided by the Vision and Change core concepts."))

        doc.append(NewPage())

        with doc.create(Subsection('Scores divided by Physiology Conceptual Themes', numbering = False)):

            with doc.create(Center()) as centered:
                doc.append(NoEscape(r"\includegraphics[width = \linewidth]{PhysMAPS_Physiology_Scores.png}"))
                doc.append(NoEscape(r"\captionof{figure}{Boxplots of scores on Physiology conceptual themes.}"))

            with doc.create(Center()) as centered:
                with centered.create(Table(position = 'h!')) as Tab:
                    with doc.create(Tabu('>{\RaggedRight}p{0.14\linewidth} >{\centering}p{0.1\linewidth} >{\centering}p{0.12\linewidth} >{\centering}p{0.08\linewidth} >{\centering}p{0.1\linewidth} >{\centering}p{0.12\linewidth} >{\centering}p{0.08\linewidth} >{\centering}p{0.08\linewidth}')) as Tab3:
                        Tab3.add_row(("", 'Homeostasis', u'Cell-cell\nCommunication', 'Gradients', 'Cell Membrane', 'Interdependence', u'Structure\n/Function', 'Evolution'))
                        Tab3.add_hline()

                        Tab3.add_row(("No. Statements", Statements[6], Statements[7], Statements[8], Statements[9], Statements[10], Statements[11], Statements[12]))

                        Tab3.add_row(("Average", Tablefy(df['SC_Phys_Homeostasis'], np.mean), Tablefy(df['SC_Phys_Cell-Cell Communication'], np.mean), Tablefy(df['SC_Phys_Flow-down Gradients'], np.mean), Tablefy(df['SC_Phys_Cell Membrane'], np.mean),
                                        Tablefy(df['SC_Phys_Interdependence'], np.mean), Tablefy(df['SC_Phys_Structure/Function'], np.mean), Tablefy(df['SC_Phys_Evolution'], np.mean)))

                        Tab3.add_row(("Std. Error", Tablefy(df['SC_Phys_Homeostasis'], StdErr), Tablefy(df['SC_Phys_Cell-Cell Communication'], StdErr), Tablefy(df['SC_Phys_Flow-down Gradients'], StdErr), Tablefy(df['SC_Phys_Cell Membrane'], StdErr),
                                        Tablefy(df['SC_Phys_Interdependence'], StdErr), Tablefy(df['SC_Phys_Structure/Function'], StdErr), Tablefy(df['SC_Phys_Evolution'], StdErr)))

                        Tab3.add_row(("Minimum", Tablefy(df['SC_Phys_Homeostasis'], np.min), Tablefy(df['SC_Phys_Cell-Cell Communication'], np.min), Tablefy(df['SC_Phys_Flow-down Gradients'], np.min), Tablefy(df['SC_Phys_Cell Membrane'], np.min),
                                        Tablefy(df['SC_Phys_Interdependence'], np.min), Tablefy(df['SC_Phys_Structure/Function'], np.min), Tablefy(df['SC_Phys_Evolution'], np.min)))

                        Tab3.add_row(("1st Quartile", Tablefy(df['SC_Phys_Homeostasis'], np.percentile, q = 25), Tablefy(df['SC_Phys_Cell-Cell Communication'], np.percentile, q = 25), Tablefy(df['SC_Phys_Flow-down Gradients'], np.percentile, q = 25), Tablefy(df['SC_Phys_Cell Membrane'], np.percentile, q = 25),
                                        Tablefy(df['SC_Phys_Interdependence'], np.percentile, q = 25), Tablefy(df['SC_Phys_Structure/Function'], np.percentile, q = 25), Tablefy(df['SC_Phys_Evolution'], np.percentile, q = 25)))

                        Tab3.add_row(("Median", Tablefy(df['SC_Phys_Homeostasis'], np.median), Tablefy(df['SC_Phys_Cell-Cell Communication'], np.median), Tablefy(df['SC_Phys_Flow-down Gradients'], np.median), Tablefy(df['SC_Phys_Cell Membrane'], np.median),
                                        Tablefy(df['SC_Phys_Interdependence'], np.median), Tablefy(df['SC_Phys_Structure/Function'], np.median), Tablefy(df['SC_Phys_Evolution'], np.median)))

                        Tab3.add_row(("3rd Quartile", Tablefy(df['SC_Phys_Homeostasis'], np.percentile, q = 75), Tablefy(df['SC_Phys_Cell-Cell Communication'], np.percentile, q = 75), Tablefy(df['SC_Phys_Flow-down Gradients'], np.percentile, q = 75), Tablefy(df['SC_Phys_Cell Membrane'], np.percentile, q = 75),
                                        Tablefy(df['SC_Phys_Interdependence'], np.percentile, q = 75), Tablefy(df['SC_Phys_Structure/Function'], np.percentile, q = 75), Tablefy(df['SC_Phys_Evolution'], np.percentile, q = 75)))

                        Tab3.add_row(("Maximum", Tablefy(df['SC_Phys_Homeostasis'], np.max), Tablefy(df['SC_Phys_Cell-Cell Communication'], np.max), Tablefy(df['SC_Phys_Flow-down Gradients'], np.max), Tablefy(df['SC_Phys_Cell Membrane'], np.max),
                                        Tablefy(df['SC_Phys_Interdependence'], np.max), Tablefy(df['SC_Phys_Structure/Function'], np.max), Tablefy(df['SC_Phys_Evolution'], np.max)))

                        Tab3.add_hline()

                    Tab.add_caption(NoEscape("Summary statistics of scores on Physiology conceptual themes."))

        doc.append(NewPage())

        with doc.create(Subsection('Student Performance on Individual Statements', numbering = False)):

            with doc.create(Center()) as centered:
                with centered.create(LongTable('>{\RaggedRight}p{0.08\linewidth} >{\centering}p{0.08\linewidth} p{0.26\linewidth} >{\centering}p{0.08\linewidth} >{\RaggedRight}p{0.19\linewidth} >{\RaggedRight}p{0.2\linewidth}', pos = 'h!')) as Tab4:
                    Tab4.add_row(("Statement No.", 'Percent Correct', 'Statement', 'Correct Answer', 'Vision and Change', 'Physiology "Big Ideas"'))
                    Tab4.add_hline()

                    for Statement, Sup in df_info.iterrows():

                        Tab4.add_row((Statement, str(int(df.loc[:, 'Q' + Statement[0] + '_' + Statement[1] + 'S'].mean(axis = 0))) + '%', NoEscape(df_info.loc[Statement, 'Statement']),
                                        df_info.loc[Statement, 'Correct Answer'], NoEscape(str(df_info.loc[Statement, 'Vision and Change'])),
                                        NoEscape(df_info.loc[Statement, 'Physiology "Big Ideas" (i.e., concepts)'])))
                        Tab4.add_hline()

                    Tab4.add_hline()

    doc.generate_pdf(clean_tex = False)

    return df
