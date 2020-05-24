"""Contains Fields related code."""


class Field:
    """
    Data structure to store column names (aka fields).

    A Field can have sub Fields in it in which case it's called Field
    group (since it has a group of Fields/Field groups inside it).
    A Field can be at a time both Field and Field group. In the
    following data, 'location' is both a Field and a Field group.
    [
        {
            'location': '45.1, -42.6'
        },
        {
            'location': {
                'latitude': '63.2',
                'longitude': '67.8'
            }
        }
    ]
    The normalized Field list would be
    ['location', 'location.latitude', 'location.longitude']

    Field has only two attributes viz,
    __self - which tells it's parent whether it's a Field (True -
    default) or not (False),
    __data - which contains the reference to sub Fields/Field groups.
    A Field by default will not have this attribute declared; it gets
    created only when a new Field/Field group is added to it. Field
    group can have it's __data as {}.
    """

    def __init__(self, set_self=True):
        self.__self = set_self

    def set_field_group(self, name):
        """Create and return a new field group.

        A field group is a Field which has it's `__data` set.

        If a Field group with name `name` already exists, just return
        it; otherwise, create a new one and return.

        :param name: Name of the new Field group.
        :return: Newly created or existing Field group.
        """
        try:
            self.__data[name]
        except KeyError:
            self.__data[name] = Field(set_self=False)
        except AttributeError:
            # noinspection PyAttributeOutsideInit
            self.__data = {name: Field(set_self=False)}

        return self.__data[name]

    def set_field(self, name):
        """Creates and returns a new Field.

        If the Field with the name `field_name` already exists, just
        return it; otherwise, create a new and return.

        :param name: Name of the Field.
        :return: newly created or existing Field.
        """
        try:
            self.__data[name].__self = True
        except KeyError:
            self.__data[name] = Field()
        except AttributeError:
            # noinspection PyAttributeOutsideInit
            self.__data = {name: Field()}

        return self.__data[name]

    def set_self(self):
        """Sets the __self to True."""
        self.__self = True

    def get_normalized_fields(self,
                              infix_char='.',
                              root_field_name='##',
                              key_so_far=None):
        """
        Return the normalized version of all the Fields inside this.

        Normalization is a process of converting Fields/Field groups
        into their absolute representations. Normalized Field list of
        {'a': {'b': 2}, 'c': '24'} is ['a.b', 'c'].

        An empty Field group is never normalized.

        :param infix_char: Character to use to join the two related
        Fields/Field groups; default is '.'.
        :param root_field_name: Name of the current Field/Field group;
        default is '##'.
        :param key_so_far: Internal to the function. Never set this
        explicitly.
        :return: List of normalized Field names.
        """
        res = [root_field_name
               if key_so_far is None
               else key_so_far] if self.__self is True else []
        try:
            key = '' if key_so_far is None else key_so_far + infix_char
            for k, v in self.__data.items():
                absolute_key = key + k
                res.extend(v.get_normalized_fields(infix_char,
                                                   root_field_name,
                                                   absolute_key))
        except AttributeError:
            pass
        return res

    def __len__(self):
        """
        Return the number of Fields/Field groups in the current Field.

        Number includes itself (if __self is True).
        """
        try:
            return len(self.__data) + int(1 if self.__self is True else 0)
        except AttributeError:
            return int(1 if self.__self is True else 0)

    def __repr__(self):
        try:
            return ("{'__SELF__': true, " + repr(self.__data)[1:]
                    if self.__self is True
                    else repr(self.__data))
        except AttributeError:
            return "{'__SELF__': true}" if self.__self is True else '{}'

    def __str__(self):
        """Output is a easy to understand json representation."""
        try:
            if self.__self is True:
                return ', '.join(
                    ['{"__SELF__": true'] + [f'"{k}": {v.__str__()}'
                                             for k, v in self.__data.items()]
                ) + '}'
            return '{' + ', '.join(f'"{k}": {v.__str__()}'
                                   for k, v in self.__data.items()) + '}'
        except AttributeError:
            return 'true' if self.__self is True else '{}'
