"""Module for testing the Point class functionality"""

import pytest

import gdfpy as gdf
from gdfpy.exceptions import CurveIntersectionError

# ! Include flipped_curves in tests

class TestCoonsPatch:

    @pytest.fixture
    def lines_clean_loop(self):
        curve_selection = tuple([
            gdf.Line(gdf.Point(0, 0, 0), gdf.Point(10, 0, 0)),
            gdf.Line(gdf.Point(10, 0, 0), gdf.Point(10, 10, 0)),
            gdf.Line(gdf.Point(10, 10, 0), gdf.Point(0, 10, 0)),
            gdf.Line(gdf.Point(0, 10, 0), gdf.Point(0, 0, 0))
        ])
        expected = tuple([
            gdf.Line(gdf.Point(0, 0, 0), gdf.Point(10, 0, 0)),
            gdf.Line(gdf.Point(10, 10, 0), gdf.Point(0, 10, 0)),
            gdf.Line(gdf.Point(0, 10, 0), gdf.Point(0, 0, 0)),
            gdf.Line(gdf.Point(10, 0, 0), gdf.Point(10, 10, 0))
        ])
        return curve_selection, expected

    @pytest.fixture
    def lines_jumbled(self):
        line1 = gdf.Line(gdf.Point(0, 0, 0), gdf.Point(10, 0, 0))
        line2 = gdf.Line(gdf.Point(10, 10, 0), gdf.Point(10, 0, 0))
        line3 = gdf.Line(gdf.Point(10, 10, 0), gdf.Point(0, 10, 0))
        line4 = gdf.Line(gdf.Point(0, 10, 0), gdf.Point(0, 0, 0))
        curve_selection = tuple([line1, line4, line2, line3])
        expected = tuple([line1, line3, line4, line2])
        return curve_selection, expected

    @pytest.fixture
    def lines_not_connected(self):
        line1 = gdf.Line(gdf.Point(0, 0, 0), gdf.Point(10, 0, 0))
        line2 = gdf.Line(gdf.Point(10, 0, 0), gdf.Point(10, 10, 0))
        line3 = gdf.Line(gdf.Point(10, 10, 0), gdf.Point(0, 10, 0))
        line4 = gdf.Line(gdf.Point(0, 10, 0), gdf.Point(5, 0, 0))
        return line1, line2, line3, line4

    init_testdata = [
        #curve1, curve2, curve3, curve4, exception, expected
        (1, 1, 1, 1, TypeError, None),
        ("1", "1", "1", "1", TypeError, None),
        (True, False, True, False, TypeError, None)
    ]

    def test_no_input(self):
        with pytest.raises(TypeError):
            gdf.CoonsPatch()

    @pytest.mark.parametrize("curve1, curve2, curve3, curve4, exception, expected", init_testdata)
    def test_init_raises_exception_on_wrong_input_type(self, curve1, curve2, curve3, curve4, exception, expected):
        if exception is not None:
            with pytest.raises(exception):
                gdf.CoonsPatch(curve1, curve2, curve3, curve4)
        else:
            assert expected == gdf.CoonsPatch(curve1, curve2, curve3, curve4)

    def test_init_clean_loop(self, lines_clean_loop):
        curve_selection, expected = lines_clean_loop
        curve1, curve2, curve3, curve4 = curve_selection
        surface = gdf.CoonsPatch(curve1, curve2, curve3, curve4)
        assert surface.curve_selection == expected

    def test_init_jumbled_curves(self, lines_jumbled):
        curve_selection, expected = lines_jumbled
        curve1, curve2, curve3, curve4 = curve_selection
        surface = gdf.CoonsPatch(curve1, curve2, curve3, curve4)
        assert surface.curve_selection == expected

    def test_init_raises_exception_on_curves_not_connected(self, lines_not_connected):
        curve1, curve2, curve3, curve4 = lines_not_connected
        with pytest.raises(CurveIntersectionError):
            gdf.CoonsPatch(curve1, curve2, curve3, curve4)
