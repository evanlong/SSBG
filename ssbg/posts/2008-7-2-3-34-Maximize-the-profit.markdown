I decided to title these entries with something more related to the title. Here's today's problem:

>Given a matrix of profit where each row represents a worker and each column represents a job maximize the profit by assigning each worker to a specific job. It is only one employee per job and one job per employee. Even if each each could make $1000 dollars on job 1 they all could not be tasked with job 1. Each job will be assigned exactly ONCE and each employee will be assigned exactly ONCE. The matrix will be NxN. The entries will be positive integers. You must return the assignment in some reasonable form. For example this string: "0->1, 1->2, 2->0" would indicate that employee 0 is doing job 1 and employee 1 is doing job 2...</blockquote>To solve this I will use a recursive dynamic programming solution which would take O(n!) time but since this problems has LOTS of overlapping subproblems my memoization decorator can be used in this problem.

The idea behind the recursive solution is something like this:

![profit](http://www.codecogs.com/eq.latex?profit%28w,&space;jobId%29&space;=&space;max%5Cleft%5C%7B%5Cbegin%7Bmatrix%7D&space;costOf%28w_1,jobId%29&space;+&space;profit%28w-w_1,jobId+1%29%5C%5C&space;&space;costOf%28w_2,jobId%29&space;+&space;profit%28w-w_2,jobId+1%29%5C%5C&space;...%5C%5C&space;costOf%28w_n,jobId%29&space;+&space;profit%28w-w_n,jobId+1%29&space;&space;%5Cend%7Bmatrix%7D%5Cright)

* w is a list of workers
* w (subscript) i is the ith element in w
* w-w (subscript) n indicates removal of that element from the list
* The costOf function is the cost of assigning a worked to a specific jobId. It ends up being a lookup in the matrix in my case

At each point we enumerate all possible job assignments a worker (A) may have and then enumerate all the job assignments their coworkers may have as a result of assigning worker (A) to each of those jobs. We end up doing this until we run out of possible assignments. This ends up being a brute force approach but just like fibonacci we can draw out the recursive calls that take place and see that there will end up being a LOT of overlapping recursive calls. That is, recursive calls to the *profit* function end up calling it with the same parameters over and over again. We can use memoization to speed things up quite a bit. That's what I do in this case.

Here is the code that I attempted to explain above. Good luck. It's not easy. But try banging your head against it for a while. There are also other ways to solve this problem. Some of them a lot faster because my solution uses a lot of recursion. I'll provide a list of other possible ways to solve it at the bottom.

    #my modified memoization function to support list hashing (its a hack)
    def mem(fn):
        mem = {}
        def mod(*args):
            arg_list = []
            for a in args:
                try:
                    arg_list.append(tuple(a))
                except:
                    arg_list.append(a)
            key = hash(tuple(arg_list))
            if mem.has_key(key):
                return mem[key]
            else:
                val = fn(*args)
                mem[key] = val
                return val
        return mod
     
    def profitimize(matrix):
        plist = range(len(matrix))
        def costMapping(m):
            tmp = 0
            for k in m:
                tmp += matrix[k][m[k]]
            return tmp
        
        @mem
        def profit(people, jobId):
            if len(people) == 0:
                return {}
     
            currCost = 0
            mapping = {}
            bestPerson = -1
            for person in people:
                indyCost = matrix[person][jobId]
                newPeople = list(people)
                newPeople.remove(person)
                result = dict(profit(newPeople, jobId+1))
                indyCost += costMapping(result)
                if currCost < indyCost:
                    currCost = indyCost
                    mapping = result
                    bestPerson = person
            mapping[bestPerson] = jobId
            
            return mapping
        return profit(plist, 0)
     
    if __name__ == '__main__':
        matrix4 = [[10,40,30,20],[20,30,20,10],[30,20,10,40],[40,10,40,30]]
        matrix7 = [[10,40,30,20,50,90,64],
                   [20,30,20,10,50,9,23],
                   [30,20,10,40,50,12,23],
                   [40,10,40,30,50,60,73],
                   [40,10,40,10,50,50,12],
                   [40,10,40,10,50,1,65],
                   [40,10,40,10,50,1,12]]
        matrix10 = [[10,40,30,20,1,50,12,60,13,25],
                   [20,30,20,10,6,12,64,24,63,12],
                   [30,20,10,40,6,75,23,86,12,45],
                   [40,10,40,30,1,36,12,64,12,53],
                   [40,10,40,30,1,36,12,64,12,53],
                   [40,10,40,30,1,36,12,64,12,53],
                   [40,10,40,30,1,36,12,64,12,53],
                   [40,10,40,30,1,36,12,64,12,53],
                   [40,10,40,30,1,36,12,64,12,53],
                   [40,10,40,30,1,36,12,64,12,53]]
        matrix10_2 = [[1,2,3,4,5,6,7,8,9,10],
                      [10,1,2,3,4,5,6,7,8,9],
                      [9,10,1,2,3,4,5,6,7,8],
                      [8,9,10,1,2,3,4,5,6,7],
                      [7,8,9,10,1,2,3,4,5,6],
                      [6,7,8,9,10,1,2,3,4,5],
                      [5,6,7,8,9,10,1,2,3,4],
                      [4,5,6,7,8,9,10,1,2,3],
                      [3,4,5,6,7,8,9,10,1,2],
                      [2,3,4,5,6,7,8,9,10,1]]
        matrix2 = [[10,20],[10,1]]
        result = profitimize(matrix10_2)
        print result

Couple of other techniques:
* <http://en.wikipedia.org/wiki/Hungarian_algorithm>
* <http://en.wikipedia.org/wiki/Matching>


