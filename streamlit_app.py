import streamlit as st
from spotify_features import *
from PyPDF2 import PdfReader
import os
import datetime

dict_musics = {
    "Whenever, Wherever - Shakira": "https://open.spotify.com/intl-fr/track/2lnzGkdtDj5mtlcOW2yRtG?si=724caa482e8f4ef3",
    "Moonlit walk - Purrple Cat":"https://open.spotify.com/intl-fr/track/1UySjE9vUN6yAcUSgh1aaQ?si=c21c5be2915248d9"
}

dict_tabs = {
    "Whenever, Wherever - Shakira": "D:\Python_projects\Piano_transpositions\Tabs\PDFs\Whenver, Wherever - Shakira.pdf",
    "Moonlit walk - Purrple Cat": "D:\Python_projects\Piano_transpositions\Tabs\PDFs\Stressed out - Twenty one pilots.pdf"
}


def read_pdf(file_path):
    text = ""
    with open(file_path, "rb") as f:
        pdf_reader = PdfReader(f)
        num_pages = len(pdf_reader.pages)
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text



def reset():
    st.session_state.track_selectbox = None


def play_pause_button():
    playback_state = spotify_player.current_playback()
    if playback_state is None:
        st.error("No active playback found.")
    else:
        if playback_state["is_playing"] == True:  # If currently playing, pause
            spotify_player.pause_playback()
            st.session_state.track_selectbox = None
        elif playback_state["is_playing"] == False:  # If currently paused, play
            spotify_player.start_playback()
    

def main():


    #ELEMENTS IN THE SIDEBAR
    with st.sidebar: 
        st.button("Start")


    #SPOTIFY CONTAINER
    with st.expander("Spotify music", expanded=True):
        with st.container(height=200,  border=True):
            
            track_chosen_selectbox = st.selectbox("Select a track", options=list(dict_musics.keys()), index=None, key="track_selectbox")

            # Display the selected option
            if track_chosen_selectbox != None:
                url_track = dict_musics[track_chosen_selectbox]
                spotify_player.play_song_from_url(url_track)
                track_title = spotify_player.title_format(url=url_track)
                st.write(track_title)

            elif spotify_player.current_playback() is not None:
                playback_state = spotify_player.current_playback()
                track_uri = playback_state["item"]["uri"]
                track_title = spotify_player.title_format(uri=track_uri)
                # st.write(playback_state["item"]["name"], "-", playback_state["item"]["artists"][0]["name"], "!")
                st.write(track_title)

            else:
                print("Name of track chosen", st.session_state.get(track_chosen_selectbox))

            st.button("Play/Pause", on_click=play_pause_button)
                
            

    with st.expander("Degrees"):
        st.container(height=300, border=True)

    with st.expander("TABS", expanded=True):
       with st.container(height=600, border=True):
            if spotify_player.current_playback() is not None:
                playback_state = spotify_player.current_playback()
                tabs_folder = os.getcwd()
                track_name = track_chosen_selectbox
                if track_name in list(dict_tabs.keys()):
                    track_tab = dict_tabs[track_name]
                    tab_path = os.path.join(tabs_folder, track_tab)
                    tablature(tab_path)
                else:
                    st.write("No track selected")

            else:
                st.write("No track selected")
    

def tablature(pdf_file_path):
    st.title("PDF Viewer")

    # Check if the file exists
    if os.path.exists(pdf_file_path):
        pdf_text = read_pdf(pdf_file_path)

        # Display the title of the PDF
        st.header(os.path.basename(pdf_file_path))

        # Display the text with a vertical scrollbar
        st.text_area("PDF Content", value=pdf_text, height=500)
    else:
        st.error("PDF file not found.")

if __name__ == "__main__":
    spotify_player = SpotifyFeatures()
    main()
