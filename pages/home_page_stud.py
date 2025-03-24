import streamlit as st
from PIL import Image  # For image handling
import sys
from pages import registration_form as r
from pages import student_cred
sys.path.append("../")
import db_connection as db
import json
import oracledb
import login_page
import os

dir = os.getcwd()
list_path=[dir,"utils","data.json"]
path = "\\".join(list_path)

path = "\\".join(list_path)
login_page_path = "\\".join([dir,"login_page"])

try:
    with open(path, "r") as f:
        data = json.load(f)
    if data['Status'] == 'Loggedin':
    # Add a sidebar for navigation (optional)
        st.sidebar.header("Features")
        
        if st.sidebar.button("Home"):
            st.session_state.page = "page1"

        if st.sidebar.button("Students Profile"):
            st.session_state.page = "page2"

        if st.sidebar.button("Change Password"):
            st.session_state.page = "page3"
        
        if st.sidebar.button("Logout"):
            st.session_state.page = "page4"

        #Pages inner content
        if 'page' in st.session_state:

            if st.session_state.page == "page1":
                # Page Title
                st.title(f"Welcome {data['username']}!")
                image = Image.open("homepageimage.png")
                st.image(image,use_container_width=True)
                st.header("About")
                st.write("This Student registration system helps company to manage students data.")
                st.header("Contact")
                st.write("For any questions or feedback, please contact: www.hitechindustrialsolutions.in ")

            if st.session_state.page == "page2":

                st.header(f"Profile Information")
                stud_info, blob_data = db.fetch_user_details(data['username'])
                st.write(f"**Name:** {stud_info[0]}")
                st.write(f"**DOB:** {stud_info[1]}")
                st.write(f"**Mobile:** {stud_info[2]}")
                st.write(f"**Email:** {stud_info[3]}")
                st.write(f"**Courses:** {stud_info[4]}")
                if blob_data == None:
                    st.write(f"**Photo:** No profile picture present")
                elif blob_data:
                    st.write(f"**Photo:**")
                    st.image(blob_data, use_container_width= True)
                else:
                    st.warning("Issue while fetching profile photo")

                
            if st.session_state.page == "page3":
                st.header("Change Password")
                with st.form("Change Password"):
                    old = st.text_input(label = "Old password:*",placeholder="Enter Old Password",type="password")
                    new_password = st.text_input(label="New Password:* ",placeholder="Enter New password",type="password")
                    re_password = st.text_input(label="Confirm new password",placeholder="Confirm new password",type="password")
                    ch_pass=st.form_submit_button("Submit")
                if ch_pass:    
                    if new_password == re_password:
                        db.change_password(data['username'],old,new_password)
            
            if st.session_state.page == "page4":
                with open(path, "w") as f:
                    if 'Status' in data:
                        data['Status'] = 'Loggedout'
                        json.dump(data, f)
                st.switch_page(login_page_path)
                
    else:
        st.warning("You are already Logged out")

except Exception as e:
    st.warning(f"Please check error: {e}")

    

