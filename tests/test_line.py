"""Module for testing the Point class functionality"""

import numpy as np
import pytest

import gdf

class TestLine:

    # ! Include flipped_direction option in tests

    init_testdata = [
        #point1, point2, exception
        (gdf.Point(0, 0, 0), 1, TypeError),
        (gdf.Point(0, 0, 0), 1.0, TypeError),
        (gdf.Point(0, 0, 0), "one", TypeError),
        (1, gdf.Point(0, 0, 0), TypeError),
        (1.0, gdf.Point(0, 0, 0), TypeError),
        ("one", gdf.Point(0, 0, 0), TypeError)
    ]

    # ! Add more test cases
    get_path_xyz_testdata = [
        # point1, point2, num_points, dist_method, flip_dir, expectation
        (gdf.Point(0, 0, 0), gdf.Point(3, 0, 0), 4, gdf.mesh.distribution_methods.DistLinear(), False, np.array([[0.0, 0.0, 0.0],[1.0, 0.0, 0.0],[2.0, 0.0, 0.0],[3.0, 0.0, 0.0]])),
        (gdf.Point(0, 0, 0), gdf.Point(0, 2, 0), 3, gdf.mesh.distribution_methods.DistLinear(), False, np.array([[0.0, 0.0, 0.0],[0.0, 1.0, 0.0],[0.0, 2.0, 0.0]])),
        (gdf.Point(0, 0, 0), gdf.Point(0, 0, 2), 3, gdf.mesh.distribution_methods.DistLinear(), False, np.array([[0.0, 0.0, 0.0],[0.0, 0.0, 1.0],[0.0, 0.0, 2.0]]))
    ]

    def test_no_input(self):
        with pytest.raises(TypeError):
            gdf.Line()

    @pytest.mark.parametrize("point1, point2, exception", init_testdata)
    def test_init_raises_exception_on_wrong_input(self, point1, point2, exception):
        with pytest.raises(exception):
            gdf.Line(point1, point2)

    @pytest.mark.parametrize("point1, point2, num_points, dist_method, flip_dir, expected", get_path_xyz_testdata)
    def test_get_path_fn(self, point1, point2, num_points, dist_method, flip_dir, expected):
        path_fn = gdf.Line(point1, point2).get_path_fn()
        dist_fn = dist_method.get_fn(flip_dir=flip_dir)
        path_xyz = np.zeros((num_points, 3))
        for i, u in enumerate(np.linspace(0, 1, num=num_points, endpoint=True)):
            path_xyz[i, :] = path_fn(dist_fn(u))
        assert (path_xyz == expected).all()
