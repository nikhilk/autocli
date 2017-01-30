# setup.py
#

import setuptools

setuptools.setup(
  name='autocli',
  version='0.6',
  author='Nikhil Kothari',
  description='Builds command line interfaces to parse objects or call functions',
  license='BSD',
  keywords='argparse automatic cli parser',
  url='https://github.com/nikhilk/autocli',
  packages=[
    'autocli'
  ],
  install_requires = [
    'argparse',
    'enum34'
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Topic :: Utilities',
    'License :: OSI Approved :: BSD License'
  ],
)
