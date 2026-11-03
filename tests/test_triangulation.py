"""Tests des cas simples et limites de la triangulation."""

from __future__ import annotations

from itertools import permutations

import pytest
from helpers import aire_triangle

from triangulator.geometry import triangulate


@pytest.mark.parametrize(
    "points",
    list(permutations([(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)])),
)
def test_trois_points_non_alignes_forment_un_triangle(points):
    """Trois points non alignés forment un triangle, quel que soit l'ordre."""
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
    triangles_geometriques = {
        frozenset(points[index] for index in triangle) for triangle in triangles
    }
    assert triangles_geometriques == {
        frozenset(((0.0, 0.0), (3.0, 0.0), (1.0, 1.0))),
        frozenset(((3.0, 0.0), (0.0, 3.0), (1.0, 1.0))),
        frozenset(((0.0, 0.0), (0.0, 3.0), (1.0, 1.0))),
    }


@pytest.mark.parametrize("points", [[], [(0.0, 0.0)], [(0.0, 0.0), (1.0, 1.0)]])
def test_moins_de_trois_points_ne_forment_pas_de_triangle(points):
    """Un ensemble de moins de trois points ne peut former aucun triangle."""
    assert triangulate(points) == []


@pytest.mark.parametrize(
    ("points", "nb_triangles"),
    [
        ([(0.0, 0.0), (2.0, 0.0), (3.0, 1.0), (1.0, 3.0), (-1.0, 1.0)], 3),
        ([(0.0, 0.0), (2.0, 0.0), (3.0, 1.0), (3.0, 3.0), (1.0, 4.0), (-1.0, 2.0)], 4),
    ],
)
def test_polygone_convexe_donne_n_moins_deux_triangles(points, nb_triangles):
    """Un polygone convexe de N sommets produit N - 2 triangles non dégénérés."""
    triangles = triangulate(points)

    assert len(triangles) == nb_triangles
    for triangle in triangles:
        assert len(triangle) == 3
        assert len(set(triangle)) == 3
        assert all(isinstance(index, int) for index in triangle)
        assert all(0 <= index < len(points) for index in triangle)
        a, b, c = (points[index] for index in triangle)
        assert aire_triangle(a, b, c) > 0


# --- Cas dont le comportement attendu reste à clarifier avec l'énoncé --------


@pytest.mark.skip(
    reason="TODO : clarifier le comportement pour des points tous alignés"
)
def test_points_alignes():
    """Points tous alignés : liste vide ou erreur, à définir avec l'énoncé."""
    assert triangulate([(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)]) == []


@pytest.mark.skip(reason="TODO : clarifier la politique de gestion des doublons")
def test_doublons():
    """Doublons : suppression ou rejet, à définir avec l'énoncé."""
    assert triangulate([(0.0, 0.0), (1.0, 0.0), (0.0, 1.0), (0.0, 0.0)]) == [(0, 1, 2)]


@pytest.mark.skip(reason="TODO : clarifier la gestion des coordonnées non finies")
def test_coordonnees_non_finies():
    """NaN et infinis : rejet ou traitement, à définir avec l'énoncé."""
    with pytest.raises(ValueError):
        triangulate([(0.0, 0.0), (1.0, 0.0), (float("nan"), 1.0)])


@pytest.mark.skip(reason="TODO : clarifier le cas d'un point sur une arête")
def test_point_sur_une_arete():
    """Un point exactement sur une arête ne doit pas produire de triangle dégénéré."""
    triangles = triangulate([(0.0, 0.0), (2.0, 0.0), (1.0, 0.0), (0.0, 2.0)])

    assert all(len(set(triangle)) == 3 for triangle in triangles)
