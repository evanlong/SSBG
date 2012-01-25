A lot of popular virtual machines are stack based. The instruction sets take their inputs from a stack and then place their outputs on the same stack. It's pretty simple at face value but the virtual machines end up doing a lot of fancy things behind the scenes to make the code run fast. 

Today I implement a REALLY REALLY BASIC stack based virtual machine that does basic math.

    :::python
    s = []
     
    def e(cmd):
        global s
        f={'add' : 's.append(s.pop()+s.pop())',
           'dup' : 's.append(s[-1])',
           'sub' : 's.append(s.pop()-s.pop())',
           'mul' : 's.append(s.pop()*s.pop())',
           'div' : 's.append(s.pop()/s.pop())',
           'peak' : 'print s[-1]',
           'out' : 'print s.pop()'
           }[cmd]
        exec(f)
     
    s.append(5)
    s.append(1)
    e('add')
    e('dup')
    s.append(12)
    e('mul')
    e('sub')
    e('peak')
    e('out')

The key of the dictionary is the instruction and the value defines what the instruction does.

