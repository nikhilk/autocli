# __init__.py
# Defines the autocli module.

from _obj import ObjectParser

def parse_object(object_type, args=None):
  """Parses an object of the specified type.

  The structure of the object (its fields and their default values) is used
  to build an argument parser.

  Args:
    - object_type: The type of object to parse.
    - args: Optional list of arguments to parse. Defaults to sys.argv[1:].

  Returns:
    An initialized object instance based on the specified flags.

  Raises:
    ValueError if the object_type is unspecified, or the object structure is invalid.
  """
  parser = ObjectParser(object_type)
  return parser.parse(args)
