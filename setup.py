from setuptools import setup

version = '0.0.1'
name = 'biscuit'
short_description = 'Auto tagging tool for Pocket ( https://getpocket.com/ )'


setup(
    name=name,
    version=version,
    author='Shoji Sugai',
    author_email="k952i4j14x17@gmail.com",
    description=short_description,
    url='https://github.com/mikanfactory/biscuit',
    packages=['biscuit'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
)
