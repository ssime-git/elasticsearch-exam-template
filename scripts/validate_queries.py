#!/usr/bin/env python3
"""
Script d'aide pour valider vos requêtes ElasticSearch
Usage: python scripts/validate_queries.py
"""
import json
import sys
from elasticsearch import Elasticsearch
from src.queries.exam_queries import query_list

def validate_query_syntax():
    """Valide la syntaxe JSON de toutes les requêtes"""
    print("🔍 Validation de la syntaxe des requêtes...")
    
    query_names = [
        'query_q2_1', 'query_q2_2', 'query_q2_3', 'query_q2_4', 'query_q2_5', 'query_q2_6',
        'query_q3', 'query_q4_1', 'query_q4_2', 'query_q4_3', 'query_q4_4',
        'query_q5_1', 'query_q5_2', 'query_q5_3', 'query_q5_4'
    ]
    
    errors = []
    
    for i, query in enumerate(query_list):
        query_name = query_names[i] if i < len(query_names) else f"query_{i}"
        
        try:
            # Teste la sérialisation JSON
            json.dumps(query)
            
            # Vérifie que ce n'est pas vide
            if not query or query == {}:
                errors.append(f"❌ {query_name}: Requête vide")
            else:
                print(f"✅ {query_name}: Syntaxe OK")
                
        except Exception as e:
            errors.append(f"❌ {query_name}: Erreur syntaxe - {e}")
    
    return errors

def test_query_execution():
    """Teste l'exécution des requêtes sur ElasticSearch"""
    print("\n🚀 Test d'exécution des requêtes...")
    
    try:
        es = Elasticsearch('localhost:9200')
        
        if not es.ping():
            print("❌ ElasticSearch non accessible sur localhost:9200")
            print("💡 Lancez: docker-compose up -d elasticsearch")
            return False
            
        # Vérifie que l'index existe
        if not es.indices.exists(index='eval_new'):
            print("❌ Index 'eval_new' non trouvé")
            print("💡 Lancez: python src/etl/etl_service.py")
            return False
            
        query_names = ['q2_1', 'q2_2', 'q2_3', 'q2_4', 'q2_5', 'q2_6',
                      'q3', 'q4_1', 'q4_2', 'q4_3', 'q4_4',
                      'q5_1', 'q5_2', 'q5_3', 'q5_4']
        
        success_count = 0
        
        for i, query in enumerate(query_list):
            query_name = query_names[i] if i < len(query_names) else f"query_{i}"
            
            try:
                if query and query != {}:
                    result = es.search(index='eval_new', body=query, timeout='30s')
                    print(f"✅ {query_name}: Exécution OK ({result['took']}ms)")
                    success_count += 1
                else:
                    print(f"⏭️ {query_name}: Requête vide - ignorée")
                    
            except Exception as e:
                print(f"❌ {query_name}: Erreur exécution - {e}")
        
        print(f"\n📊 Résultat: {success_count}/{len([q for q in query_list if q and q != {}])} requêtes réussies")
        return success_count > 0
        
    except Exception as e:
        print(f"❌ Erreur connexion ElasticSearch: {e}")
        return False

def main():
    """Fonction principale"""
    print("🔧 Validation des requêtes d'examen ElasticSearch\n")
    
    # Validation syntaxe
    syntax_errors = validate_query_syntax()
    
    if syntax_errors:
        print("\n❌ Erreurs de syntaxe détectées:")
        for error in syntax_errors:
            print(f"   {error}")
        print("\n💡 Corrigez ces erreurs avant de continuer")
        return False
    
    # Test d'exécution
    execution_ok = test_query_execution()
    
    if execution_ok:
        print("\n🎉 Validation réussie ! Vos requêtes semblent correctes.")
        print("💡 Prochaine étape: pytest tests/test_elastic_search.py")
    else:
        print("\n❌ Des problèmes ont été détectés")
        print("💡 Consultez student-guides/TROUBLESHOOTING.md")
    
    return execution_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)