from numpy import zeros, where, newaxis

omega = zeros(10)

w_1 = zeros((10, 5))
w_2 = where(omega < 1., 0., 1.)

result = w_1 * w_2[:, newaxis]
