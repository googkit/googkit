Requirements
============
When you are using python 3.2 or ealier, you should install the [mock](http://www.voidspace.org.uk/python/mock/) module.

	$ easy_install -U mock
	$ easy_install coverage

or, even:

	$ pip install -U mock
	$ pip install coverage
	


How to Test
===========
+ Run a unit test

		(in /usr/local/googkit)
		$ python -m {test_module_name}


* Run all unit tests

		(in /usr/local/googkit)
		$ python -m unittest discover

	You can try to test on python 3.x

	 	$ python3 -m unittest discover


How to measure test coverage
============================
1. Run a unit test by coverage

		(in /usr/local/googkit)
		$ coverage run -m unittest discover


2. Display report

   * on terminal

   		$ coverage report


   * on web browser (you can see more detail)

   		$ coverage html
   		$ open ./coverage-html/index.html


How to Add Test
===============
Add a test file to `test/` with the following template.


Template for Unit Test
----------------------
This is an example to unit-test a sample module.


```
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
