import pytest
import numpy as np
from rpy2.robjects import baseenv, numpy2ri
from scipy import sparse

from anndata2ri import scipy2ri
from anndata2ri.test_utils import conversions_py2rpy


mats = [
    pytest.param((2, 3), sparse.csr_matrix([[2.0, 0.0, 1.0], [0.0, 0.1, 0.0]]), id="csr"),
    pytest.param((3, 2), sparse.csc_matrix([[2.0, 0.0], [1.0, 0.0], [0.1, 0.0]]), id="csc"),
    pytest.param((2, 4), sparse.coo_matrix([[2.0, 0.0, 1.0, 0.0], [0.0, 0.1, 0.0, 3.0]]), id="coo"),
    pytest.param((4, 4), sparse.dia_matrix(([2.0, 0.4, 1.0, 0.0], [0]), (4, 4)), id="dia"),
]


@pytest.mark.parametrize("conversion", conversions_py2rpy)
@pytest.mark.parametrize("shape,dataset", mats)
def test_py2rpy(conversion, shape, dataset):
    sm = conversion(scipy2ri, dataset)
    assert tuple(baseenv["dim"](sm)) == shape

    dm = numpy2ri.converter.py2rpy(baseenv["as.matrix"](sm))
    assert np.allclose(dataset.toarray(), dm)
