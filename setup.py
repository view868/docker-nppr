from setuptools import setup, find_packages

setup(
    name='docker-nppr',
    version='0.0.1',
    keywords=('pip', 'docker', 'django', 'python', 'postgresql', 'redis', 'fabric'),
    description='A nginx/django/postgresql/redis quick deployment tool on docker',
    long_description=open('README.rst').read(),
    author='view',
    author_email='view868@gmail.com',
    license='BSD License',
    packages=find_packages(),
    include_package_data=True,
    platforms=['Any'],
    install_requires=['fabric3', 'PyYAML'],  # 这个项目需要的第三方库
    url='',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
