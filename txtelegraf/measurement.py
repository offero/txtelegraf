# coding: utf-8
# Copyright 2016 Chris Kirkos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import (absolute_import, division, print_function, unicode_literals)

import time
from types import StringTypes

# NOTE: Single slashes have bad edge cases in the parser.
# We will strip them out.
single_slash = '\\'
double_slash = r'\\'
quote = '"'
escaped_quote = r'\"'
newline = '\n'
escaped_newline = r'\n'
equals = '='
escaped_equals = r'\='
comma = ','
escaped_comma = r'\,'
space = ' '
escaped_space = r'\ '
underscore = '_'

def now_nano():
    return int(time.time() * 1e9)

def format_measurement_name(s):
    s = s.replace(single_slash, underscore)
    s = s.replace(comma, escaped_comma)
    s = s.replace(space, escaped_space)
    return s

def format_tag(s):
    s = s.replace(single_slash, underscore)
    s = s.replace(comma, escaped_comma)
    s = s.replace(equals, escaped_equals)
    s = s.replace(space, escaped_space)
    return s

format_field_name = format_tag

def format_field_value(v):
    if isinstance(v, StringTypes):
        v = v.replace(quote, escaped_quote)
        return '"%s"' % v
    # before the int check because bools are ints and ints are not bools
    elif isinstance(v, bool):
        return v and 'T' or 'F'
    elif isinstance(v, (int, long)):
        return '%di' % v
    elif isinstance(v, float):
        return str(v)
    else:
        raise Exception("Invalid field. value: %s type: %s" % (v, type(v)))

def format_tags(tags):
    return ",".join(("%s=%s" % (format_tag(k), format_tag(v)) for (k, v) in sorted(tags.items())))

def format_fields(fields):
    return ",".join(("%s=%s" % (format_field_name(k), format_field_value(v)) for (k, v) in sorted(fields.items())))

class Measurement(object):
    """
    Field Values:
        Floats - by default, InfluxDB assumes all numerical field values are floats.
        Integers - append an i to the field value to tell InfluxDB to store the number as an integer.
        Strings - double quote string field values
        Booleans - specify TRUE with t, T, true, True, or TRUE. Specify FALSE with f, F, false, False, or FALSE.

    For tag keys, tag values, and field keys always use a backslash character \ to escape:
    commas ,
    equal signs =
    spaces

    For measurements always use a backslash character \ to escape:
    commas ,
    spaces

    For string field values use a backslash character \ to escape:
    double quotes "

    For best performance you should sort tags by key before sending them to the database.

    ref:  https://docs.influxdata.com/influxdb/v1.0/write_protocols/line_protocol_tutorial/
    """
    __slots__ = ['name', 'tags', 'fields', 'time']

    def __init__(self, name, tags=None, fields=None, time=None):
        """
        name: String. Measurement name.
        tags: Dict. String->String
        fields: Dict. String->{Int,Float,String,Bool}
        time: Int. Nanoseconds since epoch.
        """
        self.name = name
        self.tags = tags or {}
        self.fields = fields or {}
        self.time = time or now_nano()

    def __repr__(self):
        return 'Measurement(name="%s", tags=%s, fields=%s, time=%s)' % \
            (self.name, self.tags, self.fields, self.time)

    def __unicode__(self):
        name = format_measurement_name(self.name)
        tags = format_tags(self.tags)
        fields = format_fields(self.fields)
        time = "%s" % self.time

        element0 = ','.join((name, tags)) if tags else name
        element1 = fields
        element2 = time

        return " ".join((element0, element1, element2))

    def __str__(self):
        return unicode(self).encode('utf-8')
