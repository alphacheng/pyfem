# Include libraries
#import os,sys; sys.path.insert(0, os.getcwd()+"\\..\\..")
import os,sys; sys.path.insert(0, os.getcwd()+"/../..")

from pyfem  import *

# Generate mesh
mesh = Mesh()

bl0 = Block2D()

bl0.set_coords([(0,0), (1,0), (1,1), (0,1)])
bl0.set_divisions(4,4)

mesh.add_blocks(bl0)

mesh.generate()

mesh.write_file("tmesh.vtk")

# Setting the domain and loading the mesh
domain = Domain()
domain.load_mesh(mesh)

# Setting element types and parameters
emodel = SeepLinPerm(k=1000)

domain.elems.set_elem_model(emodel)

#Setting boundary conditions
domain.nodes.sub(y=0.0).set_bc(wp=-10.0)
domain.nodes.sub(y=1.0).set_bc(wp=10.0)

#Setting solver and solving
domain.set_solver( SolverSeep() )
#domain.solver.set_incs(1)
domain.solver.solve()

domain.solver.write_output()

