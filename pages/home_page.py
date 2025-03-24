import streamlit as st
from PIL import Image  # For image handling
import sys
from pages import registration_form as r
from pages import student_cred
sys.path.append("../")
import db_connection as db
import login_page
import json
import os

dir = os.getcwd()
list_path=[dir,"utils","data.json"]


path = "\\".join(list_path)
login_page_path = "\\".join([dir,"login_page"])

# def admin_main():

try:
    with open(path, "r") as f:
        data = json.load(f)
    if data['Status'] == 'Loggedin':
    # Add a sidebar for navigation (optional)
        st.sidebar.header("Features")
        
        if st.sidebar.button("Home"):
            st.session_state.page = "page1"

        if st.sidebar.button("Students Info"):
            st.session_state.page = "page2"

        if st.sidebar.button("Add Student"):
            st.session_state.page = "page3"
        
        if st.sidebar.button("Create Student credentials"):
            st.session_state.page = "page4"

        if st.sidebar.button("Logout"):
            st.session_state.page = "page5"
        
        #Pages inner content
        if 'page' in st.session_state:
            if st.session_state.page == "page1":
                    # Page Title
                
                st.title(f"Welcome Admin !")
                image = Image.open("homepageimage.png")
                st.image(image,use_container_width=True)
                st.header("About")
                st.write("This Student registration system helps company to manage students data.")
                st.header("Contact")
                st.write("For any questions or feedback, please contact: www.hitechindustrialsolutions.in ")

            if st.session_state.page == "page2":
                st.header("Students Information")
                few_data=db.show_all_rows_student()
                
                for index,row in few_data.iterrows():
                    col1,col2 = st.columns([3,1])
                    with col1:
                        st.table(row[:])
                    with col2:
                        details = st.button("View full details",key=index)
                        if details:
                            st.header(f"Profile Information")
                            stud_info, blob_data = db.fetch_user_details(row.iloc[0])
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

                # for index, row in data.iterrows():
                #     col1, col2 = st.columns([3, 1])  # Adjust column widths as needed
                #     with col1:
                #         st.table(row[:-1]) # Display row data
                #     with col2:
                #         if row[-1] != "No Image":
                #             st.image(row[-1], use_container_width=True)
                #         else:
                #             st.write("No Image")

            if st.session_state.page == "page3":
                r.registration()
                
            if st.session_state.page == "page4":
                cred= student_cred.stud_cred()

                if cred is not None:
                    user,password=cred
                    db.create_cred(user,password)
            
            if st.session_state.page == "page5":
                with open(path, "w") as f:
                    if 'Status' in data:
                        data['Status'] = 'Loggedout'
                        json.dump(data, f)
                st.switch_page(login_page_path)
                
    else:
        st.warning("You are already Logged out")            
                
except Exception as e:
    st.warning(f"Please check error: {e}")
