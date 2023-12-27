import streamlit as st
import pickle
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import SelectKBest, mutual_info_classif
from sklearn.metrics import accuracy_score, confusion_matrix

# Streamlit app
# Function to preprocess data and make predictions
def preprocess_and_predict(model, new_data):
    new_data_clean = new_data.replace([np.inf, -np.inf], np.nan).dropna()
    new_data_clean = new_data_clean.dropna()

    X_new = new_data_clean.drop(' Label', axis=1)  # Adjust according to your columns
    y_new = new_data_clean[' Label']  # Adjust according to your column name

    scaler = MinMaxScaler()
    imputer = SimpleImputer(strategy='mean')

    selector = SelectKBest(mutual_info_classif, k=14)
    X_train_selected = selector.fit_transform(X_new, y_new)
    X_new_selected = selector.transform(X_new)

    scaler.fit(X_train_selected)
    X_new_selected_scaled = scaler.transform(X_new_selected)
    X_new_selected_scaled_imputed = imputer.fit_transform(X_new_selected_scaled)

    y_pred_new = model.predict(X_new_selected_scaled_imputed)
    accuracy = accuracy_score(y_new, y_pred_new)

    return y_pred_new, accuracy

def testing_csv():
    st.subheader(' IDS Prediction Model')
    # Load the saved model
    loaded_model = pickle.load(open('_14_model.sav', 'rb'))
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        new_data = pd.read_csv(uploaded_file)

        predictions, accuracy = preprocess_and_predict(loaded_model, new_data)

        if predictions[0] == 1:
            pass
        else:
            import smtplib
            from email.mime.text import MIMEText

            subject = "Intrusion Alert"
            body = "An intrusion has been detected on the network. Please investigate immediately."
            sender = "dineshmoorthi27@gmail.com"
            recipients = ["projecttestingfyp@gmail.com"]
            password = "wtai ayeq zfwa tiwr"


            def send_email(subject, body, sender, recipients, password):
                msg = MIMEText(body)
                msg['Subject'] = subject
                msg['From'] = sender
                msg['To'] = ', '.join(recipients)
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
                    smtp_server.login(sender, password)
                    smtp_server.sendmail(sender, recipients, msg.as_string())
                st.write("Message Alert sent successfully!")


            send_email(subject, body, sender, recipients, password)

        st.write(f"### Accuracy: {accuracy * 100:.4f}%")
        # Display confusion matrix
        cm = confusion_matrix(new_data[' Label'], predictions)
        st.write("### Confusion Matrix:")
        #st.write(cm)
        # Create a figure and axis objects explicitly
        fig, ax = plt.subplots()
        sns.heatmap(cm, annot=True, linewidth=0.5, linecolor="red", fmt=".0f", ax=ax)
        plt.xlabel("y_pred")
        plt.ylabel("y_true")
        st.pyplot(fig)
