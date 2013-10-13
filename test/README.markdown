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


	* on web browser (you can see detailed information):

		$ coverage html
		(then open ./coverage-html/index.html in your browser)


Adding Test Case
----------------
Add a test file to `test/`.
Following template may be useful:

```python
# Run the following command to test:
#
#     (in /usr/local/googkit)
#     $ python -m {test_module_name}
#
# See also: http://docs.python.org/3.3/library/unittest.html#command-line-interface
#
# We cannot use unittest.mock on python 2.x!
# Please install the Mock module when you use Python 2.x.
#
#     $ easy_install -U Mock
#
# See also: http://www.voidspace.org.uk/python/mock/#installing

import unittest
if not hasattr(unittest, 'mock'):
    # Python 2.x or 3.2-
    import mock
else:
    # Python 3.3 or later
    import unittest.mock as mock


# Import your module here
import sample


class TestSample(unittest.TestCase):
    def test_method(self):
        self.assertEquals(sample.method(), 'something')


if __name__ == '__main__':
    unittest.main()
```
