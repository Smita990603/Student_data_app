import streamlit as st


def stud_cred():
#Form Header
    st.header("Create credentials")

    with st.form("Create credentials"):

        user_name = st.text_input(label="Username:* (should be name of student)",placeholder="Enter Username")
        password = st.text_input(label="Password:* ",placeholder="Enter password",type="password")

        submit_form = st.form_submit_button("Submit")

        if submit_form:
            if not user_name and not password:
                st.warning("Please enter mandatory details")
            elif not user_name:
                st.warning("Please enter username")
            elif not password:
                st.warning("Please enter password")
            else:
                return user_name,password

