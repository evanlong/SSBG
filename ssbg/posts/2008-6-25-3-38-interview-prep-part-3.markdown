I have been asked to do basic string problems before. The problem for today:

>Given a string, print out each character that appears, the number of times that it appears and it must be done in the order the characters appear in the original string. And it must be done in O(n) time.

    :::python
    def do(s):
       seenMap = {}
       orderList = []
      
       for c in s:
           if not seenMap.has_key(c):
               orderList.append(c)
               seenMap[c] = 0
           seenMap[c] += 1
      
       for c in orderList:
           print c, str(seenMap[c])

The important thing here is to do it in O(n) time. It is easy to get trapped and do this in polynomial time. The trick here is to use a list to store the order that characters appear and to use a dictionary to keep track of if a character has been seen and how many times it has been seen. Provided that the has_key function has O(1) running time my algorithm is O(n).
