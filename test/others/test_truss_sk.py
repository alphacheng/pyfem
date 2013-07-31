try: import sys; sys.path.insert(0, "c:\\Dropbox\\codes\\pyfem")
except: pass


# Teste de anaalise de trelicca usando Python e elementos finitso

# Importar as bibliotecas para trabalhar com elem. finitos

from pyfem.mesh import *
from pyfem.fem  import *
from pyfem.equilib import *

# Geracaoo da malha

malha = Mesh()
malha.load_file("mesh.vtk")

exit()

# Anaalise por elementos finitos

dom = Domain()  # Criacaoo do domiinio de elementos finitos
dom.load_mesh(malha)


# definicaoo dos tipos de elementos e suas propriedades
tipo_elem = EqElasticBar(E=100000.0, A=0.01)   # E em kN/m2=kPa    e     A em m2

dom.elems.set_elem_model(tipo_elem)

# cond de contorno de deslocamento
dom.nodes.with_x(0.0).with_y(0.0).set_brys(ux=0, uy=0)
dom.nodes.with_x(1.0).with_y(0.0).set_brys(uy=0)

# cond de contrno de forcca
dom.nodes.with_y(1.0).set_brys(fy=-10.0)


# Solucaoo

dom.set_solver( SolverEq() ) # definicaoo do solver so para equiliibrio
dom.solver.solve()
dom.solver.write_output()






