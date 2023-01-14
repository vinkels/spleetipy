import streamlit as st
from stemmer import remove_instrument
import os
from pydub import AudioSegment

st.title('music stemmer app using streemer')

up_cols = st.columns([1,3])


instrument = up_cols[0].radio('Pick instrument to remove', options=["vocals", "bass","drums", "other"])

song = up_cols[1].file_uploader('Upload song to convert', type=['mp3'], accept_multiple_files=False)

if st.button('Run stemmer!'):
    if song and instrument:
        audio = AudioSegment.from_mp3(song)
        audio.export('raw/'+song.name, format='mp3')

        pre_cols = st.columns([1,1,3])
        pre_cols[0].write('Original')
        pre_cols[2].audio('raw/'+song.name)

        with st.spinner(f'Hold tight, removing {instrument}'):
            song_path = remove_instrument('raw/'+song.name, filter_instrument='drums')
        # st.success('Done!')

        post_cols = st.columns([1,1,3])
        post_cols[0].write(f'Without {instrument}')
        with open(song_path, "rb") as file:
            btn = post_cols[1].download_button(label="Download",data=file,file_name=song_path.split('/')[-1],mime="audio/mp3")
        post_cols[2].audio('raw/'+song.name)
        # st.audio(song_path)
       
    elif not song:
        st.error('Upload a song first')
    elif not instrument:
        st.error('pick an instrument to filter')


