from setuptools import setup, find_packages

setup(
    name='weatherweb',
    version='0.1',
    url='http://www.geographie.uni-bremen.de/en/climate-geography',
    license='MIT',
    author='Timo Rothepieler',
    author_email='timo.rothenpieler@uni-bremen.de',

    packages=find_packages(),
    include_package_data=True,

    install_requires=[
        "Flask",
        "Flask-SQLAlchemy",
        "Flask-Script",
        "Flask-Assets",
        "Flask-WTF",
        "Jinja2",
        "jsmin",
        "cssmin",
        "Werkzeug",
        "pyserial",
        "pytz",
    ],

    entry_points={
        'console_scripts': [
            'weatherweb_manage = weatherweb.cron:run_manager'
        ]
    }
)
