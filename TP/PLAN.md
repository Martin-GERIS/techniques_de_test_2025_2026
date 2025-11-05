# TODO

## Fonction et classe du Triangulatore

Le service de triangulation est connecté au service `Client` ainsi qu'au service `PointSetManager`. Il communique avec ces services en binaire.

### Classe `PointSet`
Un attribut nombre correspondant aux nombre de point. Un attribut liste contenant les coordonnées de chaque point.
Une méthode de conversion en `PointSetBinary`

### Classe `Triangle`
Un attribut pour les coordonnées de chaque somment.
Une méthode de conversion en `TriangleBinary`

### Classe `Triangles`
Un attribut `PointSet`. Un attribut liste contenant `Triangle`.
Une méthode de conversion en `TrianglesBinary`



## Tests unitaires

### Triangulation

Test avec un `PointSet` de 3 points                 -> Renvoie un `Triangles` de 1 triangle
Test avec un `PointSet` de 9 points                 -> Renvoie un `Triangles` de 7 triangle
Test avec un `PointSet` vide                        -> Appartion d'une erreur
Test avec une variable null                         -> Appartion d'une erreur
Test avec un `PointSet` de 1 points                 -> Appartion d'une erreur
Test avec un `PointSet` de 6 points colinéaires     -> Appartion d'une erreur

### Convertisseur PointSet Décimal

Test avec une valeur binaire correspondant à un `PointSet`              -> Renvoie le `PointSet`
Test avec une valeur binaire ne correspondant pas à un `PointSet`       -> Appartion d'une erreur
Test avec une valeur binaire correspondant à un `PointSet` dont le 
nombre de point annoncé ne correspond pas au nombre de point listé      -> Appartion d'une erreur
Test avec une valeur binaire correspondant à un `PointSet` vide         -> Appartion d'une erreur

### Convertisseur Triangles Binaire

Test avec un `Triangles`          -> une valeur binaire correspondant au `Triangles`
Test avec un `Triangles` vide     -> Appartion d'une erreur
Test avec une variable nulle      -> Appartion d'une erreur



## Tests d'intégration

### Reception PointSetID du Client

Test avec un `PointSetID` valide    -> envoie du `PointSetID` au `PointSetManager`
Test avec un `PointSetID` invalide  -> Appartion d'une erreur, envoie du message d'erreur au Client

### Reception PointSet en binaire du PointSetManager

Test avec une valeur binaire correspondant à un `PointSet`          -> envoire d'un `Triangles` correspondant 
Test avec une valeur binaire ne correspondant pas à un `PointSet`   -> Appartion d'une erreur, envoie du message d'erreur au PointSetManager



## Tests de performance

### Tests de charge

Mesure du temps de réponse avec un `PointSet` de 3 points
Mesure du temps de réponse avec un `PointSet` de 30 points
Mesure du temps de réponse avec un `PointSet` de 150 points

Mesure du temps de réponse avec 1 `PointSetID` par seconde
Mesure du temps de réponse avec 10 `PointSetID` par seconde
Mesure du temps de réponse avec 50 `PointSetID` par seconde

### Test d'endurance

Mesure du temps de réponse avec un `PointSet` de 12 points pendant 1m (un `PointSet` toute les 1 seconde)