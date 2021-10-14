# Table of contents
- [Table of contents](#table-of-contents)
- [Project overview <a name="project_overview"></a>](#project-overview-)
  - [Context <a name="context"></a>](#context-)
  - [Aim of Project <a name="aim"></a>](#aim-of-project-)
- [Demo <a name="demo"></a>](#demo-)
- [Features <a name="features"></a>](#features-)
  - [Sprint 1 <a name="sprint1"></a>](#sprint-1-)
  - [Sprint 2 <a name="sprint2"></a>](#sprint-2-)
- [Documentation <a name="documentation"></a>](#documentation-)
  - [User story <a name="user_story"></a>](#user-story-)
  - [Architecture <a name="architecture"></a>](#architecture-)
  - [Test case <a name="test_case"></a>](#test-case-)
  - [Other documents <a name="other_documents"></a>](#other-documents-)
- [System requirements, Technologies&Tools <a name="System requirements, Technologies&Tools"></a>](#System requirements, Technologies&Tools-)
- [Installation guide <a name="installation_guide"></a>](#installation-guide-)
- [Operation guide <a name="operation_guide"></a>](#operation-guide-)
- [Change log <a name="change_log"></a>](#change-log-)
- [Traceability matrix <a name="traceability_matrix"></a>](#traceability-matrix-)
- [Contact information <a name="contact"></a>](#contact-information-)


# Project overview <a name="project_overview"></a>

## Context <a name="context"></a>
*Primary Standards Dosimetry Laboratory* (PSDL) - a department in *Australian Radiation Protection and Nuclear Safety Agency (ARPANSA)*, calibrates radiation measuring instruments (chambers) and provides a report to the client with a certificate stating the results of the calibration. 

However, this process is time-consuming nowadays, and with the increasing number of calibration services from various radiotherapy providers, the spreadsheets store and read data inefficiently and insecurely.

## Aim of Project <a name="aim"></a>
The goal of this project is to provide our client a solution that can replace the manual process of transferring data and the reply on Microsoft Excel spreadsheets, including storing the data centrally, performing the analysis and providing results such as graph automatically, and finally producing the report as desired PDF certificate.

# Demo <a name="demo"></a>
demo link

# Features <a name="features"></a>

## Sprint 1 <a name="sprint1"></a>
- Select set of files from local drive
- Read chamber and client information from local file
- Update client information from interface and change local file information
- Analysis the measurement and produce the graph and table

## Sprint 2 <a name="sprint2"></a>
- A new interface that can
  - Search data by job number (CAL), client name and chamber
  - Download selected files, which is the same as the original
- Generate job number (CAL), upload to database and write into local files
- Generate PDF Report
  - Preview of the report
  - Save the report to local drive

# Documentation <a name="documentation"></a>
docuemnt

## User story <a name="user_story"></a>
- 	I want to view the client's information (e.g Name, Address, Job number) and also relevant information about their dosimeter (e.g chambers ID, serial number, model)
- I want to have visualizations(e.g graph, table of analysis results)
- I want to select 1 or more pairs of data files(Client.csv, Lab.csv) 
- I want to upload and select a set of data files from a local drive and store them in a database (or a structure of the team's choice) 
- I want to change the number of runs
- I want to output 1 set of results (document) 
- I want to generate a PDF file with relevant information about the client and their dosimeter
- I want to be able to calculate the calibration coefficient after submitting the two raw data excel files (client.csv and lab.csv)
- I want to have an installation and operation manual
- I want to have tables and graphs after selecting which run(s) for the report 


## Architecture <a name="architecture"></a>
architecture

## Test case <a name="test_case"></a>
test

## Other documents <a name="other_documents"></a>
other

# System requirements, Technologies&Tools <a name="system_requirements"></a>
Development Environment: 
Windows 10 
          Download location: https://www.microsoft.com/en-au/software-download/windows10

Python v3.8.4
          Download location: https://www.python.org/downloads/

          Guide documentation: https://docs.python.org/3/

Development IDE:
PyCharm v2021.2.2
Download location: Download PyCharm: Python IDE for Professional Developers by JetBrains

Guide documentation: https://www.jetbrains.com/pycharm/learn/

Database:
MySQL v8.0.26
          Download location: https://dev.mysql.com/downloads/mysql/

          Guide documentation: MySQL :: MySQL 8.0 Reference Manual

Packages:
pandas v1.3.1
           Pandas is a powerful toolset for analyzing structured data. It is used for data analysis and data cleaning. It is based on Numpy (providing high-performance matrix operations).

           Installation tutorial: Enter the command "pip install pandas" in the cmd window, and click Enter. Wait for it to download and install.

           Guide documentation: pandas documentation — pandas 1.3.1 documentation (pydata.org)

numpy v1.21.1
           Guide documentation: NumPy Documentation

matplotlib v3.4.3
           Matplotlib is a Python 2D plotting library, used to generate plots, histograms, power spectra, bar graphs, error graphs, scatter plots, etc.

           Installation tutorial: Enter the command "pip install matplotlib" in the cmd window, and click Enter. Wait for it to download and install.

           Guide documentation: matplotlib.pyplot — Matplotlib 3.4.3 documentation

csv v1.0
 Guide documentation: https://docs.python.org/3/library/csv.html

fpdf v1.7.2
           Used to generate pdf.

           Installation tutorial: Enter the command "pip install fpdf" in the cmd window, and click Enter.

           Guide documentation: GitHub - reingart/pyfpdf: Simple PDF generation for Python (FPDF PHP port)

pymysql v1.0.2
           Used to connect MySQL.

           Installation tutorial: Enter the command "pip install pymysql" in the cmd window, and click Enter. Wait for it to download and install.

           Guide documentation: https://pymysql.readthedocs.io/en/latest/

wx v4.1.1
           Used for Python GUI. 

           Guide documentation: https://wxpython.org/Phoenix/docs/html/

plotly v5.3.1
           Installation tutorial: Enter the command "pip install plotly" in the cmd window, and click Enter. Wait for it to download and install.

           Guide documentation: https://plotly.com/python/

kaleido v1.0.48
           Installation tutorial: Enter the command "pip install kaleido" in the cmd window, and click Enter. Wait for it to download and install.

           Guide documentation: https://pypi.org/project/kaleido/

# Installation guide <a name="installation_guide"></a>
installation_guide

# Operation guide <a name="operation_guide"></a>
operation

# Change log <a name="change_log"></a>
change_log

# Traceability matrix <a name="traceability_matrix"></a>
traceability_matrix

# Contact information <a name="contact"></a>

901065 - Xudong Zhang [xudongz1@student.unimelb.edu.au](mailto:xudongZ1@student.unimelb.edu.au) Scrum Master

900636 - Hao Liu [l11@student.unimelb.edu.au](mailto:l11@student.unimelb.edu.au) Product Owner

1053501- Yushu Qiu [yushuq@student.unimelb.edu.au](mailto:yushuq@student.unimelb.edu.au) Development Environment Lead

1045673 - Junjie Xia [juxia@student.unimelb.edu.au](mailto:juxia@student.unimelb.edu.au) Architecture Lead

1061643 - Zeying Zhang [zeying@student.unimelb.edu.au](mailto:zeying@student.unimelb.edu.au) Deployment Lead
