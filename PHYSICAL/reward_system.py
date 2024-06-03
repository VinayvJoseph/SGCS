# Script to generate rankings for sensor data in the firebase real-time databse.

import firebase_admin
from firebase_admin import credentials, db
import json
import pandas as pd

# Configurable parameters
start_date = '2023-08-01'
end_date = '2023-08-07'

# Initialisation 
flag = 0
rank_house = {} # Dictionary
rank_neighbourhood = {}
neighbourhood_weight = 0

# Initialize Firebase Admin SDK with your downloaded credentials
cred = credentials.Certificate('/home/digitaltwin/SGCS/firebase_credentials.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sgcs-1f60d-default-rtdb.firebaseio.com/'
})

# Reference to the Firebase Realtime Database
ref = db.reference('/')

# Computes the total waste for a House for all waste types.
def compute_weight(path):
    global rank_house, neighbourhood_weight;
    data = ref.child(path).get()

    # Convert data to a dataframe
    df = pd.DataFrame.from_dict(data, orient='index')
    print(df)

    # Determine start and end index
    flag = 0
    for i in range(len(df)):
        ele = df['Timestamp'].iloc[i][0:10]
        if flag ==0 and start_date == ele:
            start_index = i
            flag = 1

        if flag == 1 and end_date == df['Timestamp'].iloc[i][0:10]:
            end_index = i;

    print('Start index :', start_index)
    print('End index :', end_index)

    # Calculating aggregate weight over a time period
    organic_weight = 0; pmd_weight = 0; paper_weight = 0; total_weight = 0
    start_organic = df['Weight Organic'].iloc[start_index]
    start_pmd = df['Weight PMD'].iloc[start_index]
    start_paper = df['Weight Paper'].iloc[start_index]
    end_organic=0; end_pmd=0; end_paper=0;

    for i in range(start_index, end_index):
        value_organic = df['Weight Organic'].iloc[i]
        value_pmd = df['Weight PMD'].iloc[i]
        value_paper = df['Weight Paper'].iloc[i]

        if value_organic != 0:
            end_organic = value_organic
        else:
            organic_weight = organic_weight + (end_organic - start_organic)
            start_organic = 0

        if value_pmd != 0:
            end_pmd = value_pmd
        else:
            pmd_weight = pmd_weight + (end_pmd - start_pmd)
            start_pmd = 0

        if value_paper != 0:
            end_paper = value_paper
        else:
            paper_weight = paper_weight + (end_paper - start_paper)
            start_paper = 0

    if organic_weight == 0:
        organic_weight = end_organic - start_organic

    if pmd_weight == 0:
        pmd_weight = end_pmd - start_pmd

    if paper_weight == 0:
        paper_weight = end_paper - start_paper

    total_weight = organic_weight + pmd_weight + paper_weight
    neighbourhood_weight = neighbourhood_weight + total_weight

    print((organic_weight/1000), "kgs of Organic waste")
    print((pmd_weight/1000), "kgs of PMD waste")
    print((paper_weight/1000), "kgs of Paper waste")
    print((total_weight/1000), "kgs of Total waste")

    # Updating real-time database with results.
    path = path[5:]
    path_r = 'Result/' + path
    rank_house[path_r] = total_weight
    print(path_r)

    # Reference to the databse on the required node.
    ref_r = db.reference(path_r)

    ref_r.child('Organic').set(str(organic_weight))
    ref_r.child('PMD').set(str(pmd_weight))
    ref_r.child('Paper').set(str(paper_weight))
    ref_r.child('Total').set(str(total_weight))

# Main program

# Get a reference to the database
ref_n = db.reference('Data')
neighbourhoods = ref_n.get() # Retrieve all child nodes

# Loop through all neighbourhoods
for parent in neighbourhoods:
    path_n = 'Data/' + parent
    ref_h = db.reference(path_n)# Get a reference to houses under a neighbourhood
    houses = ref_h.get()
    print("Computing for ",parent)

    # Loop through all houses in a neighbourhood
    for child in houses:
        path_h = path_n + '/' + child
        compute_weight(path_h)

    # Update rank for each house in the real-time database.
    sorted_dict = dict(sorted(rank_house.items(), key=lambda item: item[1]))
    count = 1
    for key in sorted_dict.keys():
        ref_r = db.reference(key)
        ref_r.child('Rank').set(str(count))
        count = count+1

    rank_house = {}
    path_result = 'Result/' + parent
    rank_neighbourhood[path_result] = neighbourhood_weight
    neighbourhood_weight = 0

# Update rank for each neighbourhood in the real-time database.
sorted_dict = dict(sorted(rank_neighbourhood.items(), key=lambda item: item[1]))
count = 1
for key in sorted_dict.keys():
    ref_r = db.reference(key)
    ref_r.child('Rank').set(str(count))
    ref_r.child('Total').set(str(sorted_dict[key]))
    count = count+1


