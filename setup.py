from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='tekuila',
      version='0.1.1',
      description='Script for checking TekSavvy Quota',
      long_description=readme(),
      url='https://github.com/mikeodr/tekuila',
      author="Mike O'Driscoll",
      author_email="mike@mikeodriscoll.ca",
      license='GPL2',
      packages=['tekuila'],
      scripts=['bin/tekuila'],
      install_requires=[
              "configobj",
      ],
      zip_safe=False)
