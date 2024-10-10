# Import libraries
import streamlit as st
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from PIL import Image

# Import Functions from helper_functions.py file
from sp_helper_functions import (id_from_url
                            , convert_df_csv
                            , playlist_results
                            , album_results
                            , track_results
                            , album_label
                            , track_title
                            , artists
                            , album_trackid
                            , track_isrc
                            , album_copyright
                            , album_upc
                            , album_title
                            , album_reldate
                            , album_numtracks
                            , album_trackseq
                            , playlist_bundleid
                            , track_bundleid
                            , create_code_txt
                            , barcodes_13_digits)

# Set page configuration to wide for primary desktop use
st.set_page_config(layout="wide")

# Create dashboard sections
header = st.container()
track_data = st.container()
bundle_data = st.container()
file_buttons = st.container()

# Display Spotify logo at the top of the sidebar
image = Image.open('Spotify_Logo_RGB_Green.png')
st.sidebar.image(image)

# Input boxes API login - ID & secret
client_id = st.sidebar.text_input("Enter client ID:", "")
client_secret = st.sidebar.text_input("Enter client secret:", type="password")

# Set variables to 0 to be updated & allow display of containers when valid inputs are given by the user
auth_ready = 0
url_ready = 0

# Lists for displayed DataFrames and downloadable CSVs
track_rows = []
bundle_rows = []
tracklisting_rows = []
file_track_rows = []
file_bundle_rows = []
file_tracklisting_rows = []
barcodes = []

try:
    # Establish API connection with Spotipy
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id = client_id,
                                                        client_secret = client_secret))
    auth_ready = 1
except:
   with header:
    st.write('Please enter valid login credentials')
    auth_ready = 0

if auth_ready == 1:
    with header:
        #Text input for URL
        try:
            url = st.text_input("Enter URL:", "")
            url_type, id = id_from_url(url)

            # Validate that URL is a Spotify link for a playlist, ablum or track
            if url_type == 'album' or url_type == 'playlist' or url_type == 'track':
                url_ready = 1
            else:
                with track_data:
                    st.write('Enter a spotify URL for an Album, Playlist or Track')
                    url_ready = 0
        except:
            pass

if url_ready == 1:
    if url_type == 'album':
        album_info = album_results(sp,id)
        album_tracklist_info = album_info['tracks']['items']

        with track_data:
            st.write('Track Data')

            upc = album_upc(album_info)
            upc = barcodes_13_digits(upc)
            label = album_label(album_info)
            copyright = album_copyright(album_info)
            for track in album_tracklist_info:
                try:
                    title = track_title(track)
                    artist = artists(track)
                    trackid = album_trackid(track)
                    track_info = track_results(sp, trackid)
                    isrc = track_isrc(track_info)
                    trackseq = album_trackseq(track)
                    track_rows.append([isrc
                                    , ""
                                    , title
                                    , ""
                                    , artist
                                    , ""
                                    , label
                                    , label
                                    , label
                                    , copyright
                                    , "40"])
                    tracklisting_rows.append([upc
                                            , isrc
                                            , 1
                                            , 1
                                            , trackseq])
                except:
                    pass
            track_df = pd.DataFrame(track_rows, columns = ["ISRC"
                                                           , ""
                                                           , "Title"
                                                           , "Mix Name"
                                                           , "Artist"
                                                           , "Release Date"
                                                           , "Label"
                                                           , "Company"
                                                           , "Corporate Group"
                                                           , "Distributor"
                                                           , "Price"])
            tracklisting_df = pd.DataFrame(tracklisting_rows, columns = ["UPC"
                                                                         ,"ISRC"
                                                                         ,"Volume"
                                                                         ,"Side"
                                                                         ,"Sequence"])
            st.dataframe(track_df)  

        with bundle_data:
            st.write('Bundle Data')

            title = album_title(album_info)
            artist = artists(album_info)
            
            filename = f'{title}_{artist}'
            
            reldate = album_reldate(album_info)
            numtracks = album_numtracks(album_info)
            if numtracks > 4:
                price = 425
                bundle_class = "A"
            else:
                price = 40
                bundle_class = "S"
            bundle_rows.append([upc
                                , ""
                                , title
                                , artist
                                , reldate
                                , bundle_class
                                , "A"
                                , label
                                , label
                                , label
                                , copyright
                                , price
                                , ""
                                , ""
                                , numtracks])
            barcodes.append([upc])
            bundle_df = pd.DataFrame(bundle_rows, columns = ["UPC"
                                                             , ""
                                                             , "Title"
                                                             , "Artist"
                                                             , "Release Date"
                                                             , "Class"
                                                             , "A/V"
                                                             , "Label"
                                                             , "Company"
                                                             , "Corporate Group"
                                                             , "Distributor"
                                                             , "Price"
                                                             , " "
                                                             , "  "
                                                             , "Number of Tracks"])
            st.dataframe(bundle_df) 

            file_track_df = track_df.copy()
            file_bundle_df = bundle_df.copy()
            file_tracklisting_df = tracklisting_df.copy()  

    elif url_type == 'playlist':
        playlist_info = playlist_results(sp,id)
        playlist_tracks_info = playlist_info['tracks']['items']
        filename = playlist_info['name']

        with track_data:
            st.write('Track Data')

            for track in playlist_tracks_info:
                # Data to display in browser
                isrc = track_isrc(track['track'])
                title = track_title(track['track'])
                artist = artists(track['track'])

                # Data for files
                bundleid = playlist_bundleid(track)
                try:
                    album_info = album_results(sp,bundleid)
                    album_tracklist_info = album_info['tracks']['items']

                    upc = album_upc(album_info)
                    upc = barcodes_13_digits(upc)
                    bundle_title = album_title(album_info)
                    bundle_artist = artists(album_info)
                    label = album_label(album_info)
                    copyright = album_copyright(album_info)
                    reldate = album_reldate(album_info)
                    numtracks = album_numtracks(album_info)
                    if numtracks > 4:
                        bundle_price = 425
                        bundle_class = "A"
                    else:
                        bundle_price = 40
                        bundle_class = "S"
                except:
                    pass

                for track in album_tracklist_info:
                    try:
                        file_title = track_title(track)
                        file_artist = artists(track)
                        trackid = album_trackid(track)
                        track_info = track_results(sp, trackid)
                        file_isrc = track_isrc(track_info)
                        file_trackseq = album_trackseq(track)
                        file_track_rows.append([file_isrc
                                                , ""
                                                , file_title
                                                , ""
                                                , file_artist
                                                , ""
                                                , label
                                                , label
                                                , label
                                                , copyright
                                                , "40"])
                        file_tracklisting_rows.append([upc
                                                    , file_isrc
                                                    , 1
                                                    , 1
                                                    , file_trackseq])
                    except:
                        pass
            
                track_rows.append([isrc
                                   , ""
                                   , title
                                   , ""
                                   , artist
                                   , ""
                                   , label
                                   , label
                                   , label
                                   , copyright
                                   , "40"])
                bundle_rows.append([upc
                                , ""
                                , bundle_title
                                , bundle_artist
                                , reldate
                                , bundle_class
                                , "A"
                                , label
                                , label
                                , label
                                , copyright
                                , bundle_price
                                , ""
                                , ""
                                , numtracks])
                barcodes.append([upc])
            file_track_df = pd.DataFrame(file_track_rows)
            file_bundle_df = pd.DataFrame(bundle_rows)
            file_tracklisting_df = pd.DataFrame(file_tracklisting_rows)
            track_df = pd.DataFrame(track_rows, columns = ["ISRC"
                                                           , ""
                                                           , "Title"
                                                           , "Mix Name"
                                                           , "Artist"
                                                           , "Release Date"
                                                           , "Label"
                                                           , "Company"
                                                           , "Corporate Group"
                                                           , "Distributor"
                                                           , "Price"])
            st.dataframe(track_df)


        with bundle_data:
            st.write('Bundle Data')

            bundle_df = pd.DataFrame(bundle_rows, columns = ["UPC"
                                                             , ""
                                                             , "Title"
                                                             , "Artist"
                                                             , "Release Date"
                                                             , "Class"
                                                             , "A/V"
                                                             , "Label"
                                                             , "Company"
                                                             , "Corporate Group"
                                                             , "Distributor"
                                                             , "Price"
                                                             , " "
                                                             , "  "
                                                             , "Number of Tracks"])

            st.dataframe(bundle_df)
   

    elif url_type == 'track':
        track_info = track_results(sp,id)

        with track_data:
            st.write("Track Data") 

            title = track_title(track_info)
            artist = artists(track_info)
            isrc = track_isrc(track_info)
            
            filename = f'{title}_{artist}'

            bundleid = track_bundleid(track_info)
            album_info = album_results(sp,bundleid)
            album_tracklist_info = album_info['tracks']['items']

            upc = album_upc(album_info)
            upc = barcodes_13_digits(upc)
            bundle_title = album_title(album_info)
            bundle_artist = artists(album_info)
            label = album_label(album_info)
            copyright = album_copyright(album_info)
            reldate = album_reldate(album_info)
            numtracks = album_numtracks(album_info)
            if numtracks > 4:
                bundle_price = 425
                bundle_class = "A"
            else:
                bundle_price = 40
                bundle_class = "S"

            for track in album_tracklist_info:
                try:
                    file_title = track_title(track)
                    file_artist = artists(track)
                    trackid = album_trackid(track)
                    track_info = track_results(sp, trackid)
                    file_isrc = track_isrc(track_info)
                    file_trackseq = album_trackseq(track)
                    file_track_rows.append([file_isrc
                                            , ""
                                            , file_title
                                            , ""
                                            , file_artist
                                            , ""
                                            , label
                                            , label
                                            , label
                                            , copyright
                                            , "40"])
                    file_tracklisting_rows.append([upc
                                                   , file_isrc
                                                   , 1
                                                   , 1
                                                   , file_trackseq])
                except:
                    pass
            try:
                track_rows.append([isrc
                                    , ""
                                    , title
                                    , ""
                                    , artist
                                    , ""
                                    , label
                                    , label
                                    , label
                                    , copyright
                                    , "40"])
            except:
                pass
            track_df = pd.DataFrame(track_rows, columns = ["ISRC"
                                                           , ""
                                                           , "Title"
                                                           , "Mix Name"
                                                           , "Artist"
                                                           , "Release Date"
                                                           , "Label"
                                                           , "Company"
                                                           , "Corporate Group"
                                                           , "Distributor"
                                                           , "Price"])
            file_track_df = pd.DataFrame(track_rows)
            file_tracklisting_df = pd.DataFrame(file_tracklisting_rows)
            
            st.dataframe(track_df)          

        with bundle_data:
            st.write("Bundle Data")

            bundle_rows.append([upc
                                , ""
                                , bundle_title
                                , bundle_artist
                                , reldate
                                , bundle_class
                                , "A"
                                , label
                                , label
                                , label
                                , copyright
                                , bundle_price
                                , ""
                                , ""
                                , numtracks])
            barcodes.append([upc])
            bundle_df = pd.DataFrame(bundle_rows, columns = ["UPC"
                                                             , ""
                                                             , "Title"
                                                             , "Artist"
                                                             , "Release Date"
                                                             , "Class"
                                                             , "A/V"
                                                             , "Label"
                                                             , "Company"
                                                             , "Corporate Group"
                                                             , "Distributor"
                                                             , "Price"
                                                             , " "
                                                             , "  "
                                                             , "Number of Tracks"])
            file_bundle_df = pd.DataFrame(bundle_rows)

            st.dataframe(bundle_df)


    with file_buttons:
        st.write('Download Data')
        
        # Creates a button to download bundle data as CSV
        bundle_csv = convert_df_csv(file_bundle_df)
        st.download_button(label = "Download bundle data as CSV"
                        , data = bundle_csv
                        , file_name = f'{filename}_bundles.csv'
                        , mime = 'text/csv')
        
        # Creates a button to download track data as CSV
        track_csv = convert_df_csv(file_track_df)
        st.download_button(label = "Download track data as CSV"
                        , data = track_csv
                        , file_name = f'{filename}_tracks.csv'
                        , mime = 'text/csv')  
        
        # Creates a button to download tracklisting data as CSV
        tracklisting_csv = convert_df_csv(file_tracklisting_df)
        st.download_button(label = "Download tracklisting data as CSV"
                        , data = tracklisting_csv
                        , file_name = f'{filename}_track_listing.csv'
                        , mime = 'text/csv')
        
        
        held_bundle_search = create_code_txt(barcodes)  
        st.download_button("Download code to search for bundles in the held table", held_bundle_search)