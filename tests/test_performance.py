"""Tests de performance de la triangulation.

Marqués ``performance`` pour être lancés ou exclus séparément
"""

from __future__ import annotations

import random
import statistics
import time

import pytest

from triangulator.geometry import triangulate


def _points_grille(n: int) -> list[tuple[float, float]]:
    """Grille régulière de ``n`` points."""
    cote = int(n**0.5) + 1
    return [(float(x), float(y)) for x in range(cote) for y in range(cote)][:n]


def _points_aleatoires(n: int, graine: int) -> list[tuple[float, float]]:
    """Points uniformes reproductibles sur ``[-1000, 1000]²``."""
    rng = random.Random(graine)
    return [
        (rng.uniform(-1000.0, 1000.0), rng.uniform(-1000.0, 1000.0))
        for _ in range(n)
    ]


def _points_regroupes(n: int, graine: int) -> list[tuple[float, float]]:
    """Points regroupés autour de l'origine (gaussiennes)."""
    rng = random.Random(graine)
    return [(rng.gauss(0.0, 1.0), rng.gauss(0.0, 1.0)) for _ in range(n)]


def _mediane_duree(fonction, repetitions: int = 5) -> float:
    """Durée médiane de ``repetitions`` appels à ``fonction``."""
    durees = []
    for _ in range(repetitions):
        debut = time.perf_counter()
        fonction()
        durees.append(time.perf_counter() - debut)
    return statistics.median(durees)


@pytest.mark.performance
@pytest.mark.parametrize("n", [10, 100, 1000])
def test_performance_triangulation(n: int, record_property):
    """Mesure de la triangulation de ``n`` points aléatoires."""
    points = _points_aleatoires(n, graine=42)

    med = _mediane_duree(lambda: triangulate(points))

    record_property("mediane_triangulation_s", med)


@pytest.mark.performance
@pytest.mark.parametrize("taille", [100, 1000])
def test_performance_jeux_reproductibles(taille: int):
    """Vérifier que les trois jeux s'exécutent sur ``taille`` points."""
    for points in (
        _points_grille(taille),
        _points_aleatoires(taille, graine=7),
        _points_regroupes(taille, graine=7),
    ):
        assert isinstance(triangulate(points), list)
