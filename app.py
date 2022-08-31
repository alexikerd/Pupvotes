import yaml
import streamlit as st
from pages import Home,Dataset,Caption


if "page" not in st.session_state:
    st.session_state["page"] = "homepage"



# @st.cache
def load_content():

    with open("content.yml","rb") as f:

        return yaml.load(f,Loader=yaml.FullLoader)

content = load_content()


def translate():
    if st.session_state.new_language:
        st.session_state["lang"] = st.session_state.new_language


languages = ["English","Italiano"]
language = st.sidebar.selectbox(content[st.session_state["lang"]]["translate"],options=languages,on_change=translate,key="new_language")




pages = {
    "homepage": Home,
    "dataset": Dataset,
    "caption": Caption,
}




# @st.cache(hash_funcs={dict: lambda _: None})
def grab_page(selected_page,translation,language):
    return {"f1":selected_page(translation,language)}



index_number = list(pages.keys()).index(st.session_state["page"])
st.session_state["page"] = st.sidebar.selectbox(content[st.session_state["lang"]]["navigator"], pages.keys(), format_func=lambda x:content[st.session_state["lang"]][x]["name"],index=index_number)



current_page = grab_page(pages[st.session_state["page"]],content,st.session_state["lang"])["f1"]
current_page.render_frame()

