import pytest
import os
import json
import time
from src.etl.etl_service import ETLService

@pytest.fixture(scope="session")
def etl_service():
    """Create ETL service instance"""
    return ETLService(es_host=os.environ.get('ELASTICSEARCH_HOST', 'elasticsearch'))

@pytest.fixture(scope="session")
def es_client(etl_service):
    """Get Elasticsearch client from ETL service"""
    return etl_service.es

@pytest.fixture(scope="session")
def load_expected_results():
    """Load expected results from JSON file"""
    with open('tests/expected_results.json', 'r') as f:
        return json.load(f)

@pytest.fixture(scope="session", autouse=True)
def setup_data(etl_service):
    """Prepare Elasticsearch with proper data and mapping"""
    try:
        etl_service.run_etl("/app/data/Womens_Clothing.csv")
        # Wait for Elasticsearch to refresh
        time.sleep(2)
        return True
    except Exception as e:
        raise Exception(f"ETL process failed: {str(e)}")