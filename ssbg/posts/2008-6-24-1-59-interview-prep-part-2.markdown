This might be a pretty common interview question. I personally have never been asked it but it seems like a reasonable technical question. The problem today:

>Reverse a linked list in C. The function should have the following function signature: `node_t* rev(node_t* n);`.

I will provide an iterative solution, and a recursive solution. I came up with the iterative solution all by myself. The technique I used for the recursive solution is based off the one from the [Stanford linked list page](http://cslibrary.stanford.edu/103/) However, when I solved it today I did it from memory. I first saw their method of solving it about a year ago and liked it. The first time I tried reversing a linked list in C recursively was pretty ugly ordeal. It took multiple parameters. It had a wrapper function for something that did the work and probably had a special case for the first element to make sure it pointed at null. Bad in every way. But I learned from a better method.

Here is the iterative solution:

    :::c
    node_t* rev(node_t* n)
    {
        if(n == NULL || n->next == NULL) return n;
         
        node_t* a = NULL;
        node_t* b = n;
        node_t* c = n->next;
         
        while(c != NULL) {
          b->next = a;
          a = b;
          b = c;
          c = c->next;
        }
        b->next = a;
         
        return b;
    }

The idea here is to walk down the list and point the 'next' at the previous element. This is what reverses the list. The trick is to have 'c' keep track of the list. Once 'b->next' points to 'a' we would lose the rest of the list if we did not have 'c' holding onto it.

Now for the recursive solution:

    :::c
    node_t* rrev(node_t* n)
    {
        if(n == NULL || n->next == NULL) return n;
         
        node_t* a = n;
        node_t* b = n->next;
        node_t* rr = rrev(n->next);
        a->next = b->next; //brings the NULL along to the front
        b->next = a;
        return rr;
    }

I drew my picture of the linked list and wrote the code. You should **always** draw a picture when dealing with data structures. It saves a lot of time and you usually end up getting the code correct the first time. The main idea behind this code is to first find the end of the list. The end of the list ends up being the 'rr' variable in this example. Then as the functions return the actual reversing takes place. This is difficult to explain. The best thing to do is to draw a picture of the operations taking place. That's the way I really understood it the first time. And it's how I build it from scratch whenever I need a little puzzle to solve. Just understand that the the reversing takes place on the way back up the call stack.

