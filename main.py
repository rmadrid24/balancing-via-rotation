import sys
from util import *

rotations = 0

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
  rotations += 1
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
    # print(str(x.data) + " -> " + str(y.data) + " , rot probability: " + str(shouldRotate))
    if shouldRotate:
      if flipCoin(0.5):
        if y.parent == x:
          rot(tree_s, x, y)
  
  return tree_s

# Guess how to form forearms. go to root.left and check if it has left child
# Rotate each left child in DFS style.
# Then move to right child

def buildLeftForearm(t):
  node = t.root.left
  while node is not None:
    y = node
    # keep rotating until no left childs
    while y is not None and y.left is not None:
      rot(t, y, y.left)
      y = y.parent
    node = y.right

def buildRightForearm(t):
  node = t.root.right
  while node is not None:
    y = node
    # keep rotating until no right childs
    while y is not None and y.right is not None:
      rot(t, y, y.right)
      y = y.parent
    node = y.left  

def al(q):
  n = q.root.int[1]
  h = getHeight(n)
  s = h - 1
  # if n >= pow(2, h-1) and n <= pow(2, h-1) + pow(2, h-2) + 2:
  #   k = n - pow(2, h-1) + 1
  #   for i in range(1, k+1):
  #     rot()
  #   s = h-1
  
  for j in range(s-1,0,-1):
    k = pow(2, j) - 1
    for i in range(1, k+1):
      rot(q, getNodeFromLeftForearm(q, i), getNodeFromLeftForearm(q, i+1))

def ar(q):
  n = q.root.int[1]
  h = getHeight(n)
  s = h - 1
  # if n >= pow(2, h-1) + pow(2, h-2) and n <= pow(2, h) -2:
  #   k = n - pow(2, h-1) + pow(2, h-2)
  #   p = n - pow(2, h-1)
  #   for i in range(p-2, p-(2*k)-1, -2):
  #     rot()
  #   s = h-1
  
  for j in range(s-1,0,-1):
    k = pow(2, j) - 1
    for i in range(1, k+1):
      rot(q, getNodeFromRightForearm(q, i), getNodeFromRightForearm(q, i+1))

# implementation of algorithm A1
def a1(S, n, T):
  root_k = computeRoot(n)
  x = iterativeSearch(S.root, root_k)
  # move x to root if necessary
  while x.parent is not None:
    rot(S, x.parent, x)
  buildLeftForearm(S)
  buildRightForearm(S)
  al(S)
  ar(S)

def matchRotationsA1(t, r):
  n = t.root.int[1]
  h = getHeight(n)
  p = -2
  
  r == pow(2, h)

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
  print("Print s after a1")
  preOrder(s.root)
