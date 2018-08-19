import geometry

class LinearExtrude(geometry.Form):
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

class Parallelepiped(geometry.Form):
    def __init__(self, name, dimensions, is_centered, rotation=None, translation=None):
        super(Parallelepiped, self).__init__(name, rotation, translation)
        self.dimensions = geometry.Point3D(self.assert_point3d(dimensions))
        self.is_centered = self.assert_boolean(is_centered)

    def scad_string(self, indent=0):
        return self.indent("cube(size=%s, center=%s)" % (self.dimensions.as_scad(), ("%s" % self.is_centered).lower()), indent)
