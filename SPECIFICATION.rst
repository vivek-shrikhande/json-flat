
Specification (what in input becomes what in output?)
-----------------------------------------------------
There is no standard specification on the internet for flattening json (or converting json to csv). As the primary use case of this library was to get the csv out of json document stores, we looked at how various such data stores visualize the underlying json into a tabular format. We understood the relations between the various structures in the json using real world examples and came up with the following specification. 

There exist four types of relations in a json data viz.,

Generalized statement: ``<parent>-<child> = <parent> containing <child>``

#. object-object (object containing object)
#. object-array (object containing array)
#. array-object (array containing object)
#. array-array (array containing array)

Conversion
^^^^^^^^^^
The conversion process is called flattening in the context of this library. There are two kinds of flattening.

#. Object flattening
    Objects get converted to columns. Keys in the object represent the column headings in csv and values of the object represent column data. Nested object keys get converted to column headings in the ``<parent_object_key>.<child_object_key>`` pattern. An object (irrespective of size i.e. no of key/value pairs) flattening will produce a single row in the csv.
    
    Example: (Person1 object)

    .. code-block:: json
    
        {
            "name": "some_name",
            "address": {
                "country": "some_country",
                "state": "some_state",
                "street": "1st street",
                "building_no": "2",
                "house_no": 3
            }
        }


    .. list-table::
        :widths: 25 25 25 25 25 25
        :header-rows: 1

        * - name
          - address.country
          - address.state
          - address.street
          - address.building_no
          - address.house_no
        * - some_name
          - some_country
          - some_state
          - 1st street
          - 2
          - 3

    Here, the person has the nested ``address`` object. Each of the nested attributes like ``country``, ``state`` etc. directly belong to the person. ``address`` object is just used to group those logically related attributes into one object. So, object-object is a one-to-one relation.

#. Array flattening
    Arrays get converted to rows. Elements in the array represent the rows in csv. An array (with n elements) flattening will produce at least n rows in csv.

    Example: (Person2 object)

    .. code-block:: json

        {
            "name": "some_name",
            "addresses": [
                {
                    "country": "some_country",
                    "state": "some_state",
                    "street": "1st street",
                    "building_no": "2",
                    "house_no": 3
                },
                {
                    "country": "some_other_country",
                    "state": "some_other_state",
                    "street": "4th street",
                    "building_no": "5",
                    "house_no": 6
                }
            ]
        }

    .. list-table::
        :widths: 25 25 25 25 25 25
        :header-rows: 1

        * - name
          - address.country
          - address.state
          - address.street
          - address.building_no
          - address.house_no
        * - some_name
          - some_country
          - some_state
          - 1st street
          - 2
          - 3
        * - some_name
          - some_other_country
          - some_other_state
          - 4th street
          - 5
          - 6


    Here, the person has the nested ``address`` array (each array element being an ``address`` object). Looking at the data, we can say that the person has two addresses. Hence, when we flatten it, we get two rows (corresponding to two addresses) in the output both of which have the same name but different addresses. Hence, object-array is a one-to-many relation. So is array-object relation.

For the array-array relation (redundant relation) let’s consider the following example (student book list),

.. code-block:: json

    [
        "Operating systems",
        "Software Engineering"
        [
            "Java",
            "Python",
            "Go"
        ]
        "Data structures and algorithms",
    ]

``"Java"``, ``"Python"`` and ``"Go"`` are grouped into an array as they are all books on programming languages. But all the books belong to the same student book list. Hence, it’s a one-to-one relation. When you flatten this data, the information of grouping ``"Java"``, ``"Python"`` and ``"Go"`` is lost.

As a general rule, one-to-one relations will produce a single child row in the parent whereas one-to-many will produce many child rows in the parent.
