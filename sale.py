from database import DB
from comment import Comment

class Sale:
    def __init__(self, id, category, name, model, horsepower, price, year, condition, mileage):
        self.id = id
        self.category = category
        self.name = name
        self.model = model
        self.horsepower = horsepower
        self.price = price
        self.year = year
        self.condition = condition
        self.mileage = mileage

    @staticmethod
    def all():
        with DB() as db:
            rows = db.execute('SELECT * FROM sales').fetchall()
            return [Sale(*row) for row in rows]

    @staticmethod
    def find():
        with DB() as db:
            row = db.execute('SELECT * FROM sales WHERE id = ?', (id,)).fetchone()
            return Sale(*row)

    @staticmethod
    def find_by_category(category):
        with DB() as db:
            rows = db.execute('SELECT * FROM sales WHERE category = ?'
            (category.id,)).fetchall()
            return [Sale(*row) for row in rows]

    def create(self):
        with DB() as db:
            values = (self.category, self.name, self.model, self.horsepower,
            self.price, self.year, self.condition, self.mileage)
            db.execute('''INSERT INTO
                sales(category, name, model, horsepower)
                VALUES (?, ?, ?, ?, ?, ?, ? ,?)''', values)
            return self

    def save(self):
        with DB() as db:
            values = (
                self.category.id
                self.name,
                self.model,
                self.horsepower,
                self.price,
                self.year,
                self.condition,
                self.mileage
                self.id
            )
            db.execute('''UPDATE sales SET category_id = ?,
            name = ?, model = ?, horsepower = ?, price = ?, year = ?,
            condition = ?, mileage = ? WHERE id = ?''', values)
            return self

    def delete(self):
        with DB as db:
            db.execute('DELETE FROM sales WHERE id = ?', (self.id,))

    def comments(self):
        return Comment.find_by_post(self)