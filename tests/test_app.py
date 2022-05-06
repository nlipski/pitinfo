import unittest
from flask import current_app, url_for
from app import create_app

class TestWebApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.appctx = self.app.app_context()
        self.appctx.push()

    def tearDown(self):
        self.appctx.pop()
        self.app = None
        self.appctx = None

    def test__app(self):
        assert self.app is not None
        assert current_app == self.app

    # def test__home_page_redirect(self):
    #     response = self.client.get('/', follow_redirects=True)
    #     assert response.status_code == 200
    #     assert response.request.path == '/'


    # def test_page_urls(client):
    # # Visit home page
    #     response = client.get(url_for('main.index'), follow_redirects=True)
    #     assert response.status_code==200

    #     # Login as user and visit User page
    #     response = client.post(url_for('auth.login'), follow_redirects=True,
    #                         data=dict(email='user@example.com', password='Password1'))
    #     assert response.status_code==200
        
    #     response = client.get(url_for('main.member_page'), follow_redirects=True)
    #     assert response.status_code==200

    #     # Edit User Profile page
    #     response = client.get(url_for('main.user_profile_page'), follow_redirects=True)
    #     assert response.status_code==200
    #     response = client.post(url_for('main.user_profile_page'), follow_redirects=True,
    #                         data=dict(first_name='User', last_name='User'))
    #     response = client.get(url_for('main.member_page'), follow_redirects=True)
    #     assert response.status_code==200

    #     # Logout
    #     response = client.get(url_for('user.logout'), follow_redirects=True)
    #     assert response.status_code==200

    #     # Login as admin and visit Admin page
    #     response = client.post(url_for('user.login'), follow_redirects=True,
    #                         data=dict(email='admin@example.com', password='Password1'))
    #     assert response.status_code==200
    #     response = client.get(url_for('main.admin_page'), follow_redirects=True)
    #     assert response.status_code==200

    #     # Logout
    #     response = client.get(url_for('user.logout'), follow_redirects=True)
    #     assert response.status_code==200