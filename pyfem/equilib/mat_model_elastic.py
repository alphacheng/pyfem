# -*- coding: utf-8 -*- 
"""
PYFEM - Finite element software
Raul Durand 2010-2013.
"""

from pyfem.model import *

class ModelLinElastic(Model):

    def __init__(self, *args, **kwargs):
        Model.__init__(self);
        self.sig = tensor2()
        self.eps = tensor2()
        self.E  = 0.0
        self.nu = 0.0
        self.A  = 0.0

        data = args[0] if args else kwargs

        self.set_params(**data)
        self.set_state(**data)

    @property
    def name(self):
        return "MatModelLinElastic"

    def copy(self):
        the_copy = ModelLinElastic()
        the_copy.sig = self.sig.copy()
        the_copy.eps = self.eps.copy()
        the_copy.E   = self.E
        the_copy.nu  = self.nu
        the_copy.A   = self.A
        the_copy.ndim  = self.ndim
        the_copy.attr = self.attr.copy()
        return the_copy

    def check(self):
        return True

    def set_params(self, **params):
        self.E  = params.get("E" , 0.0)
        self.nu = params.get("nu", 0.0)
        self.A  = params.get("A" , 0.0)

    def set_state(self, **state):
        sqrt2 = 2.0**0.5
        self.sig[0] = state.get("sxx", 0.0)
        self.sig[1] = state.get("syy", 0.0)
        self.sig[2] = state.get("szz", 0.0)
        self.sig[3] = state.get("sxy", 0.0)*sqrt2
        self.sig[4] = state.get("syz", 0.0)*sqrt2
        self.sig[5] = state.get("sxz", 0.0)*sqrt2

    def stiff(self):
        E  = self.E
        nu = self.nu

        if self.attr.get("plane_stress"):
            c = E/(1.0-nu*nu)
            return array([\
                    [ c    , c*nu , 0.0 ,        0.0,        0.0,        0.0 ], \
                    [ c*nu ,    c , 0.0 ,        0.0,        0.0,        0.0 ], \
                    [  0.0 ,  0.0 , 0.0 ,        0.0,        0.0,        0.0 ], \
                    [  0.0 ,  0.0 , 0.0 , c*(1.0-nu),        0.0,        0.0 ], \
                    [  0.0 ,  0.0 , 0.0 ,        0.0,        0.0,        0.0 ], \
                    [  0.0 ,  0.0 , 0.0 ,        0.0,        0.0,        0.0 ] ] )

        # For plane strain and 3D:
        c = E/((1.0+nu)*(1.0-2.0*nu))
        return array([\
                [ c*(1.0-nu),  c*nu ,      c*nu ,            0.0,            0.0,            0.0 ], \
                [ c*nu ,  c*(1.0-nu),      c*nu ,            0.0,            0.0,            0.0 ], \
                [ c*nu ,       c*nu , c*(1.0-nu),            0.0,            0.0,            0.0 ], \
                [  0.0 ,        0.0 ,       0.0 , c*(1.0-2.0*nu),            0.0,            0.0 ], \
                [  0.0 ,        0.0 ,       0.0 ,            0.0, c*(1.0-2.0*nu),            0.0 ], \
                [  0.0 ,        0.0 ,       0.0 ,            0.0,            0.0, c*(1.0-2.0*nu) ] ] )

    def stress_update(self, deps):
        dsig = mul(self.stiff(), deps)
        self.eps += deps;
        self.sig += dsig;
        return dsig

    def get_state(self):
        return {
                "sxx" : self.sig[0],
                "syy" : self.sig[1],
                "szz" : self.sig[2],
                "sxy" : self.sig[3]/sqrt2,
                "syz" : self.sig[4]/sqrt2,
                "sxz" : self.sig[5]/sqrt2,
                }

    def get_vals(self):
        sig = self.sig
        eps = self.eps

        vals = {}

        if self.ndim==2:
            sqrt2 = 2.0**0.5
            vals["sxx"] = sig[0]
            vals["syy"] = sig[1]
            vals["szz"] = sig[2]
            vals["sxy"] = sig[3]/sqrt2
            vals["exx"] = eps[0]
            vals["eyy"] = eps[1]
            vals["ezz"] = eps[2]
            vals["exy"] = eps[3]/sqrt2
            vals["sig_m"] = (sig[0]+sig[1]+sig[2])/3.0

        if self.ndim==3:
            sqrt2 = 2.0**0.5
            vals["sxx"] = sig[0]
            vals["syy"] = sig[1]
            vals["szz"] = sig[2]
            vals["sxy"] = sig[3]/sqrt2
            vals["syz"] = sig[4]/sqrt2
            vals["sxz"] = sig[5]/sqrt2
            vals["exx"] = eps[0]
            vals["eyy"] = eps[1]
            vals["ezz"] = eps[2]
            vals["exy"] = eps[3]/sqrt2
            vals["eyz"] = eps[4]/sqrt2
            vals["exz"] = eps[5]/sqrt2
            vals["sig_m"] = (sig[0]+sig[1]+sig[2])/3.0

        return vals

    def __str__(self, margin=""):
        os = StringIO()
        print >> os, margin, "<ModelLinElastic> (",
        print >> os, "Parameters: E=", self.E, " nu=", self.nu
        print >> os, margin, "    Data: ", self.get_vals(), ")"
        return os.getvalue()

