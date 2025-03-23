import streamlit as st
import db_connection as c
import json
import os
import sys

dir = os.getcwd()
list_path=[dir,"utils","data.json"]
path = "\\".join(list_path)

def login_ui():
    username,password,role = c.fetch_login_details()
    #Header of form
    st.header("Login")

    with st.form("login page"):
        
        user = st.text_input(label="Username*",placeholder="Enter username")
        passw = st.text_input(label="Password*",placeholder="Enter password",max_chars=10,type="password")
        submit = st.form_submit_button(label="Submit")

        st.markdown(f'''New user? <a href="http://localhost:8501/registration_form" target="_self">Register</a>''', unsafe_allow_html=True)

    try:
        
        if submit:
            if not user and not passw:
                st.warning("Please enter username and password")
            elif not user:
                st.warning("Please enter username")
            elif not passw:
                st.warning("Please enter password")
            elif user in username:
                index = username.index(user)
                if password[index] == passw:
                    if role[index] == 'Admin':
                        try:
                            data={
                                'username' : 'Admin',
                                'password' : passw, 
                                'Status'   : 'Loggedin'
                            }
                            with open(path, "w") as f:
                                json.dump(data, f)
                        except:
                            print("Something went wrong while adding data to json")
                        st.switch_page('pages/home_page.py')
                        
                    elif role[index] =='Student':
                        try:
                            data={
                                'username' : user,
                                'password' : passw, 
                                'Status'   : 'Loggedin'
                            }
                            with open(path, "w") as f:
                                json.dump(data, f)
                        except:
                            print("Something went wrong while adding data to json")
                        st.switch_page('pages/home_page_stud.py')
                        
                    else:
                        st.warning("Incorrect role for login , please contact admin")
                      
                else:
                    st.warning("Password entered is incorrect")
            else:
                st.warning("Username is incorrect")
    except Exception as e:
        st.error(f"Error:{e}")


if __name__=='__main__':
    login_ui()








