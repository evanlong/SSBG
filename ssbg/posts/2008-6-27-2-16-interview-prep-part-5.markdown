The problem today is to find "dead" nodes in a graph. This sort of algorithm could be applied to all sorts of things such as eliminating the unreachable states in a DFA or unreachable code in a compiler. 

    :::python
    class State:
        def __init__(self, id):
            self.id = id
            self.outs = []
            self.visited = False
        
        def __repr__(self):
            return str(self.id)
     
    def dead(begins, all):
        def search(state):
            if state.visited:
                return
            state.visited = True
            for s in state.outs:
                search(s)
     
        for s in begins:
            search(s)
            
        removable = []
        
        for s in all:
            if not s.visited:
                removable.append(s);
        return removable
     
     
    if __name__ == "__main__":
        ss = []
        for i in range(6):
            ss.append(State(i))
        ss[0].outs = [ss[5]]
        ss[1].outs = [ss[3],ss[2]]
        ss[2].outs = [ss[1]]
        ss[3].outs = [ss[2],ss[4]]
        ss[4].outs = []
        ss[5].outs = []
        print dead([ss[1]], ss)
        for s in ss:
            s.visited = False
        print dead([ss[0]], ss)
        for s in ss:
            s.visited = False
        print dead([ss[0],ss[1]], ss)
