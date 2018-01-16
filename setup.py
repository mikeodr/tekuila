from setuptools import setup

from tekuila import __version__ as VERSION

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='tekuila',
      packages=['tekuila',
                'tekuila.isp'],
      version=VERSION,
      description='Script for checking TekSavvy (and other ISP) Quotas',
      long_description=readme(),
      url='https://github.com/mikeodr/tekuila',
      author="Mike O'Driscoll",
      author_email="mike@mikeodriscoll.ca",
      license='GPL2',
      install_requires=[
          "future",
          "configobj",
          "xmltodict"
      ],
      entry_points={
          'console_scripts': [
              'tekuila = tekuila.quota:main'
          ]
      })
