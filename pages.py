import streamlit as st

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

import pickle

from util import apply_filter1, apply_filter2

def header(text):
    st.markdown(f'<p style="background-color:#0066cc;color:#33ff33;font-size:24px;border-radius:2%;">{text}</p>', unsafe_allow_html=True)


class Page:

    def __init__(self,content):

        self.content = content
    

    def render_frame(self,lang):

        translation = self.content[lang]

        st.markdown("<h1 style='text-align: center;'>" + translation["title"] + "</h1>", unsafe_allow_html=True)
        st.sidebar.markdown(translation["sidebar-title"])
        st.write("-"*50)


        self.render_content(translation,lang)

    def render_content(self,translation,lang):

        pass





class Home(Page):

    def __init__(self,content):
        super().__init__(content["homepage"]) 


class Dataset(Page):

    def __init__(self,content):
        super().__init__(content["dataset"]) 








class Caption(Page):

    def __init__(self,content):
        super().__init__(content["caption"]) 

        self.df = pd.read_csv("appdata/cap.csv")

        self.fig = px.scatter(self.df.rename(columns=str.title),x="Dim 1",y="Dim 2", custom_data=["Subject","Title","Upvotes"],color="Subject", labels={'color': 'Subject'})
        self.fig.update_traces(hovertemplate="<br>".join(["Subject: %{customdata[0]}","Title: %{customdata[1]}","Upvotes %{customdata[2]}"]))
        self.fig.update_layout(title_text='Subject Embeddings', title_x=0.5)    


    def render_content(self,translation,lang):

        st1,st2 = st.columns(2)

        st2.markdown(f"""
        ### {translation["section1-title"]}
        
        {translation["section1-text"]}

        """)

        index1 = list(translation["sidebar-filter1-options"].keys()).index(st.session_state["filter1"])
        index2 = list(translation["sidebar-filter2-options"].keys()).index(st.session_state["filter2"])
        
        st.session_state["filter1"] = st.sidebar.selectbox(translation["sidebar-filter1-text"], translation["sidebar-filter1-options"].keys(), format_func=lambda x:translation["sidebar-filter1-options"][x],on_change=apply_filter1,key="new_filter1",index=index1) 
        st.session_state["filter2"] = st.sidebar.selectbox(translation["sidebar-filter2-text"], translation["sidebar-filter2-options"].keys(), format_func=lambda x:translation["sidebar-filter2-options"][x],on_change=apply_filter1,key="new_filter1",index=index2)
        # st.write(index1)

        st1.image(f'appdata/captionlength_count_{lang.lower()}_{st.session_state["filter1"]}.png')
        st1.image(f'appdata/captionlength_target_{lang.lower()}_{st.session_state["filter1"]}.png')

        st.write("-"*50)
        st1,st2 = st.columns(2)

        st1.markdown(f"""
        ### {translation["section2-title"]}

        {translation["section2-text"]}

        """)

        st2.image(f'appdata/captionsubject_count_{lang.lower()}_{st.session_state["filter1"]}.png')
        st2.image(f'appdata/captionsubject_target_{lang.lower()}_{st.session_state["filter1"]}.png')


        st.write("-"*50)
        st1,st2 = st.columns(2)

        st1.markdown(f"""
        ### {translation["section3-title"]}
        """)

        st1.image(f'appdata/wordcloud_{st.session_state["filter1"]}_{st.session_state["filter2"].replace("/","-")}.png')

        st2.markdown(f"""
        ### {translation["sidebar-filter2-options"][st.session_state["filter2"]]}
        
        **{translation["section3-text1"]}:** {translation[f'section3-description-{st.session_state["filter2"]}']}

        #### {translation["section3-text2"]}

        """)
        if st.sidebar.button(translation["sidebar-filter3-text"]):
            
            if st.session_state["filter1"]=="all":
                for i,s in enumerate(self.df.loc[(self.df.subject==st.session_state["filter2"]),"title"].sample(5).tolist()):
                        st2.markdown(f'**{i+1}:** {s}')
            else:
                for i,s in enumerate(self.df.loc[(self.df.subject==st.session_state["filter2"])&(self.df.category==st.session_state["filter1"]),"title"].sample(5).tolist()):
                        st2.markdown(f'**{i+1}:** {s}')

        else:

            if st.session_state["filter1"]=="all":
                for i,s in enumerate(self.df.loc[(self.df.subject==st.session_state["filter2"]),"title"].sample(5).tolist()):
                        st2.markdown(f'**{i+1}:** {s}')
            else:
                for i,s in enumerate(self.df.loc[(self.df.subject==st.session_state["filter2"])&(self.df.category==st.session_state["filter1"]),"title"].sample(5).tolist()):
                        st2.markdown(f'**{i+1}:** {s}')


        st.write("-"*50)
        st1,st2 = st.columns([1,3])

        st1.markdown(f"""
        ### {translation["section4-title"]}

        {translation["section4-text"]}

        """)


        st2.plotly_chart(self.fig,use_container_width=True)

