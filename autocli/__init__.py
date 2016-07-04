# __init__.py
# Defines the autocli module.

from _obj import ObjectParser

def parse_object(object_type, args):
  parser = ObjectParser(object_type)
  return parser.parse(args)

