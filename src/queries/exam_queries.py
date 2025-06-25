"""
Elasticsearch queries for the exam evaluation
COMPLETEZ LES REQUETES MARQUEES # TODO

Conseils:
- Testez vos requêtes une par une avec docker-compose
- Utilisez size: 0 pour les agrégations pures
- N'oubliez pas .keyword pour les champs text dans les agrégations
- Consultez la doc ElasticSearch: https://www.elastic.co/guide/en/elasticsearch/reference/7.15/
"""

# 2-1. Établir le nombre de valeurs uniques pour Division Name
query_q2_1 = {
    # TODO: Utilisez l'agrégation cardinality pour compter les divisions uniques
    # Indice: {"aggs": {"unique_divisions": {"cardinality": {"field": "..."}}}}
    "size": 0,
    "aggs": {
        # VOTRE CODE ICI
    }
}

# 2-2. Établir le nombre de valeurs uniques pour Department Name  
query_q2_2 = {
    # TODO: Comptez les départements uniques
    "size": 0,
    "aggs": {
        # VOTRE CODE ICI
    }
}

# 2-3. Établir le nombre de valeurs uniques pour Class Name
query_q2_3 = {
    # TODO: Comptez les classes uniques
    "size": 0,
    "aggs": {
        # VOTRE CODE ICI
    }
}

# 2-4. Compter les produits par département
query_q2_4 = {
    # TODO: Utilisez terms aggregation pour grouper par département
    "size": 0,
    "aggs": {
        # VOTRE CODE ICI
    }
}

# 2-5. Départements par division (requête complexe)
query_q2_5 = {
    # TODO: Agrégation imbriquée - divisions puis départements
    # Indice: Utilisez des agrégations imbriquées
    "size": 0,
    "aggs": {
        # VOTRE CODE ICI
    }
}

# 2-6. Lister les départements uniques
query_q2_6 = {
    # TODO: Listez tous les départements
    "size": 0,
    "aggs": {
        # VOTRE CODE ICI
    }
}

# 3. Vérifier les valeurs nulles
query_q3 = {
    # TODO: Utilisez missing aggregation pour chaque champ
    "size": 0,
    "aggs": {
        # VOTRE CODE ICI
    }
}

# 4-1. Distribution des ratings
query_q4_1 = {
    # TODO: Analysez la distribution des notes
    "size": 0,
    "aggs": {
        # VOTRE CODE ICI
    }
}

# 4-2. Statistiques d'âge  
query_q4_2 = {
    # TODO: Stats et histogramme des âges
    "size": 0,
    "aggs": {
        # VOTRE CODE ICI
    }
}

# 4-3. Scores par classe de produit
query_q4_3 = {
    # TODO: Agrégation par classe avec stats des ratings
    "size": 0,
    "aggs": {
        # VOTRE CODE ICI
    }
}

# 4-4. Histogramme âge avec top classes
query_q4_4 = {
    # TODO: Histogramme d'âge avec agrégation imbriquée des classes
    "size": 0,
    "aggs": {
        # VOTRE CODE ICI
    }
}

# 5-1. Termes dans les bons avis (AVANCÉ)
query_q5_1 = {
    # TODO: Significant terms dans les avis bien notés
    # Indice: Utilisez significant_text aggregation
    "size": 0,
    "query": {
        # VOTRE CODE ICI - filtrer les bons ratings
    },
    "aggs": {
        # VOTRE CODE ICI
    }
}

# 5-2. Termes dans les mauvais avis (AVANCÉ)
query_q5_2 = {
    # TODO: Significant terms dans les avis mal notés
    "size": 0,
    "query": {
        # VOTRE CODE ICI
    },
    "aggs": {
        # VOTRE CODE ICI
    }
}

# 5-3. Meilleurs produits à garder (EXPERT)
query_q5_3 = {
    # TODO: Scoring complexe avec bucket_script
    # Combinez rating, nombre d'avis, feedback positif
    "size": 0,
    "aggs": {
        # VOTRE CODE ICI - agrégation très complexe
    }
}

# 5-4. Produits à éviter (EXPERT)
query_q5_4 = {
    # TODO: Inverse de Q5-3 - produits avec mauvaises performances
    "size": 0,
    "aggs": {
        # VOTRE CODE ICI
    }
}

# Liste pour les tests automatiques (NE PAS MODIFIER)
query_list = [query_q2_1, query_q2_2, query_q2_3, query_q2_4, query_q2_5, query_q2_6, query_q3,
              query_q4_1, query_q4_2, query_q4_3, query_q4_4,
              query_q5_1, query_q5_2, query_q5_3, query_q5_4]