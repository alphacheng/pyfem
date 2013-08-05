import os,sys
from math import log

from pyfem.tools.matvec import *
from pyfem.tools.stream import *
from shape_types import *
from block import *

class BlockInset(Block):
    def __init__(self):
        """
        Block class to discretize crossing elements
        ===========================================

        This discretizes entities as reinforcements that cross the mesh.
        For example, a reinforcement entitie can be discretized into several 
        bar elements according to the tresspased elements. In addition, joint 
        elements are created to link the tresspased elements with the bar
        elements.

        STORED:
            quadratic: Flag used to obtain discretized bars with three nodes.
            punctual : Flag used to generate punctual joint elements instead
                       of continuous joint elements.

        """

        Block.__init__(self)
        self.quadratic = True # Quadratic truss elements are generated by default
        self.neighbors = []   # Neighbor shapes list to speed up shape look up
        self.punctual  = False  # Flag to define embedded punctual method

    def set_quadratic(self, value=True):
        """
        Defines if resulting bars are quadratic
        =======================================
        """

        self.quadratic = value

    def set_coords(self, C):
        """
        Sets the block coordinates 
        ==========================

        input: 
            C:  A list of lists with start and end coordinates of 
                a crossing entity. A numpy matrix is also allowed.
        """

        ncols = len(C[0])
        nrows = len(C)
        self.coords = zeros(nrows, 3)
        self.coords[:,:ncols] = array(C)[:,:ncols]
        
    def shape_func(self, shape, R):
        """
        Returns the shape function values for conventional solid shapes
        ===============================================================
        
        INPUT:
            shape: An integer that represent the shape type
            R:     A list containing natural coordinates of the point 
                   where the shape functions are evaluated
        RETURNS:
            N:     A list with all shape functions
        """

        shape_type = shape.shape_type
        r, s, t = R[0], R[1], R[2]

        if shape_type == LIN2:
            N = empty(2)
            N[0] = 0.5*(1-r)
            N[1] = 0.5*(1+r)
        elif shape_type == LIN3:
            N = empty(3)
            N[0] = 0.5*(r*r - r)
            N[1] = 0.5*(r*r + r)
            N[2] = 1.0 - r*r
        elif shape_type == QUAD4:
            N = empty(4)
            N[0] = 0.25*(1.0-r-s+r*s)
            N[1] = 0.25*(1.0+r-s-r*s)
            N[2] = 0.25*(1.0+r+s+r*s)
            N[3] = 0.25*(1.0-r+s-r*s)

        elif shape_type == QUAD8:
            N = empty(8)
            rp1=1.0+r; rm1=1.0-r
            sp1=1.0+s; sm1=1.0-s
            N[0] = 0.25*rm1*sm1*(rm1+sm1-3.0)
            N[1] = 0.25*rp1*sm1*(rp1+sm1-3.0)
            N[2] = 0.25*rp1*sp1*(rp1+sp1-3.0)
            N[3] = 0.25*rm1*sp1*(rm1+sp1-3.0)
            N[4] = 0.50*sm1*(1.0-r*r)
            N[5] = 0.50*rp1*(1.0-s*s)
            N[6] = 0.50*sp1*(1.0-r*r)
            N[7] = 0.50*rm1*(1.0-s*s)

        elif shape_type == TET4:
            N = empty(4)
            N[0] = 1.0-r-s-t
            N[1] = r
            N[2] = s
            N[3] = t

        elif shape_type == HEX8:
            N = empty(8)
            N[0] = 0.125*(1.0-r-s+r*s-t+s*t+r*t-r*s*t)
            N[1] = 0.125*(1.0+r-s-r*s-t+s*t-r*t+r*s*t)
            N[2] = 0.125*(1.0+r+s+r*s-t-s*t-r*t-r*s*t)
            N[3] = 0.125*(1.0-r+s-r*s-t-s*t+r*t+r*s*t)
            N[4] = 0.125*(1.0-r-s+r*s+t-s*t-r*t+r*s*t)
            N[5] = 0.125*(1.0+r-s-r*s+t-s*t+r*t-r*s*t)
            N[6] = 0.125*(1.0+r+s+r*s+t+s*t+r*t+r*s*t)
            N[7] = 0.125*(1.0-r+s-r*s+t+s*t-r*t-r*s*t)

        elif shape_type == HEX20:
            N = empty(20)
            rp1=1.0+r; rm1=1.0-r
            sp1=1.0+s; sm1=1.0-s
            tp1=1.0+t; tm1=1.0-t

            N[ 0] = 0.125*rm1*sm1*tm1*(-r-s-t-2)
            N[ 1] = 0.125*rp1*sm1*tm1*( r-s-t-2)
            N[ 2] = 0.125*rp1*sp1*tm1*( r+s-t-2)
            N[ 3] = 0.125*rm1*sp1*tm1*(-r+s-t-2)
            N[ 4] = 0.125*rm1*sm1*tp1*(-r-s+t-2)
            N[ 5] = 0.125*rp1*sm1*tp1*( r-s+t-2)
            N[ 6] = 0.125*rp1*sp1*tp1*( r+s+t-2)
            N[ 7] = 0.125*rm1*sp1*tp1*(-r+s+t-2)
            N[ 8] = 0.25*(1-r*r)*sm1*tm1
            N[ 9] = 0.25*rp1*(1-s*s)*tm1
            N[10] = 0.25*(1-r*r)*sp1*tm1
            N[11] = 0.25*rm1*(1-s*s)*tm1
            N[12] = 0.25*(1-r*r)*sm1*tp1
            N[13] = 0.25*rp1*(1-s*s)*tp1
            N[14] = 0.25*(1-r*r)*sp1*tp1
            N[15] = 0.25*rm1*(1-s*s)*tp1
            N[16] = 0.25*rm1*sm1*(1-t*t)
            N[17] = 0.25*rp1*sm1*(1-t*t)
            N[18] = 0.25*rp1*sp1*(1-t*t)
            N[19] = 0.25*rm1*sp1*(1-t*t)

        else:
            raise Exception("Block_inset::shape_func: Could not find shape type.")

        return N
    
    def deriv_func(self, shape, R):
        """
        Returns the shape function derivatives for conventional solid shapes
        ====================================================================
        
        INPUT:
            shape: An integer that represent the shape type
            R:     A list containing natural coordinates of the point 
                   where the shape functions are evaluated

        RETURNS:
            D:     A list with all shape functions

        """

        r, s, t = R[0], R[1], R[2]

        shape_type = shape.shape_type

        if shape_type == QUAD4:
            D = empty(2,4)
            D[0,0] = 0.25*(-1.0+s);   D[1,0] = 0.25*(-1.0+r)
            D[0,1] = 0.25*(+1.0-s);   D[1,1] = 0.25*(-1.0-r)
            D[0,2] = 0.25*(+1.0+s);   D[1,2] = 0.25*(+1.0+r)
            D[0,3] = 0.25*(-1.0-s);   D[1,3] = 0.25*(+1.0-r)

        elif shape_type == QUAD8:
            D = empty(2,8)
            rp1=1.0+r; rm1=1.0-r
            sp1=1.0+s; sm1=1.0-s

            D[0,0] = - 0.25 * sm1 * (rm1 + rm1 + sm1 - 3.0)
            D[0,1] =   0.25 * sm1 * (rp1 + rp1 + sm1 - 3.0)
            D[0,2] =   0.25 * sp1 * (rp1 + rp1 + sp1 - 3.0)
            D[0,3] = - 0.25 * sp1 * (rm1 + rm1 + sp1 - 3.0)
            D[0,4] = - r * sm1
            D[0,5] =   0.50 * (1.0 - s * s)
            D[0,6] = - r * sp1
            D[0,7] = - 0.5 * (1.0 - s * s)

            D[1,0] = - 0.25 * rm1 * (sm1 + rm1 + sm1 - 3.0)
            D[1,1] = - 0.25 * rp1 * (sm1 + rp1 + sm1 - 3.0)
            D[1,2] =   0.25 * rp1 * (sp1 + rp1 + sp1 - 3.0)
            D[1,3] =   0.25 * rm1 * (sp1 + rm1 + sp1 - 3.0)
            D[1,4] = - 0.50 * (1.0 - r * r)
            D[1,5] = - s * rp1
            D[1,6] =   0.50 * (1.0 - r * r)
            D[1,7] = - s * rm1

        elif shape_type == TET4:
            D = empty(3,4)
            D[0,0] = -1;   D[1,0] =-1;   D[2,0] =-1
            D[0,1] =  1;   D[1,1] = 0;   D[2,1] = 0
            D[0,2] =  0;   D[1,2] = 1;   D[2,2] = 0
            D[0,3] =  0;   D[1,3] = 0;   D[2,3] = 1

        elif shape_type == HEX8:
            D = empty(3,8)
            D[0,0] = 0.125*(-1.0+s+t-s*t);   D[1,0] =0.125*(-1.0+r+t-r*t);   D[2,0] =0.125*(-1.0+r+s-r*s)
            D[0,1] = 0.125*(+1.0-s-t+s*t);   D[1,1] =0.125*(-1.0-r+t+r*t);   D[2,1] =0.125*(-1.0-r+s+r*s)
            D[0,2] = 0.125*(+1.0+s-t-s*t);   D[1,2] =0.125*(+1.0+r-t-r*t);   D[2,2] =0.125*(-1.0-r-s-r*s)
            D[0,3] = 0.125*(-1.0-s+t+s*t);   D[1,3] =0.125*(+1.0-r-t+r*t);   D[2,3] =0.125*(-1.0+r-s+r*s)
            D[0,4] = 0.125*(-1.0+s-t+s*t);   D[1,4] =0.125*(-1.0+r-t+r*t);   D[2,4] =0.125*(+1.0-r-s+r*s)
            D[0,5] = 0.125*(+1.0-s+t-s*t);   D[1,5] =0.125*(-1.0-r-t-r*t);   D[2,5] =0.125*(+1.0+r-s-r*s)
            D[0,6] = 0.125*(+1.0+s+t+s*t);   D[1,6] =0.125*(+1.0+r+t+r*t);   D[2,6] =0.125*(+1.0+r+s+r*s)
            D[0,7] = 0.125*(-1.0-s-t-s*t);   D[1,7] =0.125*(+1.0-r+t-r*t);   D[2,7] =0.125*(+1.0-r+s-r*s)

        elif shape_type == HEX20:
            D = empty(3,20)
            rp1=1.0+r; rm1=1.0-r
            sp1=1.0+s; sm1=1.0-s
            tp1=1.0+t; tm1=1.0-t
            
            # Derivatives with respect to r
            D[0, 0] = -0.125*sm1*tm1*(-r-s-t-2)-0.125*rm1*sm1*tm1
            D[0, 1] =  0.125*sm1*tm1*( r-s-t-2)+0.125*rp1*sm1*tm1
            D[0, 2] =  0.125*sp1*tm1*( r+s-t-2)+0.125*rp1*sp1*tm1
            D[0, 3] = -0.125*sp1*tm1*(-r+s-t-2)-0.125*rm1*sp1*tm1
            D[0, 4] = -0.125*sm1*tp1*(-r-s+t-2)-0.125*rm1*sm1*tp1
            D[0, 5] =  0.125*sm1*tp1*( r-s+t-2)+0.125*rp1*sm1*tp1
            D[0, 6] =  0.125*sp1*tp1*( r+s+t-2)+0.125*rp1*sp1*tp1
            D[0, 7] = -0.125*sp1*tp1*(-r+s+t-2)-0.125*rm1*sp1*tp1
            D[0, 8] = -0.5*r*sm1*tm1
            D[0, 9] =  0.25*(1-s*s)*tm1
            D[0,10] = -0.5*r*sp1*tm1
            D[0,11] = -0.25*(1-s*s)*tm1
            D[0,12] = -0.5*r*sm1*tp1
            D[0,13] =  0.25*(1-s*s)*tp1
            D[0,14] = -0.5*r*sp1  *tp1
            D[0,15] = -0.25*(1-s*s)*tp1
            D[0,16] = -0.25*sm1*(1-t*t)
            D[0,17] =  0.25*sm1*(1-t*t)
            D[0,18] =  0.25*sp1*(1-t*t)
            D[0,19] = -0.25*sp1*(1-t*t)

            # Derivatives with respect to s
            D[1, 0] = -0.125*rm1*tm1*(-r-s-t-2)-0.125*rm1*sm1*tm1
            D[1, 1] = -0.125*rp1*tm1*( r-s-t-2)-0.125*rp1*sm1*tm1
            D[1, 2] =  0.125*rp1*tm1*( r+s-t-2)+0.125*rp1*sp1*tm1
            D[1, 3] =  0.125*rm1*tm1*(-r+s-t-2)+0.125*rm1*sp1*tm1
            D[1, 4] = -0.125*rm1*tp1*(-r-s+t-2)-0.125*rm1*sm1*tp1
            D[1, 5] = -0.125*rp1*tp1*( r-s+t-2)-0.125*rp1*sm1*tp1
            D[1, 6] =  0.125*rp1*tp1*( r+s+t-2)+0.125*rp1*sp1*tp1
            D[1, 7] =  0.125*rm1*tp1*(-r+s+t-2)+0.125*rm1*sp1*tp1
            D[1, 8] = -0.25*(1-r*r)*tm1
            D[1, 9] = -0.5*s*rp1*tm1
            D[1,10] =  0.25*(1-r*r)*tm1
            D[1,11] = -0.5*s*rm1*tm1
            D[1,12] = -0.25*(1-r*r)*tp1
            D[1,13] = -0.5*s*rp1*tp1
            D[1,14] =  0.25*(1-r*r)*tp1
            D[1,15] = -0.5*s*rm1*tp1
            D[1,16] = -0.25*rm1*(1-t*t)
            D[1,17] = -0.25*rp1*(1-t*t)
            D[1,18] =  0.25*rp1*(1-t*t)
            D[1,19] =  0.25*rm1*(1-t*t)

            # Derivatives with respect to t
            D[2, 0] = -0.125*rm1*sm1*(-r-s-t-2)-0.125*rm1*sm1*tm1
            D[2, 1] = -0.125*rp1*sm1*( r-s-t-2)-0.125*rp1*sm1*tm1
            D[2, 2] = -0.125*rp1*sp1*( r+s-t-2)-0.125*rp1*sp1*tm1
            D[2, 3] = -0.125*rm1*sp1*(-r+s-t-2)-0.125*rm1*sp1*tm1
            D[2, 4] =  0.125*rm1*sm1*(-r-s+t-2)+0.125*rm1*sm1*tp1
            D[2, 5] =  0.125*rp1*sm1*( r-s+t-2)+0.125*rp1*sm1*tp1
            D[2, 6] =  0.125*rp1*sp1*( r+s+t-2)+0.125*rp1*sp1*tp1
            D[2, 7] =  0.125*rm1*sp1*(-r+s+t-2)+0.125*rm1*sp1*tp1
            D[2, 8] = -0.25*(1-r*r)*sm1
            D[2, 9] = -0.25*rp1*(1-s*s)
            D[2,10] = -0.25*(1-r*r)*sp1
            D[2,11] = -0.25*rm1*(1-s*s)
            D[2,12] =  0.25*(1-r*r)*sm1
            D[2,13] =  0.25*rp1*(1-s*s)
            D[2,14] =  0.25*(1-r*r)*sp1
            D[2,15] =  0.25*rm1*(1-s*s)
            D[2,16] = -0.5*t*rm1*sm1
            D[2,17] = -0.5*t*rp1*sm1
            D[2,18] = -0.5*t*rp1*sp1
            D[2,19] = -0.5*t*rm1*sp1

        else:
            raise Exception("Block_inset::deriv_func: Could not find shape type.")
        return D
    
    def get_shape_coords(self, S):
        """
        Constructs a matrix with shape coordinates
        ==========================================

        INPUT: 
            S: Shape object
        RETURNS:
            C: A matrix with the coordinates of a shape object
        """

        ndim = 3;
        sh_type = S.shape_type
        #if sh_type==TRI3 or sh_type==TRI6 or sh_type==QUAD4 or sh_type==QUAD8:
        if sh_type in [TRI3, TRI6, QUAD4, QUAD8]:
            ndim = 2
        else:
            ndim = 3

        C = empty(len(S.points), ndim)
        for i, point in enumerate(S.points):
            C[i,0] = point.x
            C[i,1] = point.y
            if ndim==3:
                C[i,2] = point.z

        return C

    def inverse_map(self, S, X):
        """
        Determines natural coordinates of a point given in global coordinates
        =====================================================================

        INPUT: 
            S: Shape object
            X: List of global coordinates of a point
        RETURNS:
            R: List of natural coordinates of the given point
        """

        TOL   = 1.0E-4
        MAXIT = 25
        R = zeros(3)

        C = self.get_shape_coords(S)
        for k in range(MAXIT):
            # calculate Jacobian
            D = self.deriv_func(S, R)
            J = mul(D, C)

            # calculate trial of real coordinates
            N = self.shape_func(S, R)
            Xt = mul(N.T, C).T # interpolating
            
            # calculate the error
            deltaX = Xt - X;
            deltaR = mul(inv(J).T, deltaX)

            # updating local coords R
            R -= deltaR
            if norm(deltaX) < TOL: break

        return R

    def bdistance(self, S, R):
        """
        Determines an estimate of the distance of a point to the border of a shape
        ==========================================================================

        INPUT: 
            S:     Shape object
            R:     A list containing natural coordinates of the point 
                   where the shape functions are evaluated
        RETURNS:
            value: An estimate of the distance to the border.
                   Positive value means that the point is inside the shape.
                   Negative value means that the point is outside the shape.
        """

        r, s, t = R[0], R[1], R[2]

        sh_type = S.shape_type

        if sh_type==TRI3 or sh_type==TRI6:
            assert False

        if sh_type==QUAD4 or sh_type==QUAD8:
            return min(1.0 - abs(r), 1.0 - (s))

        if sh_type==HEX8 or sh_type==HEX20:
            return min(1.0 - abs(r), 1.0 - abs(s), 1.0 - abs(t))

        if sh_type==TET4 or sh_type==TET10:
            return min(r, s, t, 1.0-r-s-t)

        return -1.0
        #raise Exception("Block_inset::bdistance: Could not find shape type.")

    def is_inside(self, S, X):
        """
        Determines if a point is inside a shape
        =======================================

        INPUT: 
            S:     Shape object
            X:     List of global coordinates of a point
        RETURNS:
            value: True if the point is inside the shape
        """

        if S.shape_type in [LIN2, LIN3, LINK1, LINK2, LINK3]: return False

        TOL = 1.0E-6
    	R = self.inverse_map(S, X)
        if self.bdistance(S, R) > -TOL:
            return True;
        else: 
            return False;

    def find_shape(self, X, shapes, near_shapes=None):
        """
        Finds the shape that contains a given point
        ===========================================

        INPUT: 
            X:            List of global coordinates of a point
            shapes:       A list of shapes
            near_shapes:  A list of shapes that is know that are close to 
                          the given point
        RETURNS:
            shape:        The shape that contains the given point. 
                          In the case of the point is not contained by any shape
                          from the list 'shapes' then an exception is fired
        """

        if near_shapes is not None:
            for shape in near_shapes:
                if self.is_inside(shape, X):
                    return shape

        for shape in shapes:
            if self.is_inside(shape, X): 
                return shape
        
        raise Exception("Block_inset::find_shape: Coordinates outside mesh.")

    def find_neighbors(self, shapes, points):
        """
        Finds neighbors shapes (not being used)
        =======================================
        """

        pts_lst = sorted(points, key=lambda n: n.id)
        shp_lst = sorted(shapes, key=lambda s: s.id)

        pt_sh_lst = []
        for p in pts_lst:
            pt_sh_lst.append([])

        self.neighbors = []
        for s in shp_lst:
            self.neighbors.append(set())

        for s in shp_lst:
            for pt in s.points:
                pt_sh_lst[pt.id].append(s)

        for sh_set in pt_sh_lst:
            for sh1 in sh_set:
                for sh2 in sh_set:
                    if sh1 is sh2: continue
                    self.neighbors[sh1.id].add(sh2)

    def split(self, points, shapes, faces):
        """
        Performs the discretization of a crossed entity
        ===============================================

        This function modifies a mesh (given as sets of points and shapes)
        in order to add new shapes and points corresponding to the 
        discretization of a crossing entity.

        INPUT:
            points: A set of points of an existing mesh
            shapes: A set of shapes of an existing mesh
            faces : A set of faces. Not being used in this function but
                    inlcluded to math the function definition as in the 
                    base class.
        RETURNS:
            None
        """

        #self.find_neighbors(shapes, points)

        # Constants
        TINY = 1.0E-3
        TOL  = 1.0E-5

        # Getting initial and final coordinates
        X0 = self.coords[0,:] # Coordinate of first point
        X1 = self.coords[1,:] # Coordinate of last  point
        
        # Initial conditions
        length  = norm(X1-X0)
        tinylen = TINY*length
        bdist = 0.0        # boundary function initial value
        step  = length     # initial step length

        # Defining required vectors
        Xp = X0.copy()       # shape begin coordinates (previous point)
        X  = Xp.copy()       # test point coordinates
        T  = (X1-X0)/length  # unitary vector for the inset

        # Find the initial and final element
        init_sh  = self.find_shape(X0 + tinylen*T, shapes) # The first tresspased shape
        final_sh = self.find_shape(X1 - tinylen*T, shapes) # The last tresspased shape
        near_shapes = set([init_sh, final_sh])

        # Flag used to determine if the current segment is the final segment
        final_segment = True if init_sh==final_sh else False 
        
        # Flag for the first segment
        first_segment = True

        # Initializing more variables
        curr_sh = prev_sh = init_sh
        next_sh = final_sh

        # Last point of previous segment point coordinates
        P1_prev = None   

        # Splitting inset
        next_sh = init_sh
        while True:
            if final_segment:
                X = X1
            else:
                curr_sh = next_sh
                step = 0.5*norm(X1-X)
                X += step*T
                n = int(log(step/TOL,2)) + 1
                step0 = 0.0
                for i in range(n):
                    R     = self.inverse_map(curr_sh, X)
                    bdist = self.bdistance(curr_sh, R)
                    step *= 0.5+TOL

                    # Bisection algorithm
                    if bdist>=-TOL: # (-TOL) is needed to aproximate the 'intersection' outside the cell
                        X += step*T # forward
                    else:
                        X -= step*T # backward

                    dstep = abs(step - step0)
                    step0 = step

                if abs(dstep)>TOL:
                    print "Block_inset.split: Bisection did not converge with dstep=%23.15e"%(bdist)


            # Getting line points
            # First point
            P0 = Point(X0) if first_segment else P1
            
            # Second point
            P1 = Point(X)

            # Middle point
            P2 = Point((Xp + X)/2.0) if self.quadratic else None

            # Points
            Ps = [P0, P1, P2] if self.quadratic else [P0, P1]
            
            # Creating new points
            for i, P in enumerate(Ps):
                if i>0 or first_segment:
                    P.id = len(points)
                    points.add(P)

            # Saving segment and related nodal points
            S             = Shape()
            S.tag         = self.tag
            S.shape_type  = LIN3 if self.quadratic else LIN2
            S.id          = len(shapes)
            shapes.add(S)
            for P in Ps:
                S.points.append(P)
            
            # Saving link shape
            if self.punctual:
                # Creates discrete joint elements
                for P in Ps:
                    Sj = Shape()
                    Sj.shape_type = LINK1
                    Sj.tag = self.tag
                    Sj.points.extend(curr_sh.points)
                    Sj.points.append(P)
                    Sj.lnk_shapes = [S, curr_sh]
                    Sj.id = len(shapes3)
                    shapes.add(Sj)
            else:
                # Create a continuous joint element
                Sj = Shape()
                if not self.quadratic:
                    Sj.shape_type = LINK2
                else:
                    Sj.shape_type = LINK3

                Sj.tag = self.tag
                Sj.points.extend(curr_sh.points) # uses trespassed element points
                Sj.points.extend(S.points)       # adds bar points
                Sj.lnk_shapes = [S, curr_sh]
                Sj.id = len(shapes)
                shapes.add(Sj)

            if abs(norm(X-X0) - length) < TOL:
                return

            # Preparing for the next segment
            Xp = X.copy()
            first_segment = False
            next_sh = self.find_shape(X + tinylen*T, shapes) # The first tresspased shape

    def split_back(self, points, shapes, faces):
        """
        Performs the discretization of a crossed entity
        ===============================================

        This function modifies a mesh (given as sets of points and shapes)
        in order to add new shapes and points corresponding to the 
        discretization of a crossing entity.

        INPUT:
            points: A set of points of an existing mesh
            shapes: A set of shapes of an existing mesh
            faces : A set of faces. Not being used in this function but
                    inlcluded to math the function definition as in the 
                    base class.
        RETURNS:
            None
        """

        #self.find_neighbors(shapes, points)

        # Constants
        TINY = 1.0E-3
        TOL  = 1.0E-4

        # Getting initial and final coordinates
        X0 = self.coords[0,:] # Coordinate of first point
        X1 = self.coords[1,:] # Coordinate of last  point
        
        # Initial conditions
        length  = norm(X1-X0)
        tinylen = TINY*length
        bdist = 0.0        # boundary function initial value
        step  = length     # initial step length

        # Defining required vectors
        Xp = X0.copy()       # shape begin coordinates (previous point)
        X  = Xp.copy()       # test point coordinates
        T  = (X1-X0)/length  # unitary vector for the inset

        # Find the initial and final element
        init_sh  = self.find_shape(X0 + tinylen*T, shapes) # The first tresspased shape
        final_sh = self.find_shape(X1 - tinylen*T, shapes) # The last tresspased shape
        near_shapes = set([init_sh, final_sh])

        # Flag used to determine if the current segment is the final segment
        final_segment = True if init_sh==final_sh else False 
        
        # Flag for the first segment
        first_segment = True

        # Initializing more variables
        curr_sh = prev_sh = init_sh
        next_sh = final_sh

        # Last point of previous segment point coordinates
        P1_prev = None   

        # Splitting inset
        while True:
            #print step, bdist, curr_sh.id, prev_sh.id
            curr_sh = None
            if final_segment:
                X = X1.copy()
                prev_sh = curr_sh = final_sh
            else:
                step *= 0.5+TOL
                X    += step*T

                if self.is_inside(prev_sh, X):
                    curr_sh = prev_sh
                else:
                    curr_sh = self.find_shape(X, shapes, near_shapes)
                    near_shapes.add(curr_sh)

            if curr_sh == prev_sh:
                if final_segment:
                    bdist = 0.0
                else:
                    R = self.inverse_map(next_sh, X)
                    bdist = abs(self.bdistance(next_sh, R))

                if bdist <= TOL:  # intersection is reached!!
                    # Saving segment and related nodal points
                    S = Shape()
                    S.tag = self.tag

                    S.shape_type = LIN3 if self.quadratic else LIN2
                    
                    # First point
                    if first_segment:
                        tmpP = Point(X0)
                        P0 = tmpP.get_match_from(points)
                        if not P0: P0 = tmpP
                        P0.id = len(points)
                        points.add(P0)
                        S.points.append(P0)
                    else:
                        assert P1_prev
                        S.points.append(P1_prev)
                    
                    # Second point
                    if final_segment:
                        tmpP = Point(X)
                        P1 = tmpP.get_match_from(points)
                        if not P1: P1 = tmpP
                        P1.id = len(points)
                        points.add(P1)
                        S.points.append(P1)
                    else:
                        P1 = Point(X)
                        P1.id = len(points)
                        points.add(P1)
                        S.points.append(P1)
                        P1_prev = P1

                    # Middle point
                    if self.quadratic:
                        Xn = (Xp + X)/2.0
                        P2 = Point(Xn)
                        P2.id = len(points)
                        points.add(P2)
                        S.points.append(P2)

                    first_segment = False
                    S.id = len(shapes)
                    shapes.add(S)
                    
                    # Saving link shape
                    if self.punctual:
                        # Creates punctual joint elements
                        #Ps = [P0, P1]
                        #if self.quadratic: Ps.append(P2)
                        Ps = [P0, P1, P2] if self.quadratic else [P0, P1]

                        for P in Ps:
                            Sj = Shape()
                            Sj.shape_type = LINK1
                            Sj.tag = self.tag
                            Sj.points.extend(curr_sh.points)
                            Sj.points.append(P)
                            Sj.lnk_shapes = [S, curr_sh]
                            Sj.id = len(shapes)
                            shapes.add(Sj)
                    else:
                        # Create a continuous joint element
                        Sj = Shape()
                        if not self.quadratic:
                            Sj.shape_type = LINK2
                        else:
                            Sj.shape_type = LINK3

                        Sj.tag = self.tag
                        Sj.points.extend(curr_sh.points) # uses trespassed element points
                        Sj.points.extend(S.points)       # adds bar points
                        Sj.lnk_shapes = [S, curr_sh]
                        Sj.id = len(shapes)
                        shapes.add(Sj)

                    if final_segment: return

                    # Preparing for the next segment
                    Xp = X.copy()
                    if next_sh == final_sh:
                        final_segment = True
                    else:
                        prev_sh = next_sh
                        step = norm(X-X1)

                else: #when intersection is forward
                    step = abs(step) #advance
            else: #when intersection is backward
                step = -abs(step) #retrocession
                next_sh = curr_sh



