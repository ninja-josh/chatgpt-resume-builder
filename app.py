import streamlit as st
from readmegetter import ReadmeGetter

st.title('Welcome to the Github Project Resume Helper')

def get_summaries():
    waiting = st.text('Please wait while we retrieve and summarize your READMEs')


    if repo_link.startswith('https://github.com/') or repo_link.startswith('github.com/'):
        Getter = ReadmeGetter()
        summaries = Getter.get_summaries(repo_link)

        readmes = ['\n' + key + '\n' + summaries[key] for key in summaries.keys()]
        readmes = '\n'.join(readmes)
        st.session_state.readmes = readmes
        waiting.write('Summaries Complete')
        
        if '1' in st.session_state:
            st.session_state['1'] = ''

    else:
        waiting.write('Sorry, that is not a GitHub link')

repo_link = st.text_input('Input Github Profile Link Here', key='1')

st.button('Press to Submit Link', on_click=get_summaries)

if 'readmes' in st.session_state:
    st.markdown(st.session_state.readmes)
    st.session_state.readmes = ''