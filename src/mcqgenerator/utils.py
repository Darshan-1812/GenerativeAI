import os
import json
import traceback
from PyPDF2 import PdfReader

def read_file(file):
    try:
        if file.name.endswith(".pdf"):
            text = ""
            pdf_reader = PdfReader(file)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
            return text.strip()
        
        elif file.name.endswith(".txt"):
            return file.read().decode("utf-8")
        
        else:
            raise Exception("Unsupported file format. Only PDF and TXT are supported.")
    
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        raise Exception("Error reading the file.")

def get_table_data(quiz_str):
    try:
        # Convert the quiz JSON string to a dictionary
        quiz_dict = json.loads(quiz_str)
        quiz_table_data = []

        for key, value in quiz_dict.items():
            mcq = value["mcq"]
            options = " || ".join(
                [f"{option} -> {option_text}" for option, option_text in value["options"].items()]
            )
            correct = value["correct"]
            quiz_table_data.append({
                "MCQ": mcq,
                "Choices": options,
                "Correct": correct
            })

        return quiz_table_data

    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return None
