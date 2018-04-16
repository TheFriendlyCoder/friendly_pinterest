"""Interfaces for interacting with Pinterest users"""
import logging
import json
from friendlypins.board import Board


class User(object):
    """Abstraction around a Pinterest user and their associated data

    :param dict data: JSON data parsed from the API
    :param rest_io: reference to the Pinterest REST API
    :type rest_io: :class:`friendlypins.utils.rest_io.RestIO`
    """

    def __init__(self, data, rest_io):
        self._log = logging.getLogger(__name__)
        self._data = data
        self._io = rest_io

    def __str__(self):
        """String representation of this user, for debugging purposes

        :rtype: :class:`str`
        """
        return json.dumps(dict(self._data), sort_keys=True, indent=4)

    def __repr__(self):
        """User representation in string format

        :rtype: :class:`str`
        """
        return "<{0} ({1} {2})>".format(
            self.__class__.__name__,
            self.first_name,
            self.last_name)

    @property
    def unique_id(self):
        """Gets the internal unique ID associated with the user

        :rtype: :class:`int`
        """
        return int(self._data['id'])

    @property
    def first_name(self):
        """Gets the first name of the user

        :rtype: :class:`str`
        """
        return self._data['first_name']

    @property
    def last_name(self):
        """Gets the last name of the user

        :rtype: :class:`str`
        """
        return self._data['last_name']

    @property
    def name(self):
        """Gets the name of the user

        alias for first_name + last_name

        :rtype: :class:`str`
        """
        return "{0} {1}".format(self.first_name, self.last_name)

    @property
    def url(self):
        """Gets the URL of the users profile

        :rtype: :class:`str`
        """
        return self._data['url']

    @property
    def num_pins(self):
        """Gets the total number of pins owned by this user

        :rtype: :class:`int`
        """
        return int(self._data['counts']['pins'])

    @property
    def num_boards(self):
        """Gets the total number of boards owned by this user

        :rtype: :class:`int`
        """
        return int(self._data['counts']['boards'])

    @property
    def boards(self):
        """Generator for iterating over the boards owned by this user

        :rtype: Generator of :class:`friendlypins.board.Board`
        """
        self._log.debug('Loading boards for user %s...', self.name)

        properties = {
            "fields": ','.join([
                "id",
                "name",
                "url",
                "description",
                "creator",
                "created_at",
                "counts",
                "image"
            ])
        }

        page = 0
        while True:
            self._log.debug("Loading boards page %s", page)
            result = self._io.get("me/boards", properties)
            assert 'data' in result

            for cur_item in result['data']:
                yield Board(cur_item, self._io)

            if not result["page"]["cursor"]:
                break

            properties["cursor"] = result["page"]["cursor"]
            page += 1


if __name__ == "__main__":
    pass
