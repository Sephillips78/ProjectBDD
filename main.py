#Sebastian Phillips
#11855929
#Cpts 350
#Project BDD





from testFunctions import *

bddtrue = expr2bdd(expr(True))
bddfalse = expr2bdd(expr(False))

x = bddvars('x', 5)
y = bddvars('y', 5)





#EVEN number BDD

#Even when LSB is 0
EVEN = ~y[0] 







#PRIME number BDD

#Each prime number added individually
PRIME = (
    (~x[4]) & (~x[3]) & (~x[2]) & x[1] & x[0]  # 3 (00011)
) | (
    (~x[4]) & (~x[3]) & x[2] & (~x[1]) & x[0]  # 5 (00101)
) | (
    (~x[4]) & (~x[3]) & x[2] & x[1] & x[0]  # 7 (00111)
) | (
    (~x[4]) & x[3] & (~x[2]) & x[1] & x[0]  # 11 (01011)
) | (
    (~x[4]) & x[3] & x[2] & (~x[1]) & x[0]  # 13 (01101)
) | (
    x[4] & (~x[3]) & (~x[2]) & (~x[1]) & x[0]  # 17 (10001)
) | (
    x[4] & (~x[3]) & (~x[2]) & x[1] & x[0]  # 19 (10011)
) | (
    x[4] & (~x[3]) & x[2] & x[1] & x[0]  # 23 (10111)
) | (
    x[4] & x[3] & x[2] & (~x[1]) & x[0]  # 29 (11101)
) | (
    x[4] & x[3] & x[2] & x[1] & x[0]  # 31 (11111)
)








#RR BDD


RR = bddfalse

for u in range(32): #for each node


    v1 = (u + 3) % 32 #reachability conditions
    v2 = (u + 8) % 32

    u_bits = int_to_bits(u) #translate to binary

    for v in [v1, v2]: #for each hypothetical step 3 or 8
        
        
        v_bits = int_to_bits(v) 

        temp = bddtrue # initialization reachability of current node

        for i in range(5):
            temp &= ~x[i] if u_bits[i] == 0 else x[i] 
            temp &= ~y[i] if v_bits[i] == 0 else y[i]
        
        RR |= temp #adding reachability of current node to RR







#RR2 BDD


z = bddvars ('z', 5) #temporary node for 2 step BDD

RR_xz = RR.compose({y[i]: z[i] for i in range(5)}) #create bdd on RR replacing y with z
RR_zy = RR.compose({x[i]: z[i] for i in range(5)}) #create bdd on RR replacing x with z

RR2 = (RR_xz & RR_zy).smoothing(set(z)) #merge the two bdds while removing the temporary node z








#RR2star BDD

RR2star = RR2 #start with 2

while True:

    RR2_xz = RR2star.compose({y[i]: z[i] for i in range(5)}) #create bdd on RR2 replacing y with z

    RR2_zy = RR2.compose({x[i]: z[i] for i in range(5)}) #create bdd on RR2 replacing x with z

    temp = RR2star | (RR2_xz & RR2_zy).smoothing(set(z)) #merge the two bdds while removing the temporary node z


    if temp.equivalent(RR2star): #If the reachability of the current step is the same as all previous reachabilities ...
        break                       #... then there are no more nodes that can be reached

    RR2star = temp #update RR2star








#statementA BDD


v_exists = (EVEN & RR2star).smoothing(y) #all even numbers reachable in even number of steps (v)

u_exists = (~PRIME) | v_exists #Prime implies v exists

statementA = u_exists.smoothing(x).is_one() #For all prime numbers



run_tests()
print("statement A is ", statementA)
