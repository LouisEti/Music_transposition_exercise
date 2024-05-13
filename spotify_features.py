import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import os
import re


class SpotifyFeatures(spotipy.Spotify):
    def __init__(self, client_id=None, client_secret=None, redirect_uri=None, device_id="f874fb41e4795d8493509859d855f28f55bf9bea") -> None:
        """
        Initalize the SpotifyFeatures class with: 
        - client_id
        - client_secret 
        - redirect_uri: uri of your spotify app (in Developer Dashboard)
        - device_id
        """

        if not (client_id and client_secret and redirect_uri):
            # print('Entering the "Transposition_exercises" App')
            client_id = os.getenv("SPOTIPY_CLIENT_ID")
            client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
            redirect_uri = "https://transposition_exercise"
        
        super().__init__(auth_manager=SpotifyOAuth(client_id=client_id,
                                                   client_secret=client_secret,
                                                   redirect_uri=redirect_uri,
                                                   scope="user-modify-playback-state"))
        
        self.device_id = device_id

        if self.device_id != "f874fb41e4795d8493509859d855f28f55bf9bea":
            # If device_id is not provided, get the first available device
            devices = self.devices()
            available_devices = devices['devices']
            if available_devices:
                self.device_id = available_devices[0]['id']
        # print(self.device_id)


    def get_uri_from_url(self, url: str) -> str:
        """
        Get the uri of a song, given its URL
        """
        # Regular expression to match the unique identifier after the last slash and before the question mark
        regex = r"/([^/]+)\?"
        match = re.search(regex, url)
        if match:
            return "spotify:track:" + match.group(1)
        else:
            print("No uri found for the song")
            return None
        

    def get_id_from_url(self, url: str) -> str:
        """
        Get the id of the song given its URL
        """
        # Regular expression to match the unique identifier after the last slash and before the question mark
        regex = r"/([^/]+)\?"
        match = re.search(regex, url)
        if match:
            return  match.group(1)
        else:
            print("No uri found for the song")
            return None
        

    def play_song_from_url(self, url: str) -> str:
        """
        From a song URL, retrieve its uri and start the player

        Params:
            url = URL of the song you want to play  

        Return the uri of the song
        """

        track_uri = self.get_uri_from_url(url)
        self.start_playback(device_id=self.device_id, uris=[track_uri])

        return track_uri 
    

    def _get_time_duration_song(self, url: str) -> int:
        """
        Get the total time duration (in ms) of a song, given its url
        """

        track_id = self.get_id_from_url(url)
        track_info = self.track(track_id=track_id)
        duration_time = track_info["duration_ms"]

        return duration_time
    

    def pause_and_get_progression(self) -> int:
        """
        Pause the current playing track and return the time progression (in ms)
        """
        
        self.pause_playback()
        progress_time = self.current_user_playing_track()["progress_ms"]

        return progress_time
    

    def title_format(self, url=None, uri=None):
        """
        Return the track title in the format "track_name - track_artist" from url or uri
        """
        if url:
            track_uri = self.get_uri_from_url(url)
        elif uri:
            track_uri = uri
        else:
            print("Url or uri not given")
            return None

        track_info = self.track(track_uri)
        track_name = track_info["name"]
        track_artist = track_info["artists"][0]["name"]
        track_title = f"{track_name} - {track_artist}"

        return track_title
