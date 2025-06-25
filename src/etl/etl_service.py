"""
ETL Service for loading and transforming data into Elasticsearch
"""
import pandas as pd
from elasticsearch import Elasticsearch
import os
import logging
import time
import numpy as np
import socket
from elasticsearch import helpers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ETLService:
    def __init__(self, es_host="elasticsearch"):
        self.es_host = es_host
        self.index_name = "eval_new"
        self.es = self._connect_elasticsearch()
        
    def _wait_for_elasticsearch(self):
        """Wait for Elasticsearch to be reachable"""
        max_retries = 60  # wait up to 60 seconds
        for i in range(max_retries):
            try:
                # Try to resolve the hostname first
                socket.gethostbyname(self.es_host)
                return True
            except socket.gaierror:
                if i < max_retries - 1:  # don't sleep on the last attempt
                    logger.warning(f"Could not resolve hostname {self.es_host}, retrying in 1 second...")
                    time.sleep(1)
                continue
        return False

    def _connect_elasticsearch(self):
        """Connect to Elasticsearch with retries"""
        if not self._wait_for_elasticsearch():
            raise Exception(f"Could not resolve hostname {self.es_host} after 60 seconds")

        max_retries = 60  # wait up to 60 seconds
        for i in range(max_retries):
            try:
                client = Elasticsearch(f"http://{self.es_host}:9200")
                if client.ping():
                    logger.info("Successfully connected to Elasticsearch")
                    return client
            except Exception as e:
                if i < max_retries - 1:  # don't sleep on the last attempt
                    logger.warning(f"Connection attempt failed: {str(e)}")
                    time.sleep(1)
                continue
        
        raise Exception("Could not connect to Elasticsearch after 60 seconds")
        
    def read_data(self, file_path):
        """Read the CSV data"""
        logger.info(f"Reading data from {file_path}")
        return pd.read_csv(file_path)
        
    def transform_data(self, df):
        """Transform data before loading into Elasticsearch"""
        # Make a copy to avoid SettingWithCopyWarning
        df = df.copy()

        # Only drop rows where Rating is missing, as it's the most critical field
        df = df.dropna(subset=['Rating'])

        # Clean text fields, but preserve original case
        text_fields = ['Title', 'Review Text']
        for field in text_fields:
            df[field] = df[field].fillna('').astype(str).str.strip()

        # Clean categorical fields, preserving original case
        categorical_fields = ['Division Name', 'Department Name', 'Class Name']
        for field in categorical_fields:
            df[field] = df[field].fillna('Unknown').astype(str).str.strip()
            # Fix known typos
            if field == 'Division Name':
                df[field] = df[field].replace({'Initmates': 'Intimates', 'initmates': 'Intimates'})

        # Handle numeric fields more carefully
        df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
        df['Age'] = df['Age'].fillna(-1).clip(0, 100).astype(int)  # Use -1 for unknown age
        
        df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
        df['Rating'] = df['Rating'].clip(1, 5).astype(int)  # Ratings must be 1-5
        
        # Other integer fields can be 0 when missing
        other_int_fields = ['Recommended IND', 'Positive Feedback Count', 'Clothing ID']
        for field in other_int_fields:
            df[field] = pd.to_numeric(df[field], errors='coerce').fillna(0).astype(int)

        return df
        
    def get_index_mapping(self):
        """Get the Elasticsearch index mapping"""
        return {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0,
                # TODO: Ajoutez un analyzer personnalisé pour les reviews
                # Exemple: "analysis": {"analyzer": {"review_analyzer": {...}}}
            },
            "mappings": {
                "properties": {
                    # TODO: Définir le mapping correct pour chaque champ
                    # Age: doit être "integer"
                    # Rating: doit être "integer" 
                    # Recommended IND: doit être "integer"
                    # Positive Feedback Count: doit être "integer"
                    # Clothing ID: doit être "integer"
                    # Division Name: doit être "keyword"
                    # Department Name: doit être "keyword"
                    # Class Name: doit être "keyword"
                    # Title: doit être "text" avec analyzer et champ "keyword"
                    # Review Text: doit être "text" avec analyzer et champ "keyword"
                    
                    # VOTRE MAPPING ICI
                    # Exemple:
                    # "Age": {"type": "integer"},
                    # "Department Name": {"type": "keyword"},
                    # "Review Text": {
                    #     "type": "text",
                    #     "analyzer": "review_analyzer",
                    #     "fields": {
                    #         "keyword": {"type": "keyword", "ignore_above": 256}
                    #     }
                    # }
                }
            }
        }
        
    def create_index(self):
        """Create or recreate the Elasticsearch index with proper mappings"""
        logger.info(f"Setting up index: {self.index_name}")
        
        # Delete index if it exists
        if self.es.indices.exists(index=self.index_name):
            logger.info(f"Deleting existing index: {self.index_name}")
            self.es.indices.delete(index=self.index_name)
        
        # Create index with mapping
        logger.info(f"Creating index with mapping: {self.index_name}")
        self.es.indices.create(index=self.index_name, body=self.get_index_mapping())
        
    def load_data(self, df):
        """Load data into Elasticsearch"""
        logger.info("Loading data into Elasticsearch")

        # Convert DataFrame to list of dicts
        records = df.to_dict('records')

        # Use bulk helper to index data
        actions = [
            {
                "_index": self.index_name,
                "_source": record
            }
            for record in records
        ]

        # Process in batches of 1000
        for i in range(0, len(actions), 1000):
            batch = actions[i:i + 1000]
            helpers.bulk(self.es, batch)
            logger.info(f"Indexed {len(batch)} documents")

        # Refresh index to make data available for search
        self.es.indices.refresh(index=self.index_name)
        logger.info("Data loading completed")
        
    def run_etl(self, file_path):
        """Run the complete ETL process"""
        try:
            # Extract
            df = self.read_data(file_path)
            logger.info(f"Read {len(df)} records")
            
            # Transform
            df = self.transform_data(df)
            logger.info(f"Transformed data: {len(df)} records")
            
            # Load
            self.create_index()
            self.load_data(df)
            
            logger.info("ETL process completed successfully")
        except Exception as e:
            logger.error(f"ETL process failed: {str(e)}")
            raise

if __name__ == "__main__":
    # Get the Elasticsearch host from environment variable or use default
    es_host = os.getenv("ELASTICSEARCH_HOST", "elasticsearch")
    
    # Create ETL service and run ETL process
    etl_service = ETLService(es_host=es_host)
    etl_service.run_etl("./data/Womens_Clothing.csv")