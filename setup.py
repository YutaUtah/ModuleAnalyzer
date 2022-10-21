from setuptools import find_packages, setup

setup(
    name='pystats',
    version='1.1',
    description='Python Module Analyzer',
    author='Yuta Hayashi',
    author_email='yuta.hayashi96@gmail.com',
    url='https://github.com/YutaUtah/ModuleAnalyzer',
    keywords=['design', 'pattern', 'patterns', 'pattyrn', 'template'],
    license='MIT',
    classifiers=[],
    packages=find_packages(exclude=('tests', 'tests.*')),
)