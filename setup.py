from setuptools import setup, find_packages

setup(
    name="trader_ai",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'python-binance',
        'pandas',
        'numpy',
        'scikit-learn',
        'torch',
        'python-dotenv',
        'psycopg2-binary',
        'sqlalchemy',
        'rich',
    ]
)
