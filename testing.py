import unittest2 as unittest
import requests
from app import app
class FlaskTestCase(unittest.TestCase):
    # Ensure that Flask was set up correctly
    # def test_addcropspost(self):
    #     tester=app.test_client(self)
    #     print("hello")
    #     resp=tester.post('/AddCrops/Farmer/farmer@gmail.com',data=dict(cropType='cash crops',cropName='cotton',quantity='100',rates='100',imageURL='fertilizer.jpg'),follow_redirects=True)
    #     self.assertEqual(resp.status_code,500)
    #     resp=tester.get('/AddCrops/Farmer/farmer@gmail.com',follow_redirects=True)
    #     self.assertEqual(resp.status_code,200)

    def test_loginget(self):
        tester=app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        tester=app.test_client(self)
        resp=tester.post('/login',data=dict(email='farmer@gmail.com',pas='abcd'),follow_redirects=True)
        self.assertTrue(b'You were successfully logged in' in resp.data)
        resp=tester.get('/login',follow_redirects=True)
        self.assertEqual(resp.status_code,200)


    def test_loginload(self):
        tester=app.test_client(self)
        response=tester.get('/login', content_type='html/text')
        self.assertTrue(b'Sign In' in response.data )

    def test_registerload(self):
        tester=app.test_client(self)
        response = tester.get('/Register', content_type='html/text')
        self.assertTrue(b'Register' in response.data )
        
    def test_index(self):
        tester=app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_loginpost(self):
        tester=app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)
    
    def test_addcropget(self):
        tester=app.test_client(self)
        resp=tester.get('/AddCrops/farmer/farmer@gmail.com',follow_redirects=True)
        self.assertEqual(resp.status_code, 200)

    # def test_addfertpost(self):
    #     tester=app.test_client(self)
    #     resp=tester.post('/AddFertilizers/company/company@gmail.com',data=dict(fertname='nitrogen fertilizer',quantity='100',rates='100',imageURL='fertilizer.jpg'),follow_redirects=True)
    #     self.assertEqual(resp.status_code, 500)

    def test_addfertget(self):
        tester=app.test_client(self)
        resp=tester.get('/AddFertilizers/farmer/farmer@gmail.com',follow_redirects=True)
        self.assertEqual(resp.status_code, 200)

    def test_displayFert(self):
        tester=app.test_client(self)
        resp=tester.get('/displayFert/farmer/farmer@gmail.com',follow_redirects=True)
        self.assertEqual(resp.status_code, 200)

    # def test_requestsfeedback(self):
    #     tester=app.test_client(self)
    #     resp=tester.get('/requestsfeedback/farmer/farmer@gmail.com',follow_redirects=True)
    #     self.assertEqual(resp.status_code, 500)

    def test_requestsDisplay(self):
        tester=app.test_client(self)
        resp=tester.get('/requestsDisplay/farmer/farmer@gmail.com',follow_redirects=True)
        self.assertEqual(resp.status_code, 200)

    def test_myproduct(self):
        tester=app.test_client(self)
        resp=tester.get('/myproduct/farmer/farmer@gmail.com',follow_redirects=True)
        self.assertEqual(resp.status_code, 200)



if __name__ == '__main__':
    unittest.main()