import setuptools
import sys

setuptools.setup(
    name='uniplate',
    version='0.0.2',
    description='Python generics library using combinators from haskell\'s uniplate',
    author='Edward George',
    author_email='edwardgeorge@gmail.com',
    url='https://github.com/edwardgeorge/uniplate',
    # packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
    py_modules=['uniplate'],
    install_requires=["singledispatch"] if sys.version_info < (3, 4) else [],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python",
    ]
)
