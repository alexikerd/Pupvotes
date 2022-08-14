import streamlit as st

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px




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

    def __init__(self,translation,language):
        self.lang = language
        super().__init__(translation[self.lang]["homepage"]) 


class Dataset(Page):

    def __init__(self,translation,language):
        self.lang = language
        super().__init__(translation[self.lang]["dataset"]) 








class Caption(Page):

    def __init__(self,translation,language):
        self.lang = language
        super().__init__(translation[self.lang]["caption"]) 

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

        self.dictionary = {"other":"altro"
        ,"greeting":"saluto"
        ,"sun":"sole"
        ,"sleep":"sonno"
        ,"snow":"neve"
        ,"death/injury":"morte/danno"
        ,"attributes":"caratteristiche"
        ,"new":"nuovo"
        ,"birthday":"compleanno"
        ,"walk":"passeggiata"
        ,"cute":"carino"
        ,"playful":"giocoso"
        ,"holiday":"vacanza"
        }

        self.df["soggetto"] = self.df.subject.apply(lambda x:self.dictionary[x])


    def render_content(self):

        
        st1,st2 = st.columns(2)

        st2.markdown(f"""
        ### {self.translation["section1-title"]}
        
        {self.translation["section1-text"]}

        """)
        
        cat_filter = st.sidebar.selectbox("Category", ["all","cats","dogs"], format_func=lambda x:x.title()) 


        if self.lang=="English":
            subject_filter = st.sidebar.selectbox("Subject",self.dictionary.keys(), format_func=lambda x:x.title())       
        else:
            subject_filter = st.sidebar.selectbox("Soggetto",self.dictionary.values(), format_func=lambda x:x.title()) 



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
        st2.markdown(f"""
        #### Description
        
        **{subject_filter.title()}:** Add description of subjects here

        """)
        if st.sidebar.button("Generate Sample"):
            
            if self.lang=="English":
                for i,s in enumerate(self.df.loc[self.df.subject==subject_filter,"title"].sample(5).tolist()):
                    st1.markdown(f'**{i+1}:** {s}')

            else:
                for i,s in enumerate(self.df.loc[self.df.soggetto==subject_filter,"title"].sample(5).tolist()):
                    st1.markdown(f'**{i+1}:** {s}')



        st.write("-"*50)
        st1,st2 = st.columns(2)

        st2.markdown(f"""
        ### {self.translation["section4-title"]}

        {self.translation["section4-text"]}

        """)

