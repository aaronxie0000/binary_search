#!/bin/python3
'''
JOKE: There are 2 hard problems in computer science: cache
invalidation, naming things, and off-by-1 errors.

It's really easy to have off-by-1 errors in these problems.
Pay very close attention to your list indexes and your < vs <= operators.
'''


def find_smallest_positive(xs):
    '''
    Assume that xs is a list of numbers sorted from LOWEST to HIGHEST.
    Find the index of the smallest positive number.
    If no such index exists, return `None`.

    HINT:
    This is essentially the binary search algorithm from class,
    but you're always searching for 0.

    APPLICATION:
    This is a classic question for technical interviews.

    >>> find_smallest_positive([-3, -2, -1, 0, 1, 2, 3])
    4
    >>> find_smallest_positive([1, 2, 3])
    0
    >>> find_smallest_positive([-3, -2, -1]) is None
    True
    '''
    if len(xs) == 0:
        return None

    def go(left, right):
        if left == right:
            if xs[left] > 0:
                return left
            else:
                return None
        mid = (left + right) // 2
        if xs[mid] > 0:
            right = mid
        if xs[mid] <= 0:
            left = mid + 1
        return go(left, right)
    return go(0, len(xs) - 1)


def count_repeats(xs, x):
    '''
    Assume that xs is a list of numbers sorted from HIGHEST to LOWEST,
    and that x is a number.
    Calculate the number of times that x occurs in xs.

    HINT:
    Use the following three step procedure:
        1) use binary search to find the lowest index with a value >= x
        2) use binary search to find the lowest index with a value < x
        3) return the difference between step 1 and 2
    I highly recommend creating stand-alone functions for steps 1 and 2,
    and write your own doctests for these functions.
    Then, once you're sure these functions work independently,
    completing step 3 will be easy.

    APPLICATION:
    This is a classic question for technical interviews.

    >>> count_repeats([5, 4, 3, 3, 3, 3, 3, 3, 3, 2, 1], 3)
    7
    >>> count_repeats([3, 2, 1], 4)
    0
    '''
    if (len(xs) == 0):
        return 0
    min_index = find_larger(xs, x)
    if (min_index is None):
        return 0
    max_index = find_smaller(xs, x)
    return max_index - min_index


def find_smaller(xs, x):
    '''
    >>> find_smaller([12, 8, 8, 2, 2, 2], 2)
    6
    >>> find_smaller([12, 10, 8, 8, 8, 2, -1, -3], 8)
    5
    >>> find_smaller([1, 0, -1, -5, -10], -10)
    5
    >>> find_smaller([20, 10, 8, 7, 1, 1, 0, 0, 0], 1)
    6
    >>> find_smaller([1, 1, 1, 1, 1, 1, 1], 1)
    7
    '''

    def go(left, right):
        # base case
        if xs[left] < x and xs[left - 1] >= x:
            return left
        if xs[right] < x and xs[right - 1] >= x:
            return right
        if xs[right] == x and right == (len(xs) - 1):
            return len(xs)
        if left == right:
            return None
        # recursive
        mid = int((left + right) / 2)
        if xs[mid] >= x:
            left = mid
        if xs[mid] < x:
            right = mid
        return go(left, right)
    return go(0, len(xs) - 1)


def find_larger(xs, x):
    '''
    >>> find_larger([10, 5, 3, 1, 0],4) is None
    True
    >>> find_larger([12, 10, 8, 8, 8, 2, -1, -3], 8)
    2
    >>> find_larger([1, 0, -1, -5, -10], -10)
    4
    >>> find_larger([20, 10, 8, 7, 1, 1, 0, 0, 0], 1)
    4
    >>> find_larger([1, 1, 1, 1 ,1 , 1, 1], 1)
    0
    '''
    def go(left, right):
        # base case
        if xs[left] == x and xs[left - 1] > x:
            return left
        if xs[left] == x and left == 0:
            return left
        if xs[right] == x and xs[right - 1] > x:
            return right
        if left == right:
            return None
        # recursive
        mid = int((left + right) / 2)
        if xs[mid] <= x:
            right = mid
        if xs[mid] > x:
            left = mid + 1
        return go(left, right)
    return go(0, len(xs) - 1)


def argmin(f, lo, hi, epsilon=1e-3):
    '''
    Assumes that f is an input function that takes a float as input
    and returns a float with a unique global minimum,
    and that lo and hi are both floats satisfying lo < hi.
    Returns a number that is within epsilon of the value that minimizes
    f(x) over the interval [lo,hi]

    HINT:
    The basic algorithm is:
        1) The base case is when hi-lo < epsilon
        2) For each recursive call:
            a) select two points m1 and m2 that are between lo and hi
            b) one of the 4 points (lo,m1,m2,hi) must be the smallest;
               depending on which one is the smallest,
               you recursively call your function on the
               interval [lo,m2] or [m1,hi]

    APPLICATION:
    Essentially all data mining algorithms are just this argmin
    implementation in disguise.
    If you go on to take the data mining class (CS145/MATH166),
    we will spend a lot of time talking about different f functions
    that can be minimized and their applications.
    But the actual minimization code will all be a variant
    of this binary search.

    WARNING:
    The doctests below are not intended to pass on your code,
    and are only given so that you have an example of what the
    output should look like.
    Your output numbers are likely to be slightly different
    due to minor implementation details.
    Writing tests for code that uses floating point numbers is
    notoriously difficult.
    See the pytests for correct examples.

    >>> argmin(lambda x: (x-5)**2, -20, 20)
    5.000040370009773
    >>> argmin(lambda x: (x-5)**2, -20, 0)
    -0.00016935087808430278
    '''

    def go(lo, hi):
        # base case
        if (hi - lo) < epsilon:
            return hi
        # recursive case
        m1 = lo + (hi - lo) / 3
        m2 = lo + (hi - lo) / 3 * 2
        if f(m1) < f(m2):
            return go(lo, m2)
        if f(m2) < f(m1):
            return go(m1, hi)
    return go(lo, hi)

###############################################################
# the functions below are extra credit
#################################################################


def find_boundaries(f):
    '''
    Returns a tuple (lo,hi).
    If f is a convex function, then the minimum is guaranteed
    to be between lo and hi.
    This function is useful for initializing argmin.

    HINT:
    Begin with initial values lo=-1, hi=1.
    Let mid = (lo+hi)/2
    if f(lo) > f(mid):
        recurse with lo*=2
    elif f(hi) < f(mid):
        recurse with hi*=2
    else:
        you're done; return lo,hi
    '''


def argmin_simple(f, epsilon=1e-3):
    '''
    This function is like argmin, but it internally uses the
    find_boundaries function so that
    you do not need to specify lo and hi.

    NOTE:
    There is nothing to implement for this function.
    If you implement the find_boundaries function correctly,
    then this function will work correctly too.
    '''
    lo, hi = find_boundaries(f)
    return argmin(f, lo, hi, epsilon)
