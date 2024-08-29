# By ChatGPT
def findInterval(func, start, end, step):
    prevVal, prevF = start, func(start)
    for currentVal in range(int(start / step), int(end / step) + 1):
        currentVal = currentVal * step
        currentF = func(currentVal)
        if prevF * currentF < 0:
            return (prevVal, currentVal)
        prevVal, prevF = currentVal, currentF
    return None