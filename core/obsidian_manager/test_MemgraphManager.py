import pytest
import os
from core.obsidian_manager.MemgraphManager import MemgraphManager
from core.obsidian_manager.MemgraphManager import parse_markdown, sanitize_text


# Import the necessary modules for testing

# Path to the directory containing markdown files (Obsidian vault)
notes_dir = '/Users/dcarmocan/Projects/mind-cave'

# Initialize the MemgraphManager
mg_manager = MemgraphManager()

# Process each markdown file in the directory
for root, dirs, files in os.walk(notes_dir):
  for file in files:
    if file.endswith('.md'):
      file_path = os.path.join(root, file)
      print(f"Processing file: {file_path}")
      
      # Extract headings and links
      headings, links = parse_markdown(file_path)
      file_name = os.path.basename(file_path)
      
      # Create a node for the file
      mg_manager.create_node('File', {'name': file_name})
      
      # Create nodes and edges for each heading
      previous_heading = file_name
      for tag, heading in headings:
        sanitized_heading = sanitize_text(heading)
        heading_node = f"{file_name}_{sanitized_heading}"
        mg_manager.create_node(tag, {'name': heading_node})
        mg_manager.create_edge(previous_heading, heading_node, 'CONTAINS')
        previous_heading = heading_node

      # Create edges for links to other files
      for link in links:
        link_file_name = os.path.basename(link)
        mg_manager.create_edge(file_name, link_file_name, 'LINKS_TO')

# Merge duplicate nodes
mg_manager.merge_duplicates()


# Expected output

# Query executed successfully.
# Executing query: 
#         MATCH (n:File {name: '.md'})
#         WITH COLLECT(n) AS nodes
#         CALL {
#             WITH nodes
#             UNWIND nodes AS n
#             WITH n LIMIT 1
#             RETURN n
#         }
#         WITH nodes, n AS to_keep
#         UNWIND nodes AS n
#         WITH n, to_keep WHERE n <> to_keep
#         OPTIONAL MATCH (n)-[r]-()
#         DELETE r
#         DETACH DELETE n
#         RETURN to_keep
    
# Query executed successfully.
# Executing query: 
#         MATCH (n:File {name: 'Daily Notes.md'})
#         WITH COLLECT(n) AS nodes
#         CALL {
#             WITH nodes
#             UNWIND nodes AS n
#             WITH n LIMIT 1
#             RETURN n
#         }
#         WITH nodes, n AS to_keep
#         UNWIND nodes AS n
#         WITH n, to_keep WHERE n <> to_keep
#         OPTIONAL MATCH (n)-[r]-()
#         DELETE r
#         DETACH DELETE n
#         RETURN to_keep
    
# Query executed successfully.
