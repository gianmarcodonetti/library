import numpy as np
from scipy.cluster import hierarchy
from random import randint
import operator


def user_random_answer(min_value=-2, max_value=2):
    return randint(min_value, max_value)


def list_variance(lis):
    var = 0
    for i in range(len(lis) - 1):
        var += np.abs(lis[i] - lis[i + 1])
    return var


class SurveyMatrix(object):
    """
    Class representing a survey matrix.
    """

    def __init__(self, min_value=1, max_value=5, matrix=None, n_questions=10, n_users=30, survey_title=None):
        self.min_value = min_value
        self.max_value = max_value
        if survey_title is None:
            survey_title = "No title"
        self.survey_title = survey_title
        if matrix is None:
            matrix = []
            for i in range(n_users):
                matrix.append([])
                for j in range(n_questions):
                    matrix[i].append(user_random_answer(min_value, max_value))
            self.matrix = np.array(matrix)
            self.n_questions = n_questions
            self.n_users = n_users
        else:
            self.matrix = matrix
            self.n_questions = len(matrix[0])
            self.n_users = len(matrix)

    def __str__(self):
        result = self.survey_title + "\n" + str(self.matrix)
        return result

    def sort_by_row_goodness(self):
        row_goodness = {}
        for r in range(len(self.matrix)):
            good_el = sum([x ** 2 for x in self.matrix[r] if x > 0])
            bad_el = sum([x ** 2 for x in self.matrix[r] if x < 0])
            row_goodness[r] = bad_el + good_el
        sorted_row_good = sorted(row_goodness.items(), key=operator.itemgetter(1))

        matrix_row_sorted = []
        for i in range(len(sorted_row_good)):
            row = sorted_row_good[i][0]
            matrix_row_sorted.append(self.matrix[row])
        return SurveyMatrix(min_value=self.min_value, max_value=self.max_value, matrix=np.array(matrix_row_sorted),
                            survey_title=self.survey_title)

    def sort_by_col_variance(self):
        matrix_t = np.array(self.matrix).transpose()
        columns_variance = {}
        for c in range(len(matrix_t)):
            columns_variance[c] = list_variance(matrix_t[c])
        sorted_col_var = sorted(columns_variance.items(), key=operator.itemgetter(1))

        matrix_t_sorted = []
        for i in range(len(sorted_col_var)):
            col = sorted_col_var[i][0]
            matrix_t_sorted.append(matrix_t[col])
        return SurveyMatrix(min_value=self.min_value, max_value=self.max_value,
                            matrix=np.array(matrix_t_sorted).transpose(), survey_title=self.survey_title)

    def sort_by_col_goodness(self):
        col_goodness = {}
        matrix_t = np.array(self.matrix).transpose()
        for c in range(len(matrix_t)):
            good_el = sum([x ** 2 for x in matrix_t[c] if x > 0])
            bad_el = sum([x ** 5 for x in matrix_t[c] if x < 0])
            col_goodness[c] = sum(matrix_t[c]) + bad_el + good_el
        sorted_col_good = sorted(col_goodness.items(), key=operator.itemgetter(1))

        matrix_col_sorted = []
        for i in range(len(sorted_col_good)):
            col = sorted_col_good[i][0]
            matrix_col_sorted.append(matrix_t[col])
        return SurveyMatrix(min_value=self.min_value, max_value=self.max_value,
                            matrix=np.array(matrix_col_sorted).transpose(), survey_title=self.survey_title)

    def sort_by_dendogram(self):
        Z = hierarchy.linkage(self.matrix)
        dn = hierarchy.dendrogram(Z)
        sorted_by_dn = dn['leaves']

        matrix_dn_sorted = []
        for i in range(len(sorted_by_dn)):
            row = sorted_by_dn[i]
            matrix_dn_sorted.append(matrix[row])
        return SurveyMatrix(min_value=self.min_value, max_value=self.max_value,
                            matrix=np.array(matrix_dn_sorted), survey_title=self.survey_title)

    def obj_function(self):
        total = 0
        for i in range(len(self.matrix) - 1):
            for j in range(len(self.matrix[i]) - 1):
                total += abs(self.matrix[i][j] - self.matrix[i][j + 1]) + abs(
                    self.matrix[i][j] - self.matrix[i + 1][j]) + abs(self.matrix[i][j] - self.matrix[i + 1][j + 1])
        return total
