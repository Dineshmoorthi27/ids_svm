import streamlit as st
import mysql.connector
import account
import login
from PIL import Image
import requests
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie

import testing

st.set_page_config(page_title="IDS",layout="wide")

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='ids'
)
cursor = conn.cursor()
class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):

        self.apps.append({
            "title": title,
            "function": func
        })

    def run():
        # Function to load Lottie URL
        def load_lottieurl(url):
            r = requests.get(url)
            if r.status_code != 200:
                return None
            return r.json()
        # ---css style for contanct form ---

        def local_css(filename):
            with open(filename) as f:
                st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)
        local_css("style/style.css")

        # ---- LOAD ASSETS ----
        # Consider resizing images for responsiveness
        lottie_coding= load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")
        img_contact_form = Image.open("images/Learn-about-benefits-of-document-management-system-banner-1024x332.webp").resize((500, 430))

        st.title("NETWORK ANOMALY DETECTION USING BORDERLINE SMOTE ALGORITHM AND SUPPORT VECTOR MACHINES")
        with st.sidebar:
            selected = option_menu(
                menu_title="Menu",
                options=["Home","Account", "Documents", "Model_Test", "Contact"],
                icons=["house","person-circle","files","file-check","person-rolodex"],#bootstrp icon names are included here
                menu_icon="cast",
                default_index=0,
            )

        if selected == "Home":
            with st.container():
                st.subheader("Hi, I am Dinesh :wave:")
                st.write("#")
                st.write("This is the project to detect the  Network intrusion ")
            with st.container():
                # Abstract section
                st.write("---")
                left_column, right_column = st.columns(2)
                with left_column:
                    st.header("Abstract of our project")
                    st.write("##")
                    st.write("""Network Security is a major challenge in the digital world. Intrusion is common in many applications and intruders are sophisticated enough to change their attack pattern very often. 
                                To address this issue, the development of a model for the detection of network anomalies and intrusions. The approach utilizes the Borderline Synthetic Minority Over-Sampling Technique (SMOTE) along with Support Vector Machines (SVM) to enhance anomaly detection capabilities. By intelligently oversampling the minority class using SMOTE and training SVM, the proposed model exhibits a robust defence mechanism against network intruders. The utilization of these advanced techniques aims to augment the accuracy and efficiency of anomaly detection, minimizing false positives and ensuring prompt response to genuine threats. 
                                The results obtained from this study add to the ongoing efforts to secure data in the digital age, by combining SMOTE and SVM for network intrusion detection. 
                                """)
                with right_column:
                    st_lottie(lottie_coding, height=300, key="coding")

            # Projects section
            with st.container():
                st.write("---")
                st.header("project overview")
                st.write("##")
                image_column, text_column = st.columns((1, 2))
                with image_column:
                    st.image(img_contact_form)
                with text_column:
                    st.write(
                        """Digital transformation is taking place in most sectors around the world. A drastic effort of networking systems globally
                             has given the advantage of unlimited access to data and knowledge. With the growth in digital systems the growth of users with a malicious intent has also started to grow. 
                             Early intrusions have been made in the late 1970s and early 1980s. This was a period when most systems were not networked with one another, and internet was in a rudimentary state. 
                             Hence, the impact of any such intrusions cost only a few individuals and to the worst case, an organisation. As the years passed, more organisations entered the digital domain and started doing business online. 
                             The malicious users also started experimenting with sophisticated tools for intruding into systems over which business is done. Over the years, the pattern of intrusion has also changed. Some users with a malicious intent still try the classical intrusion techniques, which are usually detected by intrusion detection systems.
                            These classical methods follow a specific signature and hence can be detected by a signature-based intrusion detection system. However, advanced malicious users use different patterns of intrusion which are least detected by signature-based intrusion detection systems.
                            Such patterns can only be detected using an anomaly detection system.
                            These systems harness the power of artificial intelligence to perform anomaly detection. In the recent days, machine learning is applied in a higher level to detect such intrusions."""
                    )
        if selected == "Account":
            #account.login() --->used to firebase login
            login.creation()  #---> used local xamp db


        if selected == "Documents":
            st.write("Here is the document for our project")

        if selected == "Model_Test":
            testing.testing_csv()


        if selected == "Contact":
            st.header("Get in touch with me!")

            # Define form inputs
            form_name = st.text_input("Your name")
            form_email = st.text_input("Your email")
            form_message = st.text_area("Your message here")
            submit_button = st.button("Send")

            if submit_button:
                # Insert form data into the database
                query = "INSERT INTO form_submissions (name, email, message) VALUES (%s, %s, %s)"
                cursor.execute(query, (form_name, form_email, form_message))
                conn.commit()
                # Clear form values after successful submission
                form_name = ""
                form_email = ""
                form_message = ""

                st.success("Form submitted successfully!")
                # Rerun the app to reset the form values
                st.experimental_rerun()

                # Close the connection
                cursor.close()
                conn.close()
                # Display the form with updated values
                st.text_input("Your name", value=form_name)
                st.text_input("Your email", value=form_email)
                st.text_area("Your message here", value=form_message)
    run()
