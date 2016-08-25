from django.core.urlresolvers import reverse

from problem.models import Problem
from utils.nthuoj_testcase import NTHUOJ_TestCase_Basic
from utils.test_helper import *


class Tester_Problem_testcase(NTHUOJ_TestCase_Basic):
    """ test view 'problem:testcase' """

    def test_login(self):
        # user does not login
        # Expectation: redirect to login page
        pid = 1
        target_url = reverse('problem:testcase', args=[pid])
        redirect_url = reverse('users:login') + '?next=' + target_url
        response = self.ANONYMOUS_CLIENT.get(target_url)
        self.assertRedirects(response, redirect_url)

    def test_problem_not_found(self):
        # problem does not exist
        # Expectation: error 404
        pid = 0
        target_url = reverse('problem:testcase', args=[pid])
        response = self.ADMIN_CLIENT.post(target_url)
        self.assertEqual(response.status_code, 404)
        response = self.JUDGE_CLIENT.post(target_url)
        self.assertEqual(response.status_code, 404)
        response = self.NORMAL_CLIENT.post(target_url)
        self.assertEqual(response.status_code, 404)

    def test_testcase_not_found(self):
        # testcase does not exist
        # Expectation: error 404
        tid = 0
        problem = create_problem(self.JUDGE_USER)
        target_url = reverse('problem:testcase', args=[problem.pk, tid])
        response = self.ADMIN_CLIENT.post(target_url)
        self.assertEqual(response.status_code, 404)
        response = self.JUDGE_CLIENT.post(target_url)
        self.assertEqual(response.status_code, 404)
        response = self.NORMAL_CLIENT.post(target_url)
        self.assertEqual(response.status_code, 403)

    def test_testcase_misaligned(self):
        # testcase does not belong to the problem
        # Expectation: error 404
        problem = create_problem(self.JUDGE_USER)
        fake_problem = create_problem(self.JUDGE_USER)
        testcase = create_testcase(fake_problem, local_files=False)
        target_url = reverse('problem:testcase', args=[problem.pk, testcase.pk])
        response = self.ADMIN_CLIENT.post(target_url)
        self.assertEqual(response.status_code, 404)

    def test_permission(self):
        # user has no permission
        # Expectation: error 403
        problem = create_problem(self.JUDGE_USER)
        testcase = create_testcase(problem)
        target_url = reverse('problem:testcase', args=[problem.pk, testcase.pk])
        response = self.JUDGE_CLIENT.post(target_url)
        self.assertEqual(response.status_code, 200)
        response = self.NORMAL_CLIENT.post(target_url)
        self.assertEqual(response.status_code, 403)
        response = self.ANONYMOUS_CLIENT.post(target_url)
        redirect_url = reverse('users:login') + '?next=' + target_url
        self.assertRedirects(response, redirect_url)

    def test_create_testcase(self):
        # using POST method without argument 'tid', only 'time_limit' and 'memory_limit' are given
        # Expectation: create new testcase for this problem with given 'time_limit' and 'memory_limit'
        problem = create_problem(self.JUDGE_USER)
        target_url = reverse('problem:testcase', args=[problem.pk])
        data1 = {
            'time_limit': 3,
            'memory_limit': 12,
        }
        response1 = self.JUDGE_CLIENT.post(target_url, data=data1)
        self.assertEqual(response1.status_code, 200)
        testcases = Testcase.objects.filter(problem=problem).order_by('id')
        self.assertEqual(testcases[0].problem, problem)
        self.assertEqual(testcases[0].time_limit, data1['time_limit'])
        self.assertEqual(testcases[0].memory_limit, data1['memory_limit'])

    def test_testcase_file_upload(self):
        # using POST method, with arguments 'tid', 't_in' and 't_out'
        # Expectation: upload input and output files of the testcase to server
        problem = create_problem(self.JUDGE_USER)
        testcase = create_testcase(problem)
        target_url = reverse('problem:testcase', args=[problem.pk, testcase.pk])
        try:
            with open("%s%s.in" % (TEST_PATH, testcase.pk), 'r') as file_in,\
                 open("%s%s.out" % (TEST_PATH, testcase.pk), 'r') as file_out:
                    data = {
                        't_in': file_in,
                        't_out': file_out,
                    }
                    response = self.JUDGE_CLIENT.post(target_url, data=data)
        except IOError:
            print "Something went wrong when reading testcase files for testing..."
        compare_result = compare_local_and_uploaded_testcase_files(testcase.pk, testcase.pk)
        remove_testcase_file(testcase.pk, testcase.pk)
        self.assertTrue(compare_result)


class Tester_Problem_delete_testcase(NTHUOJ_TestCase_Basic):
    """ test view 'problem:delete_testcase' """

    def test_login(self):
        # user does not login
        # Expectation: redirect to login page
        pid = 1
        tid = 1
        target_url = reverse('problem:delete_testcase', args=[pid, tid])
        redirect_url = reverse('users:login') + '?next=' + target_url
        response = self.ANONYMOUS_CLIENT.delete(target_url)
        self.assertRedirects(response, redirect_url)

    def test_problem_not_found(self):
        # problem does not exist
        # Expectation: error 404
        pid = 0
        tid = 0
        target_url = reverse('problem:delete_testcase', args=[pid, tid])
        response = self.ADMIN_CLIENT.delete(target_url)
        self.assertEqual(response.status_code, 404)
        response = self.JUDGE_CLIENT.delete(target_url)
        self.assertEqual(response.status_code, 404)
        response = self.NORMAL_CLIENT.delete(target_url)
        self.assertEqual(response.status_code, 404)

    def test_testcase_not_found(self):
        # testcase does not exist
        # Expectation: error 404
        problem = create_problem(self.JUDGE_USER)
        tid = 0
        target_url = reverse('problem:delete_testcase', args=[problem.pk, tid])
        response = self.ADMIN_CLIENT.delete(target_url)
        self.assertEqual(response.status_code, 404)
        response = self.JUDGE_CLIENT.delete(target_url)
        self.assertEqual(response.status_code, 404)
        response = self.NORMAL_CLIENT.delete(target_url)
        self.assertEqual(response.status_code, 404)

    def test_testcase_misaligned(self):
        # testcase does not belong to the problem
        # Expectation: error 404
        problem = create_problem(self.JUDGE_USER)
        fake_problem = create_problem(self.JUDGE_USER_2)
        testcase = create_testcase(fake_problem, local_files=False, uploaded_files=True)
        target_url = reverse('problem:delete_testcase', args=[problem.pk, testcase.pk])
        response = self.JUDGE_CLIENT.delete(target_url)
        self.assertEqual(response.status_code, 403)

    def test_permission(self):
        # user has no permission
        # Expectation: error 403
        problem = create_problem(self.JUDGE_USER)
        testcase = create_testcase(problem, local_files=False)
        target_url = reverse('problem:delete_testcase', args=[problem.pk, testcase.pk])
        response = self.NORMAL_CLIENT.delete(target_url)
        self.assertEqual(response.status_code, 403)

    def test_delete_testcase(self):
        # both problem and testcase exist and user has permission
        # Expectation: remove input and output files of testcase from server
        problem = create_problem(self.JUDGE_USER)
        testcase = create_testcase(problem, uploaded_files=True)
        target_url = reverse('problem:delete_testcase', args=[problem.pk, testcase.pk])
        response = self.JUDGE_CLIENT.delete(target_url)
        removing_result = not os.path.isfile('%s%d.in' % (TESTCASE_PATH, testcase.pk))\
            and not os.path.isfile('%s%d.out' % (TESTCASE_PATH, testcase.pk))
        remove_testcase_file(testcase.pk, testcase.pk)
        self.assertTrue(removing_result)
        testcases = Testcase.objects.filter(problem=problem).order_by('id')
        self.assertEqual(len(testcases), 0)
