
class GeometryException(Exception):
    pass

class SCADValidation(object):

    def assert_boolean(self, value):
        if isinstance(value, bool):
            return value
        raise GeometryException("Value %s is not a boolean" % value)

    def assert_float(self, value):
        if isinstance(value, float):
            return value

        if isinstance(value, bool):
            raise GeometryException("Value %s is a bool, not a float" % value)

        if isinstance(value, int):
            return float(value)

        raise GeometryException("Value %s is not a float" % value)

    def assert_polygon(self, value):
        if isinstance(value, Polygon):
            return value

        raise GeometryException("Value %s is not a Polygon() class" % value)

    def assert_point2d(self, value):
        if isinstance(value, tuple):
            if len(value) != 2:
                raise GeometryException("Value %s needs to be a tuple of the form, (x,y)")
            x = self.assert_float(value[0])
            y = self.assert_float(value[1])
            return (x, y)

        raise GeometryException("Value %s is not a 2D Point tuple (x,y)")

class SCADGeometry(SCADValidation):
    def __init__(self, name):
        super(SCADGeometry, self).__init__()
        self.name = name

    def as_scad(self, indent=0):
        raise GeometryException("SCADGeometry.as_scad is undefined")

    def indent(self, value, indent=0):
        return "%s%s" % ('  ' * indent, value)

class Polygon(SCADGeometry):
    def __init__(self, name, points):
        super(Polygon, self).__init__(name)
        self.points = [ self.assert_point2d(x) for x in points ]

    def as_scad(self, indent=0):
        pointlist = ["(%f,%f)" % (p[0], p[1]) for p in self.points]
        return indent("polygon([%s])" % ','.join(pointlist), indent)
    

class LinearExtrude(SCADGeometry):
    def __init__(self, name, polygon, height, is_centered):
        super(LinearExtrude, self).__init__(name)
        self.polygon = self.assert_polygon(polygon)
        self.height = self.assert_float(height)
        self.is_centered = self.assert_boolean(is_centered)

    def as_scad(self, indent=0):
        return "%s\n%s" % (
            indent("linear_extrude(height=%f, center=%s)" % (self.height, ("%s" % self.is_centered).lower()), indent),
            self.polygon.as_scad(indent + 1)
        )

