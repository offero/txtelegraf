# coding: utf-8

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
    assert str(m1).startswith(expected_prefix), "Expected: %s  Found: %s" % (expected_prefix, str(m1))
