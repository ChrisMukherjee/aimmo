from __future__ import absolute_import

import unittest

from simulation.map_generator import get_random_edge_index, generate_map
from simulation.world_map import WorldMap


class ConstantRng(object):

    def __init__(self, value):
        self.value = value

    def randint(self, minimum, maximum):
        if not minimum <= self.value <= maximum:
            raise ValueError('Beyond range')
        return self.value


class TestMapGenerator(unittest.TestCase):

    def test_get_random_edge_index_can_give_all_possible(self):
        map = WorldMap.generate_empty_map(3, 4)
        get_random_edge_index(map, rng=ConstantRng(1))
        expected = frozenset((
                (0,  1), (1, 1),
                (-1, 0), (2, 0),
                (0, -1), (1, -1),
        ))
        actual = frozenset(get_random_edge_index(map, rng=ConstantRng(i))
                           for i in xrange(6))
        self.assertEqual(expected, actual)

    def test_out_of_bounds_random_edge(self):
        map = WorldMap.generate_empty_map(3, 4)
        with self.assertRaisesRegexp(ValueError, 'Beyond range'):
            get_random_edge_index(map, rng=ConstantRng(-1))

        with self.assertRaisesRegexp(ValueError, 'Beyond range'):
            get_random_edge_index(map, rng=ConstantRng(6))

    def test_map_dimensions(self):
        m = generate_map(4, 3, 1.0)
        grid = list(m.all_cells())
        self.assertEqual(len(set(grid)), len(grid), "Repeats in list")
        for c in grid:
            self.assertLessEqual(c.location.x, 1)
            self.assertLessEqual(c.location.y, 2)
            self.assertGreaterEqual(c.location.x, -1)
            self.assertGreaterEqual(c.location.y, -1)

    def test_obstable_ratio(self):
        m = generate_map(10, 10, 0.0)
        obstacle_cells = [cell for cell in m.all_cells() if not cell.habitable]
        self.assertEqual(len(obstacle_cells), 0)

    def test_map_contains_some_non_habitable_cell(self):
        m = generate_map(4, 4, 1.0)
        obstacle_cells = [cell for cell in m.all_cells() if not cell.habitable]
        self.assertGreaterEqual(len(obstacle_cells), 1)

    def test_map_contains_some_habitable_cell_on_border(self):
        m = generate_map(4, 4, 1.0)

        edge_coordinates = [
            (-1,  2), (0,  2), (1,  2), (2,  2),
            (-1,  1),                   (2,  1),
            (-1,  0),                   (2,  0),
            (-1, -1), (0, -1), (1, -1), (2, -1),
        ]
        edge_cells = (m.get_cell_by_coords(x, y) for (x, y) in edge_coordinates)
        habitable_edge_cells = [cell for cell in edge_cells if cell.habitable]

        self.assertGreaterEqual(len(habitable_edge_cells), 1)
