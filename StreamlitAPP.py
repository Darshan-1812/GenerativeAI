import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv

import streamlit as st
import sys
sys.path.append(os.path.abspath("./src"))


# Custom imports
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
 # Gemini-compatible chain

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Load the sample JSON format for response
with open(r'C:\Users\DARSHAN\OneDrive\Desktop\generativeAI\Response.json', 'r') as file:
    RESPONSE_JSON = json.load(file)

# App Header
st.write("Streamlit version:", st.__version__)
st.title("MCQ Creator with Gemini and LangChain")

# Form for user input
with st.form("user_inputs"):
    uploaded_file = st.file_uploader("Upload a PDF or TXT file")

    mcq_count = st.number_input("No. of MCQs", min_value=3, max_value=50)
    subject = st.text_input("Enter Subject", max_chars=20)
    tone = st.text_input("Complexity level of Questions", max_chars=20, placeholder="Simple")

    button = st.form_submit_button("Generate MCQs")

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Generating MCQs using Gemini..."):
            try:
                text = read_file(uploaded_file)

                # Call the Gemini-based LangChain pipeline
                response = generate_evaluate_chain.invoke({
                    "text": text,
                    "number": mcq_count,
                    "subject": subject,
                    "tone": tone,
                    "response_json": json.dumps(RESPONSE_JSON)
                })

            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("An error occurred while generating the quiz.")
            else:
                # Process and display results
                if isinstance(response, dict):
                    quiz = response.get("quiz", None)
                    if quiz:
                        table_data = get_table_data(quiz)
                        if table_data:
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            st.table(df)
                            st.text_area(label="Expert Review", value=response["review"])
                        else:
                            st.error("Error formatting the MCQ table.")
                    else:
                        st.error("Quiz generation failed.")
                else:
                    st.write("Unexpected output:", response)
