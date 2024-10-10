import streamlit as st
import musicbrainzngs as mbz
import pandas as pd

def rec_by_isrc(isrc_input):
    try:
        # Try to get the recordings by ISRC code
        mbz_isrc_results = mbz.get_recordings_by_isrc(isrc_input)
        recordings = mbz_isrc_results['isrc'].get('recording-list', [])
        return recordings
    
    # Handle web service errors
    except mbz.ResponseError as e:
        if hasattr(e, 'cause') and e.cause.code == 404:
            error = f"Not found - Error {e.cause.code}"
        else:
            error = f"Web Service Error: {e}"
        return error
    
    # Handle any other unexpected errors
    except Exception as e:
        error = f"An unexpected Error occurred: {e}"
        return error

def rec_by_mbzid(recording_id):
    try:
        # Try to get the recordings by ISRC code
        mbz_relase_results = mbz.get_recording_by_id(recording_id, includes=['artist-credits', 'releases'])
        return mbz_relase_results
    
    # Handle web service errors
    except mbz.ResponseError as e:
        if hasattr(e, 'cause') and e.cause.code == 404:
            error = f"Not found - Error {e.cause.code}"
        else:
            error = f"Web Service Error: {e}"
        return error
    
    # Handle any other unexpected errors
    except Exception as e:
        error = f"An unexpected Error occurred: {e}"
        return error            