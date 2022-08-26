import uuid

import arrow
from mongoengine import Document, StringField, IntField, DateTimeField, URLField


class Glove(Document):
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    full_name = StringField(required=True, max_length=200)
    brand = StringField(max_length=50)
    size = IntField(required=True)  # OZ
    material = StringField(max_length=100)
    color = StringField()
    description = StringField()
    url = URLField()
    olx_url = URLField(unique=True)
    updated_at = DateTimeField(default=arrow.utcnow().isoformat)
    price = IntField(required=True)

    meta = {
        'indexes': ['olx_url'],
        'ordering': ['-updated_at']
    }

    @classmethod
    def bulk_insert_gloves(cls, data):
        for glove_data in data:
            print(f"olx url: {glove_data['olx_url']}\n\n\n\n\n\n")
            exists = cls.objects(olx_url=glove_data["olx_url"])
            if not exists:
                cls.objects.insert(Glove(**glove_data))
            else:
                print("item already exists")
