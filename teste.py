import numpy as np
import matplotlib.pyplot as plt

def candidatofun(x,epsilon):
  candidato = np.random.uniform(low = x-epsilon, high = x +epsilon)
  return candidato


def hill_climbing_algorithm(f, candidato, x0, epsilon, max_it, max_n):
    x_best = x0

    f_best = f(x_best[0], x_best[1])
    i = 0
    improvement = True
    while i < max_it and improvement:
        j = 0
        improvement = False
        while j < max_n:
            y = candidato(x_best,epsilon)
            F = f(y[0],y[1])
            if F < f_best:
                improvement = True
                x_best = y
                f_best = F
                break
            j += 1
        i += 1
    return x_best


def hill_climbing_algorithm_max(f, candidato, x0, epsilon, max_it, max_n):
    x_best = x0

    f_best = f(x_best[0], x_best[1])
    i = 0
    improvement = True
    while i < max_it and improvement:
        j = 0
        improvement = False
        while j < max_n:
            y = candidato(x_best,epsilon)
            F = f(y[0],y[1])
            if F > f_best:
                improvement = True
                x_best = y
                f_best = F
                break
            j += 1
        i += 1
    return x_best






def f7(x1, x2):
    term1 = -np.sin(x1) * np.sin((x1**2 / np.pi))**(2 * 10)
    term2 = -np.sin(x2) * np.sin((2 * x2**2 / np.pi))**(2 * 10)
    return term1 + term2


x1 = np.linspace(0,np.pi,1000)


X1 , X2 = np.meshgrid (x1 , x1 )
Y = f7(X1 , X2)

i=0
fig = plt.figure ()
ax = fig.add_subplot( projection ='3d')
while i < 100:
  result = hill_climbing_algorithm(f7,candidatofun,np.array([0.5,0.5]),0.5,200,10)
  #print(result)
  x1_cand = result[0]
  x2_cand = result[1]
  f_cand = f7( x1_cand , x2_cand )
  ax.scatter( x1_cand , x2_cand , f_cand , marker ='x',s =90 , linewidth =3 , color ='red')
  i+=1
  
ax.plot_surface( X1 ,X2 ,Y , rstride =10 , cstride =10 , alpha =0.6 , cmap ="jet" )

ax.set_xlabel ('x')
ax.set_ylabel ('y')
ax.set_zlabel ('z')
ax.set_title ('f(x1 ,x2)')
plt.tight_layout ()
plt.show ()