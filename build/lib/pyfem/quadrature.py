from tools.matvec import *
from numpy import array

# LIN 2
LIN_IP2 = array([\
[  -0.577350269189625764509149e+00, 0.0, 0.0, 1.0 ], \
[   0.577350269189625764509149e+00, 0.0, 0.0, 1.0 ]])

# LIN 3
LIN_IP3 = array([\
[ -0.774596669241483377035835e+00, 0.0, 0.0, 0.555555555555555555555556e+00  ], \
[  0.000000000000000000000000e+00, 0.0, 0.0, 0.888888888888888888888889e+00  ], \
[  0.774596669241483377035835e+00, 0.0, 0.0, 0.555555555555555555555556e+00  ]])

# LIN_IP4
LIN_IP4 = array([\
[ -0.861136311594052575223946e+00, 0.0, 0.0, 0.34785484513745385737306e+00 ], \
[ -0.339981043584856264802666e+00, 0.0, 0.0, 0.65214515486254614262694e+00 ], \
[  0.339981043584856264802666e+00, 0.0, 0.0, 0.65214515486254614262694e+00 ], \
[  0.861136311594052575223946e+00, 0.0, 0.0, 0.34785484513745385737306e+00 ]])

# TRI_IP1
TRI_IP1 = array([[  1.0/3.0,  1.0/3.0,  0.0,  1.0/2.0 ]])

# TRI_IP3
TRI_IP3 = array([\
[  1.0/6.0,   1.0/6.0,   0.0,   1.0/6.0 ], \
[  2.0/3.0,   1.0/6.0,   0.0,   1.0/6.0 ], \
[  1.0/6.0,   2.0/3.0,   0.0,   1.0/6.0 ]])

# TRI_IP4
TRI_IP4 = array([\
[ 1.0/3.0,   1.0/3.0,   0.0,   -27.0/96.0 ], \
[ 1.0/5.0,   1.0/5.0,   0.0,    25.0/96.0 ], \
[ 3.0/5.0,   1.0/5.0,   0.0,    25.0/96.0 ], \
[ 1.0/5.0,   3.0/5.0,   0.0,    25.0/96.0 ]])

# TRI_IP6
TRI_IP6 = array([\
[   0.091576213509771,   0.091576213509771,    0.0,    0.109951743655322/2.0 ], \
[   0.816847572980459,   0.091576213509771,    0.0,    0.109951743655322/2.0 ], \
[   0.091576213509771,   0.816847572980459,    0.0,    0.109951743655322/2.0 ], \
[   0.445948490915965,   0.445948490915965,    0.0,    0.223381589678011/2.0 ], \
[   0.108103018168070,   0.445948490915965,    0.0,    0.223381589678011/2.0 ], \
[   0.445948490915965,   0.108103018168070,    0.0,    0.223381589678011/2.0 ]])

# QUAD 1x1
QUAD_IP1 = array([\
[     0.000000000000000,     0.000000000000000,     0.000000000000000,     4.000000000000000 ]])

# QUAD 2x2
QUAD_IP2 = array([\
[    -0.577350269189626,    -0.577350269189626,     0.000000000000000,     1.000000000000000  ], \
[     0.577350269189626,    -0.577350269189626,     0.000000000000000,     1.000000000000000  ], \
[    -0.577350269189626,     0.577350269189626,     0.000000000000000,     1.000000000000000  ], \
[     0.577350269189626,     0.577350269189626,     0.000000000000000,     1.000000000000000 ]])

# QUAD 3x3
__02r15 = 0.2*15.0**0.5
__25d81 = 25.0/81.0
__40d81 = 40.0/81.0
__64d81 = 64.0/81.0
QUAD_IP3 =  array([\
[  -__02r15 , -__02r15 , 0.0 , __25d81 ], \
[       0.0 , -__02r15 , 0.0 , __40d81 ], \
[   __02r15 , -__02r15 , 0.0 , __25d81 ], \
[  -__02r15 ,      0.0 , 0.0 , __40d81 ], \
[       0.0 ,      0.0 , 0.0 , __64d81 ], \
[   __02r15 ,      0.0 , 0.0 , __40d81 ], \
[  -__02r15 ,  __02r15 , 0.0 , __25d81 ], \
[       0.0 ,  __02r15 , 0.0 , __40d81 ], \
[   __02r15 ,  __02r15 , 0.0 , __25d81 ]])

# HEX 2x2x2
HEX_IP2 = array([\
[    -0.577350269189626,    -0.577350269189626,    -0.577350269189626,     1.000000000000000  ], \
[     0.577350269189626,    -0.577350269189626,    -0.577350269189626,     1.000000000000000  ], \
[    -0.577350269189626,     0.577350269189626,    -0.577350269189626,     1.000000000000000  ], \
[     0.577350269189626,     0.577350269189626,    -0.577350269189626,     1.000000000000000  ], \
[    -0.577350269189626,    -0.577350269189626,     0.577350269189626,     1.000000000000000  ], \
[     0.577350269189626,    -0.577350269189626,     0.577350269189626,     1.000000000000000  ], \
[    -0.577350269189626,     0.577350269189626,     0.577350269189626,     1.000000000000000  ], \
[     0.577350269189626,     0.577350269189626,     0.577350269189626,     1.000000000000000  ]])

# HEX 3x3x3
HEX_IP3 = array([\
[   -0.774596669241483,    -0.774596669241483,    -0.774596669241483,     0.171467764060357  ], \
[    0.000000000000000,    -0.774596669241483,    -0.774596669241483,     0.274348422496571  ], \
[    0.774596669241483,    -0.774596669241483,    -0.774596669241483,     0.171467764060357  ], \
[   -0.774596669241483,     0.000000000000000,    -0.774596669241483,     0.274348422496571  ], \
[    0.000000000000000,     0.000000000000000,    -0.774596669241483,     0.438957475994513  ], \
[    0.774596669241483,     0.000000000000000,    -0.774596669241483,     0.274348422496571  ], \
[   -0.774596669241483,     0.774596669241483,    -0.774596669241483,     0.171467764060357  ], \
[    0.000000000000000,     0.774596669241483,    -0.774596669241483,     0.274348422496571  ], \
[    0.774596669241483,     0.774596669241483,    -0.774596669241483,     0.171467764060357  ], \
[   -0.774596669241483,    -0.774596669241483,     0.000000000000000,     0.274348422496571  ], \
[    0.000000000000000,    -0.774596669241483,     0.000000000000000,     0.438957475994513  ], \
[    0.774596669241483,    -0.774596669241483,     0.000000000000000,     0.274348422496571  ], \
[   -0.774596669241483,     0.000000000000000,     0.000000000000000,     0.438957475994513  ], \
[    0.000000000000000,     0.000000000000000,     0.000000000000000,     0.702331961591221  ], \
[    0.774596669241483,     0.000000000000000,     0.000000000000000,     0.438957475994513  ], \
[   -0.774596669241483,     0.774596669241483,     0.000000000000000,     0.274348422496571  ], \
[    0.000000000000000,     0.774596669241483,     0.000000000000000,     0.438957475994513  ], \
[    0.774596669241483,     0.774596669241483,     0.000000000000000,     0.274348422496571  ], \
[   -0.774596669241483,    -0.774596669241483,     0.774596669241483,     0.171467764060357  ], \
[    0.000000000000000,    -0.774596669241483,     0.774596669241483,     0.274348422496571  ], \
[    0.774596669241483,    -0.774596669241483,     0.774596669241483,     0.171467764060357  ], \
[   -0.774596669241483,     0.000000000000000,     0.774596669241483,     0.274348422496571  ], \
[    0.000000000000000,     0.000000000000000,     0.774596669241483,     0.438957475994513  ], \
[    0.774596669241483,     0.000000000000000,     0.774596669241483,     0.274348422496571  ], \
[   -0.774596669241483,     0.774596669241483,     0.774596669241483,     0.171467764060357  ], \
[    0.000000000000000,     0.774596669241483,     0.774596669241483,     0.274348422496571  ], \
[    0.774596669241483,     0.774596669241483,     0.774596669241483,     0.171467764060357  ]])
