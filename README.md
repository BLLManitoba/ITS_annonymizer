# ITS file anonymizer

DISCLAIMER: Please read this readme carefully so that you ensure you understand what data are being anonymized, and what data are being left in their original format.
Researchers may also wish to rename their ITS filenames before public release, as filenames contain potentially identifying information (such as child ID #), which this program does not alter.

The anonymizer processes files line-by-line via a text editor, preserveing the original structure of the ITS file.
It allows the user to choose the folder that contains the original ITS files, and to choose the folder where they would like to save their anonymized files.

## Installation

Download the Its_anonymizer repository from GitHub.

In order for the anonymizer to work, the following python files MUST be saved in the same folder:

1. its_anon_gui2.py
2. its_anonymizer.py
3. replacements_dict.json

its_anon_gui2.py relies on the following modules, which must also be installed on your computer:

1. Tkinter (installation instructions: https://tkdocs.com/tutorial/install.html)
2. json (This package is usually included with the basic python packages, but if necessary, you can find installation instructions here: https://pythonhosted.org/json-schema-validator/installation.html)

## To use

1. Double click on the file 'its_anon_gui2.py' This will launch a user interface with several buttons.
2. Select input folder (allows user to choose input ITS files)
3. Select output folder (allows user to choose where to save anonymized files - it is recommended to have an empty output folder already made!)
4. Click "Fully anonymize files" (anonymizes all the sensitive/non-anonymous data in the files - see below for details)
5. OR Partially anonymize files:
	1. Click the desired checkbuttons to leave the desired data in the ITS file's original format.
	2. Click "Partially anonymize files"(anonymizes only data specified)
	
### Checkbuttons

Each checkbutton, if checked will exclude the corresponding row of data from anonymization. Data in each row are:

1. Child Data
	* date of birth, enrollment date, child ID
2. Time Data
	* File name, time file was created
	* All instances of timestamps throughout the file (if "only_time" is set to true in the json file, the hhmmss timestamps will be preserved with the dates anonymized)

## Anonymization and Rationale

Several different generic strings are used to replace identifying information, stored in `replacement_dict.json`. This file can be easily modified to include other information that needs to be private.

Several data points are anonymized when this program is run. See below for a description of and rationale for replacing each item.

1. Child's birthdate:

	dob replaced with 1000-01-01
	
	NOTE: Child's "chronological age" and "estimated developmental age" are NOT anonymized, as this information may be needed for meaningful data analyses. Because they only give age in months, this is not sufficient detail to extract identity and therefore not of concern.

2. Filename:

	filename replaced with new_filename_1001

	In the ITS file, the filename is listed, which contains the recording upload date and the Child ID. Knowing the upload date and child's exact age at recording could allow for birthdates to be calculated. Child ID may or may not contain identifiable information depending on a lab's data storage and labeling policy.

	NOTE: This is NOT the name the file is saved as on your disk. This program makes no changes to the names of files, it only alters information within files.

3. Date information:

	file upload date, transfer time, recording date, enrollment date, etc. replaced with 1000-01-01

	Several places throughout the ITS, information about dates that correspond closely to the date the recording was made can be found. Rationale for anonymizing this information is the same as for the filename.

4. Child ID:

	id replaced with A999

	Child ID is the ID given to the child by the lena system, and could be linked back to a participant name, depending on each lab's data storage and labeling policy.

5. Log file name:

	logfile replaced with exec10001010T100010Z_job00000001-10001010_101010_100100.upl.log

	The logfile name contains information about upload date, and the Child ID
	
There are some items that we decided to keep un-anonymous:

1. Time information:
	Specific time (hour:min:sec) information is necessary to keep to allow for time-of-day analyses.
2. Child key:
	The child key is a Lena-generated number that is specific to each individual recording, but can't be linked to other personal information about the participant.
3. Gender:
	Knowing the gender of the child without birthdate information does not reveal much about the participant, but could be useful in some analyses.
4. Recording device serial ID and version:
	Information about the recording device and software it is using are kept. In the unlikely event that a given set of recorders or software are faulty, data that were collected on those devices can be flagged and excluded if necessary.
5. Chronological age:
	This information is left as is to allow for age-effect analyses.
	Because chronological age is listed only in months, this is not sufficient detail to extract date of birth and therefore not of concern, even if recording date were to be found from other sources.
6. Group ID:
	Group ID allows researchers to organize their data into meaningful groups. Typically this would not be of concern for anonymization. However, it is possible that in some labs the group ID may be the SAME as the child ID. In such situations, labs should check whether their Child ID/Group ID contains any non-anonymized information before using this program in its current form.
7. Timezone:
	The recording's timezone, the short version of the timezone name, and whether or not daylight savings time is used is NOT anonymized, as this information may be needed for data analyses.

## Contact

If you have questions about how to use the anonymizer, bug fixes, or improvements, please contact Sarah at smacewan@mts.net
