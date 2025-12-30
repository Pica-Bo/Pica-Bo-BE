from beanie import Document

class BaseDocument(Document):
    class Settings:
        name = 'base'
