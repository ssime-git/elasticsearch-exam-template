# 🔍 ElasticSearch Cheat Sheet

## Agrégations essentielles

### Compter (cardinality)
```json
{"cardinality": {"field": "department.keyword"}}
```

### Grouper (terms)  
```json
{"terms": {"field": "class.keyword", "size": 10}}
```

### Statistiques (stats)
```json
{"stats": {"field": "rating"}}
```

### Histogramme
```json
{"histogram": {"field": "age", "interval": 10}}
```

### Significant terms (avancé)
```json
{"significant_text": {"field": "review_text", "size": 10}}
```

## Requêtes avec filtres

### Filtrer par range
```json
{
  "query": {"range": {"rating": {"gte": 4}}},
  "aggs": {...}
}
```

### Filtrer par valeurs
```json
{
  "query": {"terms": {"department.keyword": ["Tops", "Dresses"]}},
  "aggs": {...}  
}
```

## Agrégations imbriquées

```json
{
  "aggs": {
    "by_division": {
      "terms": {"field": "division.keyword"},
      "aggs": {
        "by_department": {
          "terms": {"field": "department.keyword"}
        }
      }
    }
  }
}
```

## Mapping optimal

```json
{
  "properties": {
    "age": {"type": "integer"},
    "rating": {"type": "integer"},
    "department": {"type": "keyword"},
    "review_text": {
      "type": "text",
      "analyzer": "standard",
      "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}
    }
  }
}
```