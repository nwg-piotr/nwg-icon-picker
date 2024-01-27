import os

from setuptools import setup, find_packages


def read(f_name):
    return open(os.path.join(os.path.dirname(__file__), f_name)).read()


setup(
    name='nwg-icon-picker',
    version='0.1.1',
    description='GTK icon picker with textual search',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "": ["resources/*"]
    },
    url='https://github.com/nwg-piotr/nwg-icon-picker',
    license='MIT',
    author='Piotr Miller',
    author_email='nwg.piotr@gmail.com',
    python_requires='>=3.6.0',
    install_requires=[],
    entry_points={
        'gui_scripts': [
            'nwg-icon-picker = nwg_icon_picker.main:main',
        ]
    }
)
