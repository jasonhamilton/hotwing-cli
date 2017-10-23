from distutils.core import setup

setup(
    name='hotwing_cli',
    version='0.1.0',
    url='https://github.com/jasonhamilton/hotwing_cli',
    packages=['hotwing_cli',],
    license='GPLv3',
    long_description=open('README.md').read(),
    keywords='development cnc gcode airfoil',
    entry_points = {
        'console_scripts': ['hotwing-cli=hotwing_cli:main'],
    },
    install_requires=['hotwing-core','click',],
    classifiers=[

        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.6',
        # 'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.2',
        # 'Programming Language :: Python :: 3.3',
        # 'Programming Language :: Python :: 3.4',
    ],
)