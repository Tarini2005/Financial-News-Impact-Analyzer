from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="financial-news-analyzer",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool that correlates financial news with market movements",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/financial-news-analyzer",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.20.0",
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
        "requests>=2.25.0",
        "nltk>=3.6.0",
        "yfinance>=0.1.70",
        "scikit-learn>=1.0.0",
        "wordcloud>=1.8.0",
        "tqdm>=4.60.0",
    ],
    entry_points={
        "console_scripts": [
            "financial-news-analyzer=financial_analyzer.cli:main",
        ],
    },
)
