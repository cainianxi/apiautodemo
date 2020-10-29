from setuptools import setup, find_packages

setup(name="pytest-autotest",
      version="2.1.0",
      description="pytest autotest plugins",
      author="QA",
      packages=find_packages(),
      include_package_data=True,
      py_modules=['pytest_autotest'],
      keywords='py.test pytest autotest',
      install_requires=[
          "pytest==3.3.2",
          "allure-pytest==2.2.3b1",
          "pyyaml",
          "objectpath",
          "pytz",
          "numpy",
          "regex",
      ],
      entry_points={"pytest11": ["pytest_autotest = pytest_autotest"]}

      )
