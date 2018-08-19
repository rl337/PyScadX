import pytest
import scad.shapes
import scad.geometry

test_defs = [
    {
        'class': 'Trapezoid',
        'params': {'name': 'test_trapezoid1', 'width1': 10, 'width2': 100, 'length': 10},
        'indents': 0,
        'expected_string':'''
polygon([[-5,-5],[5,-5],[50,5],[-50,5],[-5,-5]])
'''
    },
    {
        'class': 'Trapezoid',
        'params': {'name': 'test_trapezoid2', 'width1': 10, 'width2': 100, 'length': 10},
        'indents': 3,
        'expected_string':'''
      polygon([[-5,-5],[5,-5],[50,5],[-50,5],[-5,-5]])
'''
    },
    {
        'class': 'LinearExtrude',
        'params': {'name': 'test_extrude1', 'polygon': scad.shapes.Square('test_extrude1.square1', 10), 'height': 10, 'is_centered': False},
        'indents': 0,
        'expected_string':'''
linear_extrude(height=10, center=false)
  polygon([[-5,-5],[5,-5],[5,5],[-5,5],[-5,-5]])
'''
    },
]

def test_asserts():

    for test_def in test_defs:
        classname = test_def['class']
        class_params = test_def['params']
        indents = test_def['indents']
        expected_string = test_def['expected_string'].strip('\n')

        geom_class = getattr(scad.shapes, classname, None)
        if geom_class is None:
            geom_class = getattr(scad.geometry, classname, None)

        if geom_class is None:
            pytest.fail("Class %s was not in scad.shapes or scad.geometry" % classname)

        geom_obj = geom_class(**class_params)
        actual_string = geom_obj.as_scad(indents)

        assert actual_string == expected_string, "Result had string:\n%s\nExpected:\n%s\n" % (actual_string, expected_string)
