# I've found it from this page:
# http://news.ycombinator.com/item?id=1207132


from math import *

def loose_label(min,maxv):
    
    ntick = 5

    range = nicenum(maxv-min,False)
    d = nicenum(range/(ntick-1),True)
    graphmin = floor(min/d)*d
    graphmax = ceil(maxv/d)*d
    nfrac = max(-floor(log10(d)),0)

    labels = list()
    x = graphmin
    #while x <= (graphmax + .5 * d): # this is original
    while x < graphmax:
        labels.append(x)
        x += d

    return map(int,labels)



def nicenum(x,round):
    exp = floor(log10(x))
    f = float(x)/pow(10,exp)
    if round:
        if f < 1.5: nf = 1.
        elif f < 3.: nf = 2.
        elif f < 7.: nf = 5.
        else: nf = 10.
    else:
        if f <= 1. : nf = 1.
        elif f <= 2. : nf = 2.
        elif f <= 5. : nf = 5.
        else: nf = 10.

    return nf*pow(10,exp)




