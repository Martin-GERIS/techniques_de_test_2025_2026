# TODO

## Fonction et classe du Triangulatore

Le service de triangulation est connecté au service `Client` ainsi qu'au service `PointSetManager`. Il communique avec ces services en binaire.<br>

### Classe `Point`
Un attribut pour chacune des deux coordonnées<br>

### Classe `PointSet`
Un attribut liste contenant les coordonnées de chaque `Point`.<br>

### Classe `Triangle`
Un attribut pour les coordonnées de chaque somment.  <br>

### Classe `Triangles`
Un attribut `PointSet`. Un attribut liste contenant les indices des `Point` du Triangle dans le `PointSet`.<br>

### Fonction `Tringulation`
Utilise un `PointSet` pour renvoyer un `Triangles`.<br>

### Fonction `DecimalConverter`
Utilise une valeur binaire pour renvoyer un `PointSet`.<br>

### Fonction `BinaryConverter`
Utilise un `Triangles` pour renvoyer une valeur binaire correspondante.<br>

### Fonction `CallPointSetManager`
Demande à `PointSetManager` le `PointSet` relatif au `PointSetId`. Renvoit ce `PointSet` et le code de `PointSetManager`.<br>

### Fonction `GetTriangulation`
Recoit un `PointSetId` du `Client` pour lui renvoyer une valeur binaire référent un `Triangles`.<br>


## Tests unitaires

### Triangulation

- [x] Test avec un `PointSet` de 3 points                           -> Renvoie un `Triangles` de 1 triangle<br>
- [x] Test avec un `PointSet` de 6 points                           -> Renvoie un `Triangles` de 5 triangle<br>
- [x] Test avec un `PointSet` vide                                  -> Apparition d'une erreur<br>
- [x] Test avec une variable null                                   -> Apparition d'une erreur<br>
- [x] Test avec un `PointSet` de 1 points                           -> Apparition d'une erreur<br>
- [x] Test avec un `PointSet` de 3 points colinéaires               -> Apparition d'une erreur<br>
- [x] Test avec un `PointSet` de 4 points dont 3 sont colinéaires   -> Renvoie un `Triangles` de 2 triangle<br>
- [x] Test avec un `PointSet` de 3 points dont 2 superposé          -> Renvoie un `Triangles` de 2 triangle<br>

### Convertisseur PointSet Décimal

- [x] Test avec une valeur binaire correspondant à un `PointSet`              -> Renvoie le `PointSet`<br>
- [x] Test avec une valeur binaire ne correspondant pas à un `PointSet`       -> Apparition d'une erreur<br>
- [x] Test avec une valeur binaire correspondant à un `PointSet` dont le      -> Apparition d'une erreur<br>
nombre de point annoncé ne correspond pas au nombre de point listé
- [x] Test avec une valeur binaire correspondant à un `PointSet` vide         -> Apparition d'une erreur<br>

### Convertisseur Triangles Binaire

- [x] Test avec un `Triangles`          -> une valeur binaire correspondant au `Triangles`<br>
- [x] Test avec un `Triangles` vide     -> Apparition d'une erreur<br>
- [x] Test avec une variable nulle      -> Apparition d'une erreur<br>

### Appel de PointSetManager

- [x] Test avec un `PointSetId` valide                                      -> revoie `200`, un `PointSet`<br>
- [x] Test avec un `PointSetId` invalide                                    -> revoie `400`, une variable nulle<br>
- [x] Test avec un `PointSetId` valide mais inconnu                         -> revoie `404`, une variable nulle<br>
- [x] Test avec un `PointSetId` valide et une erreur de la base de données  -> revoie `503`, une variable nulle<br>



## Tests d'intégration

### Intégralité de la pipeline

- [x] Test avec un `PointSetId` valide                                                          -> revoie une valeur binaire d'un `Triangles`, `200`<br>
- [x] Test avec un `PointSetId` invalide                                                        -> `400`<br>
- [x] Test avec un `PointSetId` inconnu                                                         -> `404`<br>
- [x] Test avec un `PointSetId` valide et une erreur de communication avec `PointSetManager`    -> `503`<br>



## Tests de performance

### Tests de charge

- [x] Mesure du temps de réponse avec un `PointSet` de 3 points<br>
- [x] Mesure du temps de réponse avec un `PointSet` de 30 points<br>
- [x] Mesure du temps de réponse avec un `PointSet` de 150 points<br>

- [x] Mesure du temps de réponse avec 5 `PointSetID`<br>
- [x] Mesure du temps de réponse avec 10 `PointSetID`<br>
- [x] Mesure du temps de réponse avec 50 `PointSetID`<br>

### Test d'endurance

- [x] Mesure du temps de réponse avec un `PointSet` de 12 points pendant 1m (un `PointSet` toute les 1 seconde)<br>