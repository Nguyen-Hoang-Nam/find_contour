from setuptools import setup

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setup(
    name = 'fcontour',
    version = '0.1.0',
    author = 'Nguyen Hoang Nam',
    author_email = 'nguyenhoangnam.dev@gmail.com',
    description = 'Find contour with Canny',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/Nguyen-Hoang-Nam/fcontour',
    packages = ['fcontour'],
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires = '>=3.6',
    entry_points = {
        'console_scripts': [
            'fcontour = fcontour.__main__:main'
        ]
    },
)