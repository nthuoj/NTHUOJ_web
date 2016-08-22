from django.core.urlresolvers import reverse

from problem.models import Problem
from utils.nthuoj_testcase import NTHUOJ_TestCase_Basic
from utils.test_helper import *


class Tester_Problem_tag(NTHUOJ_TestCase_Basic):
    """ test view 'problem:tag' """

    def test_login(self):
        # user does not login
        # Expectation: redirect to login page
        pid = 1
        target_url = reverse('problem:tag', args=[pid])
        redirect_url = reverse('users:login') + '?next=' + target_url
        response = self.ANONYMOUS_CLIENT.get(target_url)
        self.assertRedirects(response, redirect_url)

    def test_problem_not_found(self):
        # problem does not exist
        # Expectation: error 404
        pid = 0
        target_url = reverse('problem:tag', args=[pid])
        data = {
            'tag_name': random_word(10),
        }
        response = self.ADMIN_CLIENT.post(target_url, data=data)
        self.assertEqual(response.status_code, 404)
        response = self.JUDGE_CLIENT.post(target_url, data=data)
        self.assertEqual(response.status_code, 404)
        response = self.NORMAL_CLIENT.post(target_url, data=data)
        self.assertEqual(response.status_code, 404)

    def test_create_tag(self):
        # problem exists
        # Expectation: create a new tag for this problem with the following constraint
        #              a) duplicate or empty string is not allowed to be added
        #              b) the string whose length is over 20 will be truncated
        problem = create_problem(self.JUDGE_USER)
        target_url = reverse('problem:tag', args=[problem.pk])
        tag_names = ['nthuoj', 'ggqaq', 'ggqaqXDD', 'nthuoj', '01234567899876543210END']
        for i in range(2):
            self.ADMIN_CLIENT.post(target_url, data={'tag_name':tag_names[i]})
        for i in range(2,4):
            self.JUDGE_CLIENT.post(target_url, data={'tag_name':tag_names[i]})
        for i in range(4,5):
            self.NORMAL_CLIENT.post(target_url, data={'tag_name':tag_names[i]})
        results = [tag.tag_name for tag in problem.tags.all()]
        expectations = ['nthuoj', 'ggqaq', 'ggqaqXDD', '01234567899876543210']
        self.assertEqual(problem.tags.count(), 4)
        self.assertTrue(set(results)==set(expectations))


class Tester_Problem_delete_tag(NTHUOJ_TestCase_Basic):
    """ test view 'problem:delete_tag' """

    def test_login(self):
        # user does not login
        # Expectation: redirect to login page
        pid = 1
        tag_id = 1
        target_url = reverse('problem:delete_tag', args=[pid, tag_id])
        redirect_url = reverse('users:login') + '?next=' + target_url
        response = self.ANONYMOUS_CLIENT.get(target_url)
        self.assertRedirects(response, redirect_url)

    def test_problem_not_found(self):
        # problem does not exist
        # Expectation: error 404
        pid = 0
        tag_id = 1
        target_url = reverse('problem:delete_tag', args=[pid, tag_id])
        response = self.ADMIN_CLIENT.get(target_url)
        self.assertEqual(response.status_code, 404)
        response = self.JUDGE_CLIENT.get(target_url)
        self.assertEqual(response.status_code, 404)
        response = self.NORMAL_CLIENT.get(target_url)
        self.assertEqual(response.status_code, 404)

    def test_tag_not_found(self):
        # tag does not exist
        # Expectation: error 404
        problem = create_problem(self.JUDGE_USER)
        tag_id = 0
        target_url = reverse('problem:delete_tag', args=[problem.pk, tag_id])
        response = self.JUDGE_CLIENT.get(target_url)
        self.assertEqual(response.status_code, 404)
        response = self.JUDGE_CLIENT.get(target_url)
        self.assertEqual(response.status_code, 404)
        response = self.NORMAL_CLIENT.get(target_url)
        self.assertEqual(response.status_code, 404)

    def test_permission(self):
        # user has no permission
        # Expectation: error 403
        problem = create_problem(self.JUDGE_USER)
        tag = create_tag('testTag', problem)
        target_url = reverse('problem:delete_tag', args=[problem.pk, tag.pk])
        response = self.NORMAL_CLIENT.get(target_url)
        self.assertEqual(response.status_code, 403)

    def test_delete_tag(self):
        # tag belongs to the problem
        # Expectation: remove the tag from the problem
        problem = create_problem(self.JUDGE_USER)
        tag_names = ['nthuoj', 'ggqaq', 'ggqaqXDD', '01234567899876543210']
        tags = []
        for i in range(4):
            new_tag = create_tag(tag_names[i], problem)
            tags.append(new_tag)
        for i in [1, 2]:
            target_url = reverse('problem:delete_tag', args=[problem.pk, tags[i].pk])
            response = self.ADMIN_CLIENT.get(target_url)
        results = [tag.tag_name for tag in problem.tags.all()]
        expectations = ['nthuoj', '01234567899876543210']
        self.assertEquals(problem.tags.count(), 2)
        self.assertTrue(set(results)==set(expectations))
