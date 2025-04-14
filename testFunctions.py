from bdd import x, y, EVEN, PRIME, RR, RR2
from functions import int_to_bits
from pyeda.inter import *



def test_rr(u, v):
    assign = {}
    u_bits = int_to_bits(u)
    v_bits = int_to_bits(v)
    for i in range(5):
        assign[x[i]] = u_bits[i]
        assign[y[i]] = v_bits[i]
    return RR.restrict(assign).is_one()



def test_rr2(u, v):
    assign = {}
    u_bits = int_to_bits(u)
    v_bits = int_to_bits(v)
    for i in range(5):
        assign[x[i]] = u_bits[i]
        assign[y[i]] = v_bits[i]
    return RR2.restrict(assign).is_one()



def run_tests():

    print("Does 27 have a path to 3", test_rr(27, 3))  
    print("Does 16 have a path to 20", test_rr(16, 20)) 

    print("Is 4 even?", EVEN.restrict({y[4]:0, y[3]:0, y[2]:1, y[1]:0, y[0]:0}).is_one())
    print("Is 13 even?", EVEN.restrict({y[4]:0, y[3]:1, y[2]:1, y[1]:0, y[0]:1}).is_one())

    print("Is 7 prime?", PRIME.restrict({x[4]:0, x[3]:0, x[2]:1, x[1]:1, x[0]:1}).is_one())
    print("Is 2 prime?", PRIME.restrict({x[4]:0, x[3]:0, x[2]:0, x[1]:1, x[0]:0}).is_one())

    print("Can 27 reach 6 in even steps?", test_rr2(27, 6))
    print("Can 27 reach 9 in even steps?", test_rr2(27, 9))   

    return
