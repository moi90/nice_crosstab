import pandas as pd
import numpy as np

from . import _version

__version__ = _version.get_versions()["version"]


def _calc_scores(crosstab, maxiter=100, tol=1e-3):
    crosstab = np.array(crosstab)

    b = np.arange(crosstab.shape[1])
    b_old = b

    for _ in range(maxiter):
        a = (crosstab * b).sum(axis=1) / crosstab.sum(axis=1)
        a = (a - np.mean(a)) / np.std(a)

        b = (a[:, np.newaxis] * crosstab).sum(axis=0) / crosstab.sum(axis=0)
        # b = (b - np.mean(b)) / np.std(b)

        diff = np.linalg.norm(b - b_old)

        if diff < tol:
            break

        b_old = b

    return a, b


def nice_crosstab(index, columns):
    """
    An extension of pandas.crosstab for two factors with "natural" ordering of rows and columns.

    The implementation is based on the algorithm presented on http://alumni.media.mit.edu/~tpminka/courses/36-350.2001/lectures/day13/.
    """

    crosstab = pd.crosstab(index, columns)

    # Sort so that high values concentrate around the diagonal
    i_scores, c_scores = _calc_scores(crosstab)

    i_order = np.argsort(i_scores)
    c_order = np.argsort(c_scores)

    return crosstab.iloc[i_order, c_order]
