from numpy import array, zeros, hstack
from numpy.linalg import norm

def Assemble_K_element(coord_start,coord_end,A,E):
  ΔV = coord_end-coord_start
  L = norm(ΔV)
  lx = ΔV[0]/L
  ly = ΔV[1]/L
  t = array([[ lx, ly, 0, 0],
             [ 0, 0, lx, ly]])
  P = E*A/L
  Kl =array([[ P, -P],
              [-P, P]])
  Ke = t.T@Kl@t
  return Ke

def Assemble_K_general(nodes,elements):
  N = len(nodes)*2
  K = zeros((N,N))
  F = zeros((N,1))
  for el in elements:
    coord_start = array([nodes[elements[el][0]][0],nodes[elements[el][0]][1]])
    coord_end = array([nodes[elements[el][1]][0],nodes[elements[el][1]][1]])
    Ke = Assemble_K_element(coord_start, coord_end, elements[el][2], elements[el][3])
    dof_e = hstack((array([nodes[elements[el][0]][2],nodes[elements[el][0]][3]]),array([nodes[elements[el][1]][2],nodes[elements[el][1]][3]])))
    for i in range(4):
      for j in range(4):
        a = dof_e[i]
        b = dof_e[j]
        K[a,b] = Ke[i,j] + K[a,b]
  return K, F

def load(F,constraints):
  for [node,constraint,value,x] in constraints:
    constraint = array(constraint)
    gl=array([x+1,x+2])*constraint
    gl = gl[gl!=0]-1
    F[gl] = F[gl] + value
  return F

def Fix(K,F,constraints):
  for joint in constraints:
    constraint = array([constraints[joint][0],constraints[joint][1]])
    gl=array([constraints[joint][2]+1,constraints[joint][2]+2])*constraint
    gl = gl[gl!=0]-1
    K[gl,:] = 0.0
    K[:,gl] = 0.0
    K[gl,gl] = 1.0
    F[gl] = 0
  return K,F
