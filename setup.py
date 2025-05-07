from setuptools import setup, find_packages

setup(
    name='streamfuels',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas>=1.2.0',
        'requests>=2.25.0',
        'beautifulsoup4>=4.9.0',
        'unidecode>=1.1.1',
        'numpy>=1.19.0',
        'editdistance>=0.5.3',
        'setuptools',
        'tqdm==4.65.0'
    ],
    extras_require={
        #se houver incompatibilidade de versoes podemos fazer assim
        # 'forecasters': [
        #     'statsmodels>=0.12.0',  
        #     'pandas>=1.2.0',       
        # ],
        # 'regressors': [
        #     'scikit-learn>=0.24.0',
        #     'matplotlib>=3.3.0',  
        # ],
    },
    author='CENTRO INTEGRADO DE SOLUÇÕES EM INTELIGÊNCIA ARTIFICIAL',
    author_email='streamfuels@example.com',
    description='Data processing and analysis tools for fuel market research',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/streamfuels/streamfuels',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
