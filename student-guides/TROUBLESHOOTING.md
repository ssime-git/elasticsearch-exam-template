# 🔧 Guide de Dépannage

## Problèmes fréquents

### 1. ElasticSearch ne démarre pas
**Symptôme:** `Connection refused` ou timeout
**Solutions:**
```bash
# Vérifier l'état des conteneurs
docker-compose ps

# Redémarrer ElasticSearch
docker-compose down
docker-compose up -d elasticsearch

# Vérifier les logs
docker-compose logs elasticsearch
```

### 2. Index non trouvé
**Symptôme:** `index_not_found_exception`
**Solutions:**
```bash
# Vérifier les index existants
curl localhost:9200/_cat/indices

# Relancer l'ETL
python src/etl/etl_service.py

# Ou via Docker
docker-compose run --rm etl
```

### 3. Erreurs de mapping
**Symptôme:** `strict_dynamic_mapping_exception`
**Solutions:**
- Vérifier le mapping dans `src/etl/etl_service.py`
- S'assurer que tous les champs sont définis
- Types corrects: integer, keyword, text

### 4. Syntaxe JSON invalide
**Symptôme:** `parsing_exception`
**Solutions:**
```bash
# Valider la syntaxe
python scripts/validate_queries.py

# Vérifier les accolades et virgules
# Utiliser un validateur JSON en ligne
```

### 5. Agrégations qui échouent
**Symptôme:** `illegal_argument_exception`
**Solutions:**
- Utiliser `.keyword` pour les champs text
- Vérifier que le champ existe
- Respecter la structure des agrégations

## Commandes de debug

### Vérifier la santé d'ElasticSearch
```bash
curl localhost:9200/_cluster/health?pretty
```

### Voir la structure de l'index
```bash
curl localhost:9200/eval_new/_mapping?pretty
```

### Compter les documents
```bash
curl localhost:9200/eval_new/_count?pretty
```

### Tester une requête simple
```bash
curl -X POST localhost:9200/eval_new/_search?pretty -H "Content-Type: application/json" -d '
{
  "size": 1,
  "query": {"match_all": {}}
}'
```

## Ressources utiles

- [Documentation ElasticSearch](https://www.elastic.co/guide/en/elasticsearch/reference/7.15/)
- [Query DSL](https://www.elastic.co/guide/en/elasticsearch/reference/7.15/query-dsl.html)
- [Agrégations](https://www.elastic.co/guide/en/elasticsearch/reference/7.15/search-aggregations.html)