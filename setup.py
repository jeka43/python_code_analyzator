from setuptools import setup, find_packages

setup(
    name='python_code_analyzator',  # Имя вашей библиотеки
    version='0.1.0',  # Текущая версия
    packages=find_packages(),  # Автоматически находит пакеты в проекте
    description='A library for analyzing Python code using GPT and PEP8.',  # Краткое описание
    long_description=open('README.md').read(),  # Подробное описание из README.md
    long_description_content_type='text/markdown',  # Формат README.md
    author='Evgeny',  # Ваше имя или псевдоним
    url='https://github.com/jeka43/python_code_analyzator',  # URL репозитория
    python_requires='>=3.6',  # Минимальная версия Python
    install_requires=[
        'requests',  # Зависимость для работы с HTTP-запросами
        'g4f>=0.2.0'  # Указание версии g4f, чтобы использовать актуальную
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license='MIT',  # Лицензия проекта
    include_package_data=True,  # Включить дополнительные файлы (например, данные внутри пакетов)
)
