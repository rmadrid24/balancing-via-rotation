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

def preOrderStr(node): 
  if not node: 
    return ""
      
  s = str(node.data)
  leftStr = preOrderStr(node.left)
  rightStr = preOrderStr(node.right)
  if leftStr != "":
    s += "," + leftStr 
  
  if rightStr != "":
    s += "," + rightStr
  return s

def printMaxIntervals(node): 
  if not node: 
    return

  if node.maxIdentical:
    print("Node has max interval" + str(node))
  printMaxIntervals(node.left) 
  printMaxIntervals(node.right)

def printMaxEquivalentIntervals(node): 
  if not node: 
    return

  if node.equivalent:
    print("Node has max equivalent subtree" + str(node))
  printMaxEquivalentIntervals(node.left) 
  printMaxEquivalentIntervals(node.right)

def getMaxIdenticalRoots(root): 
  if not root: 
    return
    
  identicalSubtreeRoots = []
  nodeStack = []
  nodeStack.append(root) 
  
  while len(nodeStack) > 0:
    node = nodeStack.pop() 
    if node.maxIdentical:
      identicalSubtreeRoots.append(node)
    else:
      if node.right is not None: 
        nodeStack.append(node.right) 
      if node.left is not None: 
        nodeStack.append(node.left) 
  
  return identicalSubtreeRoots

def getMaxEquivalentRoots(root): 
  if not root: 
    return
    
  equivalentSubtreeRoots = []
  nodeStack = []
  nodeStack.append(root) 
  
  while len(nodeStack) > 0:
    node = nodeStack.pop() 
    if node.equivalent:
      equivalentSubtreeRoots.append(node)
    else:
      if node.right is not None: 
        nodeStack.append(node.right) 
      if node.left is not None: 
        nodeStack.append(node.left) 
  
  return equivalentSubtreeRoots

#Testing
def setMaxIdenticalSubtrees2(node_s, t): 
  if not node_s: 
    return
      
  setMaxIdenticalSubtrees2(node_s.left, t) 
  setMaxIdenticalSubtrees2(node_s.right, t)
  tx = iterativeSearch(t.root, node_s.data)
  if tx.int == node_s.int:
    if isLeaf(node_s):
      node_s.identical = True
    else:
      leftEq = True
      rightEq = True
      if node_s.left is not None and not node_s.left.identical:
        leftEq = False
      
      if node_s.right is not None and not node_s.right.identical:
        rightEq = False
      
      if leftEq and rightEq:
        node_s.identical = True
        node_s.maxIdentical = True
        if node_s.left is not None:
          node_s.left.maxIdentical = False
        if node_s.right is not None:
          node_s.right.maxIdentical = False

# def setMaxIdenticalSubtrees(node_s, t): 
#   if not node_s: 
#     return
      
#   setMaxIdenticalSubtrees(node_s.left, t) 
#   setMaxIdenticalSubtrees(node_s.right, t)
#   tx = iterativeSearch(t.root, node_s.data)
#   if tx.int == node_s.int:
#     leftEq = False
#     rightEq = False
#     # check left subtree
#     if tx.left == node_s.left and tx.left is not None and tx.left.int == node_s.left.int:
#       leftEq = True
    
#     # check right subtree
#     if tx.right == node_s.right and tx.right is not None and tx.right.int == node_s.right.int:
#       rightEq = True
    
#     if leftEq and rightEq:
#       if node_s.left.left is None or node_s.left.right is None or node_s.right.left is None or node_s.right.right is None or node_s.left.maxIdentical and node_s.right.maxIdentical:
#         node_s.maxIdentical = True
#         node_s.left.maxIdentical = False
#         node_s.right.maxIdentical = False

# Test new set equivalent
def setMaxEquivalentSubtrees2(node_s, t): 
  if not node_s: 
    return
  
  tx = iterativeSearch(t.root, node_s.data)
  if tx.int == node_s.int and not node_s.identical and node_s != t.root:
    if node_s.left is not None and node_s.right is not None:
      node_s.equivalent = True
  else:
    setMaxEquivalentSubtrees2(node_s.left, t) 
    setMaxEquivalentSubtrees2(node_s.right, t)

# def setMaxEquivalentSubtrees(node_s, t): 
#   if not node_s: 
#     return
  
#   tx = iterativeSearch(t.root, node_s.data)
#   if tx.int == node_s.int and not node_s.maxIdentical and node_s != t.root:
#     if node_s.left is not None and node_s.right is not None:
#       node_s.equivalent = True
#   else:
#     setMaxEquivalentSubtrees(node_s.left, t) 
#     setMaxEquivalentSubtrees(node_s.right, t)

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
  if t.root.maxIdentical:
    return
  
  node = t.root.left
  while node is not None and node.maxIdentical == False:
    y = node
    # keep rotating until no left childs
    while y is not None and y.left is not None and y.left.maxIdentical == False:
      rotations += 1
      rot(t, y, y.left)
      y = y.parent
    node = y.right

def buildRightForearm(t):
  global rotations
  if t.root.maxIdentical:
    return
  
  node = t.root.right
  while node is not None and node.maxIdentical == False:
    y = node
    # keep rotating until no right childs
    while y is not None and y.right is not None and y.right.maxIdentical == False:
      rotations += 1
      rot(t, y, y.right)
      y = y.parent
    node = y.left 

def buildLeftForearmSimple(t):
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

def buildRightForearmSimple(t):
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

def getLeftArm(t):
  armNodes = []
  y = t.root.left
  while y is not None:
    armNodes.append(y)
    y = y.right
  
  return armNodes

def getRightArm(t):
  armNodes = []
  y = t.root.right
  while y is not None:
    armNodes.append(y)
    y = y.left
  
  return armNodes

def recordLeftArmT(t):
  leftArmMoves = []

  node = t.root.left
  while node is not None:
    y = node
    # keep rotating until no left childs
    while y is not None and y.left is not None:
      leftArmMoves.append((y.left.data, y.data))
      rot(t, y, y.left)
      y = y.parent
    node = y.right
  
  return leftArmMoves

def recordRightArmT(t):
  rightArmMoves = []
  
  node = t.root.right
  while node is not None:
    y = node
    # keep rotating until no right childs
    while y is not None and y.right is not None:
      rightArmMoves.append((y.right.data, y.data))
      rot(t, y, y.right)
      y = y.parent
    node = y.left

  return rightArmMoves

def al(q, t):
  global rotations
  
  n = q.root.int[1] - q.root.int[0] + 1
  th = getHeight(n)
  # handling case A of paper
  if n >= pow(2, th-1) and n <= pow(2, th-1) + pow(2, th-2) - 2:
    leaves = []
    nodes = list(range(t.root.left.int[0], t.root.left.int[1] + 1))
    # print(nodes)
    k = n - pow(2, th-1) + 1
    for i in range(0, k):
      leaves.append(nodes[2*i])
    
    # print(leaves)
    w = q.root.left
    while w is not None:
      if w.data in leaves:
        rotations += 1
        rot(q, w, w.right)
        w = w.parent
      w = w.right

  copyT = copyNode(t.root, None)
  leftArmMoves = recordLeftArmT(Tree(copyT))
  while len(leftArmMoves) > 0:
    op = leftArmMoves.pop()
    v = q.root.left
    present = False
    while v is not None and not isLeaf(v) and not v.maxIdentical:
      if v.data == op[0]:
        present = True
        break
      else: 
        v = v.right
    
    if present and v.right.data == op[1]:
      rotations += 1
      rot(q, v, v.right)

def ar(q, t):
  global rotations

  n = q.root.int[1] - q.root.int[0] + 1
  th = getHeight(n)

  # handling case C of paper
  if n >= pow(2, th-1) + pow(2, th-2) and n <= pow(2, th) - 2:
    # print("Case C")
    # preprocessing on case c
    leaves = []
    nodes = list(reversed(range(t.root.right.int[0], t.root.right.int[1] + 1)))
    # print(nodes)
    k = n - pow(2, th-1) - pow(2, th-2)
    p = n - pow(2, th-1)
    for i in range(p-2, p-(2*k)-1, -2):
      leaves.append(nodes[i-1])
    
    # print(leaves)
    w = q.root.right
    while w is not None:
      if w.data in leaves:
        rotations += 1
        rot(q, w, w.left)
        w = w.parent
      w = w.left

  copyT = copyNode(t.root, None)
  rightArmMoves = recordRightArmT(Tree(copyT))
  while len(rightArmMoves) > 0:
    op = rightArmMoves.pop()
    v = q.root.right
    present = False
    while v is not None and not isLeaf(v) and not v.maxIdentical:
      if v.data == op[0]:
        present = True
        break
      else: 
        v = v.left
    
    if present and v.left.data == op[1]:
      rotations += 1
      rot(q, v, v.left)

# implementation of algorithm A1
def a1(Q, n, T, showResult=True):
  global rotations

  # print("Starting a1")
  # print("Start: ", end='')
  # preOrder(Q.root)
  # print("")
  root_k = computeRoot(n)
  x = iterativeSearch(Q.root, Q.root.int[0] + root_k - 1)
  # move x to root if necessary
  while Q.root != x:
    rotations += 1
    rot(Q, x.parent, x)
  buildLeftForearmSimple(Q)
  buildRightForearmSimple(Q)
  # print("Forearms: ", end='')
  # preOrder(Q.root)
  # print("")
  al(Q, T)
  ar(Q, T)
  # print("End: ", end='')
  # preOrder(Q.root)
  # print("")
  if showResult:
    ss = preOrderStr(Q.root)
    ts = preOrderStr(T.root)
    if ss == ts:
      print("S and T are equal!")
    else:
      print("S and T are not equal")
    
    print("Actual rotations A1: " + str(rotations))

# implementation of algorithm A2
def a2(Q, n, T, showResult=True):
  # print("Starting a2")
  global rotations
  if not Q.root.maxIdentical:
    # print("Start: ", end='')
    # preOrder(Q.root)
    # print("")

    root_k = computeRoot(n)
    x = iterativeSearch(Q.root, root_k)
    # move x to root if necessary
    while Q.root != x:
      rotations += 1
      rot(Q, x.parent, x)

    buildLeftForearm(Q)
    buildRightForearm(Q)
    # print("After forearms A2")
    # print("S: ", end='')
    # preOrder(Q.root)
    # print("")

    if not Q.root.left.maxIdentical:
      al(Q, T)
    if not Q.root.right.maxIdentical:
      ar(Q, T)
    # print("End: ", end='')
    # preOrder(Q.root)
    # print("")
  
  if showResult:
    ss = preOrderStr(Q.root)
    ts = preOrderStr(T.root)
    if ss == ts:
      print("S and T are equal!")
    else:
      print("S and T are not equal")
    
    print("Actual rotations A2: " + str(rotations))

# implementation of algorithm A3
def a3(Q, n, T):
  # print("Starting a3")
  global rotations

  maxIntervalRoots = getMaxEquivalentRoots(Q.root)
  for root in maxIntervalRoots:
    if not root.maxIdentical:
      # print("calling a1 with " + str(root))
      root_t = iterativeSearch(T.root, root.data)
      temp_n = root.int[1] - root.int[0] + 1
      sub_s = Tree(root)
      sub_t = Tree(root_t)
      a1(sub_s, temp_n, sub_t, False)
      root.maxIdentical = True

  # print("Before A2: ", end='')
  # preOrder(Q.root)
  # print("")
  a2(Q, n, T, False)
  # print("End: ", end='')
  # preOrder(Q.root)
  # print("")
  ss = preOrderStr(Q.root)
  ts = preOrderStr(T.root)
  if ss == ts:
    print("S and T are equal!")
  else:
    print("S and T are not equal")
  
  print("Actual rotations A3: " + str(rotations))

def getTreeSizeWithoutArm(root, lArm, rArm):
  current = root  
  stack = []
  nodes = 0
  while True:
    if current is not None:
      stack.append(current)   
      current = current.left  
    elif(stack): 
      current = stack.pop() 
      if not current in lArm and not current in rArm:
        nodes += 1
      current = current.right  
    else:
      break
  
  return nodes
  # return root.int[1] - root.int[0] + 1

def getSubtreeSize(root):
  return root.int[1] - root.int[0] + 1

# required for matching theorem 3
def removeMaxIdenticalSubtrees(node):
  if not node: 
    return
      
  node.maxIdentical = False
  removeMaxIdenticalSubtrees(node.left) 
  removeMaxIdenticalSubtrees(node.right)

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

def rotationsA2(t, n, s):
  h = getHeight(n)
  p = float('-inf')
  
  if n >= pow(2, h-1) and n <= pow(2, h-1) + pow(2, h-2) - 2:
    p = 1
  elif n == pow(2, h-1) + pow(2, h-2) - 1:
    p = 0
  elif n >= pow(2, h-1) + pow(2, h-2) and n<= pow(2, h) - 1:
    p = -1
  
  leftArm = getLeftArm(t)
  rightArm = getRightArm(t)
  savings = 0
  maxIdenticalRoots = getMaxIdenticalRoots(s.root)
  for root in maxIdenticalRoots:
    savings += getTreeSizeWithoutArm(root, leftArm, rightArm)
  
  return (2 * n) - (2 * math.floor(math.log2(n))) - cs(t.root) - (2*savings) + p

def rotationsA3(t, n, s):
  savings = 0
  maxIdenticalRoots = getMaxEquivalentRoots(s.root)
  for root in maxIdenticalRoots:
    savings += math.floor(math.log2(getSubtreeSize(root)))
  
  return (2 * n) - (2 * math.floor(math.log2(n))) - cs(t.root) - (2*savings) + len(maxIdenticalRoots) + 1

def printCase(n):
  h = getHeight(n)
  if n >= pow(2, h-1) and n <= pow(2, h-1) + pow(2, h-2) - 2:
    print("Case A")
  elif n == pow(2, h-1) + pow(2, h-2) - 1:
    print("Case B")
  elif n >= pow(2, h-1) + pow(2, h-2) and n<= pow(2, h) - 2:
    print("Case C")
  elif n == pow(2, h) - 1:
    print("Case D")

if __name__=="__main__":
  tests = [1000, 1100, 1200, 1300, 1400]
  for test in tests:
    n = test
    print("Starting trees with " + str(n) + " nodes")
    printCase(n)
    arr = [x for x in range(1, n + 1)]
    root_t = sortedArrayToBST(arr)
    t = Tree(root_t)
    rotations = 0
    s = buildS(t)
    # print("T: ", end='')
    # preOrder(t.root)
    # print("")
    # print("S: ", end='')
    # preOrder(s.root)
    # print("")

    print("Testing A1")
    a1Rotations = rotationsA1(t, n)
    print("A1 expected rotations: " + str(a1Rotations))
    root_copy1 = copyNode(s.root, None)
    Q1 = Tree(root_copy1)
    rotations = 0
    a1(Q1, n, t)

    # print("Final A1: ", end='')
    # preOrder(Q1.root)
    # print("")

    print("Testing A2")
    root_copy2 = copyNode(s.root, None)
    Q2 = Tree(root_copy2)
    setMaxIdenticalSubtrees2(Q2.root, t)
    printMaxIntervals(Q2.root)
    a2Rotations = rotationsA2(t, n, Q2)
    print("A2 expected rotations: " + str(a2Rotations))
    rotations = 0
    a2(Q2, n, t)

    # print("Final A2: ", end='')
    # preOrder(Q2.root)
    # print("")

    print("Testing A3")
    root_copy3 = copyNode(s.root, None)
    Q3 = Tree(root_copy3)
    setMaxIdenticalSubtrees2(Q3.root, t)
    # printMaxIntervals(Q3.root)
    setMaxEquivalentSubtrees2(Q3.root, t)
    printMaxEquivalentIntervals(Q3.root)
    # keep only equivalent trees so that theorem 3 matches
    removeMaxIdenticalSubtrees(Q3.root)
    a3Rotations = rotationsA3(t, n, Q3)
    print("A3 expected rotations: " + str(a3Rotations))
    rotations = 0
    a3(Q3, n, t)

    # print("Final A3: ", end='')
    # preOrder(Q3.root)
    print("--------------")
