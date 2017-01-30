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

    The structure of the object (its fields and their default values) is used
    to build an argument parser.

    Args:
      - object_type: The type of object to parse.

    Returns:
      An initialized object instance based on the specified flags.

    Raises:
      ValueError if the object_type is unspecified or invalid.
    """
    if not object_type:
      raise ValueError('The type of object to parse must be specified.')

    self._object_type = object_type
    self._parser, self._supports_extra, self._requires_argv = _build_parser(object_type)

  def parse(self, args=None):
    """Parses an instance of the object from the specified set of flags.

    Args:
      args: the sequence of strings to parse. Uses sys.argv[1:] by default.
    Returns:
      The parsed object instance if there was no error.
    """
    if args is None:
      args = sys.argv[1:]

    if self._supports_extra:
      parsed_args, extra_args = self._parser.parse_known_args(args)
    else:
      parsed_args = self._parser.parse_args(args)

    obj = self._object_type()
    obj.__dict__.update(vars(parsed_args))

    if self._supports_extra:
      obj._extra = extra_args
    if self._requires_argv:
      obj._args = args

    # If the object implements the callable interface, invoke the object, so
    # it can do any additional initialization logic.
    if callable(obj):
      obj = obj()

    return obj


def _build_parser(object_type):
  parser = argparse.ArgumentParser(add_help=False)

  members = _members(object_type)
  for name, value in members.items.iteritems():
    value_type = type(value)

    # Flag names are the same as field names, with underscores replaced with hyphens.
    flag = '--' + name.replace('_', '-')

    # Simple types (float, int, string)
    if isinstance(value, (float, int, str)):
      # Simple types
      parser.add_argument(flag, type=value_type, default=value)
    elif value_type is bool:
      # For booleans, the default is the specified value, and a flag is added to override it.
      if value:
        parser.add_argument('--no-' + flag, dest=name, default=True, action='store_false')
      else:
        parser.add_argument(flag, default=False, action='store_true')
    elif isinstance(value, enum.Enum):
      # Enums are parsed via a lookup, and enum values are turned into choices.
      parser.add_argument(flag, type=_enum_parser(value_type), default=value.name,
                          choices=list(value_type))
    elif isinstance(value, types.FunctionType):
      # Functions provide a way to do custom parsing.
      parser.add_argument(flag, type=value, default=None)
    elif isinstance(value, list):
      if not len(value):
        raise ValueError('Invalid list for "%s". Lists must not be empty.' % name)

      nargs = '*'
      required = False

      # If the last value is a list, that is used to specify list behavior.
      # '*': 0+
      # '+': 1+ (list becomes required)
      # #: N (list becomes required)
      last_value = value[-1]
      if type(last_value) is list:
        nargs = last_value[0]
        required = nargs != '*'
        value = value[:-1]

      first_value = value[0]
      first_value_type = type(first_value)
      if isinstance(first_value, (float, int, str)):
        parser.add_argument(flag, type=first_value_type, nargs=nargs, required=required,
                            default=value)
      elif isinstance(first_value, enum.Enum):
        parser.add_argument(flag, type=_enum_parser(first_value_type),
                            choices=list(first_value_type),
                            nargs=nargs, required=required, default=value)
      elif first_value_type is types.FunctionType:
        parser.add_argument(flag, type=first_value, nargs=nargs, required=required)
      else:
        raise ValueError('Unsupported value for "%s" ("%s")' % (name, str(first_value_type)))
    else:
      raise ValueError('Unsupported value for "%s" ("%s").' % (name, str(value_type)))

  return parser, members.extra, members.args


def _members(object_type, members=None):
  if members is None:
    members = argparse.Namespace()
    members.items = dict()
    members.extra = False
    members.args = False

  for name, value in object_type.__dict__.iteritems():
    if name == '_extra':
      members.extra = True
    elif name == '_args':
      members.args = True
    elif not name.startswith('_') and value is not None:
      members.items[name] = value
  
  base_type = object_type.__base__
  if base_type is not object:
    _members(base_type, members)

  return members


def _enum_parser(enum_type):
  def parser(s):
    return enum_type[s]
  return parser
