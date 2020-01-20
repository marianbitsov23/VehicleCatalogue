from database import DB
from comment import Comment

class Sale:
    def __init__(self, id, name, model, horsepower, price, year, condition, mileage, category, file_path, user_id):
        self.id = id
        self.name = name
        self.model = model
        self.horsepower = horsepower
        self.price = price
        self.year = year
        self.condition = condition
        self.mileage = mileage
        self.category = category
        self.file_path = file_path
        self.user_id = user_id

    @staticmethod
    def all():
        with DB() as db:
            rows = db.execute('SELECT * FROM sales').fetchall()
            return [Sale(*row) for row in rows]

    @staticmethod
    def find(id):
        with DB() as db:
            row = db.execute('SELECT * FROM sales WHERE id = ?', (id,)).fetchone()
            return Sale(*row)

    @staticmethod
    def find_by_category(category):
        with DB() as db:
            rows = db.execute(
                'SELECT * FROM sales WHERE category_id = ?',
                (category.id,)
            ).fetchall()
            return [Sale(*row) for row in rows]        

    @staticmethod
    def find_by_user_id(user_id):
        with DB() as db:
            rows = db.execute(
                'SELECT * FROM sales WHERE user_id = ?',
                (user_id,)
            ).fetchall()
            return [Sale(*row) for row in rows]

    def create(self):
        with DB() as db:
            values = (self.name, self.model, self.horsepower,
            self.price, self.year, self.condition, self.mileage, self.category.id, self.file_path, self.user_id)
            db.execute('''INSERT INTO
                sales (name, model, horsepower,
                price, year, condition, mileage, category_id, file_path, user_id)
                VALUES (?, ?, ?, ?, ?, ?, ? ,? ,?, ?)''', values)
            return self

    def save(self):
        with DB() as db:
            values = (
                self.name,
                self.model,
                self.horsepower,
                self.price,
                self.year,
                self.condition,
                self.mileage,
                self.category.id,
                self.file_path,
                self.user_id,
                self.id
            )
            db.execute('''UPDATE sales SET 
            name = ?, model = ?, horsepower = ?, price = ?, year = ?,
            condition = ?, mileage = ?, category_id = ?, file_path = ?, user_id =? WHERE id = ?''', values)
            return self

    def delete(self):
        with DB() as db:
            db.execute('DELETE FROM sales WHERE id = ?', (self.id,))

    def comments(self):
        return Comment.find_by_sale(self)