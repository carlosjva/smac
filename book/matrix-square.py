# matrix-square.py

# Copyright (C) 2020 Greenweaves Software Limited

# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with GNU Emacs.  If not, see <http://www.gnu.org/licenses/>.

# Exercise 3.4: implement Alg 3.3, matrix-square

import math,matplotlib.pyplot as plt,numpy as np,os
from matplotlib import rc

phi_helper = {}
V          = {}


@np.vectorize
def trotter(i,j):
   return V[abs(i)] * phi_helper[abs(i-j)] * V[abs(j)]

if __name__=='__main__':
   import argparse
      
   parser = argparse.ArgumentParser('Exercise 3.4: calculate density matrix by matrix squaring')
   parser.add_argument('--beta',   default=0.1, type=float,                      help='Inverse temperature')
   parser.add_argument('--h',      default=1,   type=float,                      help='Planck\'s constant')
   parser.add_argument('-m','--m', default=1.0, type=float,                      help='Mass of particle')
   parser.add_argument('--omega',  default=1.0, type=float,                      help='Frequency')
   parser.add_argument('--n',      default=100, type=int,                        help='Number of steps')
   parser.add_argument('--L',      default=5,   type=float,                      help='Length')
   parser.add_argument('--show',                            action='store_true', help='Show plot')
   parser.add_argument('--rows',   default=4,   type=int,                        help='Number of rows to plot')
   parser.add_argument('--cols',   default=4,   type=int,                        help='Number of columns to plot')
   
   args     = parser.parse_args() 

   beta     = args.beta  
   step     = args.L / args.n
   phi_mult = math.sqrt(args.m/(2*math.pi*args.h*args.h*beta))
   grid_i   = [i for i in range(-args.n,args.n+1)]
   I,J      = np.meshgrid(grid_i,grid_i)
   grid_x   = [i * step for i in range(-args.n,args.n+1)]
   X,Y      = np.meshgrid(grid_x,grid_x)
   
   for i in range(-args.n,args.n+1):
      for j in range(i,args.n+1):
         if not (j-i) in phi_helper:
            phi_helper[(j-i)] = phi_mult * math.exp(- (args.m * (step*(i-j))**2)/(2 * args.h**2 * beta))
            
   for i in range(args.n+1):
      V[i]= math.exp(-0.5 * beta * 0.5 * args.m * args.omega  **2 * (step * i)**2)
      
   rho = trotter(I,J)

   rc('font',**{'family':'serif','serif':['Palatino']})
   rc('text', usetex=True)
   plt.figure(figsize=(5,5))
   for i in range(args.rows*args.cols):
      plt.subplot(args.rows,args.cols,i+1)
      plt.pcolor(X,Y,rho)
      plt.colorbar()
      plt.title(r'$\rho(x,x^{{\prime}},{0:.4f})$'.format(beta))
      beta *= 2      
      rho  = np.dot(step,  np.dot(rho, rho))
   plt.savefig('{0}.png'.format(os.path.splitext(os.path.basename(__file__))[0]))    
   if args.show:
      plt.show()        
