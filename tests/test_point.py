"""Module for testing the Point class functionality"""

import pytest

import gdfgen as gdf

class TestPoint:

    init_testdata = [
        #x, y, z, exception, expected
        ("one", 0, 0, TypeError, None),
        (0, "one", 0, TypeError, None),
        (0, 0, "one", TypeError, None),
        (True, 0, 0, None, gdf.Point(1.0, 0.0, 0.0)),
        (0, True, 0, None, gdf.Point(0.0, 1.0, 0.0)),
        (0, 0, True, None, gdf.Point(0.0, 0.0, 1.0)),
        (False, 0, 0, None, gdf.Point(0.0, 0.0, 0.0)),
        (0, False, 0, None, gdf.Point(0.0, 0.0, 0.0)),
        (0, 0, False, None, gdf.Point(0.0, 0.0, 0.0)),
        ( 0,  0,  0, None, gdf.Point( 0.0,  0.0,  0.0)),
        (+1, +1, +1, None, gdf.Point(+1.0, +1.0, +1.0)),
        (-1, -1, -1, None, gdf.Point(-1.0, -1.0, -1.0))
    ]

    get_distance_testdata = [
        #point1, point2, exception, expected
        (gdf.Point(0, 0, 0), 1, TypeError, None),
        (gdf.Point(0, 0, 0), 1.0, TypeError, None),
        (gdf.Point(0, 0, 0), "one", TypeError, None),
        (1, gdf.Point(0, 0, 0), TypeError, None),
        (1.0, gdf.Point(0, 0, 0), TypeError, None),
        ("one", gdf.Point(0, 0, 0), TypeError, None),
        (gdf.Point(0, 0, 0), gdf.Point(3, 4, 0), None, 5.0),
        (gdf.Point(-3, -4, 0), gdf.Point(0, 0, 0), None, 5.0)
    ]

    set_relative_to_testdata = [
        #point, dx, dy, dz, exception, expected
        (None, 0.0, 0.0, 0.0, ValueError, None),
        (1, 0, 0, 0,TypeError, None),
        (1.0, 0, 0, 0, TypeError, None),
        ("one", 0, 0, 0, TypeError, None),
        (True, 0, 0, 0, TypeError, None),
        (False, 0, 0, 0, TypeError, None),
        (gdf.Point(0, 0, 0), "one", 0, 0, TypeError, None),
        (gdf.Point(0, 0, 0), 0, "one", 0, TypeError, None),
        (gdf.Point(0, 0, 0), 0, 0, "one", TypeError, None),
        (gdf.Point(0, 0, 0),  0,  0,  0, None, gdf.Point( 0,  0,  0)),
        (gdf.Point(0, 0, 0),  1,  1,  1, None, gdf.Point( 1,  1,  1)),
        (gdf.Point(0, 0, 0), -1, -1, -1, None, gdf.Point(-1, -1, -1))
    ]

    def test_no_input(self):
        with pytest.raises(TypeError):
            gdf.Point()

    @pytest.mark.parametrize("x, y, z, exception, expected", init_testdata)
    def test_init_raises_exception_on_wrong_input_type(self, x, y, z, exception, expected):
        if exception is not None:
            with pytest.raises(exception):
                p = gdf.Point(x, y, z)
        else:
            p = gdf.Point(x, y, z)
            assert p == expected

    @pytest.mark.parametrize("point1, point2, exception, expected", get_distance_testdata)
    def test_get_distance(self, point1, point2, exception, expected):
        if exception is not None:
            with pytest.raises(exception):
                distance = gdf.Point.get_distance(point1, point2)
        else:
            distance = gdf.Point.get_distance(point1, point2)
            assert distance == expected

    @pytest.mark.parametrize("point1, dx, dy, dz, exception, expected", set_relative_to_testdata)
    def test_set_relative_to(self, point1, dx, dy, dz, exception, expected):
        if exception is not None:
            with pytest.raises(exception):
                point = gdf.Point.set_relative_to(point1, dx, dy, dz)
        else:
            point = gdf.Point.set_relative_to(point1, dx, dy, dz)
            assert point == expected
