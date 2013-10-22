Unit-Testing Googkit
====================


Requirements
------------
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
import googkit.compat.unittest

# Import your module here
import sample


class TestSample(unittest.TestCase):
    def test_method(self):
        self.assertEquals(sample.method(), 'something')


if __name__ == '__main__':
    unittest.main()
```


### Using doctest
If you want to use [doctest](http://docs.python.org/3.3/library/doctest.html#module-doctest),
add the following test file to `test/`.

```python
import unittest
import doctest
import sample


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(sample))
    return tests


if __name__ == '__main__':
    unittest.main()
```
