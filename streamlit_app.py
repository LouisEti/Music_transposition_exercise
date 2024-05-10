import streamlit as st
from spotify_features import *
from PyPDF2 import PdfReader
import os
import datetime

dict_musics = {
    "Whenever, Wherever - Sharkira": "https://open.spotify.com/intl-fr/track/2lnzGkdtDj5mtlcOW2yRtG?si=724caa482e8f4ef3",
    "Moonlit walk - Purrple Cat":"https://open.spotify.com/intl-fr/track/1UySjE9vUN6yAcUSgh1aaQ?si=c21c5be2915248d9"
}

track_interrupted = False

def convert_ms_to_min(duration_ms):
    """
    Convert milliseconds duration into min:sec format.
    Return time_convertion, minute unit and seconds
    """
    #Get the min where seconds are scaled between 0 and 100 and not 60 -> e.g. 3,84 minutes
    no_convert = duration_ms / 60000
    
    #Retrieve only the minute unit
    min_unit = int(no_convert)
    
    #Retrieve the non_converted seconds left 
    sec_left = abs(no_convert - min_unit)

    #Convert the seconds into 0-60 format 
    seconds = int(sec_left * 60)+1

    #Display the time in the "min:sec" format
    time_convertion = f"{min_unit}:{seconds}"

    return time_convertion, min_unit, seconds


def get_list_of_all_minutes(minutes, seconds):
    """
    Get a list of all the seconds between 0:00 and min:sec 
    """
    final_list = []
    min = 0
    sec = 0
    while min < minutes:
        for s in range(60):
            if s <= 9:
                final_list.append(f"{min}:0{s}")
            else: 
                final_list.append(f"{min}:{s}")
        min += 1
    
    while sec <= seconds:
        final_list.append(f"{min}:{sec}")
        sec += 1

    return final_list


def read_pdf(file_path):
    text = ""
    with open(file_path, "rb") as f:
        pdf_reader = PdfReader(f)
        num_pages = len(pdf_reader.pages)
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text


# def spotify_area():



def main():
    

    #ELEMENTS IN THE SIDEBAR
    with st.sidebar: 
        st.button("Start")


    #SPOTIFY CONTAINER
    with st.expander("Spotify music"):
        with st.container(height=200,  border=True):
            track_name_chosen = st.selectbox("Choose a song", options=list(dict_musics.keys()), index=None)
            if track_name_chosen:
                url_track = dict_musics[track_name_chosen]
                duration_time_track = spotify_player._get_time_duration_song(url_track)
                spotify_player.play_song_from_url(url_track)
                list_of_times = slidebar_spotify(duration_time_track)
                # Spotify track embed HTML code
                spotify_track_embed_code = """
                <iframe style="border-radius:12px" src="https://open.spotify.com/embed/track/1UySjE9vUN6yAcUSgh1aaQ?utm_source=generator" width="100%" height="352" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
                """

                # Display the Spotify track embed code
                st.components.v1.html(spotify_track_embed_code, width=800, height=400)
                
                # st.button("Pause/Play", on_click=spotify_player.pause_and_get_progression())
                # while track_interrupted == False:
                #     st.select_slider(track_name_chosen, options=list_of_times, value=list_of_times)
                #     time.sleep(1)
                #     value += 1
                
            

    with st.expander("Degrees"):
        st.container(height=300, border=True)

    with st.expander("TABS"):
        st.container(height=600, border=True)
    


def slidebar_spotify(length_track):
    time_track_converted, min_track, sec_track = convert_ms_to_min(length_track)
    list_of_times = get_list_of_all_minutes(min_track, sec_track)
    # st.select_slider(track_name, options=list_of_times, value=0)
    return list_of_times




def tab_area():
    st.title("PDF Viewer")

    # Specify the path to your PDF file
    pdf_file_path = "D:\Python_projects\Piano_transpositions\Tabs\PDFs\Whenver, Wherever - Shakira.pdf"

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
