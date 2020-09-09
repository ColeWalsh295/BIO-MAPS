# Bio-MAPS

Biology Measuring Achievement and Progression in Science (Bio-MAPS), is a suite of diagnostic assessments that aim to measure student understanding across a degree program and are aligned with the Vision and Change nationally-validated set of core biology concepts. The diagnostic assessments include:
-EcoEvo-MAPS (Ecology and Evolution)
-Molecular Biology Capstone
-Phys-MAPS (Physiology)
-GenBio-MAPS (General Biology)

For more information about these assessments and how to administer them in your class, check out the [Cornell Physics Education Research Lab website](http://cperl.lassp.cornell.edu/bio-maps).
 
# Scripts in this repository

`Automation-Files` contains python scripts used in the automatic administration of these assessments via Qualtrics. Instructors indicate via an online link their interest in deploying these assessments in their classes, then a unique survey is generated and the link to that survey is emailed to the instructor. The automated system also sends email reminders, activates and deactivates surveys, and shares surveys with collaborators. After a survey has closed, the system sends instructors a summary report of their class' performance as well as list of students who completed the assessment. Instructors are able to change the date that they would like a survey to close by completing a separate course date change, which is also monitored by the administration system.

`Instructor_Dasboard` contains R scripts (and one python script) used to construct instructor dashboards deployed via [shinyapps.io]( https://cderatcornell.shinyapps.io/Bio-MAPS/). The dashboard allows instructors to interactively engage with and download identifiable data from their class. Instructors can view student performance along a number of variables, compare two of their classes, or compare their class to the national dataset.

`Processing_Scripts` includes python functions and a jupyter notebook for downloading Bio-MAPS data and building the master datasets that are used as part of the instructor dashboard.
