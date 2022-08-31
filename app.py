import yaml
import streamlit as st
from pages import Home,Dataset,Caption


if "index" not in st.session_state:
    st.session_state["index"] = "homepage"


# @st.cache
def load_translator():

    with open("translator.yml","rb") as f:

        return yaml.load(f,Loader=yaml.FullLoader)

translator = load_translator()



def choose_language():
    return st.sidebar.selectbox("Choose a language / Sceglia una lingua", ["English","Italiano"])

language = choose_language()



pages = {
    "homepage": Home,
    "dataset": Dataset,
    "caption": Caption,
}




# @st.cache(hash_funcs={dict: lambda _: None})
def grab_page(selected_page,translation):
    return {"page":selected_page(translation)}



index_number = list(pages.keys()).index(st.session_state["index"])
st.session_state["index"] = st.sidebar.selectbox(translator["navigator"][language], pages.keys(), format_func=lambda x:translator[x][language]["name"],index=index_number)



current_page = grab_page(pages[st.session_state["index"]],translator)["page"]
current_page.render_frame(language)

