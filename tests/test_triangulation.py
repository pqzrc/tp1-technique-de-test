"""Tests des cas simples et limites du contrat de triangulation."""

from itertools import permutations

import pytest

from triangulator.geometry import triangulate


@pytest.mark.parametrize(
    "points",
    list(permutations([(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)])),
)
def test_trois_points_non_alignes_forment_un_triangle(points):
    """Trois points non alignés forment un triangle, quel que soit l'ordre des indices."""
    triangles = triangulate(points)

    assert len(triangles) == 1
    assert len(triangles[0]) == 3
    assert all(type(index) is int for index in triangles[0])
    assert set(triangles[0]) == {0, 1, 2}


@pytest.mark.parametrize(
    "points",
    list(permutations([(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)])),
)
def test_quatre_coins_dun_carre_forment_deux_triangles(points):
    """Les deux triangles couvrent le carré, quelle que soit la diagonale choisie."""
    triangles = triangulate(points)

    assert len(triangles) == 2
    assert all(len(triangle) == 3 and len(set(triangle)) == 3 for triangle in triangles)
    assert all(set(triangle) <= {0, 1, 2, 3} for triangle in triangles)
    assert len(set(triangles[0]) & set(triangles[1])) == 2
    assert set(triangles[0]) | set(triangles[1]) == {0, 1, 2, 3}
    assert all(type(index) is int for triangle in triangles for index in triangle)

    # Les deux découpages autorisés sont définis indépendamment de l'algorithme.
    corners = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    geometric_triangles = {
        frozenset(points[index] for index in triangle) for triangle in triangles
    }
    allowed = [
        {frozenset(corners[index] for index in triangle) for triangle in split}
        for split in [((0, 1, 2), (0, 2, 3)), ((0, 1, 3), (1, 2, 3))]
    ]
    assert geometric_triangles in allowed


@pytest.mark.parametrize(
    "points",
    list(permutations([(0.0, 0.0), (3.0, 0.0), (0.0, 3.0), (1.0, 1.0)])),
)
def test_point_interieur_forme_trois_triangles(points):
    """Un point strictement intérieur découpe le triangle extérieur en trois."""
    triangles = triangulate(points)

    assert len(triangles) == 3
    assert all(len(triangle) == 3 for triangle in triangles)
    assert all(type(index) is int for triangle in triangles for index in triangle)
    assert all(0 <= index < len(points) for triangle in triangles for index in triangle)
    assert {frozenset(points[index] for index in triangle) for triangle in triangles} == {
        frozenset(((0.0, 0.0), (3.0, 0.0), (1.0, 1.0))),
        frozenset(((3.0, 0.0), (0.0, 3.0), (1.0, 1.0))),
        frozenset(((0.0, 0.0), (0.0, 3.0), (1.0, 1.0))),
    }


@pytest.mark.parametrize("points", [[], [(0.0, 0.0)], [(0.0, 0.0), (1.0, 1.0)]])
def test_moins_de_trois_points_ne_forment_pas_de_triangle(points):
    """Un ensemble de moins de trois points ne peut former aucun triangle."""
    assert triangulate(points) == []
