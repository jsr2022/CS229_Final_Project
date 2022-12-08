import numpy as np


def delta_pitch(pitch):
    n = len(pitch)
    deltas = np.zeros(n-1)
    for i in range(n-1):
        deltas[i] = pitch[i+1]-pitch[i]
    return deltas


def delta_volume(volume):
    volume = 1000*volume #scaling
    n = len(volume)
    deltas = np.zeros(n - 1)
    for i in range(n - 1):
        deltas[i] = np.abs(volume[i + 1] - volume[i])
    return deltas

#pitch min is defined to be 0. granularity is integer length of each pitch interval
def get_pitch_dist(pitch_deltas):
    num_ranges = int(pitch_max / pitch_granularity)
    weights = np.zeros(num_ranges)
    for i in range(num_ranges):
        interval_no = int(pitch_deltas[i]/pitch_granularity)
        weights[interval_no] += 1
    return weights

#volume min is defined to be 0. granularity is integer length of each volume interval
def get_vol_dist(vol_deltas, num_ranges, vol_max):
    vol_granularity = vol_max/num_ranges
    weights = np.zeros(num_ranges)
    for i in range(len(vol_deltas)):
        interval_no = int(vol_deltas[i]/vol_granularity)
        weights[interval_no] += 1
    return weights/len(vol_deltas)

#concatenates pitch distribution with volume distribution
def feature(song):
    dp = delta_pitch(p)
    dv = delta_volume(v)
    pitch_dist = get_pitch_dist(dp)
    vol_dist = get_vol_dist(dv)
    phi_x = np.concatenate((pitch_dist, vol_dist))
    return phi_x


def monomialize_single(x):
    l = x.shape[0]
    monomials = np.zeros(l * l)
    for i in range(l):
        for j in range(l):
            monomials[i * l + j] = x[i] * x[j]
    return monomials

def monomializer(x):
    l = x[0].shape[0]
    x_prime = np.zeros((x.shape[0], l*l))
    for k in range(x.shape[0]):
        monomials = np.zeros(l*l)
        for i in range(l):
            for j in range(l):
                monomials[i*l + j] = x[k][i]*x[k][j]
        x_prime[k] = monomials
    return x_prime


def poly_regression(x, y, learning_rate):
    x = np.append(np.ones((x.shape[0], 1)), x, axis=1)
    x = monomializer(x)
    theta_0 = np.zeros(len(x[0]))
    s = np.zeros(len(x[0]))
    for k in range(x.shape[0]):
        s += (y[k] - np.dot(theta_0, x[k])) * x[k]
    theta_1 = theta_0 + learning_rate * s
    i = 0
    while True:
        i += 1
        theta_0 = theta_1
        s = np.zeros(len(x[0]))
        for j in range(x.shape[0]):
            s += (y[j] - np.dot(theta_0, x[j])) * x[j]
        theta_1 = theta_0 + learning_rate * s
        #if i % 5 == 0:
            #print(np.linalg.norm(theta_1 - theta_0))
        if np.linalg.norm(theta_1 - theta_0) < 1e-2:
            break
    return theta_1


def linear_regression(x, y, learning_rate):
    #don't forget to add intercept term!
    x = np.append(np.ones((x.shape[0], 1)), x, axis=1)
    theta_0 = np.zeros(len(x[0]))
    s = np.zeros(len(x[0]))
    for k in range(x.shape[0]):
        s += (y[k]-np.dot(theta_0, x[k]))*x[k]
    theta_1 = theta_0 + learning_rate*s
    i=0
    while True:
        i+=1
        theta_0 = theta_1
        s = np.zeros(len(x[0]))
        for j in range(x.shape[0]):
            s += (y[j] - np.dot(theta_0, x[j])) * x[j]
        theta_1 = theta_0 + learning_rate * s
        #if i % 5 == 0:
            #print(np.linalg.norm(theta_1-theta_0))
        if np.linalg.norm(theta_1-theta_0) < 1e-2:
            break
    return theta_1
