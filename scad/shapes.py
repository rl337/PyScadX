import geometry

class Trapezoid(geometry.Polygon):
    def __init__(self, name, width1, width2, length):
        super(Trapezoid, self).__init__(name, [
                (-width1/2, -length/2),
                ( width1/2, -length/2),
                ( width2/2,  length/2),
                (-width2/2,  length/2),
                (-width1/2, -length/2)
            ]
        )

class Square(geometry.Polygon):
    def __init__(self, name, length):
        super(Square, self).__init__(name, [
                (-length/2, -length/2),
                ( length/2, -length/2),
                ( length/2,  length/2),
                (-length/2,  length/2),
                (-length/2, -length/2)
            ]
        )
