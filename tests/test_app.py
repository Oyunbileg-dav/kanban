import unittest
from app import app, db, User, Todo

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config.TestConfig')
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        user = User(username='abc', email='cdf', password='ghjklzxc')
        self.assertEqual(user.username, 'abc')
        self.assertEqual(user.email, 'cdf')
        self.assertEqual(user.password, 'ghjklzxc')

    def test_create_task(self):
        todo = Todo(id='123456', title='run test', status='doing')
        self.assertEqual(todo.id, '123456')
        self.assertEqual(todo.title, 'run test')
        self.assertEqual(todo.status, 'doing')

    def test_db_user(self):
        user = User(username='abc', email='cdf', password='ghjklzxc')
        db.session.add(user)
        db.session.commit()
        assert user in db.session

    def test_db_todo(self):
        todo = Todo(id='123456', title='run test', status='doing')
        db.session.add(todo)
        db.session.commit()
        assert todo in db.session
        
