from setuptools import setup, find_packages

setup(
    name="smartsearch",
    version="1.0.0",
    author="Mohammad Arifur Rahman",
    description="Search keywords in PDF files with web interface",
    long_description="Smart Search PDF allows you to upload PDF files and search for keywords with a clean web interface built with Streamlit.",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.28.0",
        "pandas>=1.5.0", 
        "PyMuPDF>=1.23.0",
    ],
    entry_points={
        "console_scripts": [
            "smartsearch=smartsearch.run:main",
        ],
    },
    package_data={
        "smartsearch": ["styles.css"],
    },
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", 
        "Operating System :: OS Independent",
    ],
)