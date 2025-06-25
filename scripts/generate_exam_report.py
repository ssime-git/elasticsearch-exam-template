#!/usr/bin/env python3
"""
Script de génération de rapport d'examen pour ElasticSearch
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path
import xml.etree.ElementTree as ET

class ExamReportGenerator:
    def __init__(self):
        self.test_results = {}
        self.exam_score = 0
        self.total_points = 0
        self.student_info = self._get_student_info()
        
    def _get_student_info(self):
        """Récupère les informations de l'étudiant depuis la PR"""
        return {
            'name': os.getenv('GITHUB_ACTOR', 'Student'),
            'pr_number': os.getenv('GITHUB_PR_NUMBER', 'Unknown'),
            'branch': os.getenv('GITHUB_HEAD_REF', 'Unknown'),
            'commit': os.getenv('GITHUB_SHA', 'Unknown')[:8],
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def parse_pytest_results(self, junit_file="test-results/pytest-results.xml"):
        """Parse les résultats pytest depuis le fichier JUnit XML"""
        if not os.path.exists(junit_file):
            print(f"Fichier de résultats non trouvé: {junit_file}")
            return
            
        try:
            tree = ET.parse(junit_file)
            root = tree.getroot()
            
            for testcase in root.findall('.//testcase'):
                test_name = testcase.get('name')
                class_name = testcase.get('classname')
                time_taken = float(testcase.get('time', 0))
                
                # Détermine si le test a réussi
                failure = testcase.find('failure')
                error = testcase.find('error')
                skipped = testcase.find('skipped')
                
                status = 'PASSED'
                message = ''
                
                if failure is not None:
                    status = 'FAILED'
                    message = failure.get('message', '')
                elif error is not None:
                    status = 'ERROR'
                    message = error.get('message', '')
                elif skipped is not None:
                    status = 'SKIPPED'
                    message = skipped.get('message', '')
                
                self.test_results[test_name] = {
                    'status': status,
                    'class': class_name,
                    'time': time_taken,
                    'message': message,
                    'points': self._calculate_points(test_name, status)
                }
                
        except Exception as e:
            print(f"Erreur lors du parsing des résultats: {e}")
    
    def _calculate_points(self, test_name, status):
        """Calcule les points pour un test donné"""
        # Grille de notation basée sur le nom du test
        point_map = {
            'test_unique_division_names': 5,
            'test_unique_department_names': 5,
            'test_unique_class_names': 5,
            'test_products_by_department': 10,
            'test_departments_by_division': 15,
            'test_null_values': 10,
            'test_rating_distribution': 10,
            'test_age_stats': 10,
            'test_class_scores': 15,
            'test_age_histogram_classes': 15,
            'test_best_rated_terms': 20,
            'test_worst_rated_terms': 20,
            'test_best_reviews': 25,
            'test_worst_reviews': 25,
            # Tests ETL
            'test_index_exists': 10,
            'test_index_mapping': 10,
            'test_data_loaded': 15,
            'test_data_types': 10,
            'test_data_constraints': 10
        }
        
        max_points = point_map.get(test_name, 5)
        self.total_points += max_points
        
        if status == 'PASSED':
            return max_points
        elif status == 'SKIPPED':
            return max_points // 2
        else:
            return 0
    
    def calculate_score(self):
        """Calcule le score final"""
        earned_points = sum(result['points'] for result in self.test_results.values())
        self.exam_score = (earned_points / self.total_points * 100) if self.total_points > 0 else 0
        return self.exam_score
    
    def generate_markdown_report(self):
        """Génère un rapport Markdown pour les commentaires PR"""
        passed_tests = sum(1 for r in self.test_results.values() if r['status'] == 'PASSED')
        failed_tests = sum(1 for r in self.test_results.values() if r['status'] == 'FAILED')
        total_tests = len(self.test_results)
        
        status_emoji = "✅" if self.exam_score >= 80 else "❌"
        
        markdown_content = f"""## {status_emoji} Rapport d'Examen ElasticSearch

**Score Final: {self.exam_score:.1f}%**

### 📊 Résumé
- ✅ Tests réussis: {passed_tests}
- ❌ Tests échoués: {failed_tests}
- 📝 Total: {total_tests}

### 📋 Détail par catégorie

| Catégorie | Tests | Points | Statut |
|-----------|-------|--------|---------|
"""
        
        # Grouper les tests par catégorie
        categories = {
            'ETL & Setup': ['test_index_exists', 'test_index_mapping', 'test_data_loaded', 
                           'test_data_types', 'test_data_constraints'],
            'Analyse de base': ['test_unique_division_names', 'test_unique_department_names', 
                               'test_unique_class_names', 'test_products_by_department'],
            'Analyse avancée': ['test_departments_by_division', 'test_null_values', 
                               'test_rating_distribution', 'test_age_stats'],
            'Requêtes complexes': ['test_class_scores', 'test_age_histogram_classes', 
                                  'test_best_rated_terms', 'test_worst_rated_terms'],
            'Business Intelligence': ['test_best_reviews', 'test_worst_reviews']
        }
        
        for category, tests in categories.items():
            category_tests = [t for t in tests if t in self.test_results]
            if category_tests:
                passed_in_category = sum(1 for t in category_tests 
                                       if self.test_results[t]['status'] == 'PASSED')
                points_in_category = sum(self.test_results[t]['points'] for t in category_tests)
                max_points_in_category = sum(self._get_max_points(t) for t in category_tests)
                
                status_icon = "✅" if passed_in_category == len(category_tests) else "⚠️"
                markdown_content += f"| {category} | {passed_in_category}/{len(category_tests)} | {points_in_category}/{max_points_in_category} | {status_icon} |\n"
        
        if self.exam_score >= 80:
            markdown_content += """
### 🎉 Félicitations !
Votre examen ElasticSearch est validé ! Vous maîtrisez bien les concepts de recherche et d'analyse de données.

**Prochaines étapes :**
- Votre PR peut être mergée
- Certificat d'examen généré
"""
        else:
            failed_tests_list = [name for name, result in self.test_results.items() 
                               if result['status'] == 'FAILED']
            markdown_content += f"""
### 📝 Actions requises
Votre examen nécessite des corrections. Tests à revoir :

{chr(10).join(f"- ❌ {test}" for test in failed_tests_list)}

**Conseils :**
- Vérifiez vos requêtes ElasticSearch dans `src/queries/exam_queries.py`
- Consultez student-guides/ELASTICSEARCH_CHEATSHEET.md
- Testez vos requêtes localement avec `python scripts/validate_queries.py`
"""
        
        with open('exam-report.md', 'w', encoding='utf-8') as f:
            f.write(markdown_content)
    
    def _get_max_points(self, test_name):
        """Retourne le nombre maximum de points pour un test"""
        point_map = {
            'test_unique_division_names': 5,
            'test_unique_department_names': 5,
            'test_unique_class_names': 5,
            'test_products_by_department': 10,
            'test_departments_by_division': 15,
            'test_null_values': 10,
            'test_rating_distribution': 10,
            'test_age_stats': 10,
            'test_class_scores': 15,
            'test_age_histogram_classes': 15,
            'test_best_rated_terms': 20,
            'test_worst_rated_terms': 20,
            'test_best_reviews': 25,
            'test_worst_reviews': 25,
            'test_index_exists': 10,
            'test_index_mapping': 10,
            'test_data_loaded': 15,
            'test_data_types': 10,
            'test_data_constraints': 10
        }
        return point_map.get(test_name, 5)

def main():
    """Fonction principale"""
    generator = ExamReportGenerator()
    
    # Parse les résultats de tests
    generator.parse_pytest_results()
    
    # Calcule le score
    score = generator.calculate_score()
    
    # Génère le rapport
    generator.generate_markdown_report()
    
    print(f"Rapport généré - Score final: {score:.1f}%")
    
    # Définit le code de sortie pour les actions GitHub
    exit_code = 0 if score >= 80 else 1
    sys.exit(exit_code)

if __name__ == "__main__":
    main()