from setuptools import setup

setup(name='SAS_Scraper',
      version='1.0',
      description='Tool for scraping nhl player stat data',
      url='https://github.com/fullrobot/SAS_Scraper.git',
      install_requires=[
        "beautifulsoup4==4.5.1",
        "bs4==0.0.1",
        "lxml==3.6.4",
        "argparse"],
      zip_safe=False)
