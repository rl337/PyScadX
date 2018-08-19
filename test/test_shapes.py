import pytest
import scad.shapes


test_defs = [
    {
        'shape': 'Trapezoid',
        'params': {'name': 'test_trapezoid1', 'width1': 10, 'width2': 100, 'length': 10},
        'expected_points': [(-5.0,-5.0), (5.0, -5.0), (50.0, 5.0), (-50.0, 5.0), (-5.0, -5.0)]
    },
    {
        'shape': 'Square',
        'params': {'name': 'test_square1', 'length': 10},
        'expected_points': [(-5.0,-5.0), (5.0, -5.0), (5.0, 5.0), (-5.0, 5.0), (-5.0, -5.0)]
    },
]

def test_asserts():

    for test_def in test_defs:
        shape = test_def['shape']
        shape_params = test_def['params']
        expected_points = test_def['expected_points']

        shape_class = getattr(scad.shapes, shape)

        shape_obj = shape_class(**shape_params)
        actual_points = shape_obj.points

        assert len(actual_points) == len(expected_points), "Got %d points, expected %d points" % (len(actual_points), len(expected_points))

        assert actual_points == expected_points, "Result had points: %s. Expected %s" % (actual_points, expected_points)
