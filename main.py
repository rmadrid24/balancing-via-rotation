import sys
from util import *

# function to convert sorted array to a balanced BST 
def sortedArrayToBST(arr):
  if not arr: 
    return None

  # find middle
  n = len(arr)
  mid = n // 2
    
  # make the middle element the root 
  root = Node(arr[mid])
  root.int = (arr[0], arr[n-1])

  # left subtree of root has all 
  # values <arr[mid] 
  root.left = sortedArrayToBST(arr[:mid])
      
  # right subtree of root has all  
  # values >arr[mid] 
  root.right = sortedArrayToBST(arr[mid+1:])
  
  if root.left is not None:
    root.left.parent = root
  
  if root.right is not None:
    root.right.parent = root
  
  return root

def rot(tree, x, y):
  if y < x:
    righRotate(tree, x, y)
  elif y > x:
    leftRotate(tree, x, y)

def preOrder(node): 
  if not node: 
    return
      
  print( + node.data, end = ' ') 
  preOrder(node.left) 
  preOrder(node.right)

def buildS(t):
  root_s = copyNode(t.root, None)
  tree_s = Tree(root_s)
  edges = getEdges(tree_s.root)
  for edge in edges:
    x = edge[0]
    y = edge[1]
    shouldRotate = edge[2]
    print(str(x.data) + " -> " + str(y.data) + " , rot probability: " + str(shouldRotate))
    if shouldRotate:
      # add flipCoin(0.5)
      if y.parent == x:
        rot(tree_s, x, y)
  
  return tree_s

# implementation of algorithm A1
def a1(S, n, T):
  root_t = computeRoot(n)
  print("Root t " + str(root_t))

if __name__=="__main__":
  n = int(sys.argv[1])
  print("Starting trees with " + str(n) + " nodes")
  arr = [x for x in range(1, n + 1)]
  root_t = sortedArrayToBST(arr)
  t = Tree(root_t)
  s = buildS(t)
  print("Print t")
  preOrder(t.root)
  print("")
  print("Print s")
  preOrder(s.root)

  print("")
  a1(s, n, t)
