
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')

import re
from flask import Flask
from flask import render_template
from flask import make_response
from flask import request
app = Flask(__name__)

df = pd.read_csv('gun-violence-data.csv', index_col=0, encoding='latin-1')


@app.route("/")
def hello():
    # return str(df.head(20)['name'])
    return render_template('index.html', taco = 'dog') # Note: must import this

# Get data for a specific month, sliced by state:
@app.route('/month')
def month():
    choice = request.args.get('mo')
    spec = df[df['date'].str.match('.*' + '-' + choice + '-' + '.*')]
    states = spec.groupby('state')['n_killed'].sum()
    return states.to_json(orient='split')

# Get data for a specific state, sliced by month:
@app.route('/state')
def state():
    choice = request.args.get('st')
    spec = df[df['state'] == choice]
    months = spec.groupby('month')['n_killed'].sum()
    return months.to_json(orient='split')

# Get total deaths sliced by month, across all states (No client-side sister route yet):
@app.route('/totalByMonth')
def avg():
    res = []
    for i in range(1, 13):
        # res.append('{:02}'.format(i)) # Perfect, just what we want
        month = '{:02}'.format(i)
        month_total = df[df['date'].str.match('.*-' + month + '-.*')]['n_injured'].sum() # Can do n_killed as well
        res.append(month_total)
    return str(res)

# Determine whether a given month for a state is above or below average, for that state's yearly killings (No client-side sister route yet):
@app.route('/relativeToAvg')
def rel():
    choice = request.args.get('st')
    res = []
    # First get the total killings in that state, then divide by 12 to get average per month:
    total = df[df['state'] == choice]['n_killed'].sum()
    avg = total / 12

    # Then go through each month, sum up its killings, and find difference from average or expected value:
    for i in range(1, 13):
        month = '{:02}'.format(i)
        month_total = df[(df['date'].str.match('.*-' + month + '-.*')) & (df['state'] == choice)]['n_killed'].sum()
        res.append(month_total / avg)
    return str(res)

# Sample URL: http://localhost:5000/byDistrict?dist=senate&type=count
@app.route('/byDistrict')
def dist():
    choice = request.args.get('dist')
    choice2 = request.args.get('type')
    if (choice == 'house'):
        gb = 'state_house_district'
    elif (choice == 'senate'):
        gb = 'state_senate_district'
    elif (choice == 'congress'):
        gb = 'congressional_district'

    if choice2 == 'sum':
        totals = df.groupby(gb)['n_killed'].sum() # Could also count number of incidents. Do number dead/incident.
    elif choice2 == 'count':
        totals = df.groupby(gb)['date'].count()

    return totals.to_json(orient='split')












# How would we get the average number of deaths in each state, sliced by month?s





names = df.groupby('state')['state'] # Not quite working as intended
states = df.groupby('state')['n_killed'].sum() # Can also do .mean()

# Add a month/year column to track against that


# AHA! We don't need to make a new column -- we just need to add the 'str' bit here!:
spec = df[df['date'].str.match('.*' + '-03-' + '.*')]
#
states = spec.groupby('state')['n_killed'].sum()



# Phew, fortunately this isn't necessary: --- Or hmmm... will it be necessary if we want to GROUPBY month?
# This takes a really long time -- maybe use a generator??:
def addMonths():
    spans = []
    for r in df.iterrows():
        # Important: this is how you grab info when iterrating through rows:
        month = r[1].date[5:7]
        spans.append(month)
    return spans

# df['month'] = pd.Series(addMonths(), index=df.index)
#
# spec = df[df['month'] == '01']
# states = spec.groupby('state')['n_killed'].sum()
#
# for s in states:
#     print(s)



# states.plot(kind="barh", colormap="winter")
# plt.show() # ahhhhh the old plt.show()



if __name__ == "__main__":
    app.run()


# ayy
