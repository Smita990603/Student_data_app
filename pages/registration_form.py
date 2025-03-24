import streamlit as st
from datetime import datetime as d
import datetime
import sys
import os
sys.path.append("../")
import db_connection as db

def registration():
#Form Header
    st.header("Registration Form")

    with st.form("Registration form"):

        Name = st.text_input(label="Student Name:* ",placeholder="Enter Student Name")

        #Date selection
        today = datetime.date.today()
        eighteen_year = today.replace(year=today.year-18)
        Birthday = st.date_input(label="Birth-Date*",min_value=datetime.date(1925, 1, 1),max_value=eighteen_year)
        oracle_date = f'{Birthday}'

        #Phone number should be 10 digits
        Phone = st.text_input(label="Phone Number*",max_chars=10,placeholder="Enter Phone Number")
        
        Email = st.text_input(label="Email address*",placeholder="Enter Email Address")
        st.write("Please select courses*")
        Courses = ["Python", "Java", "Database"]
        selected_options = []
        for option in Courses:
            if st.checkbox(option):
                selected_options.append(option)

        #upload photo
        upload_photo = st.file_uploader("Upload photo('jpg', 'jpeg', 'png')*",type = ["jpg", "jpeg", "png"])
        submit_form = st.form_submit_button("Submit")

    try:
        if submit_form:
            if not Name or not Phone or not Email or not selected_options or not upload_photo:
                st.warning("Please enter all information")
            else:
                if len(Phone)<10 or Phone.startswith(('0','1','2','3','4','5')):
                    st.warning("Please enter valid mobile number")
                else:
                    st.warning("Register successfully")
                    photo_data_bytes=upload_photo.getvalue()
                    courses_string = ", ".join(selected_options)
                    Int_Phone=int(Phone)
                    result = {
                        'name': Name,
                        'birthday': oracle_date,
                        'phone': Int_Phone,
                        'email': Email,
                        'courses': courses_string,
                        'photo': photo_data_bytes
                    }
            if result is not None:
                db.add_student(result)
                    
    except Exception as e:
        st.error(e)


if __name__ == '__main__':
    registration()