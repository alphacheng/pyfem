# Element analysis models
from elem_model_eq import *
from elem_model_truss import *
from elem_model_line_joint import *

# Material models
from mat_model_elastic import *
from mat_model_elastic_bar     import *
from mat_model_plastic_bar     import *
from mat_model_drucker_prager     import *
from mat_model_mohr_coulomb       import *
from mat_model_mohr_coulomb_joint import *

#Solver
from solver_eq import *


############################################################################## Solid elements


class EqElasticSolid(ElemModelEq):
    def __init__(self, *args, **kwargs):
        ElemModelEq.__init__(self, *args, **kwargs)
        mat_model = ModelLinElastic(*args, **kwargs)
        self.set_mat_model(mat_model)

class EqDruckerPragerSolid(ElemModelEq):
    def __init__(self, *args, **kwargs):
        ElemModelEq.__init__(self, *args, **kwargs)
        mat_model = MatModelDruckerPrager(*args, **kwargs)
        self.set_mat_model(mat_model)

class EqMohrCoulombSolid(ElemModelEq):
    def __init__(self, *args, **kwargs):
        ElemModelEq.__init__(self, *args, **kwargs)
        mat_model = MatModelMohrCoulomb(*args, **kwargs)
        self.set_mat_model(mat_model)

############################################################################## Line elements


class EqElasticBar(ElemModelTruss):
    def __init__(self, *args, **kwargs):
        ElemModelTruss.__init__(self, *args, **kwargs)
        mat_model = ModelElasticBar(*args, **kwargs)
        self.set_mat_model(mat_model)

class EqPlasticBar(ElemModelTruss):
    def __init__(self, *args, **kwargs):
        ElemModelTruss.__init__(self, *args, **kwargs)
        mat_model = ModelPlasticBar(*args, **kwargs)
        self.set_mat_model(mat_model)


############################################################################## Joint elements


class EqMohrCoulombJoint(ElemModelLineJoint):
    def __init__(self, *args, **kwargs):
        ElemModelLineJoint.__init__(self, *args, **kwargs)
        mat_model = MatModelMohrCoulombJoint(*args, **kwargs)
        self.set_mat_model(mat_model)