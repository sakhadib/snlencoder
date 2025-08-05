from setuptools import setup, find_packages

setup(
    name='snlencoder',
    version='0.1',
    packages=find_packages(),
    description='Compact 16-bit binary encoder for Snake and Ladder game moves with parity check',
    author='Sakhawat Adib',
    author_email='sakhawat.adib@email.com',
    url='https://github.com/sakhadib/snlencoder',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
