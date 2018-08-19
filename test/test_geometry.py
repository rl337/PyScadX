import pytest
import scad.geometry


test_defs = [
    {
        'function': 'assert_boolean',
        'value': True,
        'expected': True,
        'expected_type': bool
    },
    { 
        'function': 'assert_boolean',
        'value': False,
        'expected': False,
        'expected_type': bool
    },
    {
        'function': 'assert_boolean',
        'value': None,
        'exception': scad.geometry.GeometryException,
    },
    {
        'function': 'assert_boolean',
        'value': "omg",
        'exception': scad.geometry.GeometryException,
    },
    {
        'function': 'assert_boolean',
        'value': "123",
        'exception': scad.geometry.GeometryException,
    },
    {
        'function': 'assert_float',
        'value': 1,
        'expected': 1.0,
    },
    {
        'function': 'assert_float',
        'value': None,
        'exception': scad.geometry.GeometryException,
    },
    {
        'function': 'assert_float',
        'value': "omg",
        'exception': scad.geometry.GeometryException,
    },
    {
        'function': 'assert_float',
        'value': False,
        'exception': scad.geometry.GeometryException,
    },
    {
        'function': 'assert_point2d',
        'value': (5,4),
        'expected': (5.0, 4.0),
    },
    {
        'function': 'assert_point2d',
        'value': (2.5,4.5),
        'expected': (2.5, 4.5),
    },
    {
        'function': 'assert_point2d',
        'value': None,
        'exception': scad.geometry.GeometryException,
    },
    {
        'function': 'assert_point2d',
        'value': (None,3.0),
        'exception': scad.geometry.GeometryException,
    },
    {
        'function': 'assert_point2d',
        'value': (1.5,"omg"),
        'exception': scad.geometry.GeometryException,
    },
    {
        'function': 'assert_point2d',
        'value': (1.5,),
        'exception': scad.geometry.GeometryException,
    },
    {
        'function': 'assert_point2d',
        'value': (1.5, 2.0, 3.5),
        'exception': scad.geometry.GeometryException,
    },
]

def test_asserts():
    geom = scad.geometry.SCADGeometry("test")

    for test_def in test_defs:
        func = getattr(geom, test_def['function'])
        if 'exception' in test_def:
            with pytest.raises(test_def['exception']):
                func(test_def['value'])
        else:
            y = func(test_def['value'])
            if 'expected_type' in test_def:
                assert type(y) == test_def['expected_type'], "Result %s  was not expected type" % y
            if 'expected' in test_def:
                assert y == test_def['expected'], "Result %s was not expected." % y
