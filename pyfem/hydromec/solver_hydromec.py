from pyfem.solver import *
from pyfem.tools.matvec import *
from pyfem.equilib.elem_model_eq   import *
from pyfem.seepage.elem_model_seep import *
from elem_model_hydromec import *

import math
from numpy.linalg import norm
import scipy
from scipy.sparse import lil_matrix
from scipy import *
from scipy.sparse.linalg import factorized

class SolverHydromec(Solver):
    def __init__(self):
        Solver.__init__(self)
        self.name = "SolverHydromec"
        self.DU   = None
        self.DF   = None
        self.K    = None
        self.K11  = None
        self.K12  = None
        self.K21  = None
        self.K22  = None
        self.LUsolver = None
        self.plane_stress = False
        self.time_lapse = 0.0

    def prime_and_check(self):
        nnodes = len(self.nodes)

        # Check if all elem models are set
        for e in self.elems:
            if not e.elem_model:
                raise Exception("SolveHydromec.prime_and_check: Element model was not set")

        # Setting extra linked elements
        for e in self.elems:
            e.elem_model.lnk_elem_models= []
            for lnk_e in e.lnk_elems:
                e.elem_model.lnk_elem_models.append(lnk_e.elem_model)

        # Checking all elements
        for e in self.elems:
            e.elem_model.prime_and_check()

        # Fill active elements collection
        self.aelems = []
        for e in self.elems:
            emodel = e.elem_model
            suitable_elems = [ElemModelHydromec, ElemModelEq, ElemModelSeep]
            is_suitable    = any([isinstance(e.elem_model, etype) for etype in suitable_elems])

            if not is_suitable:
                raise Exception("SolveHydromec.prime_and_check: Element model is not suitable")
            if e.elem_model.is_active:
                self.aelems.append(e)

        # Fill collection of prescribed dofs and unknown dofs
        self.pdofs = []
        self.udofs = []

        for n in self.nodes:
            for dof in n.dofs:
                if dof.prescU:
                    self.pdofs.append(dof)
                else:
                    self.udofs.append(dof)

        self.dofs = []
        for dof in self.udofs:
            self.dofs.append(dof)
        for dof in self.pdofs:
            self.dofs.append(dof)
        for i, dof in enumerate(self.dofs):
            dof.eq_id = i

        self.ndofs = len(self.dofs)

        if not self.pdofs: raise Exception("SolveHydromec.prime_and_check: No prescribed dofs=")

    def mountK(self, dt):
        ndofs = len(self.dofs)
        r, c, v = [], [], []
        self.alpha = 1.0

        calc_funcs = [ "calcH"      , "calcK"    , "calcM"    , "calcL"    , "calcC" ]
        loc_funcs  = [ "get_H_loc"  , "get_K_loc", "get_M_loc", "get_L_loc", "get_C_loc"]
        matr_coefs = [ self.alpha*dt, 1.0        , 1.0        , 1.0        , 1.0 ]

        for e in self.aelems:
            for func, lfunc, coef in zip(calc_funcs, loc_funcs, matr_coefs):
                if hasattr(e.elem_model, func):
                    M   = getattr(e.elem_model, func)()*coef
                    loc = getattr(e.elem_model, lfunc)()
                    if isinstance(loc, tuple):
                        rloc = loc[0]
                        cloc = loc[1]
                    else:
                        rloc = loc
                        cloc = loc

                    for i in range(M.shape[0]):
                        for j in range(M.shape[1]):
                            r.append(rloc[i])
                            c.append(cloc[j])
                            v.append(M[i,j])

        self.K = scipy.sparse.coo_matrix((v, (r,c)), (ndofs, ndofs))

    def add_submatrix(self, r,c,v, M, rloc, cloc):
        for i in range(M.shape[0]):
            for j in range(M.shape[1]):
                r.append(rloc[i])
                c.append(cloc[j])
                v.append(M[i,j])

    def mountRHS(self, RHS, dt):
        ndofs = len(self.dofs)

        # Vector with natural values
        #RHS = array([dof.bryF for dof in self.dofs])

        for e in self.aelems:
            # Permeability matrix
            H   = e.elem_model.calcH()
            # Total pore-pressure vector
            P = [ node.keys["wp"].U for node in e.elem_model.nodes ]
            #print P
            #Permeability map
            loc = e.elem_model.get_H_loc()
            RHS[loc] += -dt*mul(H,P)
            #OUT('dt*mul(H,P)')


            Qh = e.elem_model.calcQh()
            RHS[loc] += dt*Qh
            #OUT('dt*Qh')
            #OUT('dt*mul(H,P) - dt*Qh')

        return RHS

        #print "dt: ", dt
        #print RHS
        #exit()

    def solve(self, Dt):
        scheme = self.scheme

        self.stage += 1
        if not scheme: scheme = "MNR"

        if self.verbose:
            print "Solver: SolveHydromec"
            print "  stage", self.stage, ":"
            print "  scheme:", self.scheme

        # Initialize SolveHydromec object and check
        self.prime_and_check()

        if self.verbose:
            print "  active elems:", len(self.aelems)
            print "  unknown dofs:", len(self.udofs)

        # Init U and F vectors
        lam   = 1.0/self.nincs
        dt    = lam*Dt
        U     = array([dof.bryU for dof in self.dofs])
        F     = array([dof.bryF for dof in self.dofs])
        #F     = self.mountRHS(dt)

        nu    = len(self.udofs)
        DU    = lam*U
        DF    = lam*F
        DFint = None
        R     = None

        # Check for applied natural boundary conditions
        force = 0.0
        for i, dof in enumerate(self.udofs):
            force += abs(F[dof.eq_id])

        no_natural = True if force==0.0 else False

        if no_natural and (scheme == "MNR" or scheme == "NR"):
            raise Exception("SolveHydromec.solve: Select scheme needs dofs with prescribed natural values")

        # Solve accros increments
        for self.inc in range(1, self.nincs+1):
            if scheme == "MNR" or scheme == "NR":
                if self.verbose: print "  increment", self.inc, ":"
                DU = lam*U
                DF = lam*F
                dt = lam*Dt
                calcK    = True
                converged = False
                DFi = DF.copy()
                DFint_ac = zeros(self.ndofs)

                for it in range(self.nmaxits):
                    if it: DU *= 0.0

                    DFint, R = self.solve_inc(DU, DFi, dt, calcK) # Calculates DU, DFint and completes DFi
                    dt  = 0.0  # Time is not applied again
                    if scheme=="MNR": calcK = False

                    DFi       = DFi - DFint
                    DFint_ac += DFint

                    self.residue = 0.0
                    for dof in self.udofs:
                        self.residue += abs(DF[dof.eq_id] - DFint_ac[dof.eq_id])/force
                        #print dof.owner_id, DF[dof.eq_id], DFint_ac[dof.eq_id]

                    if self.verbose: print "    it", it+1, " error =", self.residue

                    if math.isnan(self.residue): raise Exception("SolveHydromec.solve: Solver failed")

                    if self.residue < self.precision:
                        converged = True
                        break

                if not converged:
                    raise Exception("SolveHydromec.solve: Solver with scheme (M)NR did not converge")

            if scheme == "FE":
                DF = lam*F
                DFint, R, DFext = self.solve_inc(DU, DF, dt)
                #self.residue = norm(R)/(norm(DFint)*self.nincs)
                #if not no_natural:
                    #self.residue = norm(R)/(norm(DFint)*self.nincs)
                #else:
                self.residue = 0.0
                for dof in self.udofs:
                    self.residue += (DFext[dof.eq_id] - DFint[dof.eq_id])**2
                self.residue = self.residue/(norm(DFext)*self.nincs + 1.)

                if math.isnan(self.residue): raise Exception("SolveHydromec.solve: Solver failed")
                if self.verbose: print "  increment:", self.inc, " error = ", self.residue

            if self.track_per_inc:
                self.write_history()

        if self.verbose: print "  end stage:", self.stage

    def solve_inc(self, DU, DF, dt, calcK=True):
        """
          [  K11   K12 ]  [ U1? ]    [ F1  ]
          [            ]  [     ] =  [     ]
          [  K21   K22 ]  [ U2  ]    [ F2? ]"""

        nu     = len(self.udofs)
        np     = len(self.pdofs)
        ndof   = len(self.dofs)
        decomp = True if calcK else False
        scheme = self.scheme
        incver = True if self.verbose and nu>500 else False

        if calcK:
            if incver: print "    building system...", ; sys.stdout.flush()
            self.mountK(dt)

            # Mount K11.. K22 matrices
            cK = self.K.tocsc()
            self.K11 = cK[:nu , :nu ]
            self.K12 = cK[:nu ,  nu:]
            self.K21 = cK[ nu:, :nu ]
            self.K22 = cK[ nu:,  nu:]
            cK = None # Free memory

        DF = self.mountRHS(DF, dt)
        #OUT("DF")

        F1 = DF[:nu]
        U2 = DU[nu:]

        # Solve linear system
        F2 = self.K22*U2  # sparse matrix * dense vector
        if nu:
            if incver: print "solving...", ; sys.stdout.flush()

            if scheme == "MNR" and decomp: 
                self.LUsolver = factorized(self.K11)

            if scheme == "NR" or scheme == "FE": 
                self.LUsolver = factorized(self.K11)

            RHS = F1 - self.K12*U2
            U1  = scipy.sparse.linalg.spsolve(self.K11, RHS)
            F2 += self.K21*U1

        # Complete vectors
        for i, dof in enumerate(self.udofs): DU[dof.eq_id] = U1[i]
        for i, dof in enumerate(self.pdofs): DF[dof.eq_id] = F2[i]

        if incver: print "updating..." ; sys.stdout.flush()
        DFint = self.update_elems_and_nodes(DU, dt) # Also calculates DFint

        R = DF - DFint
        return DFint, R, DF

    def update_elems_and_nodes(self, DU, dt):
        DFint = zeros(len(self.dofs))

        # Updating elements
        for e in self.aelems:
            e.elem_model.update_state(DU, DFint, dt)

        # Updating dofs
        for i, dof in enumerate(self.dofs):
            dof.U += DU[i]
            dof.F += DFint[i]

        return DFint













