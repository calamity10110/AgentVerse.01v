from tinydb import TinyDB, Query

class MemoryService:
    def __init__(self, db_path='memory.json'):
        self.db = TinyDB(db_path)

    def save(self, key: str, value):
        """
        Saves a value to the memory with a given key.
        If the key already exists, it will be updated.
        """
        self.db.upsert({'key': key, 'value': value}, Query().key == key)
        print(f"Memory saved with key: {key}")

    def retrieve(self, key: str):
        """
        Retrieves a value from the memory by its key.
        """
        result = self.db.search(Query().key == key)
        if result:
            return result[0]['value']
        else:
            return None

    def search(self, query):
        """
        Searches the memory for entries matching the given query.
        """
        return self.db.search(query)
