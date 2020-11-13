import random
import math

class Node: 
  def __init__(self, val): 
    self.data = val
    self.left = None
    self.right = None
    self.parent = None
    self.int = None
  
  def __str__(self):
        return 'Node {self.data} with left child {self.left.data}, right child {self.right.data}, and int {self.int}'.format(self=self)
  
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

def copyNode(node, p):
  if node is None:
    return None
  
  temp = Node(node.data)
  temp.parent = p
  tempLeft = copyNode(node.left, temp)
  tempRight = copyNode(node.right, temp)
  temp.left = tempLeft
  temp.right = tempRight

  return temp

def computeRoot(n):
  h = math.ceil(math.log2(n+1))
  print("h=" + str(h))
  root_t = -1
  if n >= math.pow(2, h-1) and n <= math.pow(2, h-1) + (math.pow(2, h-2) - 2):
    root_t = n - math.pow(2, h-2) + 1
  elif n >= math.pow(2, h-1) + math.pow(2, h-1) - 1 and n <= math.pow(2, h) -1:
    root_t = math.pow(2, h-1)
  
  return root_t

# iterative-search

# Guess how to form forearms

#do i need to add height property to node

def flipCoin(p):
  r = random.random()
  return r < p