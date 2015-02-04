# http://rosettacode.org/wiki/Reduced_row_echelon_form#Python
def toReducedRowEchelonForm(m):
    lead = 0
    rowCount = len(m)
    columnCount = len(m[0])
    for r in range(rowCount):
        if lead >= columnCount:
            return
        i = r
        while m[i][lead] == 0:
            i += 1
            if i == rowCount:
                i = r
                lead += 1
                if columnCount == lead:
                    return
        m[i], m[r] = m[r], m[i]
        lv = m[r][lead]
        m[r] = [mrx / float(lv) for mrx in m[r]]
        for i in range(rowCount):
            if i != r:
                lv = m[i][lead]
                m[i] = [iv - lv * rv for rv, iv in zip(m[r], m[i])]
        lead += 1

'''m = []
m.append([-2, 0, 0, -3, 0, -3, 0, -2,  -2, 0.3042558307285405])
m.append([0, -3, -3, 0, 0, 0, -3, 0, -2, 0.01532740794485761])
m.append([-2, -3, 0, 0, -3, 0, -3, 0, -2, -0.19278656920234558])
m.append([0, 0, -3, 0, 0, -3, -3, 0, 0, -0.20293724966622162])
m.append([-2, 0, 0, -3, -3, 0, -3, -2, 0, -0.8125151392813887])
m.append([-2, 0, -3, 0, -3, 0, -3, 0, 0, 0.6866932422171602])
m.append([-2, 0, -3, 0, 0, -3, 0, 0, 0, -0.44348726639363556])
m.append([-2, 0, -3, -3, 0, 0, -3, 0, 0, -0.5290150221171112])
m.append([0, -3, 0, 0, -3, -3, 0, 0, 0, -0.11499411739073598])

toReducedRowEchelonForm(m)

result_row = []

for element in m:
    result_row.append(element[-1])
print(result_row)'''