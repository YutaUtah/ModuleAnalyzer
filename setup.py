from setuptools import find_packages, setup

setup(
    name='pystats',
    version='1.1',
    description='Python Module Analyzer',
    author='Yuta Hayashi',
    author_email='yuta.hayashi96@gmail.com',
    url='https://github.com/YutaUtah/ModuleAnalyzer',
    keywords=['python module', 'analyzer', 'file management', 'search', 'python'],
    license='MIT',
    classifiers=[],
    packages=find_packages(exclude=('tests', 'tests.*')),
    entry_points={
        'console_scripts':[
            'pystats = pystats.__main__:main',
        ],
    },
)