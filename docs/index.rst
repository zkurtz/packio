packio reference guide
============================

- packio is collection of utilities for working with pandas objects.
- We're `on pypi <https://pypi.org/project/packio/>`_, so ``pip install packio``
- `Github repo <https://github.com/zkurtz/packio>`_

.. rst-class:: quick-links

Quick Links
-----------

Here's an overview of the main features. Click on the links for detailed API documentation:

* :func:`packio.zipping.zip`: A simple wrapper for `shutil.make_directory`, defaulting to use the `zip` format.
* :func:`packio.zipping.unzip`: Uses `zipfile` to unzip a zip archive.
* :func:`packio.zipping.zipflat`: Builds a flat zip archive from a list of file fullpaths.
* :func:`packio.zipping.unzipflat`: Unzips a flat zip archive into a directory.
* :class:`packio.io.Writer`: A context manager to write python objects directly to a zip archive. 
* :class:`packio.io.Reader`: A context manager to read python objects directly from a zip archive.

.. toctree::
   :maxdepth: 3
   :caption: Standard docs tree

   autoapi/packio/index
