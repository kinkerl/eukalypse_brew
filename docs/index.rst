eukalypse_brew 
==========================================

Contents:

.. toctree::
   :maxdepth: 2

eukalypse_brew is a mixture of diffrent tests to make very basic functional testing of websites or features of websites possible.

 * Is my robots.txt or sitemap.xml still there and valid?
 * Does file1.pdf and file2.txt still exist, is my API responding and is the response valid?

I know you dont mistakes and most of the time and API libraries and helpers create valid things, but not always. Its important to trust your code but its more important to check if the user gets what he expects.

Brew is designed to be used in a - daily or hourly - testing suite but can be used in any other environment as well.


Take a look at the Tests for the usage.
For example, setup the Brew object of your website:

.. literalinclude:: ../tests/test_core.py
   :pyobject: MyBrewTest.setUp

check if the sitemap is ok:


.. literalinclude:: ../tests/test_core.py
   :pyobject: MyBrewTest.test_sitemap_success



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

