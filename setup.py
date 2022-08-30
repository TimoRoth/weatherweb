from setuptools import setup, find_packages

setup(
    name='weatherweb',
    version='0.1',
    url='https://www.geographie.uni-bremen.de/en/climate-geography',
    license='MIT',
    author='Timo Rothepieler',
    author_email='timo.rothenpieler@uni-bremen.de',

    packages=find_packages(),
    include_package_data=True,

    install_requires=[
        "Flask",
        "Flask-SQLAlchemy",
        "Flask-Assets",
        "Flask-WTF",
        "Flask-CacheControl",
        "Flask-Cors",
        "Jinja2",
        "jsmin",
        "cssmin",
        "htmlmin",
        "Werkzeug",
        "pyserial",
        "pytz",
        "tzlocal",
    ]
)
