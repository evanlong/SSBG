Find the maximum sum of a subsequence in a list of positive and negative integer numbers and also provide the range over which it occurs. 

    :::python
    def maxsub(lst):
        sidx = 0
        eidx = 0
        currMax = 0
        currSum = 0
        for i in range(len(lst)):
            currSum += lst[i]
            if currSum > currMax:
                currMax = currSum
                eidx = i
            elif currSum < 0:
                currSum = 0
                sidx = i + 1
        return (currMax,sidx,eidx)
            
    if __name__ == "__main__":
        a = [1,2,3,-4,5]
        b = [1,-2,3,4,5,-4,5]
        c = [-1,-2,-3]
        print maxsub(a)
        print maxsub(b)
        print maxsub(c)
