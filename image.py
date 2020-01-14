from sale import Sale
from database import DB

class Image:
    def __init__(self, id, name, file, sale):
        self.id = id
        self.name = name
        self.file = file
        self.sale = sale

    def upload_image(self):
        with DB() as db:
            values = (self.name, self.file, self.sale.id)
            db.execute('INSERT INTO images (name, file, sale_id) VALUES (?, ? ,?)', values)

            return self
