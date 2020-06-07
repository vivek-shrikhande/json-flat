import setuptools

with open('README.rst', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='json-flat',
    version='1.0.0',
    author='Vivek Shrikhande',
    author_email='vivekshrikhande444@gmail.com',
    description='A Python library to flatten a nested json',
    long_description=long_description,
    url='https://github.com/vivek-shrikhande/json-flat',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='~=3.6',
)
