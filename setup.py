from setuptools import setup, find_packages

setup(
    name="SurrealTools",
    version="1.0.0",
    author="isrt",
    description="Ein stylisches Terminal-Tool-Hub für Network, Osint und Utilities.",
    long_description_content_type="text/markdown",
    url="https://github.com/skorbjen",
    packages=find_packages(),
    py_modules=["SurrealTools"],
    install_requires=[
        "colorama>=0.4.6",
        # Falls deine Tools in src/ weitere Libraries brauchen, hier ergänzen:
        # "requests",
        # "scapy",
        # "pillow", 
    ],
    entry_points={
        "console_scripts": [
            "surreal=SurrealTools:main_menu",
        ],
    },
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)