import numpy as np

# generate normal variable 

# standard normal 
def generate_normal1(n):
    n = int(n/2)
    u1  = np.random.uniform(0,1,size = n)
    v = -np.log(1-u1) * 2
    u2 = np.random.uniform(0,1,size = n)
    w = u2 * 2 * np.pi
    x1 = np.sqrt(v) * np.cos(w)
    x2 = np.sqrt(v) * np.sin(w)
    result = np.append(x1,x2)
    return result

# normal with mu and sigma
def generate_normal2(n,mu,sigma):
    n = int(n/2)
    u1  = np.random.uniform(0,1,size = n)
    v = -np.log(1-u1) * 2
    u2 = np.random.uniform(0,1,size = n)
    w = u2 * 2 * np.pi
    x1 = mu + sigma *(np.sqrt(v) * np.cos(w))
    x2 = mu + sigma *(np.sqrt(v) * np.sin(w))
    result = np.append(x1,x2)
    return result

# possible odd n
def generate_normal3(n,mu,sigma):
    N = n
    n = int(n/2)
    u1  = np.random.uniform(0,1,size = n)
    v = -np.log(1-u1) * 2
    u2 = np.random.uniform(0,1,size = n)
    w = u2 * 2 * np.pi
    x1 = mu + sigma *(np.sqrt(v) * np.cos(w))
    x2 = mu + sigma *(np.sqrt(v) * np.sin(w))
    result = np.append(x1,x2)
    if N % 2 == 1:
        print("d")
        u1  = np.random.uniform(0,1,size = 1)
        v = -np.log(1-u1) * 2
        u2 = np.random.uniform(0,1,size = 1)
        w = u2 * 2 * np.pi
        x1 = mu + sigma *(np.sqrt(v) * np.cos(w))
        result = np.append(result, x1)
    return result

# generate 1 value
def generate_normal4(mu,sigma):
    u = np.random.uniform(0,1,size=2)
    v = -np.log(1-u[0]) * 2
    w = u[1] * 2 * np.pi
    x1 = mu + sigma *(np.sqrt(v) * np.cos(w))
    return x1