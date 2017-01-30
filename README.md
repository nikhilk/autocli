# AutoCLI Python Library

A tiny utility library that builds argparse ArgumentParsers based on
reflecting an example object and conventions.

Currently, this library provides support for parsing objects from a set
of flags specified on the command line. In the future, this will also
support the ability to invoke methods.

## Object Parsing

The object to be parsed is declared as a vanilla Python class with fields
and default values. The structure of this class is inspected and converted
into corresponding argparse flags.

Once the class has been inspected, instances of the class can be instantiated
by parsing a set of flags.

### Example

```
import autocli

class Metric(object):
  value = 123
  unit = 'm'

metric = autocli.parse_object(Metric, ['--value', 10])
assert(metric.value == 10)
assert(metric.unit == 'm')
```

See the included tests for more examples.


### Conventions and Mapping

* Public fields (those not beginning with underscore), with a specified value are mapped
  to flags.
* Flag names are constructed with the field name, with underscores replaced with hyphens.
  Note that booleans have additional semantics described below.
* The specified values for fields are considered as default values.
* Supported types: `int`, `float`, `str`, `bool`, enums, `list` (of `int`, `float`, `str` and enums),
  as well as support for custom types.
* For boolean values, if the specified default is `True`, a `--no-field-name` is added
  to override to `False`.
* For enums, the list of enum values is mapped to a set of choices.
* For lists, the value must be a list of at least length 1. The type of the first value is
  used to determine the type of flag to add. By default lists support 0 or more items, and are
  optional.
  The last element of a list maybe a list with a single element (['*'] for default behavior,
  [+] for 1 or more items, and [N] for exactly N items).
* For custom types, the default value should be a function that accepts a string, and returns
  a parsed value. Custom types do not have defaults.


### Additional Notes

* The library supports derived classes. Members of all classes in the hierarchy are
  flattened into a single list of flags.
* A class can include a special field called `_extra`. If present, this member is assigned
  all unparsed/extra flags. If absent, an unparseable flag results in an error.
* A class can include a special field called `_args`. If present, this member is assigned
  the raw flags used to parse the object.
* A class can implement the `callable` interface. If the class implements this, it is
  invoked once all the members have been initialized.
* Enum support is based on the `enum.Enum` class in the `enum34` library.
