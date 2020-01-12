from database import DB

class Comment:
    def __init__(self, id, sale, message):
        self.id = id
        self.sale = sale
        self.message = message

    def create(self):
        with DB() as db:
            values = (self.sale.id, self.message)
            db.execute('INSERT INTO comments (sale_id, message) VALUES (?, ?)', values)
            
            return self

    @staticmethod
    def find_by_sale(sale):
        with DB() as db:
            rows = db.execute('SELECT * FROM comments WHERE sale_id = ?',
            (sale.id,)
            ).fetchall()
            return [Comment(*row) for row in rows]
