from setuptools import find_packages, setup


setup(
    name="web-security-snapshot",
    version="0.1.0",
    description="Simple public web security posture snapshot CLI",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests>=2.32.0,<3.0.0",
        "certifi>=2024.0.0",
        "dnspython>=2.6.0,<3.0.0",
    ],
    entry_points={
        "console_scripts": [
            "websnapshot=websnapshot.cli:main",
        ]
    },
    python_requires=">=3.10",
)
