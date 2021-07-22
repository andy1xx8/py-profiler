import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_profiler",
    version="0.2.0",
    author="Andy Le",
    author_email="tauit.dnmd@gmail.com",
    description="A library to measure your method, function execution time.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andy1xx8/py-profiler",
    project_urls={
        "Bug Tracker": "https://github.com/andy1xx8/py-profiler/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    include_package_data=True,
    package_data={
        # If any package contains *.txt files, include them:
        "": ["*.txt"],
        "py_profiler": ["templates/*.html"],
    },
    python_requires=">=3.6",
)