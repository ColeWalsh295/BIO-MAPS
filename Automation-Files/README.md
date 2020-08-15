The scripts included here are part of the automated administration system used to administer the Bio-MAPS suite of assessments.

`PythonAutomation_BIOMAPS.py` includes the main administration code and functions that communicate with the Qualtrics survey platform.

`ReportGen_BIOMAPS.py` includes functions that leverage `pylatex` to generate summary reports of student performance on an assessment. These functions are called by
`PythonAutomation_BIOMAPS.py` as part of the administration system, but can be called independently to generate reports for any Bio-MAPS dataset.

`ReportGraph_BIOMAPS.py` includes functions that score students' responses to the individual assessments and generate summary box plots of students' scores along various
dimensions. These functions are called by `ReportGen_BIOMAPS.py` as part of the administration system, but can be called independently to generate reports for any Bio-MAPS dataset.
