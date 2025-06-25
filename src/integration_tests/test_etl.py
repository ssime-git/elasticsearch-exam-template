import pytest
from elasticsearch import Elasticsearch
import os

@pytest.fixture(scope="session")
def es_client():
    """Create Elasticsearch client"""
    host = os.getenv("ELASTICSEARCH_HOST", "elasticsearch")
    es = Elasticsearch(hosts=[host])
    return es

def test_index_exists(es_client):
    """Test if the index was created"""
    assert es_client.indices.exists(index="eval_new")

def test_index_mapping(es_client):
    """Test if the index has the correct mapping"""
    mapping = es_client.indices.get_mapping(index="eval_new")
    properties = mapping["eval_new"]["mappings"]["properties"]
    
    assert "Age" in properties
    assert properties["Age"]["type"] == "integer"
    assert "Rating" in properties
    assert properties["Rating"]["type"] == "integer"
    assert "Class Name" in properties
    assert properties["Class Name"]["type"] == "keyword"

def test_index_settings(es_client):
    """Test if the index has the correct settings"""
    settings = es_client.indices.get_settings(index="eval_new")
    index_settings = settings["eval_new"]["settings"]["index"]
    
    # Check number of shards and replicas
    assert int(index_settings["number_of_shards"]) > 0
    assert "number_of_replicas" in index_settings

def test_data_loaded(es_client):
    """Test if data was loaded correctly"""
    # Check document count
    count = es_client.count(index="eval_new")["count"]
    assert count > 0, "No documents were loaded"
    
    # Check if we can query the data
    result = es_client.search(
        index="eval_new",
        body={
            "size": 1,
            "query": {"match_all": {}}
        }
    )
    
    assert len(result["hits"]["hits"]) > 0, "No documents found in search"
    
    # Check document structure
    doc = result["hits"]["hits"][0]["_source"]
    required_fields = ["Age", "Rating", "Class Name", "Department Name", "Review Text"]
    for field in required_fields:
        assert field in doc, f"Field {field} missing from document"

def test_data_types(es_client):
    """Test if the data types are correct in loaded documents"""
    result = es_client.search(
        index="eval_new",
        body={
            "size": 1,
            "query": {"match_all": {}}
        }
    )
    
    doc = result["hits"]["hits"][0]["_source"]
    
    # Check numeric fields
    assert isinstance(doc["Age"], (int, float))
    assert isinstance(doc["Rating"], (int, float))
    assert isinstance(doc["Positive Feedback Count"], (int, float))
    
    # Check text fields
    assert isinstance(doc["Review Text"], str)
    assert isinstance(doc["Class Name"], str)
    assert isinstance(doc["Department Name"], str)

def test_data_constraints(es_client):
    """Test if the data meets business constraints"""
    result = es_client.search(
        index="eval_new",
        body={
            "size": 0,
            "aggs": {
                "rating_stats": {
                    "stats": {
                        "field": "Rating"
                    }
                },
                "age_stats": {
                    "stats": {
                        "field": "Age"
                    }
                }
            }
        }
    )
    
    # Check rating constraints
    rating_stats = result["aggregations"]["rating_stats"]
    assert rating_stats["min"] >= 1, "Rating should not be less than 1"
    assert rating_stats["max"] <= 5, "Rating should not exceed 5"
    
    # Check age constraints
    age_stats = result["aggregations"]["age_stats"]
    assert age_stats["min"] >= 0, "Age should not be negative"
    assert age_stats["max"] <= 100, "Age should be reasonable"