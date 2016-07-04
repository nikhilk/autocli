# test.py
# Demonstrates basic usage of autocli

import autocli
import enum
import json

class OS(enum.Enum):
  Mac = 1
  Linux = 2
  Windows = 3

class Computers(object):

  os = OS.Mac
  version = '1.0'
  count = 1
  cpu = 3.75
  ram = 16.0
  disk = True
  gpu = False
  volumes = ['']
  metadata = json.loads

class Job(object):

  count = 1
  _extra = []


op = autocli.ObjectParser(Computers)
o = op.parse([])
assert(o.os == OS.Mac)
assert(o.version == '1.0')

o = op.parse(['--os', 'Linux', '--version', 'debian:jessie'])
assert(o.os == OS.Linux)
assert(o.version == 'debian:jessie')
assert(o.metadata is None)

o = op.parse(['--metadata', '{"foo":"bar"}'])
assert(o.metadata['foo'] == 'bar')

o = op.parse(['--volumes', '/aaa', '--volumes', '/bbb'])
assert(len(o.volumes) == 2)
assert(o.volumes[1] == '/bbb')

o = op.parse(['--count', '2', '--ram', '10'])
assert(o.count == 2)
assert(o.ram == 10.0)

j = autocli.parse_object(Job, ['--count', '2', 'some', 'more', 'args'])
assert(j.count == 2)
assert(j._extra is not None)
assert(len(j._extra) == 3)
assert(j._extra[1] == 'more')
