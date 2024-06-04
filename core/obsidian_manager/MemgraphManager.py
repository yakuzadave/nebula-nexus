from __future__ import annotations
from typing import Optional, Dict, List, Any, Iterator
import os
import sys
import logging
import pandas as pd
import numpy as np

import requests
import json
import time
from pathlib import Path
from gqlalchemy import Memgraph


import os
import re
from typing import List
from gqlalchemy import Memgraph
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.prompts import MessagesPlaceholder, PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage


# notes_dir = Path("/Users/dcarmocan/Projects/mind-cave")
notes_dir = "/Users/dcarmocan/Projects/mind-cave"


import os
import mgclient
from markdown import Markdown
from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension
import re

# Initialize the MemgraphManager
class MemgraphManager:
    def __init__(self):
        try:
            self.connection = mgclient.connect(host='localhost', port=7687, lazy=False)
            self.connection.autocommit = True
        except Exception as e:
            print(f"Failed to connect to Memgraph: {e}")
            raise

    def execute_query(self, query: str):
        print(f"Executing query: {query}")
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            print("Query executed successfully.")
            return results
        except Exception as e:
            print(f"Failed to execute query: {e}")
            if cursor:
                cursor.close()
            raise

    def find_duplicates(self):
        query = """
        MATCH (n)
        WITH n.name AS name, collect(n) AS nodes
        WHERE size(nodes) > 1
        RETURN name, nodes
        """
        return self.execute_query(query)

    def merge_nodes(self, name):
        sanitized_name = sanitize_text(name)
        merge_query_corrected = f"""
        CALL merge.node(
            ['File'], 
            {{name: '{sanitized_name}'}},
            {{}},
            {{}}
        ) YIELD node
        RETURN node
        """
        self.execute_query(merge_query_corrected)

    def merge_duplicates(self):
        duplicates = self.find_duplicates()
        for name, _ in duplicates:
            try:
                self.merge_nodes(name)
            except Exception as e:
                print(f"Failed to merge nodes with name '{name}': {e}")

    def create_node(self, label: str, properties: dict):
        props = ", ".join([f"{k}: '{sanitize_text(v)}'" for k, v in properties.items()])
        query = f"CREATE (n:{label} {{{props}}})"
        self.execute_query(query)

    def create_edge(self, from_node: str, to_node: str, relationship: str):
        query = f"""
        MATCH (a), (b)
        WHERE a.name = '{sanitize_text(from_node)}' AND b.name = '{sanitize_text(to_node)}'
        CREATE (a)-[r:{relationship}]->(b)
        """
        self.execute_query(query)

    def search_nodes(self, label: str, property_name: str, property_value: str):
        query = f"MATCH (n:{label} {{{property_name}: '{property_value}'}}) RETURN n"
        return self.execute_query(query)

    def search_relationships(self, relationship: str):
        query = f"MATCH ()-[r:{relationship}]->() RETURN r"
        return self.execute_query(query)

# Custom Markdown extension to extract headings
class HeadingExtractor(Treeprocessor):
    def __init__(self, md):
        super().__init__(md)
        self.headings = []

    def run(self, root):
        for element in root:
            if element.tag.startswith('h'):
                self.headings.append((element.tag, element.text))
        return root

class ExtractHeadings(Extension):
    def extendMarkdown(self, md):
        heading_extractor = HeadingExtractor(md)
        md.treeprocessors.register(heading_extractor, 'extract_headings', 10)
        md.heading_extractor = heading_extractor

# Function to parse a markdown file and extract headings and links
def parse_markdown(file_path):
    md = Markdown(extensions=[ExtractHeadings()])
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    md.convert(content)
    links = re.findall(r'\[.*?\]\((.*?)\)', content)
    return md.heading_extractor.headings, links

# Function to sanitize text for Cypher queries
def sanitize_text(text):
    if text is None:
        return "None"
    sanitized = re.sub(r"[^a-zA-Z0-9_\s]", "", text.replace("'", "\\'").replace("#", "").replace("?", ""))
    return sanitized


# export the Class

if "__file__" in globals():
    print("MemgraphManager.py is being run as a script.")
    mg = MemgraphManager()
    mg.merge_duplicates()
else:
    print("MemgraphManager.py is being imported as a module.")
    mg = MemgraphManager()
    mg.merge_duplicates()
    print("MemgraphManager initialized.")
    print("Memgraph duplicates merged.")

