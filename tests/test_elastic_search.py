# test_elastic_exam.py
import os
import sys
import pytest
from elasticsearch import Elasticsearch
import json

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.queries.exam_queries import (
    query_q2_1, query_q2_2, query_q2_3, query_q2_4, query_q2_5, query_q2_6, query_q3,
    query_q4_1, query_q4_2, query_q4_3, query_q4_4,
    query_q5_1, query_q5_2, query_q5_3, query_q5_4
)

def test_unique_division_names(es_client, load_expected_results):
    """Test Q2-1: Count unique division names"""
    result = es_client.search(index="eval_new", body=query_q2_1)
    expected = load_expected_results["2-1"]["unique_division_name"]["value"]
    assert abs(result["aggregations"]["unique_division_name"]["value"] - expected) <= expected * 0.1

def test_unique_department_names(es_client, load_expected_results):
    """Test Q2-2: Count unique department names"""
    result = es_client.search(index="eval_new", body=query_q2_2)
    expected = load_expected_results["2-2"]["unique_department_name"]["value"]
    assert abs(result["aggregations"]["unique_department_name"]["value"] - expected) <= expected * 0.1

def test_unique_class_names(es_client, load_expected_results):
    """Test Q2-3: Count unique class names"""
    result = es_client.search(index="eval_new", body=query_q2_3)
    expected = load_expected_results["2-3"]["unique_class_name"]["value"]
    assert abs(result["aggregations"]["unique_class_name"]["value"] - expected) <= expected * 0.1

def test_products_by_department(es_client, load_expected_results):
    """Test Q2-4: Count products by department"""
    result = es_client.search(index="eval_new", body=query_q2_4)
    expected_buckets = load_expected_results["2-4"]["products_by_department"]["buckets"]
    result_buckets = result["aggregations"]["products_by_department"]["buckets"]
    
    for exp, res in zip(expected_buckets, result_buckets):
        assert exp["key"] == res["key"]
        assert abs(exp["doc_count"] - res["doc_count"]) <= exp["doc_count"] * 0.1

def test_departments_by_division(es_client, load_expected_results):
    """Test Q2-5: Count departments by division"""
    result = es_client.search(index="eval_new", body=query_q2_5)
    expected_buckets = load_expected_results["2-5"]["by_division"]["buckets"]
    result_buckets = result["aggregations"]["by_division"]["buckets"]
    
    for exp, res in zip(expected_buckets, result_buckets):
        assert exp["key"] == res["key"]
        # Check department counts within each division
        exp_deps = {b["key"]: b["doc_count"] for b in exp["by_department"]["buckets"]}
        res_deps = {b["key"]: b["doc_count"] for b in res["by_department"]["buckets"]}
        
        for key in exp_deps:
            assert key in res_deps
            # Allow for a 20% difference in counts
            tolerance = exp_deps[key] * 0.2
            assert abs(exp_deps[key] - res_deps[key]) <= tolerance, \
                f"Count mismatch for {key}: expected {exp_deps[key]}, got {res_deps[key]}"

def test_null_values(es_client, load_expected_results):
    """Test Q3: Check for null values in dataset"""
    result = es_client.search(index="eval_new", body=query_q3)
    expected_nulls = load_expected_results["3"]
    result_nulls = result["aggregations"]
    
    # Check missing counts for each field
    for field in ["missing_division", "missing_department", "missing_class", 
                 "missing_age", "missing_rating", "missing_review_text"]:
        assert abs(expected_nulls[field]["doc_count"] - result_nulls[field]["doc_count"]) <= 10

def test_rating_distribution(es_client, load_expected_results):
    """Test Q4-1: Rating distribution"""
    result = es_client.search(index="eval_new", body=query_q4_1)
    expected_buckets = load_expected_results["4-1"]["rating_distribution"]["buckets"]
    result_buckets = result["aggregations"]["rating_distribution"]["buckets"]
    
    for exp, res in zip(expected_buckets, result_buckets):
        assert exp["key"] == res["key"]
        assert abs(exp["doc_count"] - res["doc_count"]) <= exp["doc_count"] * 0.1

def test_age_stats(es_client, load_expected_results):
    """Test Q4-2: Age statistics"""
    result = es_client.search(index="eval_new", body=query_q4_2)
    expected_stats = load_expected_results["4-2"]["age_stats"]
    result_stats = result["aggregations"]["age_stats"]
    
    # Allow 2 years margin for age statistics
    for key in ["min", "max", "avg"]:
        assert abs(expected_stats[key] - result_stats[key]) <= 2

def test_class_scores(es_client, load_expected_results):
    """Test Q4-3: Class rating statistics"""
    result = es_client.search(index="eval_new", body=query_q4_3)
    expected_buckets = load_expected_results["4-3"]["class_scores"]["buckets"]
    result_buckets = result["aggregations"]["class_scores"]["buckets"]
    
    for exp, res in zip(expected_buckets, result_buckets):
        assert exp["key"] == res["key"]
        assert abs(exp["avg_score"]["value"] - res["avg_score"]["value"]) <= 0.5

def test_age_histogram_classes(es_client, load_expected_results):
    """Test Q4-4: Age histogram with top classes"""
    result = es_client.search(index="eval_new", body=query_q4_4)
    expected_buckets = load_expected_results["4-4"]["age_histogram"]["buckets"]
    result_buckets = result["aggregations"]["age_histogram"]["buckets"]
    
    for exp, res in zip(expected_buckets, result_buckets):
        assert exp["key"] == res["key"]
        assert abs(exp["doc_count"] - res["doc_count"]) <= exp["doc_count"] * 0.1

def test_best_rated_terms(es_client, load_expected_results):
    """Test Q5-1: Top rated products"""
    result = es_client.search(index="eval_new", body=query_q5_1)
    expected_buckets = load_expected_results["5-1"]["significant_terms"]["buckets"]
    actual_buckets = result["aggregations"]["significant_terms"]["buckets"]
    
    # Compare only the keys and their presence, not exact counts as they may vary
    expected_keys = {b["key"] for b in expected_buckets}
    actual_keys = {b["key"] for b in actual_buckets}
    assert len(actual_keys.intersection(expected_keys)) >= len(expected_keys) * 0.8, \
        "At least 80% of expected terms should be present in actual results"

def test_worst_rated_terms(es_client, load_expected_results):
    """Test Q5-2: Lowest rated products"""
    result = es_client.search(index="eval_new", body=query_q5_2)
    expected_buckets = load_expected_results["5-2"]["significant_terms"]["buckets"]
    actual_buckets = result["aggregations"]["significant_terms"]["buckets"]
    
    # Compare only the keys and their presence, not exact counts as they may vary
    expected_keys = {b["key"] for b in expected_buckets}
    actual_keys = {b["key"] for b in actual_buckets}
    assert len(actual_keys.intersection(expected_keys)) >= len(expected_keys) * 0.8, \
        "At least 80% of expected terms should be present in actual results"

def test_best_reviews(es_client, load_expected_results):
    """Test Q5-3: Best reviews"""
    result = es_client.search(index="eval_new", body=query_q5_3)
    actual_buckets = result["aggregations"]["by_product"]["buckets"]
    
    # Check if we have results
    assert len(actual_buckets) > 0, "Should have some top rated products"
    
    # Check if the first product has high rating and positive feedback
    top_product = actual_buckets[0]
    assert top_product["avg_rating"]["value"] >= 4.0, "Top product should have high rating"
    assert top_product["positive_feedback"]["value"] > 0, "Top product should have positive feedback"

def test_worst_reviews(es_client, load_expected_results):
    """Test Q5-4: Worst reviews"""
    result = es_client.search(index="eval_new", body=query_q5_4)
    actual_buckets = result["aggregations"]["by_product"]["buckets"]
    
    # Check if we have results
    assert len(actual_buckets) > 0, "Should have some poorly rated products"
    
    # Check if the first product has low rating
    worst_product = actual_buckets[0]
    assert worst_product["avg_rating"]["value"] <= 2.0, "Worst product should have low rating"