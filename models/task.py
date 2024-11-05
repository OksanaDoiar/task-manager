class Task:

    def __init__(self, title: str, description: str, status: str):
        self.id = None
        self.title = title
        self.description = description
        self.status = status

    def to_dict(self):
        return {
            "id": self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status
        }