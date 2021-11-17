Step by Step guide to deploying dashboard on Heroku

# **Step 1: Create a new folder for your project**
mkdir bt4103_dashboard
<br>
cd bt4103_dashboard

<br>

# **Step 2: Initialize the folder with git and a virtualenv**

git init
<br>
virtualenv venv
<br>
source venv/Scripts/activate

virtualenv creates a fresh Python instance. You will need to reinstall your app's dependencies with this virtualenv:

pip install dash
<br>
pip install plotly
<br>
pip install numpy
<br>
pip install pandas
<br>
pip install dash_bootstrap_components

You will also need a new dependency, gunicorn, for deploying the app:

pip install gunicorn

<br>

# **Step 3: Initialize the folder with the app, a .gitignore file, requirements.txt, and a Procfile for deployment**

_add in the dashboard.py file_

## Step 3.1. Add the .gitignore file
This should go inside the .gitignore file
<br>
venv
<br>
*.pyc
<br>
.DS_Store
<br>
.env

## Step 3.2. Add the Procfile file
This should go inside the Procfile file

web: gunicorn dashboard:server

## Step 3.3. Create the requirements.txt file

requirements.txt describes your Python dependencies. You can fill this file in automatically with:

pip freeze > requirements.txt

<br>

# Step 4: Copy data files into this repository
Files read as input for the dashboard

## Step 4.1. Create sub-folders
mkdir data

mkdir results

<br>
Check that sub-folders are created successfully:

1. Go to the data directory: <i>cd data</i>
2. Go to the results directory: <i>cd ../results </i>
3. Go back to the root directory: <i>cd ..</i>

## Step 4.2. Copy .csv files into the sub-folders

'data' folder should contain:

1. companylabels.csv
2. esg_initiatives.csv

'results' folder should contain:

1. all_initiatives.csv
2. all_percent.csv
3. sentiment_score.csv
4. bigram_df.csv

# **Step 5: Initialize Heroku, add files to Git, and deploy**

heroku create <your_webapp_name>
<br>
(eg.heroku create bt4103-esg-dashboard)
<br>
git add . # add all files to git
<br>
git commit -m 'Initial app boilerplate'
<br>
git push heroku master # deploy code to heroku
<br>
heroku ps:scale web=1  # run the app with a 1 heroku "dyno"

You should be able to view your app at https://bt4103-esg-dashboard.herokuapp.com/

<br>

# **Step 6: Update the code and redeploy**

When you modify dashboard.py with your own code, you will need to add the changes to git and push those changes to heroku.

git status # view the changes
<br>
git add .  # add all the changes
<br>
git commit -m 'a description of the changes'
<br>
git push heroku master



### _Reference: https://dash.plotly.com/deployment_
