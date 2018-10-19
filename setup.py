import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tf_tagfresh",
    version="0.0.2",
    author="Afraz",
    author_email="afrazkhan@gmail.com",
    description="Check your Terraform sources are fresh",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/afrazkhan/tf_tagfresh",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts=['scripts/tf_tagfresh.py'],
    zip_safe=False
)
