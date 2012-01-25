The reason I am doing this is to prep myself for interview's I plan/hope to have this fall. My past experience has been pretty bad when it comes to technical questions. I usually end up feeling completely stupid because I get a fairly simple question wrong. And when there are just 2 or 3 during a 45 minute interview my chances of getting another interview plummet. So the plan is that everyday this summer I will solve one technical problem that might arise during an interview. I will also try and provide a couple of different solutions to illustrate possible pitfalls. All solutions will be implemented in Python or C.

The first problem:
>Given a [binary tree](http://en.wikipedia.org/wiki/Binary_tree), determine if it is a valid [binary search tree](http://en.wikipedia.org/wiki/Binary_search_tree).

Wikipedia will do a better job of describing these two data structures. The task is to write some code that takes in a binary tree and returns true if it is a valid binary search tree and false otherwise.

To solve this problem I ended up doing an inorder traversal of the tree. This ends up being the best solution with O(n) complexity. So here it goes:

    :::python
    def checkValidBtree(tt):
        def inOrder(t,min):
           if t == None: return (True,min)
           valid,min = inOrder(t.left,min)
           if valid == False: return (False,min)
           if min == None:
               min = t.data
           elif min > t.data:
               return (False,min)
           min = t.data
           return inOrder(t.right,min)
    return inOrder(tt,None)[0]

The inner function ends up doing the bulk of the work. The 'min' parameter is used to keep track of the most recently seen value in the tree. It is important because it allows us to verify that the next value in the traversal is always larger than the previous one. As soon as this rule is violated we know that we have encountered a binary tree that is not a valid binary search tree.
