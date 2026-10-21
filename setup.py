from setuptools import setup
import os


def package_files(package, directory):
    paths = []
    for (path, directories, filenames) in os.walk(package+"\\"+directory):
        for filename in filenames:
            paths.append(os.path.join('..', directory, filename))
    return paths


setup(
    name='BEaSTagger',
    version='1.2',
    packages=['beast'],
    install_requires=[
        'torch>=2.6,<3',
        'spacy>=3.7.5,<3.8',
        'tqdm>=4.44.1',
        'numpy>=1.26.4,<2',
        'pandas>=2.2.3,<3',
        'scikit-learn~=1.6.1',
        'setuptools>=49.2.1',
        'requests>=2.32.5,<3',
        'click>=8.1,<9'
    ],
    extras_require={'stanza': ['stanza>=1.12.2']},
    package_data={'beast': package_files('beast', 'data\\default')},
    include_package_data=True,
    url='https://github.com/procesaur/BEaSTagger',
    license='GPL',
    author='Mihailo Škorić',
    author_email='procesaur@gmail.com',
    description='POS tagging tool based on Bidirectional, Expandable and Stacked architecture.'
)
