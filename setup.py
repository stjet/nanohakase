from setuptools import setup

setup(
    name="nanohakase",
    url="https://github.com/jetstream0/nanopie",
    author="John Doe",
    author_email="prussia@prussia.dev",
    packages=["nanohakase"],
    install_requires=["requests", "ed25519_blake2b"],
    version="0.0.5",
    license="MIT",
    description="A python library to simplify sending and receiving Nano. Also a RPC wrapper. Self fork of bananopie.",
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5"
)
