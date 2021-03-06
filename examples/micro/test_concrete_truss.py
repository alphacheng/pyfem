# Include libraries
from pyfem import *

# Generate mesh

L = 8.0
H = 4.0
nx = 64
ny = 32

#Blocks 
block = Block2D()
#block.make_box( (0,0),  (8,1) )
#block.set_divisions(64,8)

block.make_box( (0,0),  (L,H) )
block.set_divisions(nx, ny)

block.make_truss(htag='h', vtag='v', dtag='d')

msh = Mesh(block)
msh.generate()
msh.write_file("tmesh.vtk")


# Setting the domain and loading the mesh
dom = Domain(mesh=msh)

# Setting element types and parameters
mat_h = EqConcreteTruss(E=20e6, A=0.03, sig_yc=200e3, sig_yt = 40e3)
mat_v = EqConcreteTruss(E=20e6, A=0.03, sig_yc=200e3, sig_yt = 40e3)
mat_d = EqConcreteTruss(E=20e6, A=0.03, sig_yc=200e3, sig_yt = 40e3)

dom.elems.sub(tag='h').set_elem_model(mat_h)
dom.elems.sub(tag='v').set_elem_model(mat_v)
dom.elems.sub(tag='d').set_elem_model(mat_d)

#Setting solver 
solver = SolverEq(domain=dom, scheme="NR", nincs=2)
solver.set_precision(1e-3)
t_elem = dom.elems[3]
solver.track(t_elem)
solver.set_track_per_inc(True)


# Stage 1
# ====================================================

#Setting boundary conditions
dom.nodes.sub(x=0).set_bc(ux=0, uy=0)
dom.nodes.sub(x=L).set_bc(ux=0, uy=0)
dom.nodes.sub(x=L/2., y=H).set_bc(fy=-6000.*10)

solver.solve()
solver.write_output()

# Stage 2
# ====================================================

dom.nodes.sub(x=0).set_bc(ux=0, uy=0)
dom.nodes.sub(x=L).set_bc(ux=0, uy=0)
dom.nodes.sub(x=L/2., y=H).set_bc(fy=-500.)

solver.solve()
solver.write_output()

# Stage 3
# ====================================================

dom.nodes.sub(x=0).set_bc(ux=0, uy=0)
dom.nodes.sub(x=L).set_bc(ux=0, uy=0)
dom.nodes.sub(x=L/2., y=H).set_bc(fy=-500.)

solver.solve()
solver.write_output()

# Stage 4
# ====================================================

dom.nodes.sub(x=0).set_bc(ux=0, uy=0)
dom.nodes.sub(x=L).set_bc(ux=0, uy=0)
dom.nodes.sub(x=L/2., y=H).set_bc(fy=-500.)

solver.solve()
solver.write_output()

# ====================================================



