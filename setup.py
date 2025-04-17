from setuptools import setup, find_packages

setup(
    name="template_project",
    version="0.1.0",
    description="A Python project template with CI/CD workflows",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/your-username/template-repo",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "requests>=2.28.0",
        "numpy>=1.21.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "flake8>=4.0",
            "black>=22.0",
            "mypy>=1.0",
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
            "bandit>=1.7",
            "safety>=2.4",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
        ],
        "test": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
        ],
    },
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "template-cli = template_project.main:main",  # Adjust if needed
        ],
    },
    zip_safe=False,
)
