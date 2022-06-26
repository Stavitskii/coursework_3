from run import app

class TestApi:

    def test_app_all_posts_ststus_code(self):
        """Test, if a valid list comes"""
        response = app.test_client().get('/api/posts', follow_redirects=True)
        assert response.status_code == 200, "The status code of all posts is wrong"
        assert response.mimetype == "application/json", "Not a JSON appeared"
