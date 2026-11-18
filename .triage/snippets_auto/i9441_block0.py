    @abstractmethod
    def db_check_table_exist(self, table: str, dataset: str = "", project_id: str = "") -> bool:
        """Check if table exists in database."""
....
