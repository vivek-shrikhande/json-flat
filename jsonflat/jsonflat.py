"""Module responsible for flattening the input json."""

from functools import reduce
from itertools import zip_longest

from .field import Field


class JsonFlat:
    """Class responsible for flattening the input json."""

    def __init__(self, field_infix_char='.', root_element_name='##'):
        self._field_infix_char = field_infix_char
        self._root_element_name = root_element_name

    def _a_flat(self, input_rows, fields=None, key_so_far=None):
        if fields is None:
            fields = Field(False)

        output_rows = list()
        absolute_key = (self._root_element_name if key_so_far is None
                                                else key_so_far)

        for input_row in input_rows:
            if isinstance(input_row, dict):
                # lol - lists of lists
                _, row, lol = self._o_flat(input_row, fields, key_so_far)
                if lol:
                    for tpl in zip_longest(*lol, fillvalue={}):
                        output_rows.append(
                            {**row, **reduce(lambda d1, d2: {**d1, **d2}, tpl)}
                        )
                else:
                    output_rows.append(row)

            elif isinstance(input_row, list):
                output_rows.extend(self._a_flat(input_row,
                                                fields,
                                                key_so_far)[-1])

            else:
                output_rows.append({absolute_key: input_row})
                fields.set_self()

        return fields, output_rows

    def _o_flat(self, input_row, fields=None, key_so_far=None):
        output_row, lol = dict(), list()

        if fields is None:
            fields = Field(False)

        if not input_row and key_so_far is not None:
            fields.set_self()
            output_row[key_so_far] = None

        key = '' if key_so_far is None else key_so_far + self._field_infix_char

        for k, v in input_row.items():
            absolute_key = key + k

            if isinstance(v, dict):
                _, row, _lol = self._o_flat(v,
                                            fields.set_field_group(k),
                                            absolute_key)
                output_row.update(row)
                lol.extend(_lol)

            elif isinstance(v, list):
                _, rows = self._a_flat(v,
                                       fields.set_field_group(k),
                                       absolute_key)
                if rows:
                    lol.append(rows)
                else:
                    fields.set_field(k)
                    output_row[absolute_key] = None

            else:
                output_row[absolute_key] = v
                fields.set_field(k)

        return fields, output_row, lol

    def flatten(self, input_rows):
        """Returns a flattened version of the input_rows."""
        if not isinstance(input_rows, list):
            input_rows = [input_rows]

        fields, output_rows = self._a_flat(input_rows)
        norm_fields = fields.get_normalized_fields(self._field_infix_char,
                                                   self._root_element_name)
        return {'field_names': norm_fields, 'rows': output_rows}
