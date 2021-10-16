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
    - [High-level Diagram](#high-level-diagram)
    - [Database Diagram](#database-diagram)
  - [Test case <a name="test_case"></a>](#test-case-)
  - [Product Backlog <a name="product_backlog"></a>](#product-backlog-)
  - [Other documents <a name="other_doc"></a>](#other-documents-)
- [System requirements, Technologies & Tools <a name="System_requirements"></a>](#system-requirements-technologies--tools-)
- [Installation guide <a name="installation_guide"></a>](#installation-guide-)
- [Operation guide <a name="operation_guide"></a>](#operation-guide-)
  - [Button Introduction](#button-introduction)
  - [Workflow under different use cases](#workflow-under-different-use-cases)
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


## User story <a name="user_story"></a>

![User Story](https://github.com/xudongguan202/COMP90082_DC_Bluering/blob/main/docs/user_story.pdf)

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

### High-level Diagram
![high-level-diagram](https://github.com/xudongguan202/COMP90082_DC_Bluering/blob/main/docs/high-level.png)

**Description**

- This application contains 4 Parts, which are Present Layer, Application Layer, Processing Layer and File System Layer.

- In Present Layer, it mainly focus on presenting the results to the user.

- In Application Layer, it is used for realising two main feature, which are Generate PDF and Analysis Data.

- In terms of Processing Layer, this layer contains some Python function to process the data.

- The File System Layer is used to store all the data that used in analysis, which can be used for refer in future.

### Database Diagram
![high-level-diagram](https://github.com/xudongguan202/COMP90082_DC_Bluering/blob/main/docs/database.png)


## Test case <a name="test_case"></a>
![Sprint 1 Test](tests/Sprint1_UTA.pdf)

![Sprint 2 Test](tests/Sprint2_UTA.pdf)

## Product Backlog <a name="product_backlog"></a>
![Sprint 1 Backlog](docs/Sprint1_Backlog.pdf)

![Sprint 2 Backlog](docs/Sprint2_Backlog.pdf)

## Other documents <a name="other_doc"></a>

Design Notebook

![Design Notebook](https://github.com/xudongguan202/COMP90082_DC_Bluering/blob/main/docs/Design_Notebook.pdf)

Motivational Model

![Motivational Model](https://github.com/xudongguan202/COMP90082_DC_Bluering/blob/main/docs/motivational.pdf)


# System requirements, Technologies & Tools <a name="System_requirements"></a>
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
     Guide documentation: https://github.com/reingart/pyfpdf<br/>

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

## Button Introduction

1. Main Frame

![Main frame](https://github.com/xudongguan202/COMP90082_DC_Bluering/blob/main/operation_guide/main.png?raw=true)

**1.1 Browse:** select file from local drive

**1.2 Check box:** check the box to use the files for analysis

**1.3 Confirm:** to check the file validation

**1.4 Compare:** start analysing and generate graph and table

**1.5 Read Information:** display information on the interface

**1.6 Update Information:** write the information filled in the interface to local files

**1.7 Upload Data:** upload all files to database

**1.8 Download Data:** jump to database page

**1.9 Generate PDF:** jump to report page

2. Database Frame

![Database frame](https://github.com/xudongguan202/COMP90082_DC_Bluering/blob/main/operation_guide/database.png?raw=true)

**2.1 Search:** search files in database by filled conditions (job id, client name, chamber)

**2.2 File:** left click to select a file, press Ctrl and left click to select multiple files

**2.3 Browse:** choose saving path

**2.4 Download CSV:** download selected files to the chosen path

3. PDF Frame

![PDF frame](https://github.com/xudongguan202/COMP90082_DC_Bluering/blob/main/operation_guide/pdf.png?raw=true)

**3.1 Save:** save the report to the local drive

## Workflow under different use cases

- To get analysis graph and table
  1. Choose data files by **1.1 Browse**
  2. Check the box (**1.2 Check box**) to select runs for analysis
  3. Check file validation by **1.3 Confirm**
  4. Start analysing by **1.4 Compare**
  5. A new window with result will pop-up
- To read or update information
  1. Choose data files by **1.1Browse**
  2. Check the box (**1.2 Check box**) to select runs for analysis
  3. Check file validation by **1.3 Confirm**
  4. Read information by **1.5 Read Information**
  5. Fill the information in the text box
  6. Write to the local file by **1.6 Update Information**
- To upload files
  1. Complete **read and update** steps above (files must be updated if the client information is missing)
  2. Upload to database by **1.7 Upload Data**
- To generate PDF report
  1. Complete **read and update** steps above (files must be updated if the client information is missing)
  2. A preview of the report will be opened in new window by pressing **1.9 Generate PDF**
  3. Save the report to local drive by **3.1 Save**
  4. Other operations can be done through the top bar
- To download files
  1. Go to database frame by **1.8 Download Data**
  2. Fill in search conditions (any number of conditions can be used for searching)
  3. Press 2.1 Search to search (support fuzzy search)
  4. Choose files in the **2.2 tree** structure by left click (press Ctrl to select multiple files)
  5. Choose saving path by **2.3 Browse**
  6. Download file by pressing **2.4 Download CSV**


# Change log <a name="change_log"></a>
In this section, the changes applied to our design and user story are discussed.

Sprint 1:

1. Mainframe GUI design: We use left to right operation sequence instead of up to down to make sure that it is easier for users to operate in a reasonable order
2. Add Confirm button: We integrate "check validation" functionality to a new button "Confirm" instead of part of "Compare", which makes it easier for users to check if they select the right file before all operations.
3. Text input for "operator": We add a new text input for "operator" as it is required in the client information section. (User Story 3)

Sprint 2:

1. Job ID: It is now read-only. Job ID will be automatically generated after uploading to the database and write into the local file no matter it exists or not. 
2. Validation check: "Operator" can be different in different runs of one measurement.
3. DCC with XML format is no longer one of the requirements. (User Story 10)

# Traceability matrix <a name="traceability_matrix"></a>
traceability_matrix

# Contact information <a name="contact"></a>

901065 - Xudong Zhang [xudongz1@student.unimelb.edu.au](mailto:xudongZ1@student.unimelb.edu.au) Scrum Master

900636 - Hao Liu [l11@student.unimelb.edu.au](mailto:l11@student.unimelb.edu.au) Product Owner

1053501- Yushu Qiu [yushuq@student.unimelb.edu.au](mailto:yushuq@student.unimelb.edu.au) Development Environment Lead

1045673 - Junjie Xia [juxia@student.unimelb.edu.au](mailto:juxia@student.unimelb.edu.au) Architecture Lead

1061643 - Zeying Zhang [zeying@student.unimelb.edu.au](mailto:zeying@student.unimelb.edu.au) Deployment Lead
