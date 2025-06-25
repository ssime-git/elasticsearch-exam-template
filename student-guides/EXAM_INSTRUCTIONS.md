# 📚 Guide d'Examen ElasticSearch

## 🎯 Objectifs pédagogiques
- Maîtriser les requêtes ElasticSearch (Query DSL)
- Comprendre les agrégations simples et complexes
- Optimiser le mapping et l'indexation
- Analyser des données business avec ElasticSearch

## 📋 Exercices à compléter

### Partie 1: Setup et ETL (50 points)
**Fichier:** `src/etl/etl_service.py`
- Compléter le mapping ElasticSearch optimal
- Gérer les types de données correctement

### Partie 2: Analyses de base (50 points)  
**Fichier:** `src/queries/exam_queries.py`
- Q2-1 à Q2-6: Agrégations simples (cardinality, terms)
- Q3: Vérification qualité des données

### Partie 3: Analyses avancées (50 points)
- Q4-1 à Q4-4: Histogrammes, statistiques, agrégations imbriquées

### Partie 4: Business Intelligence (50 points)
- Q5-1 à Q5-4: Analyse de sentiment, scoring complexe

## 🚀 Processus de travail

### 1. Setup local
```bash
git clone [VOTRE-FORK]
cd elasticsearch-exam-template
docker-compose up -d elasticsearch
```

### 2. Développement itératif
```bash
# Testez vos requêtes une par une
python -c "
from src.queries.exam_queries import query_q2_1
from elasticsearch import Elasticsearch
es = Elasticsearch('localhost:9200')
result = es.search(index='eval_new', body=query_q2_1)
print(result)
"
```

### 3. Tests automatiques
```bash
# Tests ETL
docker-compose run --rm integration-tests

# Tests des requêtes  
pytest tests/test_elastic_search.py -v
```

### 4. Soumission
- Créer une PR avec titre: "Examen ElasticSearch - [Votre Nom]"
- Les tests automatiques valideront votre travail
- Score minimum requis: 80%

## 💡 Conseils

### Requêtes fréquentes
```json
// Compter des valeurs uniques
{"aggs": {"count": {"cardinality": {"field": "champ.keyword"}}}}

// Grouper par catégorie
{"aggs": {"groups": {"terms": {"field": "champ.keyword"}}}}

// Statistiques numériques  
{"aggs": {"stats": {"stats": {"field": "champ_numerique"}}}}

// Histogramme
{"aggs": {"histo": {"histogram": {"field": "age", "interval": 10}}}}

// Filtrer puis agréger
{"query": {"range": {"rating": {"gte": 4}}}, "aggs": {...}}
```

### Pièges à éviter
- ❌ Oublier `.keyword` pour les champs text
- ❌ Mauvais type dans le mapping (text au lieu d'integer)  
- ❌ Syntaxe JSON invalide
- ❌ Requêtes trop lentes (> 30s)

### Debug
```bash
# Vérifier l'index
curl localhost:9200/eval_new/_mapping

# Tester une requête
curl -X POST localhost:9200/eval_new/_search -H "Content-Type: application/json" -d @query.json
```