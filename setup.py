from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='tekuila',
      version='2.0.0',
      description='Script for checking TekSavvy (and other ISP) Quotas',
      long_description=readme(),
      url='https://github.com/mikeodr/tekuila',
      author="Mike O'Driscoll",
      author_email="mike@mikeodriscoll.ca",
      license='GPL2',
      packages=['tekuila'],
      scripts=['bin/tekuila'],
      install_requires=[
              "configobj",
              "xmltodict"
      ],
      zip_safe=False)
