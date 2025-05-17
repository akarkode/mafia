from setuptools import setup, find_packages

setup(
    name='mafia',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'fastapi', 
        'scikit-learn', 
        'redis', 
        'httpx'
    ],
    author='akarkode',
    description='Middleware AI Firewall & Injection Avoidance',
    python_requires='>=3.8',
)
