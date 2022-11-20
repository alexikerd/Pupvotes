import streamlit as st

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

import pickle

from util import apply_filter1, apply_filter2, apply_filter3a, apply_filter3b

def header(text):
    st.markdown(f'<p style="background-color:#0066cc;color:#33ff33;font-size:24px;border-radius:2%;">{text}</p>', unsafe_allow_html=True)


class Page:

    def __init__(self,content):

        self.content = content
    

    def render_frame(self,lang):

        translation = self.content[lang]

        st.markdown("<h1 style='text-align: center;'>" + translation["title"] + "</h1>", unsafe_allow_html=True)
        st.write("-"*50)

        if "sidebar-title" in translation:
            st.sidebar.markdown(translation["sidebar-title"])


        self.render_content(translation,lang)

    def render_content(self,translation,lang):

        pass





class Home(Page):

    def __init__(self,content):
        super().__init__(content["homepage"]) 


    def render_frame(self,lang):

        translation = self.content[lang]

        st.markdown("<h1 style='text-align: center;'>" + translation["title"] + "</h1>", unsafe_allow_html=True)
        st.markdown("<small><h1 style='text-align: center;'>" + "Robert Ikerd" + "</h1><small>", unsafe_allow_html=True)
        st.write("-"*50)





class Dataset(Page):

    def __init__(self,content):
        super().__init__(content["dataset"]) 


    def render_content(self,translation,lang):



        st1,st2 = st.columns(2)
        st1.markdown(f"""
        ### {translation["section1-title"]}
        
        {translation["section1-text"]}
        """)

        st2.image("appdata/dogpictures.png")
        st2.image("appdata/catpictures.png")


        st.write("-"*50)
        st1,st2 = st.columns(2)

        for _ in range(3):
            st1.write("")

        st1.image("appdata/pawpularity.png")

        st2.markdown(f"""
        ### {translation["section2-title"]}
        
        {translation["section2-text"]}
        
        """)       



        st.write("-"*50)
        st1,st2 = st.columns(2)


        st2.image(f'appdata/target_hist_{lang.lower()}.png')
        st2.image(f'appdata/target_hist_logged_{lang.lower()}.png')
        st1.markdown(f"""
        ### {translation["section3-title"]}
        
        {translation["section3-text"]}
        
        """)



        st.write("-"*50)






class TimeSeries(Page):

    def __init__(self,content):
        super().__init__(content["timeseries"]) 


    def render_content(self,translation,lang):



        index1 = list(translation["sidebar-filter1-options"].keys()).index(st.session_state["filter1"])
        st.session_state["filter1"] = st.sidebar.selectbox(translation["sidebar-filter1-text"], translation["sidebar-filter1-options"].keys(), format_func=lambda x:translation["sidebar-filter1-options"][x],on_change=apply_filter1,key="new_filter1",index=index1) 



        st1,st2 = st.columns(2)


        st1.image(f'appdata/posts_over_time_{st.session_state["filter1"]}.png')
        st1.image(f'appdata/popularity_over_time_{st.session_state["filter1"]}.png')


        st2.markdown(f"""
        ### {translation["section1-title"]}
        
        {translation["section1-text"]}
        """)



        st.write("-"*50)
        st1,st2 = st.columns(2)

        st1.markdown(f"""
        ### {translation["section2-title"]}
        
        {translation["section2-text"]}
        """)

        st2.image(f'appdata/posts_hourly_{st.session_state["filter1"]}.png')
        st2.image(f'appdata/popularity_hourly_{st.session_state["filter1"]}.png')


 
        st.write("-"*50)
        st1,st2 = st.columns(2)


        st1.image(f'appdata/competition_{st.session_state["filter1"]}.png')

        st2.markdown(f"""
        ### {translation["section3-title"]}
        
        {translation["section3-text"]}
        """)




        st.write("-"*50)







class Caption(Page):

    def __init__(self,content):
        super().__init__(content["caption"]) 

        self.df = pd.read_csv("appdata/cap.csv")

        # self.fig = px.scatter(self.df.rename(columns=str.title),x="Dim 1",y="Dim 2", custom_data=["Subject","Title","Upvotes"],color="Subject", labels={'color': 'Subject'})
        # self.fig.update_traces(hovertemplate="<br>".join(["Subject: %{customdata[0]}","Title: %{customdata[1]}","Upvotes %{customdata[2]}"]))
        


    def render_content(self,translation,lang):

        st1,st2 = st.columns(2)

        st2.markdown(f"""
        ### {translation["section1-title"]}
        
        {translation["section1-text"]}

        """)

        index1 = list(translation["sidebar-filter1-options"].keys()).index(st.session_state["filter1"])
        index2 = list(translation["sidebar-filter2-options"].keys()).index(st.session_state["filter2"])
        
        st.session_state["filter1"] = st.sidebar.selectbox(translation["sidebar-filter1-text"], translation["sidebar-filter1-options"].keys(), format_func=lambda x:translation["sidebar-filter1-options"][x],on_change=apply_filter1,key="new_filter1",index=index1) 
        st.session_state["filter2"] = st.sidebar.selectbox(translation["sidebar-filter2-text"], translation["sidebar-filter2-options"].keys(), format_func=lambda x:translation["sidebar-filter2-options"][x],on_change=apply_filter2,key="new_filter2",index=index2)


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
        # st1,st2 = st.columns([1,3])

        # st1.markdown(f"""
        # ### {translation["section4-title"]}

        # {translation["section4-text"]}

        # """)

        # self.fig.update_layout(title_text=translation["section4-plot-title"], title_x=0.5)

        # st2.plotly_chart(self.fig,use_container_width=True)




class Subreddit(Page):

    def __init__(self,content):
        super().__init__(content["subreddit"]) 

        self.df = pd.read_csv("appdata/sub.csv")


    def render_content(self,translation,lang):


        index1 = list(translation["sidebar-filter1-options"].keys()).index(st.session_state["filter1"])        
        st.session_state["filter1"] = st.sidebar.selectbox(translation["sidebar-filter1-text"], translation["sidebar-filter1-options"].keys(), format_func=lambda x:translation["sidebar-filter1-options"][x],on_change=apply_filter1,key="new_filter1",index=index1) 


        index3a = list(translation["sidebar-filter3-options"].keys()).index(st.session_state["filter3a"])
        st.session_state["filter3a"] = st.sidebar.selectbox(translation["sidebar-filter3-texta"], translation["sidebar-filter3-options"].keys(), format_func=lambda x:translation["sidebar-filter3-options"][x],on_change=apply_filter3a,key="new_filter3a",index=index3a)

        index3b = list(translation["sidebar-filter3-options"].keys()).index(st.session_state["filter3b"])

        yoptions = {k:v for k,v in translation["sidebar-filter3-options"].items() if k != st.session_state["filter3a"]}

        try:
            index3b = list(yoptions.keys()).index(st.session_state["filter3b"])
        except:
            index3b = 0


        st.session_state["filter3b"] = st.sidebar.selectbox(translation["sidebar-filter3-textb"], yoptions.keys(), format_func=lambda x:yoptions[x],on_change=apply_filter3b,key="new_filter3b",index=index3b)

 
        if st.session_state["filter1"]=="all":
            self.fig = px.scatter(data_frame=self.df.sort_values("category"),x=st.session_state["filter3a"],y=st.session_state["filter3b"],color="category",hover_name="subreddit",color_discrete_sequence=["red","blue"],labels=translation["sidebar-filter3-options"])
        else:
            self.fig = px.scatter(data_frame=self.df[self.df.category==st.session_state["filter1"]],x=st.session_state["filter3a"],y=st.session_state["filter3b"],hover_name="subreddit",color="category",color_discrete_sequence=["red" if st.session_state["filter1"]=="cats" else "blue"],labels=translation["sidebar-filter3-options"])

        self.fig.update_layout(legend_title="Category",legend_title_font_size=20)
        self.fig.update_xaxes(range=[self.df[st.session_state["filter3a"]].min()*0.9,self.df[st.session_state["filter3a"]].max()*1.2])
        self.fig.update_yaxes(range=[self.df[st.session_state["filter3b"]].min()*0.9,self.df[st.session_state["filter3b"]].max()*1.2])


        st.plotly_chart(self.fig,use_container_width=True)





        st.write("-"*50)