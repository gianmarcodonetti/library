import numpy as np
from scipy.cluster import hierarchy
from random import randint
import operator
import matplotlib.pyplot as plt
from matplotlib import colors
from plotly import offline
import plotly.graph_objs as go
import itertools


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

    def __init__(self, min_value, max_value, matrix=None, questions=None, users=None, n_questions=10, n_users=30,
                 survey_title=None):
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
        if questions:
            self.questions = questions
        else:
            self.questions = ['Question ' + str(i) for i in range(self.n_questions)]
        if users:
            self.users = users
        else:
            self.users = ['User ' + str(i) for i in range(self.n_users)]
        assert len(self.users) == self.n_users, "Number of users mismatch"
        assert len(self.questions) == self.n_questions, "Number of questions mismatch"

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

    def plot_matrix(self):
        title = self.survey_title

        # colors = ['#0000ff', '#0080ff', '#00ffff', '#00ff80', '#00ff00']
        my_cmap = colors.ListedColormap(['red', 'yellow', 'green'])

        bounds = [0, 3, 6, 10]
        norm = colors.BoundaryNorm(bounds, my_cmap.N)

        fig = plt.Figure(figsize=(self.n_questions * 3, self.n_users), dpi=80, facecolor='w', edgecolor='k')
        plt.imshow(self.matrix, interpolation='nearest', cmap=my_cmap, norm=norm)
        plt.title(title, size=10)
        plt.colorbar()

        # for i, j in itertools.product(range(len(self.matrix)), range(len(self.matrix[0]))):
        #     plt.text(j, i, self.matrix[i][j],
        #              horizontalalignment="center",
        #              color="black")

        plt.grid(False)
        plt.tight_layout()
        plt.xlabel('Questions')
        plt.ylabel('Users')
        plt.show()

    def plot_heatmap(self):
        title = self.survey_title
        z = self.matrix
        y = self.users
        x = self.questions

        my_cmap = colors.ListedColormap(['red', 'yellow', 'green'])
        bounds = [0, 3, 6, 10]
        norm = colors.BoundaryNorm(bounds, my_cmap.N)

        # Plot it out
        fig, ax = plt.subplots()
        heatmap = ax.pcolor(z, cmap=my_cmap, norm=norm, alpha=0.8)
        plt.colorbar(heatmap)

        # Format
        fig = plt.gcf()
        fig.set_size_inches(8, 11)
        # Turn off the frame
        ax.set_frame_on(False)
        # Put the major ticks at the middle of each cell
        ax.set_yticks(np.arange(len(y)) + 0.5, minor=False)
        ax.set_xticks(np.arange(len(x)) + 0.5, minor=False)

        # More natural, table-like display
        ax.invert_yaxis()
        ax.xaxis.tick_top()
        ax.set_xticklabels(x, minor=False)
        ax.set_yticklabels(y, minor=False)

        # Rotate the x axis ticks
        plt.xticks(rotation=45)

        # Turn off all the ticks
        ax = plt.gca()
        for t in ax.xaxis.get_major_ticks():
            t.tick1On = False
            t.tick2On = False
        for t in ax.yaxis.get_major_ticks():
            t.tick1On = False
            t.tick2On = False

    def plotly_heatmap(self):
        title = self.survey_title
        z = self.matrix
        y = [i for i in range(self.n_users)]
        x = [i for i in range(self.n_questions)]
        # colors = ['#0000ff', '#0080ff', '#00ffff', '#00ff80', '#00ff00']
        my_cmap = colors.ListedColormap(['red', 'yellow', 'green'])

        bounds = [0, 3, 6, 10]
        norm = colors.BoundaryNorm(bounds, my_cmap.N)

        colorscale = [[0, '#3D9970'], [1, '#001f3f']]  # custom colorscale
        trace = go.Heatmap(x=x, y=y, z=z, colorscale=colorscale, showscale=False)
        annotations = []
        for n, row in enumerate(z):
            for m, val in enumerate(row):
                var = z[n][m]
                annotations.append(
                    dict(
                        text=str(val),
                        x=x[m], y=y[n],
                        xref='x1', yref='y1',
                        font=dict(color='black'),
                        showarrow=False)
                )

        fig = go.Figure(data=[trace])
        fig['layout'].update(
            title="Annotated Heatmap",
            annotations=annotations,
            xaxis=dict(ticks='', side='top'),
            yaxis=dict(ticks='', ticksuffix='  '),
            # width=700,
            # height=700,
            # autosize=False
        )

        offline.iplot(fig)
        return fig
