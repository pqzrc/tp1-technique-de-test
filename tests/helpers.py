"""Outils géométriques minimaux utilisés par les tests."""

from __future__ import annotations


def produit_vectoriel(
    a: tuple[float, float],
    b: tuple[float, float],
    c: tuple[float, float],
) -> float:
    """Produit vectoriel 2D des vecteurs (b - a) et (c - a).

    Le signe indique l'orientation : positif si (a, b, c) est direct, négatif
    sinon, et nul si les trois points sont alignés.
    """
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def aire_triangle(
    a: tuple[float, float],
    b: tuple[float, float],
    c: tuple[float, float],
) -> float:
    """Aire du triangle (a, b, c), moitié de la valeur absolue du produit vectoriel."""
    return abs(produit_vectoriel(a, b, c)) / 2
