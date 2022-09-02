import yaml
import streamlit as st
from pages import Home,Dataset,Caption
from util import translate, flip_page


if "page" not in st.session_state:
    st.session_state["page"] = "homepage"

if "lang" not in st.session_state:
    st.session_state["lang"] = "English"

if "filter1" not in st.session_state:
    st.session_state["filter1"] = "all"
    st.session_state["filter2"] = "attributes"



# @st.cache
def load_content():

    with open("content.yml","rb") as f:

        return yaml.load(f,Loader=yaml.FullLoader)

content = load_content()




languages = ["English","Italiano"]
lang_index = languages.index(st.session_state["lang"])
st.session_state["lang"] = st.sidebar.selectbox(content["translate"][st.session_state["lang"]],options=languages,on_change=translate,key="new_language",index=lang_index)




pages = {
    "homepage": Home,
    "dataset": Dataset,
    "caption": Caption,
}




@st.cache(hash_funcs={dict: lambda _: None})
def grab_page(selected_page,translation):
    return {"f1":selected_page(translation)}




page_index = list(pages.keys()).index(st.session_state["page"])
selected_page = st.sidebar.selectbox(content["navigator"][st.session_state["lang"]], pages.keys(), format_func=lambda x:content[x][st.session_state["lang"]]["name"],on_change=flip_page,key="new_page",index=page_index)





current_page = grab_page(pages[selected_page],content)["f1"]
current_page.render_frame(st.session_state["lang"])

