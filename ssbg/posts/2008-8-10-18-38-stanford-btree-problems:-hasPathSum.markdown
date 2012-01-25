I decided to go through some of the [Stanford Btree problems](http://cslibrary.stanford.edu/110/BinaryTrees.html). Today I wrote a solution to the hasPathSum problem and part of the printPaths problem in SML. My solution will take a binary tree and return a list of all the paths that will sum to the given sum. A path starts at the root and ends at the descendant whose integer value adds to the sum.

    :::OCaml
    datatype itree = Node of itree * int * itree
            | Leaf
     
    val mytree = Node(
            Node(
             Node(
       Node(Leaf,~3,Leaf),
       2,
       Node(Leaf,12,Leaf)),
      4,
      Leaf),
            1,
            Node(Node(Leaf,15,Leaf),
          3,
          Leaf))
     
    (*
     -should handle positive/negative weights
     -should find all paths in the tree that are equal to this sum
    *)
    fun hasPathSum root sum =
        let
          fun search (Node(left,i,right)) path accum all_paths =
       let
         val new_path = (i::path)
         val new_accum = (accum + i)
         val get_left_paths = search (left) (new_path) (new_accum)
         val get_right_paths = search (right) (new_path) (new_accum)
         val new_all_paths = if sum = new_accum then 
          ((rev new_path)::all_paths)
        else
          all_paths
       in
         get_right_paths (get_left_paths new_all_paths)
       end
     | search (Leaf) (_) (_) (all_paths) = all_paths
        in
          search (root) ([]) (0) ([])
        end
     
    hasPathSum (mytree) (4) (*result: [[1,3], [1, 4, 2, ~3]] *)
    hasPathSum (mytree) (1) (*result: [[1]]*)
    hasPathSum (mytree) (1024) (*result: [] *)

