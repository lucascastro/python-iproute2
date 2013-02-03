# coding=utf-8
from distutils.core import setup


f = open('README.rst')
try:
    readme_content = f.read()
except:
    readme_content = ''
finally:
    f.close()

setup(
    name='python-iproute2',
    version='0.0.5',
    packages=['iproute2'],
    url='https://github.com/nwhalen/python-iproute2',
    download_url='https://github.com/nwhalen/python-iproute2/tarball/master',
    author='Nick Whalen',
    long_description=readme_content,
    requires=['cidrize (>=0.6.3)'],
    packages=['iproute2'],
    provides=[''],
    keywords='iproute2',
    author_email='nickw@mindstorm-networks.net',
    description='iproute2 helper package for Python',
    license='Apache License 2.0',
    classifiers=['Development Status :: 3 - Alpha',
                 'Intended Audience :: Developers',
                 'Natural Language :: English',
                 'Operating System :: POSIX :: Linux',
                 'Programming Language :: Python :: 2',
                 'License :: OSI Approved :: Apache Software License',
                 'Topic :: Software Development :: Libraries',
                 'Topic :: Software Development :: Libraries :: Python Modules',
                 ],
)
