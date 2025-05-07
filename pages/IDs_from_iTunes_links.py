import streamlit as st
import re

# Functions
def ids_from_urls(at_links):
    
    url_id_map = {}
    
    for url in at_links:        
        try:
            url_regex = re.search(r"(\d+)$", url)            
            if url_regex:
                url_id_map[url] = url_regex.group()
                
        except AttributeError:
            url_id_map[url] = 'invalid input'
            
    return url_id_map

# Set page configuration to wide for primary desktop use
st.set_page_config(layout="wide")

# Create dashboard sections
header = st.container()
links_input = st.container()
output_ids = st.container()
compare_ids = st.container()
flagging_isrcs = st.container()

# Header Sction of page
with header:
    st.write("Extract IDs from iTunes links, add into code & compares output IDs for email back!")
    
# Main page section
with links_input:
    
    at_links = st.text_area('Paste links here')
    at_links = at_links.split("\n")
    url_id_map = ids_from_urls(at_links)
    id_list = list(url_id_map.values())
    st.write()

        
with output_ids:
    
    id_list_code = [f"'{id_}'" for id_ in id_list]
    
    id_code = f'''select distinct(ISRC), null as barcode, title, null as mix_name, artist, null as RD, label, label, label, distributor,'0' as price, identifier
from excep_dig_apple_master
where identifier in ({", ".join(id_list_code)})
order by identifier;'''
        
    st.code(id_code, language='sql')
    
with compare_ids:
    
    output_ids = st.text_area('Paste output IDs here')
    output_ids = output_ids.split("\n")
    missing_urls = [url for url, id_ in url_id_map.items() if id_ not in output_ids]
    missing_urls_out = '\n'.join(missing_urls)
    
    st.code(f"""Hi,
\nHope you are well! 
\nThese have been added and flagged, with the exception of the below:
\n{missing_urls_out}
\nThanks,""", language = 'csv')

with flagging_isrcs:
    
    isrcs = st.text_area('Paste output ISRCs here')
    isrcs = isrcs.split("\n")
    isrc_list = list(isrcs)
    isrc_list_code = [f"'{isrc}'" for isrc in isrc_list]
    
    isrc_code = f"""--Spot check a couple to make sure all is fine
declare

cursor c_1 is
select id pro_id
from products
where id in (select pro_id
             from tracks
             where id in (select tra_id
                          from ISRCs
                          where ISRC in ({", ".join(isrc_list_code)})))
and id not in (select pro_id from pro_pel where pel_id = 37)
;
begin

for r_1 in c_1 loop
insert into pro_pel
values (r_1.pro_id, '37', trunc(sysdate));

 end loop;

commit;

 end;
"""
    st.code(isrc_code, language='sql')