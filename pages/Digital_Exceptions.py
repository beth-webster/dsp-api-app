import musicbrainzngs as mbz
import streamlit as st
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from mbz_helper_functions import (rec_by_isrc
                                  , rec_by_mbzid)


# Set page configuration to wide for primary desktop use
st.set_page_config(layout="wide")

# Create dashboard sections
header = st.container()
identifier_input = st.container()
musicbrainz_output_info = st.container()
spotify_output_info = st.container()


# set User agent and hostname
mbz.set_useragent("bwebbo_music_data_app", "0.1", "bethawebster0@gmail.com")
mbz.set_hostname("beta.musicbrainz.org")



isrc_ready = 0
upc_ready = 0

track_rows = []

with header:
    st.header('Data for digital tracks/bundles')

with identifier_input:
    col_isrc, col_or, col_upc = st.columns([3,1,3])
    with col_isrc:
        try:
            isrc_input = st.text_input("Enter ISRC:", "")
            
            if len(isrc_input) != 12:
                st.write('ISRC must be 12 characters')
                isrc_ready = 0
            else:
                isrc_ready = 1
        except:
            pass
    
    with col_or:
        col1, col2, col3 = st.columns(3)
        with col2:
            st.write('OR')  
    
    with col_upc:
        try:
            upc_input = st.text_input("Enter UPC:", "")
            
            if len(upc_input) != 12:
                st.write("UPC must be 13 digits... But this doesn't work yet")
                upc_ready = 0
            else:
                upc_ready = 1
        except:
            pass   
    
    if isrc_ready == 1:
        
        with musicbrainz_output_info:
            st.header('Music Brainz Info')
            mbz_isrc_results = rec_by_isrc(isrc_input)
            for recording in mbz_isrc_results:
                try:
                    recording_id = recording.get('id', None)
                    title = recording.get('title', None)
                    length = recording.get('length', None)    
                    track_rows.append([isrc_input
                                    , title
                                    , length
                                    , recording_id])
                except:
                    pass     
            track_df = pd.DataFrame(track_rows, columns=["ISRC"
                                                        , "Title"
                                                        , "Length (ms)"
                                                        , "Music Brainz ID"])
            st.dataframe(track_df)        
            
            st.write(mbz_isrc_results)
            st.write(track_df['Music Brainz ID'].iloc[0])            
            mbz_rel_results = rec_by_mbzid(track_df['Music Brainz ID'].iloc[0])
            st.write(mbz_rel_results)
            

            
        
        with spotify_output_info:
            st.header('Spotify Info')
            st.write("This also doesn't work yet...")
            

            
            
            
            
            
            
            