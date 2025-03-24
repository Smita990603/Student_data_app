import oracledb
import streamlit as st
import pandas as pd
import os
from pages import registration_form as r

def conn():
    try:
        # Replace with your Oracle database credentials
        username = "SYSTEM"
        password = "Smita123"
        dsn = oracledb.makedsn("DESKTOP-LB9SKCG", "1521", service_name="orcldb") # create data source name.

        # Establish the connection
        connection = oracledb.connect(user=username, password=password, dsn=dsn)

        # Create a cursor object
        cursor = connection.cursor()

        return cursor,connection

    except oracledb.Error as error:
        print("Error connecting to Oracle:", error)
    
def fetch_user_details(name):
    try:

        cursor,connection = conn()
        # Fetch the result
        cursor.execute(f"SELECT * FROM Student where Name = '{name}'")
        result = cursor.fetchone()
        if result[5]:
            blob_data = result[5].read()
        else:
            blob_data = None
        return result, blob_data
    
    except Exception as error:
        st.error( error)

    finally:
    # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close() 


def show_all_rows_student():
    
    try:
        cursor,connection = conn()
        # Fetch the result
        cursor.execute("SELECT * FROM Student")
        
        result = cursor.fetchall()
        Names = []
        Birthdate=[]
        Mobile=[]
        Email=[]
        Courses=[]
        Photo=[]
        
        for i in range(0,len(result)) :
            Names.append(result[i][0])
            Birthdate.append(result[i][1])
            Mobile.append(result[i][2])
            Email.append(result[i][3])
            Courses.append(result[i][4])
            
            if isinstance(result[i][5], oracledb.LOB):
                blob_data = result[i][5].read()
                if blob_data.startswith(b'\xFF\xD8\xFF'):
                    mime_type = "image/jpeg"
                    file_name = f"image_{i}.jpg"
                elif blob_data.startswith(b'\x89PNG\r\n\x1a\n'):
                    mime_type = "image/png"
                    file_name = f"image_{i}.png"
                else:
                    st.warning("Incorrect image format")

                if blob_data:
                    Photo.append(blob_data)
                    # download=st.download_button(
                    #     label=f"Photo of student {i}",
                    #     data=bytes(blob_data),
                    #     file_name=file_name,
                    #     mime=mime_type,
                    #     key=f"download_{i}"
                    # )  
                    # Photo.append("Image")
            else:
                Photo.append("No Image")
        
        
        data = pd.DataFrame({
        'Name': Names,
        'Birthdate': Birthdate,
        'Mobile Number': Mobile,
        'Email': Email,
        'Courses': Courses,
        'Photo': Photo,
        })

        few_data = pd.DataFrame({
        'Name': Names
        })
        return few_data
        # st.table(data)
    except oracledb.Error as error:
        st.error("Error connecting to Oracle:", error)

    finally:
    # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def add_student(result):
     
    try:
        cursor,connection = conn()
        query = """ INSERT INTO Student (Name, Birthday, Phone, Email, Courses, Photo) 
            VALUES (:name, TO_DATE(:birthday, 'YYYY-MM-DD'), :phone, :email, :courses, :photo)
        """
        cursor.execute(query, result)
        connection.commit()
        print("Inserted")
        
    except Exception as e:
        print("Error:",e)
    
    finally:
    # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        
def create_cred(username,password):
    try:
        cursor,connection = conn()
        tuple1=(username,password,'Student')
        query=f"Insert into login_details (Username,password,Role) values {tuple1}"
        cursor.execute(query)
        connection.commit()
        

    except oracledb.Error as error:
        print("Error connecting to Oracle:", error)

    finally:
    # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def change_password(user,passw,new):
    try:
        cursor,connection = conn()

        select_query = f"SELECT Password FROM login_details where Username = '{user}' "
        cursor.execute(select_query)
        result = cursor.fetchone()
        if(result[0] == passw):
            update_query = "UPDATE login_details SET Password = :p WHERE Username = :n"
            cursor.execute(update_query, (new, user))
            st.write("Password changed successfully")
        connection.commit()

    except Exception as e:
        st.warning(e)
    
    finally:
    # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def fetch_login_details():
    try:
        cursor,connection = conn()
        cursor.execute("SELECT * FROM login_details")
        result = cursor.fetchall()

        username=[]
        password=[]
        role=[]
        for i in range(0,len(result)) :
            username.append(result[i][0])
            password.append(result[i][1])
            role.append(result[i][2])

        return username,password,role
        

    except oracledb.Error as error:
        print("Error connecting to Oracle:", error)

    finally:
    # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()




    
        
