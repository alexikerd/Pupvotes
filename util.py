import streamlit as st

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



def translate():

    if st.session_state.new_language:
        st.session_state["lang"] = st.session_state.new_language


def flip_page():

    if st.session_state.new_page:
        st.session_state["page"] = st.session_state.new_page



def apply_filter1():

    if st.session_state.new_filter1:
        st.session_state["filter1"] = st.session_state.new_filter1



def apply_filter2():

    if st.session_state.new_filter2:
        st.session_state["filter2"] = st.session_state.new_filter2

def apply_filter3a():

    if st.session_state.new_filter3a:
        st.session_state["filter3a"] = st.session_state.new_filter3a

def apply_filter3b():

    if st.session_state.new_filter3b:
        st.session_state["filter3b"] = st.session_state.new_filter3b



def label(x):

    subjects = {"holiday":["santa","xmas","christmas","holiday","valentine","halloween","easter","thanksgiving"]
            ,"death/injury":["rash","worried","cancer"," rip","broke her","broke his","hard time bending ","not feeling so good","not feeling well","the labs gone","splenectomy","post op","passed away","miss her","miss him","surgery","seizure","missing","hospital","hit by car","died"]
            ,"birthday":["birthday"]
            ,"sleep":["comfy","exhausted","tuckered","yawn","relax","cozy","cuddly","chill","dreaming","lazy","bed time","bedtime","slumber","lazing","blanket","snooze","sleepy","snug ","sleep","cuddlin","tired","snoozin","loungin","snuggle","cuddle","chillin","sweepy","leisure","nappin","nap ","nap,"]
            ,"new":["new add","rescued","newest","just adopted","welcome to the fam"]
            ,"sun":["sunny","beach","enjoying morning sun","soaking up the sun","enjoying the sun","sunshine","enjoying the shade","in the sun","sunbeam","sun beam"]
            ,"snow":["snow","winter","cold","-3"]
            ,"attributes":["tail","bean","paw","face","eyes","snoot"," ears"]
            ,"playful":["game of tag","zoomies","play","fetch","tug"]
            ,"walk":["walk","stroll","leash","hike"]
            ,"greeting":["good morning","good evening","good night","Good murrrrning"]+[f'happy {wk}' for wk in ['saturday', 'friday', 'thursday', 'wednesday', 'tuesday', 'monday', 'sunday']]
            ,"cute":["baby","babies","goodest","adorable","beautiful","cutie","cute","handsome"]
        }

    
    for subject,keywords in subjects.items():
        
        for kw in keywords:
            if kw in x.lower():
                return subject
            
    return "other"



def load_dataset():

    df = pd.read_csv("data.csv",parse_dates=["posted","scraped"])



    df["age"] = (df.scraped - df.posted).dt.total_seconds()//3600
    df["weekday"] = df.posted.dt.day_name()
    df["weekday_number"] = df.posted.dt.dayofweek
    df["hour"] = df.posted.dt.hour
    df["date"] = pd.to_datetime(df.posted.dt.date)
    df["year"] = df.posted.dt.year
    df["month"] = df.posted.dt.month
    df["yrmnth"] = (df.year-2021)*12 + df.month
    df["target"] = np.log(df.upvotes+1)


    df["fhost"] = df.url.apply(lambda x: "imgur" if "imgur" in x else "reddit")
    df["format"] = df.url.apply(lambda x: x.split(".")[-1])

    df["timestep"] = (df.posted - df.posted.min()).dt.days

    sub = pd.read_csv("subscribers.csv",parse_dates=["timestamp"])

    sub["date"] = sub.timestamp.dt.date

    sub = sub.pivot(index="date",columns=["subreddit"],values="subscribers")

    # Correcting any missing dates
    daterange = pd.date_range(start=df.date.min(),end=df.date.max(),freq="D")
    sub = sub.reindex(daterange)

    # Filling in the new NULL values
    sub.interpolate(method="linear",inplace=True)
    sub.bfill(inplace=True)


    # Adding the date back into the columns so we can melt the updated dataset
    sub["date"] = pd.to_datetime(sub.index)
    sub = pd.melt(sub,id_vars="date")


    # Joining the two dataframes together
    df = df.merge(sub.rename(columns={"value":"subscribers"}),how="left",on=["date","subreddit"])





    stage1 = df.groupby(["date","subreddit","category","hour"],as_index=False).agg({"upvotes":"count"}).rename(columns={"upvotes":"competition_subreddit"})
    stage2 = stage1.groupby(["date","hour","category"],as_index=False).agg({"competition_subreddit":"sum"}).rename(columns={"competition_subreddit":"competition_category"})
    stage3 = stage2.groupby(["date","hour"],as_index=False).agg({"competition_category":"sum"}).rename(columns={"competition_category":"competition_total"})



    df = df.merge(stage1,how="left",on=["date","hour","subreddit","category"]).merge(stage2,how="left",on=["date","hour","category"]).merge(stage3,how="left",on=["date","hour"])


    df["title_length"] = df.title.apply(lambda x: len(x.split(" ")))
    df["length"] = df.title_length.astype(str)
    for i in range(3):    
        df.loc[(df.title_length>=(5*i+15))&(df.title_length<(5*i+20)),"length"] = f'{5*i+15}-{5*i+19}'
    for i in range(4):
        df.loc[(df.title_length>=(10*i+30))&(df.title_length<(10*i+40)),"length"] = f'{10*i+30}-{10*i+39}'

    df["exclamation"] = df.title.str.contains("!")


    for kw in pd.read_csv("keywords.csv").keywords:
        
        df[f'keyword_{kw}'] = df.title.str.lower().str.contains(kw)



    df["subject"] = df.title.apply(label)
    df["subscriber_logged"] = np.log(df.subscribers)

    # df["target"] -= df.target.mean()
    # df["target"] /= df.target.std() 

    
    return df
