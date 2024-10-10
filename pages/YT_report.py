import streamlit as st
import pandas as pd
import numpy as np

def less_than_half_prev(df, comparrison_col):
    df_below = df[df[comparrison_col]!=0]
    df_below = df[df[comparrison_col]<50]
    df_below[comparrison_col] = (df_below[comparrison_col].astype(int)).astype(str) + '%'
    df_below = df_below[["LWPOSN", "POSITION", "TITLE", "ARTIST", "LABEL", "FRI YT", "SAT YT", "SUN YT", "MON YT", "TUE YT", "WED YT", "THU YT", comparrison_col]]
    return df_below

# Set page configuration to wide for primary desktop use
st.set_page_config(layout="wide")

# Create dashboard sections
header = st.container()
file_upload = st.container()
data_section = st.container()

# Header Sction of page
with header:
    st.write("Analysis for YT report")
    
with file_upload:
    # Import Data
    yt_data = st.file_uploader('Drag the YT report here')
    # Make data into DataFrame
    try:
        yt_data = pd.read_csv(yt_data)
        df = yt_data.iloc[:, :-1]
        
        # Add column for WTD sales
        df["WTD"] = df["FRI YT"]+df["SAT YT"]+df["SUN YT"]+df["MON YT"]+df["TUE YT"]+df["WED YT"]+df["THU YT"]
        df['WTD_VS_LW'] = round((df["WTD"]/df["LW YT"])*100)
        df['SAT_VS_FRI'] = round((df["SAT YT"]/df["FRI YT"])*100)
        df['SUN_VS_SAT'] = round((df["SUN YT"]/df["SAT YT"])*100)
        df['MON_VS_SUN'] = round((df["MON YT"]/df["SUN YT"])*100)
        df['TUE_VS_MON'] = round((df["TUE YT"]/df["MON YT"])*100)
        df['WED_VS_TUE'] = round((df["WED YT"]/df["TUE YT"])*100)
        df['THU_VS_WED'] = round((df["THU YT"]/df["WED YT"])*100)
        
        with data_section:
            st.write("Raw Data")
            st.dataframe(df)
            
            
            st.write("Below expected compared to last week")
            
            if (df["SAT YT"] == 0).all() == True:
                df_below_lw = df[df['WTD_VS_LW']<(1/7)*100]
            elif (df["SUN YT"] == 0).all() == True:
                df_below_lw = df[df['WTD_VS_LW']<(2/7)*100]
            elif (df["MON YT"] == 0).all() == True:
                df_below_lw = df[df['WTD_VS_LW']<(3/7)*100]
            elif (df["TUE YT"] == 0).all() == True:
                df_below_lw = df[df['WTD_VS_LW']<(4/7)*100]
            elif (df["WED YT"] == 0).all() == True:
                df_below_lw = df[df['WTD_VS_LW']<(5/7)*100]
            elif (df["THU YT"] == 0).all() == True:
                df_below_lw = df[df['WTD_VS_LW']<(6/7)*100]
            df_below_lw['WTD_VS_LW'] = (df_below_lw['WTD_VS_LW'].astype(int)).astype(str) + '%'
            df_below_lw = df_below_lw[["LWPOSN", "POSITION", "TITLE", "ARTIST", "LABEL", "LW YT", "WTD", "FRI YT", "SAT YT", "SUN YT", "MON YT", "TUE YT", "WED YT", "THU YT", "WTD_VS_LW"]]      
            st.dataframe(df_below_lw)            
                
            st.write("Saturday less than half of Friday")
            df_below_fri = less_than_half_prev(df, 'SAT_VS_FRI')
            st.dataframe(df_below_fri)
            
            st.write("Sunday less than half of Saturday")
            df_below_sat = less_than_half_prev(df, 'SUN_VS_SAT')
            st.dataframe(df_below_sat)
            
            st.write("Monday less than half of Sunday")
            df_below_sun = less_than_half_prev(df, 'MON_VS_SUN')
            st.dataframe(df_below_sun)
            
            st.write("Tuesday less than half of Monday")
            df_below_mon = less_than_half_prev(df, 'TUE_VS_MON')
            st.dataframe(df_below_mon)
            
            st.write("Wednesday less than half of Tuesday")
            df_below_tue = less_than_half_prev(df, 'WED_VS_TUE')
            st.dataframe(df_below_tue)
            
            st.write("Thursday less than half of Wednesday")
            df_below_wed = less_than_half_prev(df, 'THU_VS_WED')
            st.dataframe(df_below_wed)
    
    except ValueError:
        st.write("Upload the YT report")