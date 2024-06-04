from core.obsidian_manager.CollectionManager import CollectionManager
from core.obsidian_manager.CypherQueryHandler import CypherQueryHandler
from core.obsidian_manager.MemgraphManager import MemgraphManager
from core.obsidian_manager.GeneralQueryAgent import GeneralQueryAgent



class VaultManager:
    def __init__(self, directory: str, memgraph):
        self.collection_manager = CollectionManager(directory, memgraph)
        self.memgraph = memgraph
        self.query_handler = CypherQueryHandler()

    def update_vault(self):
        """Updates the entire vault by processing all Markdown files."""
        print("Updating vault...")
        self.collection_manager.process_directory()
        print("Vault update complete.")

    def clear_repo(self, repo_path: str):
        """Clears all data related to a specific repository."""
        print(f"Clearing repository: {repo_path}...")
        query = self.query_handler.get_delete_all_for_repo_query(repo_path)
        self.memgraph.execute(query)
        print(f"Repository {repo_path} cleared.")

    def clear_file(self, file_path: str):
        """Clears all data related to a specific file."""
        print(f"Clearing file: {file_path}...")
        query = self.query_handler.get_delete_graph_for_file_query(file_path)
        self.memgraph.execute(query)
        print(f"File {file_path} cleared.")

    def rename_file(self, old_file_path: str, new_file_path: str):
        """Renames a file in the vault."""
        print(f"Renaming file from {old_file_path} to {new_file_path}...")
        query = self.query_handler.get_rename_file_query(old_file_path, new_file_path)
        self.memgraph.execute(query)
        print(f"File renamed from {old_file_path} to {new_file_path}.")

    def export_repo(self, repo_path: str):
        """Exports the data for a specific repository."""
        print(f"Exporting repository: {repo_path}...")
        query = self.query_handler.get_export_for_repo_path_query(repo_path)
        result = self.memgraph.execute(query)
        print(f"Repository {repo_path} exported.")
        return result

    def export_file(self, file_path: str):
        """Exports the data for a specific file."""
        print(f"Exporting file: {file_path}...")
        query = self.query_handler.get_export_for_file_path_query(file_path)
        result = self.memgraph.execute(query)
        print(f"File {file_path} exported.")
        return result

    def get_schema_for_repo(self, repo_path: str):
        """Gets the schema for a specific repository."""
        print(f"Getting schema for repository: {repo_path}...")
        query = self.query_handler.get_schema_for_repo_query(repo_path)
        result = self.memgraph.execute(query)
        print(f"Schema for repository {repo_path} obtained.")
        return result
