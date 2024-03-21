"""Module for testing the Point class functionality"""

import pytest

import gdf

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
        (gdf.Point(0, 0, 0), "one", 0, 0, TypeError, None),
        (gdf.Point(0, 0, 0), 0, "one", 0, TypeError, None),
        (gdf.Point(0, 0, 0), 0, 0, "one", TypeError, None),
        (gdf.Point(0, 0, 0),  0,  0,  0, ValueError, None),
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
                result = gdf.Point(x, y, z)
        else:
            result = gdf.Point(x, y, z)
            assert result == expected

    @pytest.mark.parametrize("point1, point2, exception, expected", get_distance_testdata)
    def test_get_distance(self, point1, point2, exception, expected):
        if exception is not None:
            with pytest.raises(exception):
                result = gdf.Point.get_distance(point1, point2)
        else:
            result = gdf.Point.get_distance(point1, point2)
            assert result == expected

    @pytest.mark.parametrize("point1, dx, dy, dz, exception, expected", set_relative_to_testdata)
    def test_set_relative_to(self, point1, dx, dy, dz, exception, expected):
        if exception is not None:
            with pytest.raises(exception):
                result = point1.create_relative_point(dx, dy, dz)
        else:
            result = point1.create_relative_point(dx, dy, dz)
            assert result == expected
