from database import get_db

class User:
    @staticmethod
    def get_all():
        db = get_db()
        users = db.execute('SELECT * FROM users ORDER BY created DESC').fetchall()
        return users
    
    @staticmethod
    def get_by_id(user_id):
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        return user
    
    @staticmethod
    def create(name, email, phone):
        db = get_db()
        try:
            db.execute(
                'INSERT INTO users (name, email, phone) VALUES (?, ?, ?)',
                (name, email, phone)
            )
            db.commit()
            return True
        except db.IntegrityError:
            return False
    
    @staticmethod
    def update(user_id, name, email, phone):
        db = get_db()
        db.execute(
            'UPDATE users SET name = ?, email = ?, phone = ? WHERE id = ?',
            (name, email, phone, user_id)
        )
        db.commit()
    
    @staticmethod
    def delete(user_id):
        db = get_db()
        db.execute('DELETE FROM users WHERE id = ?', (user_id,))
        db.commit()