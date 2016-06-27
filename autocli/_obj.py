# _obj.py
# Implements Object parsing from a set of flags.

import argparse
import enum
import sys
import types


class ObjectParser(object):
  """Parses objects from a set of flags.
  """

  def __init__(self, object_type):
    """Initializes an instance of an ObjectParser.

    Args:
      - object_type: The type of object to parse. The structure of the object
        is used to build a flag parser.

    Returns:
      An initialized object instance based on the specified flags.

    Raises:
      ValueError if the object_type is left unspecified.
    """
    if not object_type:
      raise ValueError('The type of object to parse must be specified.')

    self._object_type = object_type
    self._argparser, self._extra_args = ObjectParser._build_parser(object_type)

  def parse(self, flags=None):
    """Parses an instance of the object from the specified set of flags.

    Args:
      flags: the sequence of strings to parse. Uses sys.argv[1:] by default.
    Returns:
      The parsed object instance if there was no error.
    """
    if flags is None:
      flags = sys.argv[1:]

    if self._extra_args:
      args, extra_args = self._argparser.parse_known_args(flags)
    else:
      args = self._argparser.parse_args(flags)

    obj = self._object_type()
    obj.__dict__.update(vars(args))

    if self._extra_args:
      obj._extra = extra_args

    return obj

  @staticmethod
  def _build_parser(object_type):
    """Builds a parser to match the interface of the specified object type.

    Returns:
      The ArgumentParser to parse flags, and whether the object support extra
      arbitrary flags.
    """
    parser = argparse.ArgumentParser(add_help=False)
    supports_extra_args = False

    for name, value in object_type.__dict__.iteritems():
      if name == '_extra':
        supports_extra_args = True
        continue
      if name.startswith('_'):
        continue

      # Flag names are based on field names
      flag = '--' + name
      if type(value) == float:
        parser.add_argument(flag, type=float, default=value)
      elif type(value) == int:
        parser.add_argument(flag, type=int, default=value)
      elif type(value) == str:
        parser.add_argument(flag, type=str, default=value)
      elif type(value) == bool:
        if value:
          # If the default for a boolean is True, a --no-field arg is
          # added to allow setting False
          flag = '--no-' + name
          parser.add_argument(flag, dest=name, default=True, action='store_false')
        else:
          parser.add_argument(flag, default=False, action='store_true')
      elif issubclass(type(value), enum.Enum):
        parser.add_argument(flag, type=_enum_parser(type(value)), default=value.name,
                            choices=list(type(value)))
      elif type(value) == types.FunctionType:
        parser.add_argument(flag, type=value, default=None)
      elif type(value) == list:
        if len(value) != 1:
          raise ValueError('List field %s must have one element' % name)

        value = value[0]
        if issubclass(type(value), enum.Enum):
          parser.add_argument(flag, type=_enum_parser(type(value)), choices=list(type(value)),
                              action='append')
        elif type(value) == types.FunctionType:
          parser.add_argument(flag, type=value, action='append')
        else:
          parser.add_argument(flag, type=type(value), action='append')
      else:
        raise ValueError('Unsupported object field type %s of type %s' % (name, str(type(value))))

    return parser, supports_extra_args


def _enum_parser(enum_type):
  def parser(s):
    return enum_type[s]
  return parser
