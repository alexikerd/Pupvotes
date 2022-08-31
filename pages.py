import streamlit as st

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

import pickle

from sentence_transformers import SentenceTransformer

def header(text):
    st.markdown(f'<p style="background-color:#0066cc;color:#33ff33;font-size:24px;border-radius:2%;">{text}</p>', unsafe_allow_html=True)


class Page:

    def __init__(self,translation):

        self.translation = translation
    

    def render_frame(self):

        st.markdown("<h1 style='text-align: center;'>" + self.translation["title"] + "</h1>", unsafe_allow_html=True)
        st.sidebar.markdown(self.translation["sidebar-title"])
        st.write("-"*50)


        self.render_content()

    def render_content(self):

        pass





class Home(Page):

    def __init__(self,content,language):
        self.lang = language
        super().__init__(content[self.lang]["homepage"]) 


class Dataset(Page):

    def __init__(self,content,language):
        self.lang = language
        super().__init__(content[self.lang]["dataset"]) 








class Caption(Page):

    def __init__(self,content,language):
        self.lang = language
        super().__init__(content[self.lang]["caption"]) 

        self.df = pd.read_csv("data.csv",parse_dates=["posted","scraped"])
        self.df["weekday"] = self.df.posted.dt.day_name()

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
            ,"greeting":["good morning","good evening","good night","Good murrrrning"]+[f'happy {wk.lower()}' for wk in self.df.weekday.unique()]
            ,"cute":["baby","babies","goodest","adorable","beautiful","cutie","cute","handsome"]
           }

        def label(x):
    
            for subject,keywords in subjects.items():
                
                for kw in keywords:
                    if kw in x.lower():
                        return subject
                    
            return "other"

        self.df["subject"] = self.df.title.apply(label)
        self.embeddor = SentenceTransformer('all-MiniLM-L6-v2')
        
        with open("models/sentemb.pkl","rb") as f:
            self.model = pickle.load(f)


    def render_content(self):

        st1,st2 = st.columns(2)

        st2.markdown(f"""
        ### {self.translation["section1-title"]}
        
        {self.translation["section1-text"]}

        """)
        
        cat_filter = st.sidebar.selectbox(self.translation["sidebar-filter1-text"], self.translation["sidebar-filter1-options"].keys(), format_func=lambda x:self.translation["sidebar-filter1-options"][x]) 
        sub_filter = st.sidebar.selectbox(self.translation["sidebar-filter2-text"], self.translation["sidebar-filter2-options"].keys(), format_func=lambda x:self.translation["sidebar-filter2-options"][x])


        st1.image(f'appdata/captionlength_count_{self.lang.lower()}_{cat_filter}.png')
        st1.image(f'appdata/captionlength_target_{self.lang.lower()}_{cat_filter}.png')

        st.write("-"*50)
        st1,st2 = st.columns(2)

        st1.markdown(f"""
        ### {self.translation["section2-title"]}

        {self.translation["section2-text"]}

        """)

        st2.image(f'appdata/captionsubject_count_{self.lang.lower()}_{cat_filter}.png')
        st2.image(f'appdata/captionsubject_target_{self.lang.lower()}_{cat_filter}.png')


        st.write("-"*50)
        st1,st2 = st.columns(2)

        st1.markdown(f"""
        ### {self.translation["section3-title"]}
        """)

        st1.image(f'appdata/wordcloud_{cat_filter}_{sub_filter.replace("/","-")}.png')

        st2.markdown(f"""
        ### {self.translation["sidebar-filter2-options"][sub_filter]}
        
        **{self.translation["section3-text1"]}:** {self.translation[f'section3-description-{sub_filter}']}

        #### {self.translation["section3-text2"]}

        """)
        if st.sidebar.button(self.translation["sidebar-filter3-text"]):
            
            if cat_filter=="all":
                for i,s in enumerate(self.df.loc[(self.df.subject==sub_filter),"title"].sample(5).tolist()):
                        st2.markdown(f'**{i+1}:** {s}')
            else:
                for i,s in enumerate(self.df.loc[(self.df.subject==sub_filter)&(self.df.category==cat_filter),"title"].sample(5).tolist()):
                        st2.markdown(f'**{i+1}:** {s}')

        else:

            if cat_filter=="all":
                for i,s in enumerate(self.df.loc[(self.df.subject==sub_filter),"title"].sample(5).tolist()):
                        st2.markdown(f'**{i+1}:** {s}')
            else:
                for i,s in enumerate(self.df.loc[(self.df.subject==sub_filter)&(self.df.category==cat_filter),"title"].sample(5).tolist()):
                        st2.markdown(f'**{i+1}:** {s}')


        sampletext = st.sidebar.text_input(self.translation["sidebar-filter4-text"],"He is my snuggle partner")

        st.write("-"*50)

        st1,st2 = st.columns(2)

        st1.markdown(f"""
        ### {self.translation["section4-title"]}
        """)        



        st.write("-"*50)
        st1,st2 = st.columns(2)

        st2.markdown(f"""
        ### {self.translation["section5-title"]}

        {self.translation["section5-text"]}

        """)

        st1.dataframe(self.df.iloc[self.get_knn(sampletext)][["title"]].rename(columns={"title":"Captions"}))



    def get_knn(self,sentence):

        distances,indices = self.model.kneighbors(self.embeddor.encode([sentence]))

        return list(indices)[0]

