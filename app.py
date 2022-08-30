import yaml
import streamlit as st
from pages import Home,Dataset,Caption

# st.markdown("# Pupvotes \U0001F436")
# st.sidebar.markdown("# Homepage \U0001F431")



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

@st.cache(hash_funcs={dict: lambda _: None})
def grab_page(selected_page,translation):
    return {"page":selected_page(translation)}


selected_page = st.sidebar.selectbox(translator["navigator"][language], pages.keys(), format_func=lambda x:translator[x][language]["name"])


current_page = grab_page(pages[selected_page],translator)["page"]
current_page.render_frame(language)

