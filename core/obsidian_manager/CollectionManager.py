import re
import os
from core.obsidian_manager.CypherQueryHandler import CypherQueryHandler




class CollectionManager:
    """Manages a collection of Markdown files in a directory. Extracts information from the Markdown files and stores it in MemGraph.
    

    """
    def __init__(self, directory, memgraph):
        self.directory = directory
        self.memgraph = memgraph
        self.query_handler = CypherQueryHandler()

    def extract_links(self, content):
        """Extracts links from the content of a Markdown file."""
        links = re.findall(r'\[\[([^\]]+)\]\]', content)  # Matches [[Link]]
        return links

    def parse_markdown(self, content):
        """Parses Markdown content to extract headings and their hierarchy."""
        headings = []
        lines = content.split('\n')
        for line in lines:
            match = re.match(r'^(#+)\s+(.*)', line)
            if match:
                level = len(match.group(1))
                text = match.group(2)
                headings.append((level, text))
        return headings

    def create_nodes_and_edges(self, file_name, content):
        """Creates nodes and edges in MemGraph based on the Markdown content."""
        headings = self.parse_markdown(content)
        links = self.extract_links(content)

        # Create a top-level node for the file
        query = """
        MERGE (n:File {name: $name})
        ON CREATE SET n.content = $content
        """
        params = {"name": file_name, "content": content}
        self.memgraph.execute_and_fetch(query, params)

        last_nodes = {0: file_name}  # To keep track of last nodes at each heading level
        for level, text in headings:
            node_name = f"{file_name}::{text}"
            query = """
            MERGE (n:Heading {name: $name, level: $level, text: $text})
            """
            params = {"name": node_name, "level": level, "text": text}
            self.memgraph.execute_and_fetch(query, params)

            # Create an edge from the last node of the previous level to this node
            parent_node = last_nodes[level - 1]
            query = """
            MATCH (p {name: $parent_name}), (c {name: $child_name})
            MERGE (p)-[:CONTAINS]->(c)
            """
            params = {"parent_name": parent_node, "child_name": node_name}
            self.memgraph.execute_and_fetch(query, params)

            last_nodes[level] = node_name

        # Create edges to linked files
        for link in links:
            query = """
            MATCH (a:File {name: $file_name}), (b:File {name: $link_name})
            MERGE (a)-[:LINKS_TO]->(b)
            """
            params = {"file_name": file_name, "link_name": link}
            self.memgraph.execute_and_fetch(query, params)

    def process_file(self, file_path):
        """Process a single Markdown file and store in MemGraph."""
        try:
            with open(file_path, 'r', encoding='utf-8') as md_file:
                content = md_file.read()
                file_name = os.path.basename(file_path).replace('.md', '')
                print(f"Processing file: {file_path}")
                self.create_nodes_and_edges(file_name, content)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    def process_directory(self):
        """Walk through the directory and process each Markdown file."""
        for root, _, files in os.walk(self.directory):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    self.process_file(file_path)
    
    def merge_duplicates(self):
        queries = [
            """
            MATCH (n)
            WITH n.name AS name, collect(n) AS nodes
            WHERE size(nodes) > 1
            CALL apoc.refactor.mergeNodes(nodes) YIELD node
            RETURN node
            """,
            """
            MATCH (n)-[r]->(m)
            WHERE n IS NULL OR m IS NULL
            DELETE r
            """
        ]

        for query in queries:
            self.execute_query(query)
