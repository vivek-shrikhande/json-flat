Documentation
=============

class JsonFlat(field_infix_char='.', root_element_name='##')
------------------------------------------------------------

Main class responsible for flattening the json.

**Parameters**

- field_infix_char
    Character used to concatenate parent field name and child field name. Defaults to ``.``.

    **Example:**

    Input

    .. code-block:: json

        {"a": { "b": 123 }}

    Output

    .. code-block:: json

        {
            "field_names": ["a.b"],
            "rows": [
                { "a.b": 123 }
            ]
        }


- root_element_name
    Name to use when the input doesn't contain an attribute name (only occurs in case of arrays). Defaults to ``##``.

    **Example:**

    Input

    .. code-block:: json

        ["a", "b", 123]

    Output

    .. code-block:: json

        {
            "field_names": ["##"],
            "rows": [
                { "##": "a" },
                { "##": "b" },
                { "##": 123 }
            ]
        }

**Methods**

- flatten(input_rows)
    Returns a flattened version of the input_rows.

    - **input_rows** - The input data to flatten.
