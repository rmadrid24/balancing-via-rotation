import random
import math

class Node: 
  def __init__(self, val): 
    self.data = val
    self.left = None
    self.right = None
    self.parent = None
    self.int = None
    self.maxIdentical = False
    self.identical = False
    self.equivalent = False
    self.rep = ""
  
  def __str__(self):
        return 'Node {self.data} with int {self.int}'.format(self=self)
  
  def __hash__(self):
    return hash(self.data)

  def __eq__(self, other):
    return (
      self.__class__ == other.__class__ and
      self.data == other.data
    )
  
  def __gt__(self, other):
    return (
      self.__class__ == other.__class__ and
      self.data > other.data
    )
  
  def __lt__(self, other):
    return (
      self.__class__ == other.__class__ and
      self.data < other.data
    )

class Tree:
  def __init__(self, root):
    self.root = root

def getEdges(node):
  if node is None: 
    return []

  edges = []
  if node.left is not None:
    edges.append((node, node.left, flipCoin(0.1)))
  
  if node.right is not None:
    edges.append((node, node.right, flipCoin(0.1)))
  
  return edges + getEdges(node.left) + getEdges(node.right)

def leftRotate(t, x, y):
  x.right = y.left
  if y.left is not None:
    y.left.parent = x
  y.parent = x.parent
  if x.parent is None:
    t.root = y
  elif x == x.parent.left:
    x.parent.left = y
  else:
    x.parent.right = y
  
  y.left = x
  x.parent = y

  # updating intervals
  lx = x.int[0]
  ry = y.int[1]
  if x.right is not None:
    x.int = (lx, x.right.int[1])
  else:
    x.int = (lx,x.data)
  
  y.int = (lx, ry)

def righRotate(t, x, y):
  x.left = y.right
  if y.right is not None:
    y.right.parent = x
  y.parent = x.parent
  if x.parent is None:
    t.root = y
  elif x == x.parent.left:
    x.parent.left = y
  else:
    x.parent.right = y
  
  y.right = x
  x.parent = y

  # updating intervals
  rx = x.int[1]
  ly = y.int[0]
  if x.left is not None:
    x.int = (x.left.int[0], rx)
  else:
    x.int = (x.data,rx)
  
  y.int = (ly, rx)

def copyNode(node, p):
  if node is None:
    return None
  
  temp = Node(node.data)
  temp.parent = p
  temp.int = node.int
  temp.maxIdentical = node.maxIdentical
  temp.equivalent = node.equivalent
  temp.rep = node.rep
  temp.identical = node.identical
  tempLeft = copyNode(node.left, temp)
  tempRight = copyNode(node.right, temp)
  temp.left = tempLeft
  temp.right = tempRight

  return temp

def computeRoot(n):
  h = getHeight(n)
  root_t = -1
  if n >= pow(2, h-1) and n <= pow(2, h-1) + pow(2, h-2) - 2:
    root_t = n - pow(2, h-2) + 1
  elif n >= pow(2, h-1) + pow(2, h-2) - 1 and n <= pow(2, h) -1:
    root_t = pow(2, h-1)
  
  return root_t

def getHeight(n):
  return math.ceil(math.log2(n+1))

def iterativeSearch(x, k):
  while x is not None and k != x.data:
    if k < x.data:
      x = x.left
    else:
      x = x.right
  return x

def isLeaf(node):
  if node.left is None and node.right is None:
    return True
  return False

def cs(root_t):
  return ls(root_t) + rs(root_t)

def ls(root_t):
  f = root_t.left
  sum = 0
  while f is not None:
    sum += 1
    f = f.right

  return sum

def rs(root_t):
  f = root_t.right
  sum = 0
  while f is not None:
    sum += 1
    f = f.left

  return sum

def flipCoin(p):
  r = random.random()
  return r < p