# 📚 Examen ElasticSearch - Template Étudiant

## 🎯 Objectif
Démontrer votre maîtrise d'ElasticSearch en complétant les requêtes et optimisations manquantes.

## 🚀 Démarrage rapide

### 1. Fork et clone
```bash
git clone [VOTRE-FORK]
cd elasticsearch-exam-template
```

### 2. Démarrage de l'environnement
```bash
# Démarrer ElasticSearch
docker-compose up -d elasticsearch

# Attendre que ES soit prêt (1-2 minutes)
docker-compose logs -f elasticsearch
```

### 3. Exécuter l'ETL
```bash
docker-compose run --rm etl
```

### 4. Valider votre travail
```bash
# Validation rapide
python scripts/validate_queries.py

# Tests complets
pytest tests/test_elastic_search.py -v
```

## 📁 Fichiers à modifier

### ✏️ Obligatoires
- `src/queries/exam_queries.py` - **Complétez toutes les requêtes**
- `src/etl/etl_service.py` - **Optimisez le mapping**

### 📖 Ressources
- `student-guides/EXAM_INSTRUCTIONS.md` - Guide détaillé
- `student-guides/ELASTICSEARCH_CHEATSHEET.md` - Aide-mémoire
- `student-guides/TROUBLESHOOTING.md` - Résolution de problèmes

## 🎯 Critères de validation

| Catégorie | Points | Seuil |
|-----------|--------|--------|
| ETL & Mapping | 50 pts | 40 pts |
| Analyses de base | 50 pts | 40 pts |
| Analyses avancées | 50 pts | 35 pts |
| Business Intelligence | 50 pts | 30 pts |
| **TOTAL** | **200 pts** | **≥ 160 pts (80%)** |

## 📤 Soumission

1. **Testez localement** - Toutes les requêtes doivent passer
2. **Créez une PR** - Titre: "Examen ElasticSearch - [Votre Nom]"
3. **Validation automatique** - Les GitHub Actions valideront votre travail
4. **Feedback immédiat** - Rapport détaillé posté sur votre PR

## 🆘 Support

- 📖 Consultez les guides dans `student-guides/`
- 🐛 Utilisez `scripts/validate_queries.py` pour débugger
- 🔍 Vérifiez les logs: `docker-compose logs elasticsearch`
- ❓ Créez une issue GitHub pour l'aide technique

---

**Bonne chance ! 🍀**

*Temps estimé: 3-4 heures | Niveau: Intermédiaire*