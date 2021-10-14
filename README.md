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
- [System requirements, Technologies&Tools <a name="System_requirements"></a>](#System-requirements-)
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

# System requirements, Technologies&Tools <a name="System_requirements"></a>
- **Development Environment**: 
  - **Windows 10** <br/>
    Download location: https://www.microsoft.com/en-au/software-download/windows10<br/>
    
  - **Python v3.8.4**<br/>
    Download location: https://www.python.org/downloads/<br/>
    Guide documentation: https://docs.python.org/3/<br/>
    
- **Development IDE**:
  - **PyCharm v2021.2.2**<br/>
    Download location: https://www.jetbrains.com/pycharm/download/#section=windows<br/>
    Guide documentation: https://www.jetbrains.com/pycharm/learn/<br/>
    
- **Database**:
   - **MySQL v8.0.26**<br/>
     Download location: https://dev.mysql.com/downloads/mysql/<br/>
     Guide documentation: https://dev.mysql.com/doc/refman/8.0/en/<br/>
     
- **Packages**:
   - **pandas v1.3.1**<br/>
     Pandas is a powerful toolset for analyzing structured data. It is used for data analysis and data cleaning. It is based on Numpy (providing high-performance matrix operations).<br/>
     Guide documentation: https://pandas.pydata.org/pandas-docs/stable/index.html<br/>
     
   - **numpy v1.21.1**<br/>
     Guide documentation: https://numpy.org/doc/<br/>
     
   - **matplotlib v3.4.3**<br/>
     Matplotlib is a Python 2D plotting library, used to generate plots, histograms, power spectra, bar graphs, error graphs, scatter plots, etc.<br/>
     Guide documentation: https://matplotlib.org/stable/api/pyplot_summary.html<br/>
     
   - **csv v1.0**<br/>
     Guide documentation: https://docs.python.org/3/library/csv.html<br/>

   - **fpdf v1.7.2**<br/>
     Used to generate pdf.<br/>
     Guide documentation: GitHub - reingart/pyfpdf: Simple PDF generation for Python (FPDF PHP port)<br/>

   - **pymysql v1.0.2**<br/>
     Used to connect MySQL.<br/>
     Guide documentation: https://pymysql.readthedocs.io/en/latest/<br/>

   - **wx v4.1.1**<br/>
     Used for Python GUI. <br/>
     Guide documentation: https://wxpython.org/Phoenix/docs/html/<br/>

   - **plotly v5.3.1**<br/>
     Used for graph plot.<br/>
     Guide documentation: https://plotly.com/python/<br/>

   - **kaleido v1.0.48**<br/>
     Guide documentation: https://pypi.org/project/kaleido/<br/>
     
   | **Package**          | **cmd Window Download**              |
   |:--------------------:|:------------------------------------:|
   |pandas v1.3.1         |*pip install pandas*                  |
   |numpy v1.21.1         |*pip install numpy*                   |
   |matplotlib v3.4.3     |*pip install matplotlib*              |
   |fpdf v1.7.2           |*pip install fpdf*                    |
   |pymysql v1.0.2        |*pip install PyMySQL*                 |
   |wx v4.1.1             |*pip install -U wxPython*             |
   |plotly v5.3.1         |*pip install plotly*                  |
   |kaleido v1.0.48       |*pip install -U kaleido*              |
           
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
