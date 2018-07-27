from random import randint as ri

def get(v1, par):
    if par[v1] == v1:
        return v1
    ans = get(par[v1], par)
    par[v1] = ans
    return ans

def un(v1, v2, par, deep):
    v1 = get(v1, par)
    v2 = get(v2, par)
    if v1 == v2:
        return
    if deep[v1] > deep[v2]:
        v1, v2 = v2, v1
    par[v1] = v2
    if deep[v1] == deep[v2]:
        deep[v2] += 1

def gen(hor, ver, w, h):
    edge = []
    for i in range(w - 1):
        for j in range(h - 1):
            cur = i * h + j
            edge.append((ri(0, 100000000000), cur, cur + 1))
            edge.append((ri(0, 100000000000), cur, cur + h))
    par = [i for i in range(w * h)]
    deep = [0] * (w * h)
    edge.sort()
    for i in edge:
        v1 = i[1]
        v2 = i[2]
        if get(v1, par) != get(v2, par):
            r = v1 % h
            c = v1 // h
            if v2 - v1 == 1:
                ver[c][r] = True
            else:
                hor[r][c] = True
            un(v1, v2, par, deep)
