n, k = map(int, input().split())
def get_c(n, k):
    # print('n = '.format(n))
    # print('k = '.format(k))
    if k == 0:
        return 1
    elif k > n:
        return 0
    else:
        return get_c(n-1, k) + get_c(n-1, k-1)
print(get_c(n,k))
# test