Unit-Testing Googkit
====================


System Requirements
-------------------
`coverage` is required for measuring test coverage:

	$ easy_install coverage

If you are using python 3.2 or ealier, you should install [mock](http://www.voidspace.org.uk/python/mock/) module:

	$ easy_install -U mock


Running Unit Tests
------------------
* Running a specified unit test:

		(in /usr/local/googkit)
		$ python -m {test_module_name}


* Running all unit tests:

		(in /usr/local/googkit)
		$ python -m unittest discover

	If you want to run unit tests with python 3.x:

	 	$ python3 -m unittest discover


Measuring test coverage
-----------------------
1. Run all unit tests with `coverage`

		(in /usr/local/googkit)
		$ coverage run -m unittest discover


2. Display report

	* on the terminal:

		$ coverage report


	* on the web browser (you can see detailed information):

		$ coverage html
		(then open ./coverage-html/index.html in your browser)


Adding Test Case
----------------
Add a test file to `test/`.
Following template may be useful:

```python
import unittest
try:
    # Python 3.3 or later
    import unittest.mock as mock
except ImportError:
    # Python 2.x or 3.2-
    import mock


# Import your module here
import sample


class TestSample(unittest.TestCase):
    def test_method(self):
        self.assertEquals(sample.method(), 'something')


if __name__ == '__main__':
    unittest.main()
```
