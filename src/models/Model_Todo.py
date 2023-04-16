from src.factory.database import Database

class Todo(object):
    def __init__(self):
        self.db = Database()

        self.collection_name = "todo_data"

        self.fields = {
            "title": "string",
            "description": "string",
            "completed": "boolean",
            "created": "datetime",
            "updated": "datetime"
        }

        # Required Fields for Create
        self.create_required_fields = ["title", "description", "completed"]

        # Optional Fields for Create
        self.create_optional_fields = []

        # Required Fields for Update
        self.update_required_fields = ["title", "description", "completed"]
        
        # Optional Fields for Update
        self.update_optional_fields = []

    def create(self, todo):
        return self.db.insert(todo, self.collection_name)
        
    def find(self, todo):
        return self.db.find(todo, self.collection_name)
        
    def find_by_id(self, id):
        return self.db.find_by_id(id, self.collection_name)
        
    def update(self, id, todo):
        return self.db.update(id, todo, self.collection_name)
        
    def delete(self, id):
        return self.db.delete(id, self.collection_name)