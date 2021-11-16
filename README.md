# Exploring Portfolio Decarbonization using AI
NUS BT4103 Capstone Project AY21/22 Sem 1

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
