import sys
from util import *

rotations = 0

# function to convert sorted array to a almost complete balanced tree 
def sortedArrayToBST(arr):
  if not arr: 
    return None

  # find root
  n = len(arr)
  r = computeRoot(n) - 1

  root = Node(arr[r])
  root.int = (arr[0], arr[n-1])

  # left subtree of root has all 
  # values <arr[r] 
  root.left = sortedArrayToBST(arr[:r])
      
  # right subtree of root has all  
  # values >arr[r] 
  root.right = sortedArrayToBST(arr[r+1:])
  
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
    # print(str(x.data) + " -> " + str(y.data) + " , rot probability: " + str(shouldRotate))
    if shouldRotate:
      if flipCoin(0.5):
        if y.parent == x:
          rot(tree_s, x, y)
  
  return tree_s

def buildLeftForearm(t):
  global rotations
  node = t.root.left
  while node is not None:
    y = node
    # keep rotating until no left childs
    while y is not None and y.left is not None:
      rotations += 1
      rot(t, y, y.left)
      y = y.parent
    node = y.right

def buildRightForearm(t):
  global rotations
  node = t.root.right
  while node is not None:
    y = node
    # keep rotating until no right childs
    while y is not None and y.right is not None:
      rotations += 1
      rot(t, y, y.right)
      y = y.parent
    node = y.left  

def al(q, t):
  global rotations
  n = t.root.int[1]
  th = getHeight(n)
  h = getForearmsHeight(t)[0]
  s = h
  # handling case A of paper
  if n >= pow(2, th-1) and n <= pow(2, th-1) + pow(2, th-2) - 2:
    k = n - pow(2, th-1) + 1
    for i in range(1, k+1):
      rotations += 1
      rot(q, getNodeFromLeftForearm(q, i), getNodeFromLeftForearm(q, i+1))
    s = h - 1
  
  for j in range(s-1,0,-1):
    k = pow(2, j) - 1
    for i in range(1, k+1):
      rotations += 1
      rot(q, getNodeFromLeftForearm(q, i), getNodeFromLeftForearm(q, i+1))

def ar(q, t):
  global rotations
  n = t.root.int[1]
  th = getHeight(n)
  h = getForearmsHeight(t)[1]
  s = h
  # handling case C of paper
  if n >= pow(2, th-1) + pow(2, th-2) and n <= pow(2, th) - 2:
    k = n - pow(2, th-1) - pow(2, th-2)
    p = n - pow(2, th-1)
    for i in range(p-2, p-(2*k)-1, -2):
      rotations += 1
      rot(q, getNodeFromRightForearm(q, i), getNodeFromRightForearm(q, i+1))
    s = h-1
  
  for j in range(s-1,0,-1):
    k = pow(2, j) - 1
    for i in range(1, k+1):
      rotations += 1
      rot(q, getNodeFromRightForearm(q, i), getNodeFromRightForearm(q, i+1))

# implementation of algorithm A1
def a1(S, n, T):
  global rotations
  root_k = computeRoot(n)
  x = iterativeSearch(S.root, root_k)
  # move x to root if necessary
  while x.parent is not None:
    rotations += 1
    rot(S, x.parent, x)
  buildLeftForearm(S)
  buildRightForearm(S)
  al(S, T)
  ar(S, T)

def rotationsA1(t, n):
  h = getHeight(n)
  p = float('-inf')
  
  if n >= pow(2, h-1) and n <= pow(2, h-1) + pow(2, h-2) - 2:
    p = 1
  elif n == pow(2, h-1) + pow(2, h-2) - 1:
    p = 0
  elif n >= pow(2, h-1) + pow(2, h-2) and n<= pow(2, h) - 1:
    p = -1
  
  return (2 * n) - (2 * math.floor(math.log2(n))) - cs(t.root) + p

if __name__=="__main__":
  # n = int(sys.argv[1])
  # print("Starting trees with " + str(n) + " nodes")
  tests = [500, 1000, 1500]
  # arr = [x for x in range(1, n + 1)]
  # root_t = sortedArrayToBST(arr)
  # t = Tree(root_t)
  # maxRotations = rotationsA1(t)
  # print("Upper bound rotations: " + str(maxRotations))
  for test in tests:
    n = test
    print("Starting trees with " + str(n) + " nodes")
    arr = [x for x in range(1, n + 1)]
    root_t = sortedArrayToBST(arr)
    t = Tree(root_t)
    maxRotations = rotationsA1(t, n)
    print("Upper bound rotations: " + str(maxRotations))
    for i in range(0,5):
      rotations = 0
      s = buildS(t)
      # print("T: ", end='')
      # preOrder(t.root)
      # print("")
      # print("Initial S: ", end='')
      # preOrder(s.root)
      # print("")

      a1(s, n, t)
      # print("Resulting S: ", end='')
      # preOrder(s.root)
      # print("")
      print("Test " + str(i) + " with " + str(test) + " nodes: " + str(rotations) + " rotations")
