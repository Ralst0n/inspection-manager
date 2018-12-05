from django.test import Client, TestCase

from .fakedata import test_project

c = Client()
projects_url = '/api/projects/'

class ProjectViewsTest(TestCase):
    '''verify that all CRUD views for project function as expected'''

    def test_project_index_response(self):
        ''' project list page returns ok status'''
        response = c.get('/projects/')
        self.assertEqual(response.status_code, 200)

    def test_project_post_response(self):
        ''' post request to `/api/projects/` return created status'''
        response = c.post(
            projects_url,
            test_project,
        )
        self.assertEqual(response.status_code, 201)

    def test_project_delete_response(self):
        c.post(projects_url, test_project)
        response = c.delete('/projects/103.411')
        self.assertEqual(response.status_code, 204)
