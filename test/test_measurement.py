# coding: utf-8
# Copyright 2016 Chris Kirkos
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

from txtelegraf import Measurement

def test_measurement():
    m1 = Measurement(
        name="metric-name",
        tags={"tag1": "tagval1"},
        fields={"integer_field": 10, "float_field": 10.0,
                "boolean_field": True, "string_field": "yoohoo"}
    )
    assert m1.time is not None

    expected_prefix = (
            'metric-name,tag1=tagval1'
            ' boolean_field=T,float_field=10.0,integer_field=10i,'
            'string_field="yoohoo"')
    assert str(m1).startswith(expected_prefix), "Expected: '%s' \nFound: '%s'" % (expected_prefix, str(m1))

    # quote in tag name
    # quote in tag value

def test_measurement_escape_chars():
    m2 = Measurement(
        name=r'something with=weird,chars',
        tags={r'tag, 1': r'tagval=1'},
        fields={r'string field': 'quote"inside'},
        time=10000000
    )
    expected_string = (
        r'something\ with=weird\,chars,'
        r'tag\,\ 1' '=' r'tagval\=1'
        r' string\ field' '=' r'"quote\"inside"'
        r' 10000000'
    )
    assert str(m2) == expected_string, "\nExpect:\t'%s'\nFound:\t'%s'" % (expected_string, str(m2))

    m3 = eval(repr(m2))
    assert m3.name == m2.name
    assert m3.tags == m2.tags

def test_measurement_no_tags():
    m4 = Measurement(
        name="metric-name",
        tags={},
        fields={"integer_field": 10, "float_field": 10.0,
                "boolean_field": True, "string_field": "yoohoo"}
    )
    assert m4.time is not None

    expected_prefix = (
            'metric-name'
            ' boolean_field=T,float_field=10.0,integer_field=10i,'
            'string_field="yoohoo"')
    assert str(m4).startswith(expected_prefix), "Expected: '%s' \nFound: '%s'" % (expected_prefix, str(m4))
