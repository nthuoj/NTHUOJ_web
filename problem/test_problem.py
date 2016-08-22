from django.core.urlresolvers import reverse

from problem.problem_info import get_problem_file_extension
from problem.models import Problem, Submission
from utils.nthuoj_testcase import NTHUOJ_TestCase_Basic
from utils.test_helper import *


class Tester_Problem_new(NTHUOJ_TestCase_Basic):
    """ test view 'problem:new' """

    def test_login_redirect(self):
        # user does not login
        # Expectation: redirect to login page
        target_url = reverse('problem:new')
        redirect_url = reverse('users:login')
        response = self.ANONYMOUS_CLIENT.get(target_url)
        self.assertRedirects(response, redirect_url)

    def test_user_no_permission(self):
        # user has no permission
        # Expectation: 302 redirect chain
        target_url = reverse('problem:new')
        redirect_url = reverse('users:login') + '?next=' + target_url
        response = self.NORMAL_CLIENT.post(target_url, follow=True)
        self.assertEqual(response.redirect_chain,
            [('http://testserver/users/login/', 302), ('http://testserver/', 302)])

    def test_has_no_problem_name(self):
        # using POST method but argument 'pname'(problem name) is empty string
        # Expectation: redirect to view 'problem'
        target_url = reverse('problem:new')
        response = self.ADMIN_CLIENT.post(target_url, data={'pname':''})
        redirect_url = reverse('problem:problem')
        self.assertRedirects(response, redirect_url)

    def test_judge_client_create_problem(self):
        # argument 'pname'(problem name) is not empty string
        # Expectation: create a new problem successfully and redirect to view 'edit'
        pname = random_word(20)
        target_url = reverse('problem:new')
        response = self.JUDGE_CLIENT.post(target_url, data={'pname':pname}, follow=True)
        pid = Problem.objects.all().order_by("-pk")[0].pk
        redirect_url = reverse('problem:edit', args=[pid])
        self.assertRedirects(response, redirect_url)
        self.assertEqual(response.context['problem'].pname, pname)


class Tester_Problem_detail(NTHUOJ_TestCase_Basic):
    """ test view 'problem:detail' """

    def test_problem_not_found(self):
        """ test view 'detail' """
        # problem does not exist
        # Expectation: error 404
        pid = 1000000
        target_url = reverse('problem:detail', args=[pid])
        response = self.ADMIN_CLIENT.get(target_url)
        self.assertEqual(response.status_code, 404)
        response = self.JUDGE_CLIENT.get(target_url)
        self.assertEqual(response.status_code, 404)
        response = self.NORMAL_CLIENT.get(target_url)
        self.assertEqual(response.status_code, 404)
        response = self.ANONYMOUS_CLIENT.get(target_url)
        self.assertEqual(response.status_code, 404)
        

    def test_user_permission(self):
        # user has permission or not
        # Expectation: error 403 or 200
        problem = create_problem(self.JUDGE_USER);
        target_url = reverse('problem:detail', args=[problem.pk])
        response = self.ADMIN_CLIENT.get(target_url)
        self.assertEqual(response.status_code, 200)
        response = self.JUDGE_CLIENT.get(target_url)
        self.assertEqual(response.status_code, 200)
        response = self.NORMAL_CLIENT.get(target_url)
        self.assertEqual(response.status_code, 403)
        response = self.ANONYMOUS_CLIENT.get(target_url)
        self.assertEqual(response.status_code, 403)


class Tester_Problem_delete_problem(NTHUOJ_TestCase_Basic):
    """ test view 'problem:delete_problem' """

    def test_problem_not_found(self):
        # problem does not exist
        # Expectation: error 302 or 404
        pid = 0
        target_url = reverse('problem:delete_problem', args=[pid])
        response = self.ADMIN_CLIENT.get(target_url)
        self.assertEqual(response.status_code, 404)
        response = self.JUDGE_CLIENT.get(target_url)
        self.assertEqual(response.status_code, 404)
        response = self.NORMAL_CLIENT.get(target_url)
        self.assertEqual(response.status_code, 404)
        response = self.ANONYMOUS_CLIENT.get(target_url)
        self.assertEqual(response.status_code, 302)

    def test_user_permission(self):
        # user has permission or not
        # Expectation: status 200, 403 or 404
        problem = create_problem(self.JUDGE_USER)
        target_url = reverse('problem:delete_problem', args=[problem.pk])
        redirect_url = reverse('users:login') + '?next=' + target_url
        response = self.ANONYMOUS_CLIENT.get(target_url)
        self.assertRedirects(response, redirect_url)
        response = self.NORMAL_CLIENT.get(target_url)
        self.assertEqual(response.status_code, 403)
        redirect_url = reverse('problem:problem')
        response = self.JUDGE_CLIENT.get(target_url)
        self.assertRedirects(response, redirect_url)
        problem = create_problem(self.JUDGE_USER)
        target_url = reverse('problem:delete_problem', args=[problem.pk])
        response = self.ADMIN_CLIENT.get(target_url)
        self.assertRedirects(response, redirect_url)
        # already deleted, so it shows 404
        response = self.ADMIN_CLIENT.get(target_url)
        self.assertEqual(response.status_code, 404)


class Tester_Problem_edit(NTHUOJ_TestCase_Basic):
    """ test view 'problem:edit' """

    def test_login(self):
        # user does not login
        # Expectation: redirect to login page
        pid = 1
        target_url = reverse('problem:edit', args=[pid])
        redirect_url = reverse('users:login') + '?next=' + target_url
        response = self.ANONYMOUS_CLIENT.get(target_url)
        self.assertRedirects(response, redirect_url)

    def test_problem_not_found(self):
        # problem does not exist
        # Expectation: error 404
        pid = 1000000
        target_url = reverse('problem:edit', args=[pid])
        response = self.ADMIN_CLIENT.get(target_url)
        self.assertEqual(response.status_code, 404)

    def test_permission(self):
        # user has no permission
        # Expectation: error 403
        problem = create_problem(self.JUDGE_USER)
        target_url = reverse('problem:edit', args=[problem.pk])
        response = self.NORMAL_CLIENT.get(target_url)
        self.assertEqual(response.status_code, 403)

    def test_edit_property(self):
        # using POST method with arguments 'description', 'input', 'output',
        #   'sample_in', 'sample_out', 'visible', 'judge_source', 'judge_type',
        #   and 'judge_language'
        # Expectation: edit problem with respect to those arguments, and redirect to view 'detail'
        problem = create_problem(self.JUDGE_USER)
        target_url = reverse('problem:edit', args=[problem.pk])
        data = POST_data_of_editing_Problem(self.JUDGE_USER)
        response = self.JUDGE_CLIENT.post(target_url, data=data, follow=True)
        redirect_url = reverse('problem:detail', args=[problem.pk])
        self.assertRedirects(response, redirect_url)
        edited_problem = response.context['problem']
        self.assertEqual(edited_problem.description, data['description'])
        self.assertEqual(edited_problem.input, data['input'])
        self.assertEqual(edited_problem.output, data['output'])
        self.assertEqual(edited_problem.sample_in, data['sample_in'])
        self.assertEqual(edited_problem.sample_out, data['sample_out'])
        self.assertEqual(edited_problem.visible, data['visible'])
        self.assertEqual(edited_problem.judge_source, data['judge_source'])
        self.assertEqual(edited_problem.judge_type, data['judge_type'])
        self.assertEqual(edited_problem.judge_language, data['judge_language'])

    def test_upload_special_judge_code(self):
        # using POST method with argument 'special_judge_code'
        # Expectation: upload special judge code to server successfully
        problem = create_problem(self.JUDGE_USER)
        target_url = reverse('problem:edit', args=[problem.pk])
        data = POST_data_of_editing_Problem(self.JUDGE_USER, judge_type=Problem.SPECIAL)
        file_ex = get_problem_file_extension(problem)
        special_judge_code = create_judge_code('special', problem.pk, file_ex)
        try:
            with open(special_judge_code, 'r') as fp:
                data['special_judge_code'] = fp
                response = self.JUDGE_CLIENT.post(target_url, data=data, follow=True)
        except (IOError, OSError):
            print "Something went wrong when reading special judge files for testing..."
            raise
        uploaded_special_judge_code = '%s%s%s' % (SPECIAL_PATH, problem.pk, file_ex)
        try:
            compare_result = compare_local_and_uploaded_file(
                special_judge_code, uploaded_special_judge_code)
        except (IOError, OSError):
            raise
        finally:
            remove_file_if_exists(special_judge_code)
            remove_file_if_exists(uploaded_special_judge_code)
        self.assertTrue(compare_result)

    def test_upload_partial_judge_code_and_header(self):
        # using POST method with argument 'partial_judge_code' and 'partial_judge_header'
        # Expectation: upload partial judge code and header to server successfully
        problem = create_problem(self.JUDGE_USER)
        target_url = reverse('problem:edit', args=[problem.pk])
        data = POST_data_of_editing_Problem(self.JUDGE_USER, judge_type=Problem.PARTIAL)
        file_ex = get_problem_file_extension(problem)
        partial_judge_code = create_judge_code('partial', problem.pk, file_ex)
        partial_judge_header = create_judge_code('partial', problem.pk, '.h')
        try:
            with open(partial_judge_code, 'r') as fp, open(partial_judge_header, 'r') as fp2:
                data['partial_judge_code'] = fp
                data['partial_judge_header'] = fp2
                response = self.JUDGE_CLIENT.post(target_url, data=data, follow=True)
        except (IOError, OSError):
            print "Something went wrong when reading partial judge files for testing..."
            raise
        uploaded_partial_judge_code = '%s%s%s' % (PARTIAL_PATH, problem.pk, file_ex)
        uploaded_partial_judge_header = '%s%s.h' % (PARTIAL_PATH, problem.pk)
        try:
            compare_result = compare_local_and_uploaded_file(
                partial_judge_code, uploaded_partial_judge_code)
            compare_result2 = compare_local_and_uploaded_file(
                partial_judge_header, uploaded_partial_judge_header)
        except (IOError, OSError):
            raise
        finally:
            remove_file_if_exists(partial_judge_code)
            remove_file_if_exists(uploaded_partial_judge_code)
            remove_file_if_exists(partial_judge_header)
            remove_file_if_exists(uploaded_partial_judge_header)
        self.assertTrue(compare_result and compare_result2)

    def test_change_judge_type_from_special_to_partial_judge(self):
        # changing judge type from special judge to partial judge
        # Expectation: remove all special judge files with respect to this problem
        problem = create_problem(self.JUDGE_USER)
        target_url = reverse('problem:edit', args=[problem.pk])
        data = POST_data_of_editing_Problem(self.JUDGE_USER, judge_type=Problem.SPECIAL)
        file_ex = get_problem_file_extension(problem)
        special_judge_code = create_judge_code('special', problem.pk, file_ex)
        try:
            with open(special_judge_code, 'r') as fp:
                data['special_judge_code'] = fp
                response = self.JUDGE_CLIENT.post(target_url, data=data, follow=True)
        except (IOError, OSError):
            print "Something went wrong when reading special judge files for testing..."
            raise
        data = POST_data_of_editing_Problem(self.JUDGE_USER, judge_type=Problem.PARTIAL)
        partial_judge_code = create_judge_code('partial', problem.pk, file_ex)
        partial_judge_header = create_judge_code('partial', problem.pk, '.h')
        try:
            with open(partial_judge_code, 'r') as fp, open(partial_judge_header, 'r') as fp2:
                data['partial_judge_code'] = fp
                data['partial_judge_header'] = fp2
                response = self.JUDGE_CLIENT.post(target_url, data=data, follow=True)
        except (IOError, OSError):
            print "Something went wrong when reading partial judge files for testing..."
            raise
        uploaded_special_judge_code = '%s%s%s' % (SPECIAL_PATH, problem.pk, file_ex)
        result = os.path.isfile(uploaded_special_judge_code)
        uploaded_partial_judge_code = '%s%s%s' % (PARTIAL_PATH, problem.pk, file_ex)
        uploaded_partial_judge_header = '%s%s.h' % (PARTIAL_PATH, problem.pk)
        try:
            compare_result = compare_local_and_uploaded_file(
                partial_judge_code, uploaded_partial_judge_code)
            compare_result2 = compare_local_and_uploaded_file(
                partial_judge_header, uploaded_partial_judge_header)
        except (IOError, OSError):
            raise
        finally:
            remove_file_if_exists(special_judge_code)
            remove_file_if_exists(uploaded_special_judge_code)
            remove_file_if_exists(partial_judge_code)
            remove_file_if_exists(uploaded_partial_judge_code)
            remove_file_if_exists(partial_judge_header)
            remove_file_if_exists(uploaded_partial_judge_header)
        self.assertFalse(result)
        self.assertTrue(compare_result)
        self.assertTrue(compare_result2)

    def test_change_judge_type_from_partial_judge_to_special_judge(self):       
        # changing judge type from partial judge to special judge
        # Expectation: remove all partial judge files with respect to this problem
        problem = create_problem(self.JUDGE_USER)
        target_url = reverse('problem:edit', args=[problem.pk])
        data = POST_data_of_editing_Problem(self.JUDGE_USER, judge_type=Problem.PARTIAL)
        file_ex = get_problem_file_extension(problem)
        partial_judge_code = create_judge_code('partial', problem.pk, file_ex)
        partial_judge_header = create_judge_code('partial', problem.pk, '.h')
        try:
            with open(partial_judge_code, 'r') as fp, open(partial_judge_header, 'r') as fp2:
                data['partial_judge_code'] = fp
                data['partial_judge_header'] = fp2
                response = self.JUDGE_CLIENT.post(target_url, data=data, follow=True)
        except (IOError, OSError):
            print "Something went wrong when reading partial judge files for testing..."
            raise
        data = POST_data_of_editing_Problem(self.JUDGE_USER, judge_type=Problem.SPECIAL)
        file_ex = get_problem_file_extension(problem)
        special_judge_code = create_judge_code('special', problem.pk, file_ex)
        try:
            with open(special_judge_code, 'r') as fp:
                data['special_judge_code'] = fp
                response = self.JUDGE_CLIENT.post(target_url, data=data, follow=True)
        except (IOError, OSError):
            print "Something went wrong when reading special judge files for testing..."
            raise
        uploaded_special_judge_code = '%s%s%s' % (SPECIAL_PATH, problem.pk, file_ex)
        uploaded_partial_judge_code = '%s%s%s' % (PARTIAL_PATH, problem.pk, file_ex)
        uploaded_partial_judge_header = '%s%s.h' % (PARTIAL_PATH, problem.pk)
        result = os.path.isfile(uploaded_partial_judge_code)
        result2 = os.path.isfile(uploaded_partial_judge_header)
        try:
            compare_result = compare_local_and_uploaded_file(
                special_judge_code, uploaded_special_judge_code)
        except (IOError, OSError):
            raise
        finally:
            remove_file_if_exists(special_judge_code)
            remove_file_if_exists(uploaded_special_judge_code)
            remove_file_if_exists(partial_judge_code)
            remove_file_if_exists(uploaded_partial_judge_code)
            remove_file_if_exists(partial_judge_header)
            remove_file_if_exists(uploaded_partial_judge_header)
        self.assertFalse(result)
        self.assertFalse(result2)
        self.assertTrue(compare_result)


class Tester_Problem_rejudge(NTHUOJ_TestCase_Basic):
    """ test view 'problem:rejudge' """

    def test_login(self):
        """ test view 'rejudge' """
        # user does not login
        # Expectation: redirect to login page
        target_url = reverse('problem:rejudge')
        redirect_url = reverse('users:login') + '?next=' + target_url
        response = self.ANONYMOUS_CLIENT.get(target_url)
        self.assertRedirects(response, redirect_url)

    def test_problem_not_found(self):
        # problem does not exist
        # Expectation: error 404
        pid = 0
        target_url = reverse('problem:rejudge')
        response = self.NORMAL_CLIENT.get(target_url, data={'pid':pid})
        self.assertEqual(response.status_code, 404)

    def test_permission(self):
        # user has no permission
        # Expectation: error 403
        problem = create_problem(self.JUDGE_USER)
        target_url = reverse('problem:rejudge')
        response = self.NORMAL_CLIENT.get(target_url, data={'pid':problem.pk})
        self.assertEqual(response.status_code, 403)

    def test_rejudge(self):
        # using GET method with argument 'pid', and problem exists, and user has permission
        # Expectation: rejudge all submissions with respect to this problem
        problem = create_problem(self.JUDGE_USER)
        target_url = reverse('problem:rejudge')
        users = [self.ADMIN_USER, self.JUDGE_USER, self.NORMAL_USER]
        submission_statuses = [Submission.ACCEPTED, Submission.NOT_ACCEPTED, Submission.COMPILE_ERROR,
                             Submission.RESTRICTED_FUNCTION, Submission.JUDGE_ERROR, Submission.JUDGING]
        for i in range(3):
            for j in range(2):
                create_submission(problem, users[i], submission_statuses[i*2+j])
        response = self.JUDGE_CLIENT.get(target_url, data={'pid':problem.pk})
        submissions = Submission.objects.filter(problem=problem)
        for submission in submissions:
            self.assertEqual(submission.status, Submission.WAIT)
