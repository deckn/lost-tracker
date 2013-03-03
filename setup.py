from setuptools import setup, find_packages
setup(
   name="lost-tracker",
   version="1.2",
   packages=find_packages(),
   install_requires=[
        'Flask==0.9',
        'Flask-SQLAlchemy==0.16',
        'SQLAlchemy==0.8.0b2',
        'psycopg2==2.4.6',
      ],
   package_data={'lost_tracker': [
       'templates/*.html',
       'static/icons/*.png',
       'static/js/*.js'
       ]},
   author="Michel Albert",
   author_email="michel@albert.lu",
   description="Tracker for Lost in the Darkness",
   license="BSD",
   url="http://exhuma.github.com/lost-tracker",
)
