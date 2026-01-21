import streamlit as st
import google.generativeai as genai
from PIL import Image
import datetime as dt
import os

# Configure the model
gemini_api_key = os.getenv('project-testing')
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-2.5-flash-lite')

# Let's create sidebar for image upload

st.sidebar.title(":red[Upload the image of defect]")
uploaded_image = st.sidebar.file_uploader('Choose an image file', type=['png', 'jpg', 'jpeg', 'jfif'],
                                          accept_multiple_files= True)

uploaded_image = [Image.open(image) for image in uploaded_image]
if uploaded_image:
    st.sidebar.success('Image uploaded successfully!')
    st.sidebar.subheader(':blue[Uploaded Image]')
    st.sidebar.image(uploaded_image)

# Let's create the main page

st.title(':orange[STRUCTURAL DEFECTS : - ] :blue[AI Assistant Tool For Structural Defects Detection.] ')
st.markdown('#### :green[This application takes the images of the structural defects from the construction site and prepares the AI assisted report]')
title = st.text_input('Enter the title of the report here : ')
name = st.text_input('Enter your name of the person who has prepared report : ')
desig = st.text_input('Enter your designation of the person who has prepared report : ')
org = st.text_input('Enter the name of the organization of the person who has prepared report : ')

# Creating button of submit

if st.button('SUBMIT') :
    with st.spinner('Processing.....'):
        prompt = f'''
        <Role> You are an expert in structural engineering with 20+ years of experience in structural industry.
        <Goal> You need to prepare a detailed report on structural defects based on the images provided by the user.
        <Context> The Images shared by the user has been attached.
        <format> The report should be in the follwing format:
        * Do not include HTML format like 'br' and another.
        * Add title at the top of the report . The title provided by the user is : {title}
        * next add name,designation and organization of the person who has prepared the report also include the date. Following are the details provided by the user:
        name  : {name}  
        designation  : {desig}
        organization  : {org}
        date : {dt.datetime.now().date()}
        * Identify and classify the defect for eg : crack,spalling,corrosion, honeycombing,leakage etc.
        * There could be more than one defects in images . Identify all the defects persent in the images separately.
        * For each defect identified provide a short description of the defect and it's potential impact on the structure.
        * For each defect measure the severity as low , medium or high. Also, mentioning if the defect is inevitable or avoidable.
        * Provide the short term and long term solution for the repair alogn with an estimated cost in INR and estimated time.
        * What precautionary measures can be taken to avoid in future.
        <Instructions> 
        * The report generated should be in word format.
        * Use bullet points and tabular format where ever possible.
        * Make sure the report doesn't exceeds 3 pages.

        '''

        response= model.generate_content([prompt, *uploaded_image], generation_config={'temperature':0.9})

        st.write(response.text)

        # Creating button for downloading the file
    if st.download_button(label= 'Click to Download Report',
                          data = response.text,
                          file_name= 'structural_defect_report.txt',
                          mime= 'text/plain'):
        st.success('Report downloaded successfully!')
            



