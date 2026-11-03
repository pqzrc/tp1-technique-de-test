"""Triangulation d'un ensemble de points 2D."""

from __future__ import annotations


def triangulate(points: list[tuple[float, float]]) -> list[tuple[int, int, int]]:
    """Retourner les indices des sommets de chaque triangle obtenu.

    Les triangles retournés doivent former une triangulation valide de
    l'enveloppe convexe de ``points`` : non dégénérés, sans chevauchement,
    couvrant exactement l'enveloppe et utilisant chaque point distinct.

    L'algorithme doit être implémenté « from scratch », sans bibliothèque de
    géométrie externe.
    """
    raise NotImplementedError("Algorithme de triangulation à implémenter")
