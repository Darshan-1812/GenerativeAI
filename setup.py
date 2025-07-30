from setuptools import find_packages,setup

setup(
    name='mcqgenrator',
    version='0.0.1',
    author='darshan girase',
    author_email='darshangirase18@gmail.com',
    install_requires=["google-generativeai","langchain","streamlit","python-dotenv","PyPDF2"],
    packages=find_packages()
)