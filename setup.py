from setuptools import setup, find_packages

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="spam-classification",
    version="0.1.0",
    description="SMS Spam Classification with ML and Agent",
    author="ligap123",
    author_email="ligap123@example.com",
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.12",
    entry_points={
        "console_scripts": [
            "spam-classification=src.streamlit_app:main",
        ],
    },
)
