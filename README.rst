json-flat
=========
A Python library to flatten a nested json.

(Try out online at https://vivek-shrikhande.github.io/json-to-csv-web-app)

Use cases
---------
* To get a csv file [1]_ out of the json document stores like elasticsearch, mongodb, bigquery etc [2]_. All of these databases allow their documents to be nested. Out there are plenty of libraries which can convert plain json (not nested) to csv but really suck when the json is nested. This is the real use case we wanted to solve and this library came out as a result.

Installation
------------
.. code-block:: Python

    pip install json-flat

Quick Start
-----------
.. code-block:: python

    from jsonflat import JsonFlat

    # Load the input json into python data structure.

    # An input list of rows (nested or plain).
    rows = [
        {'a': 1, 'b': {}, 'c': {'d': 73}},
        {'a': 'hello', 'b': ['thank', 'you']}
    ]

    print(JsonFlat().flatten(rows))

.. code-block:: python

    {
        'field_names': ['a', 'b', 'c.d'],
        'rows': [
            {'a': 1, 'b': None, 'c.d': 73},
            {'a': 'hello', 'b': 'thank'},
            {'a': 'hello', 'b': 'you'}
        ]
    }


* ``field_names`` is an array of all the fields (attributes) encountered in the input json. The order of the fields will be based on their appearance in input json. A field appearing first in the input json will be the first in the ``field_names``, second will be the second and so on.
* ``rows`` is an array containing the actual flattened rows. This is guaranteed to be always an array of objects irrespective of what the input looks like. No guarantee that the order of keys within each object is the same as that of the input (use ``field_names`` for ordering related stuff). Also no guarantee that each of these objects contain all the keys appearing in the ``field_names`` (use null as the value for the non-existing keys) but guaranteed to contain all the keys appearing in the input json corresponding to this object.

Documentation
-------------
Read the `documentation <https://github.com/vivek-shrikhande/json-flat/blob/master/DOCUMENTATION.rst>`_.

Specification (what in input becomes what in output?)
-----------------------------------------------------
Read the `specification <https://github.com/vivek-shrikhande/json-flat/blob/master/SPECIFICATION.rst>`_.

Footnotes
---------
.. [1] No native functionality in the library to get csv. Use Python's built in module ``csv`` on the flattened data.
.. [2] To be specific, Elasticsearch is a search engine, MongoDB is a database and BigQuery is a data warehouse. For simplicity, all of these are considered to be json document stores or simply databases. Defining what these applications exactly are isn't the goal of this documentation.
