Today is a two-for-one deal since I forgot to post anything yesterday.

>Write a Python decorator to add <http://en.wikipedia.org/wiki/Memoization> to any function.


Python decorators are very nice. Django uses them for users to specify which 
views require login and things of that nature. Decorators give the ability to 
modify how a function will behave. Now memoization is a technique that can be 
used to speed up a recursive solution to a dynamic programming problem. Today 
my example isn't really a dynamic programming problem (because I am a bit 
lazy) but will illustrate how much of a speed up you can get by using 
memoization.

    :::python
    import time
     
    def mem(fn):
      mem = {}
      def mod(*args,**kwargs):
          key = hash((args,tuple([(k,kwargs[k]) for k in kwargs])))
          if mem.has_key(key):
              return  mem[key]
          else:
              val = fn(*args,**kwargs)
              mem[key] = val
              return val
      return mod
     
    @mem
    def fib(n):
      if n == 1 or  n == 2:
          return 1
      else:
          return fib(n-1) + fib(n-2)
     
    t1 = time.time()
    fib(35)
    t2 = time.time()
     
    print t2-t1

With the @mem decorating the function it takes: 0.0002 seconds to compute fib(35). Without @mem it takes about 10 seconds. (Results may vary depending on your computer).

Now for the second part:

>You are on an alien world preparing for a potential invasion. The planet has some sort of [dampening field](http://www.memory-alpha.org/en/wiki/Dampening_field) covering it so you cannot use any sort of wireless communication. Your mission is to connect all the bases under your command with the least amount of wire. Every base must be able to communicate to every other base. A base will be able to communicate with any other base if a path exists between the two.

This can be solved by creating a minimum spanning tree.
    
    :::python
    bases = [
        #distance, #start base, #end base
        (5,0,1),
        (5,0,2),
        (2,0,5),
        (10,1,5),
        (30,1,2),
        (3,1,3),
        (6,1,4),
        (4,2,5),
        (6,2,3),
        (6,2,4),
        (7,3,5),
        (3,4,3)
    ]
     
    def wire(num_bases,data):
        base_to_set = {}
        connections = []
        data.sort()
        for i in range(num_bases):
            base_to_set[i] = set([i])
        cost = 0
        for entry in data:
            base1_set = base_to_set[entry[1]]
            base2_set = base_to_set[entry[2]]
            if len(base1_set.intersection(base2_set)) > 0:
                continue
            merge = base1_set.union(base2_set)
            for item_id in merge:
                base_to_set[item_id] = merge
            cost += entry[0]
            connections.append((entry[1],entry[2]))
            
        return (connections,cost)

The function takes in the number of bases and a list of tuples that contain the cost and two base ids indicating they are connected.
