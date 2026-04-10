from setuptools import setup, find_packages

setup(
    name="github-scraper",
    version="1.0.0",
    description="GitHub 数据分析与爬虫工具",
    author="wdg631",
    packages=find_packages(),
    python_requires=">=3.9",
    entry_points={
        "console_scripts": ["gh-scraper=main:main"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
