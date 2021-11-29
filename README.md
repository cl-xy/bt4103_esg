# Exploring Portfolio Decarbonization using AI
NUS BT4103 Capstone Project AY21/22 Sem 1

We wish to express our sincerest appreciation and gratitude to Professor Lee Boon Kee and Mr Puneet
Gupta from NatWest Markets who have made all this possible. Thank you for being ever so patient with us and our problems and for guiding us through accomplishing the project objectives.

## Background
Climate change is one of the major threat to the world. Regulators across the world are taking active steps to promote green & sustainable finance to address climate risk. A number of Fortune 500 companies have made commitments to reduce carbon. Various asset managers are working out their strategic approaches to decarbonise their investment
portfolios.

This project explores how different Real money clients, Pension funds, Asset managers have set out decarbonisation targets and are making progress against their targets within their portfolios. 

## Approach
With sustainability, ESG and TCFD reports from over 115 financial institutions (Asian Banks, Asset Managers, Insurance, Pension Funds), a multi-pronged approach was devised to understand companies' commitment and stance towards portfolio decarbonization. 

Using topic modelling, we extracted topics from the reports and their corresponding keywords. Subsequently, each sentence was allocated a dominant topic and categorised into decarbonization related vs decarbonization unrelated. For each company, the percentage of decarbonization disclosure was calculated based on the number of decarbonization related sentences.

Using sentiment analysis, companies' sentiments towards portfolio decarbonization was scaled on a range of 0 to 1, with 1 indicating high commitment towards portfolio decarbonization. 

Using bigram analysis, the top 10 bigrams' associated with each company was identified and displayed on the dashboard. Bigrams was chosen as the metric as many esg keywords comes in the form of bigrams eg. green finance. 

## Technology Stack

### Programming Languages
Python

| Architecture | Technology Used |
| -------------| --------------- |
| Repository   | GitHub          |
| Backend      | Python          |
| External Database | NA         |
| Development & Deployment | Python |
| Frontend Visualization | Python|
| Dashboard deployment | Heroku  |

## Getting Started

This project runs on Python. Users will have to create a conda environment first. 

```
conda env create -f environment.yml
```

## Sample Dashboard
A dashboard was built using Python Dash to monitor companies' efforts and targets in portfolio decarbonization. 

There are 2 main tabs:
1. Individual Company
2. Company Comparison

In the **Individual Company** tab, users can view metrics related to each company's decarbonization efforts. 

![alt text](https://github.com/cl-xy/bt4103_esg/blob/main/documentations/dashboard_1.PNG)

In the **Company Comparison** tab, users can compare metrics between 2 companies and determine which company performs better. 

![alt text](https://github.com/cl-xy/bt4103_esg/blob/main/documentations/dashboard_2.PNG)


## Files

### .ipynb_checkpoints
Ignore this folder

### .vscode
Ignore this folder

### data
Contains sustainability reports in .pdf format and company labels data for dashboard. 

### documentations
Contains final presentation, final report and project documentation

### guides
Contains guides to install the mallet package on Windows environment and deploy dashboard to Heroku

### model/ldamallet
Contains a saved LDAMallet model with files: corpus.txt, id2word.dict

The same model can be loaded into the notebook when running the code. 

### results
Contains data obtained from data analysis and to be fed into the dashbord. 

### .DS_Store
Ignore this file

### WIN_BT4103_Decarbonization.ipynb
Compiled notebook containing codes for sentiment analysis, topic modelling and bigram analysis

### dashboard.py
Python code to build the dashboard

### environment.yml
To create the conda environment to run the codes
