import pandas as pd 
import streamlit as st 
import numpy as np 
import json 
import plotly.express as px 

def ingress(df):
    # TODO write docstring 
    # TODO convert the birthday column to datetimes 
    # take birthday column from todays datetime to get age
    # convert/round the age to a whole number of years
    df['SEX'] = df['SEX'].map(
        {1:'Male',
         2:'Female'}
    )
    df['DOB'] = pd.to_datetime(df['DOB'], format="%d/%m/%Y", errors='coerce')
    df['AGE'] = pd.to_datetime('today').normalize() - df['DOB']
    df['AGE'] = (df['AGE'] / np.timedelta64(1, 'Y')).astype('int')
    return df

def gender_count(df):
    # TODO doctring
    # TODO write test
    male = len(df[df['SEX'] == 'Male'])
    female = len(df[df['SEX'] == 'Female'])

    return male, female 

def child_count(df):
    # TODO doctring
    # TODO write test
    return len(df['CHILD'].unique())

st.title('903 Header analysis app')

upload = st.file_uploader("Upload 903 Header file")

if upload:
    df = pd.read_csv(upload)

    with st.sidebar:
        ethncities = st.sidebar.multiselect(
            'Select ethnicties for analysis',
            df['ETHNIC'].unique(),
            df['ETHNIC'].unique()
        )

    df = df[df['ETHNIC'].isin(ethncities)]

    df = ingress(df)
    child_pop = child_count(df)
    male, female = gender_count(df)
    average_age = round(df['AGE'].mean())

    st.write(f'The total population of children is: {child_pop}.')
    st.write(f'The total number of males is: {male}')
    st.write(f'The total number of females is: {female}')
    st.write(f'The average age is: {average_age}')

    gender_bar = px.bar(df, 
                        x='SEX',
                        title='Number of children of each sex in 903 data',
                        labels={'SEX':'Sex',
                                'count':'Number of children'})
    st.plotly_chart(gender_bar)

    ethnic_bar = px.bar(df, 
                        x='ETHNIC',
                        title='Number of children of each ethncity in 903 data',
                        labels={'ETHNIC':'Ethnicity',
                                'count':'Number of children'})
    st.plotly_chart(ethnic_bar)
    
    age_hist = px.histogram(df['AGE'],
                        title='Spread of ages of children in 903 data',
                        labels={'value':'Age',
                                'count':'Number of children'})
    st.plotly_chart(age_hist)

    st.dataframe(df)
    

