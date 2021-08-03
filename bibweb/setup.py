from setuptools import setup, find_packages


setup(
    name="bibweb",
    version="0.1",
    install_requires = [
        "jinja2",
        "click"
     ],
    packages=find_packages('.'),
    package_dir={'': '.'},
    entry_points={
        'console_scripts' :[
            'bib2json=bibweb.bib2:bib2json',
            'bib2html=bibweb.bib2:bib2html'
        ]
        }
)
