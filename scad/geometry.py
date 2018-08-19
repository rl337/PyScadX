
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

    def assert_rotation(self, value):
        if isinstance(value, tuple):
            if len(value) != 3:
                raise GeometryException("Value %s needs to be a tuple of the form, (x_degrees,y_degrees,z_degrees)")
            x = self.assert_float(value[0])
            y = self.assert_float(value[1])
            z = self.assert_float(value[2])
            return (x, y, z)

        if value is None:
            return None

        raise GeometryException("Value %s is not a rotation tuple(x_degrees,y_degrees,z_degrees) or None" % value)

    def assert_translation(self, value):
        if isinstance(value, tuple):
            if len(value) != 3:
                raise GeometryException("Value %s needs to be a tuple of the form, (delta_x,delta_y,delta_z)")
            x = self.assert_float(value[0])
            y = self.assert_float(value[1])
            z = self.assert_float(value[2])
            return (x, y, z)

        if value is None:
            return None

        raise GeometryException("Value %s is not a translation tuple(delta_x,delta_y,delta_z) or None" % value)

    def assert_form(self, value):
        if isinstance(value, Form):
            return value

        raise GeometryException("Value %s is not a Form() class" % value)

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
        pointlist = ["[%g,%g]" % (p[0], p[1]) for p in self.points]
        return self.indent("polygon([%s])" % ','.join(pointlist), indent)

class Form(SCADGeometry):
    def __init__(self, name, rotation, translation):
        super(Form, self).__init__(name)
        self.rotation = self.assert_rotation(rotation)
        self.translation = self.assert_translation(translation)

    def as_scad(self, indent=0):
        result = ""
        if self.translation is not None:
            result += self.indent("translate([%g,%g,%g])\n" % (self.translation[0], self.translation[1], self.translation[2]), indent)
            indent += 1
        if self.rotation is not None:
            result += self.indent("rotate([%g,%g,%g])\n" % (self.rotation[0], self.rotation[1], self.rotation[2]), indent)
            indent += 1
        result += self.scad_string(indent)
        return result

    def scad_string(self, indent=0):
        raise GeometryException("Form.scad_string() is not implemented")

class LinearExtrude(Form):
    def __init__(self, name, polygon, height, is_centered, rotation=None, translation=None):
        super(LinearExtrude, self).__init__(name, rotation, translation)
        self.polygon = self.assert_polygon(polygon)
        self.height = self.assert_float(height)
        self.is_centered = self.assert_boolean(is_centered)

    def scad_string(self, indent=0):
        return "%s\n%s" % (
            self.indent("linear_extrude(height=%g, center=%s)" % (self.height, ("%s" % self.is_centered).lower()), indent),
            self.polygon.as_scad(indent + 1)
        )

class Union(Form):
    def __init__(self, name, forms, rotation=None, translation=None):
        super(Union, self).__init__(name, rotation, translation)
        self.forms = [ self.assert_form(form) for form in forms ]

    def scad_string(self, indent=0):
        opener = self.indent("union() {", indent)
        closer = self.indent("}", indent, indent)
        body = '\n'.join([ "%s;" % form.as_scad(indent + 1) for form in self.forms ])
        return "%s\n%s\n%s" % (opener, body, closer)
