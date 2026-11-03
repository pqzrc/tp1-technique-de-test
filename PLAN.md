# Plan de tests

On utilisera pytest et on simulera les réponses du PointSetManager pour tester les différents cas, même quand ce service est indisponible. Les tests seront écrits avant l'implémentation. Chaque cas indiquera ses données d'entrée, le résultat attendu et les assertions permettant de le vérifier.

Les comportements non précisés par le sujet seront clarifiés avant d'être figés dans les tests : ordre des octets du format binaire, traitement des doublons, points alignés, coordonnées non finies et réponse HTTP en cas de contenu distant invalide. Pour moins de trois points, les tests actuels retiennent une liste de triangles vide.

## Tests unitaires

on teste les conversions et le calcul séparément, sans appeler le PointSetManager

Test 1 : lecture et écriture du format binaire

On teste séparément PointSet et Triangles avec des octets de référence indépendants de l'encodeur. La lecture doit retrouver les coordonnées, compteurs et indices attendus ; l'écriture doit produire exactement les octets de référence. On utilise notamment des coordonnées négatives et des fractions exactement représentables, comme 1.5, un ensemble vide et plusieurs triangles partageant des sommets.

On vérifie les tailles : 4 + 8N octets pour PointSet, 8 + 8N + 12T pour Triangles. On ajoute des aller-retours encodage/décodage, sans en faire la seule vérification : deux conversions pourraient partager la même erreur. L'ordre des octets doit être confirmé avec le PointSetManager.

Test 2 : Données binaires incorrectes

On fournit des données vides, un compteur tronqué, des coordonnées tronquées, un compteur incompatible avec la taille du contenu et des octets supplémentaires. Pour Triangles, on teste aussi un compteur de triangles tronqué, des indices tronqués et des indices hors limites. Le programme doit détecter le problème sans produire un résultat partiel. L'exception interne attendue et la politique concernant les octets supplémentaires seront définies avant l'implémentation.

Test 3 : Triangulation simple

Avec trois points non alignés, on doit obtenir un triangle utilisant exactement les trois sommets.
Avec les quatre coins d'un carré, on doit obtenir deux triangles correspondant à l'une des deux diagonales possibles. On vérifie les sommets, l'absence de doublons et la couverture, pas seulement le nombre de triangles.
Avec un point strictement à l'intérieur d'un triangle, on doit obtenir les trois triangles reliant ce point aux trois arêtes extérieures.
On prévoit également un polygone convexe de plus de quatre sommets pour dépasser les cas minimaux.

Test 4 : Vérification des triangles obtenus

On vérifie que chaque triangle possède trois indices entiers distincts et valides, une aire non nulle et utilise uniquement les points fournis. Aucun triangle ne doit être répété, même avec un ordre de sommets différent. Tous les points distincts doivent être utilisés selon la politique retenue pour les doublons.

Les triangles doivent couvrir l'enveloppe convexe sans trou ni chevauchement. On compare la somme des aires à l'aire de l'enveloppe et on vérifie séparément l'absence de chevauchement : la somme seule ne suffit pas. Les vérifications ne doivent pas simplement réutiliser l'algorithme testé.

On change l'ordre des points et on vérifie encore la validité géométrique, sans exiger les mêmes indices ni la même diagonale. On prévoit aussi des translations et changements d'échelle sur des cas bien choisis. Aucune propriété de Delaunay n'est imposée par le sujet.

Test 5 : Cas limites de la triangulation

Pour aucun point, un point ou deux points, les tests actuels attendent une liste de triangles vide. On prévoit également des points alignés, des doublons, des points tous identiques et des points sur une arête avec d'autres points non alignés. On clarifiera les résultats attendus pour ces autres cas : erreur ou résultat vide, suppression ou rejet des doublons, conservation des sommets dans le format de sortie.

Test 6 : Coordonnées difficiles

On choisit des jeux explicites de points très proches et de coordonnées très grandes ou très petites représentables en float sur 4 octets. On vérifie les propriétés du test 4 avec une tolérance justifiée et adaptée à l'échelle. On vérifie également les coordonnées après encodage/décodage : deux valeurs distinctes en Python peuvent devenir identiques en float sur 4 octets. On prévoit NaN et les infinis, avec une politique de rejet ou de traitement à définir. Ces tests vérifient la robustesse du calcul.

## Tests d’intégration de composants : API

On teste la route de l’API avec les conversions et le calcul. On simule le PointSetManager pour contrôler ses réponses et ses pannes.

Test 7 : Réponse de l'API

Un GET /triangulation/{pointSetId} avec un identifiant valide et un ensemble existant doit répondre 200 avec Content-Type application/octet-stream. On décode le corps et on vérifie les sommets et triangles attendus. On vérifie également la récupération du bon ensemble auprès du PointSetManager.

Test 8 : Vérification de l'identifiant

On envoie plusieurs identifiants mal formés, dont "lkj". L'API doit répondre 400 sans appeler le PointSetManager.
Avec un UUID valide et une réponse 404 simulée du PointSetManager, elle doit répondre 404.

Test 9 : Problème avec le PointSetManager

On teste séparément une connexion refusée, un délai d'attente dépassé et une réponse HTTP 503 du PointSetManager. Le Triangulator doit répondre 503 avec un JSON d'erreur conforme. On vérifie qu'un délai d'attente est configuré et que la requête utilise GET /pointset/{pointSetId} avec le bon identifiant.

On ajoute une réponse HTTP 200 contenant un binaire invalide : le Triangulator ne doit pas répondre avec une triangulation réussie. Le statut attendu dans ce cas doit être défini et documenté.

Test 10 : Erreur pendant le calcul

On simule une exception de la fonction de triangulation et on vérifie que l'API répond 500. Ce scénario est distinct des cas géométriques limites pris en charge normalement.
Pour toutes les réponses d'erreur, on vérifie Content-Type application/json et la présence des champs code et message, tous deux de type chaîne.

Test 11 : Plusieurs demandes à la suite

Sur la même instance de l'application, on demande la triangulation de deux ensembles aux résultats clairement différents. Chaque réponse doit correspondre au bon ensemble, sans réutiliser les données précédentes. On prévoit également la séquence réussite, échec, réussite.

Test 12 : Retour à la normale après une panne

Sur la même instance de l'application, on simule une récupération indisponible et on vérifie la réponse 503. On simule ensuite une récupération réussie : une nouvelle requête doit répondre 200 avec les bons triangles, sans redémarrer le Triangulator. On vérifie qu'un nouvel appel au PointSetManager a effectivement lieu.

## Tests d’intégration entre services

on vérifie les échanges avec le vrai PointSetManager

Test 13 : fonctionnement complet

Avec le vrai PointSetManager, on enregistre un ensemble de points, on vérifie la réponse 201 et on récupère le champ pointSetId. On demande ensuite sa triangulation et on vérifie le statut 200, le type de contenu et les triangles décodés. Ce test vérifie notamment la compatibilité réelle du format binaire.

On documente les prérequis de lancement du service. Ces tests porteront un marqueur integration et seront sélectionnables séparément ; en son absence, leur non-exécution sera explicitement signalée. Ils complètent les simulations sans les remplacer.

## Tests de performance

On mesure le temps pris par les opérations

Test 14 : performances

On mesure séparément encodage, décodage et triangulation avec 10, 100 et 1 000 points. On utilise des jeux reproductibles : grilles, points aléatoires avec graine fixe et points regroupés. Les données sont préparées hors de la mesure ; les mesures sont répétées et leur médiane est rapportée, avec l'environnement d'exécution.

Ces tests portent un marqueur performance pour être lancés ou exclus séparément. L'objectif initial est de mesurer et comparer, sans seuil arbitraire dépendant de la machine.

## Exécution, couverture et qualité

Les cibles make test, make unit_test, make perf_test, make coverage, make lint et make doc seront fournies conformément au README. make unit_test exclura les tests de performance et make perf_test les sélectionnera.

Le rapport de couverture permettra de repérer les lignes et branches non exercées, notamment les branches d'erreur. La couverture ne remplace pas la pertinence des assertions. On vérifiera également ruff check sans retirer de règles fournies et la génération de documentation HTML avec pdoc3.
