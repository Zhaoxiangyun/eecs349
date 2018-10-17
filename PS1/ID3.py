#from node import Node
import math
import pdb


def ID3(data,default):
#  '''
#  Takes in an array of examples, and returns a tree (an instance of Node) 
#  trained on the examples.  Each example is a dictionary of attribute:value pairs,
#  and the target class variable is a special attribute with the name "Class".
#  Any missing attributes are denoted with a value of "?"
#  '''
   
    data = data
    attributes = [*data[0].keys()]
    target = 'Class'
    vals = [record[target] for record in data]
    default = MODE(data,target)
    if not data or (len(attributes)-1)<=0:
        return default
    elif vals.count(vals[0]) == len(vals):
       return vals[0]
    else:
        best = attr_choose(data, attributes, target)
        tree = {best:{}}
        major_val = MODE(data,best)     
        for i in range(len(data)):
            if data[i][best] == '?':
                data[i][best] = major_val
        for val in get_values(data,best):
            new_data = get_data(data,best,val)
            subtree = ID3(new_data,tree)
            tree[best][val] = subtree
            tree[best]['major_val'] = major_val            
    return tree       
# Class Node which will be used while classify a test-instance using the tree which was built earlier

class Node():
    value = ""
    children = []
    def __init__(self, val, dictionary):
        self.value = val
        if (isinstance(dictionary, dict)):
            self.children = dictionary.keys()

def prune_node(node,examples):

    new_node = node.copy()
    tree = node
    target = 'Class'
    if isinstance(tree,dict):
       return MODE(examples,target)
    else:
       return tree
     
      


def prune(node, examples):
  '''
  Takes in a trained tree and a validation set of examples.  Prunes nodes in order
  to improve accuracy on the validation data; the precise pruning strategy is up to you.
  '''
  tree = node
  if isinstance(tree,dict):
    tempDict = tree.copy()
  else:
     tempDict = tree
  if isinstance(tempDict,dict):
      index = 0
      old_acc = test(tempDict,examples)
      for key in [*tempDict.keys()]:
       if isinstance(tempDict[key],dict):
         for val in [*tempDict[key].keys()]:
            new_data = get_data(examples,key,val)
            if not isinstance(tempDict[key][val],dict):
                     index = index + 1
            else:
              if len(new_data) == 0 :
                  del tempDict[key][val]
                  continue
              else:   
                subtree = prune(tempDict[key][val], new_data)
                tempDict[key][val] = subtree
      if index == len([*tempDict[key].keys()]):
            node_1 = prune_node(tempDict,examples) 
            new_acc =test(node_1,examples)
            if new_acc>=old_acc:
                  tempDict = node_1
  return tempDict




#  q = []
#  output = []
#  q.append(node)
#  while len(q) !=0:
#      n = q.pop(0)
#      n = prune_iter(n.examples)
#      children = n.children
#      if len(children) !=0:
#          for c in 
def test(node,examples):
  '''
  Takes in a trained tree and a test set of examples.  Returns the accuracy (fraction
  of examples the tree classifies correctly).
  '''
  
  results = []
  target = 'Class'
  for data in examples:
      result = evaluate(node,data)
      if result != "Null":
           results.append(result == data[target])
  try:
    accuracy = float(results.count(True))/float(len(results))
  
  except:
     accuracy = 1
  return accuracy
def evaluate(node, example):


#  '''
#  Takes in a tree and one example.  Returns the Class value that the tree
#  assigns to the example.
#  '''
#

  target = 'Class'
  tree = node
  if not isinstance(tree,dict):
      result = tree
  else:    
      tempDict = tree.copy()
      result = ""
      entry = example
      while(isinstance(tempDict, dict)):
          keys_list = [*tempDict.keys()]
          root = Node(keys_list[0],keys_list[0])
          tempDict = tempDict[keys_list[0]]
          value = entry[root.value]
          if value == '?':

             value = tempDict['major_val']
                            
          if (value in tempDict.keys()):
              child=Node(value,tempDict[value])
              result = tempDict[value]
              tempDict = tempDict[value]
              
          else:
              result = "Null"
              break
  return result        
def get_target_data(data,target,val):
 
    new_data = []
    for sample in data:
        if sample[target] == val:
            new_data.append(sample)
    return new_data        
def MODE(data,target):

    freq = {}
    index = target
    for tuple in data:

        if tuple[index]=='?':
            continue
        
        if (tuple[index] in freq):
            freq[tuple[index]] += 1 
        else:
            freq[tuple[index]] = 1
    max = 0
    major = ""

    for key in freq.keys():
        if freq[key]>max:
            max = freq[key]
            major = key

    return major

def attr_choose(data, attributes, target):
    
    attributes.remove(target)
    
    best = attributes[0]
    maxGain = 0;
    for attr in attributes:
        newGain = info_gain(attributes, data, attr, target) 
        if newGain>maxGain:
            maxGain = newGain
            best = attr

    return best

def info_gain(attributes, data, attr, targetAttr):
    freq = {}
    subsetEntropy = 0.0
 #   i = attributes.index(attr)
    for entry in data:
        if entry[attr]=='?':
            continue
        if (entry[attr] in freq):
            freq[entry[attr]] += 1.0
        else:
            freq[entry[attr]]  = 1.0

    for val in freq.keys():
        valProb        = freq[val] / sum(freq.values())
        dataSubset     = [entry for entry in data if entry[attr] == val]
        subsetEntropy += valProb * entropy(attributes, dataSubset, targetAttr)

    return (entropy(attributes, data, targetAttr) - subsetEntropy)

# This function will get all the rows of the data where the chosen "best" attribute has a value "val"
def get_data(data,best, val):

    new_data = []
    #index = attributes.index(best)

    for entry in data:
        if (entry[best] == val):
            newEntry = {}
            for i in entry:
                if(i != best):
                    newEntry[i] = entry[i]
            new_data.append(newEntry)

    return new_data

# This function will get unique values for that particular attribute from the given data
def get_values(data, attr):

   # index = attributes.index(attr)
    values = []

    for entry in data:
        if entry[attr] not in values:
            values.append(entry[attr])

    return values

def entropy(attributes, data, targetAttr):

    freq = {}
    dataEntropy = 0.0
    for entry in data:
        if (entry[targetAttr] in freq):
            freq[entry[targetAttr]] += 1.0
        else:
            freq[entry[targetAttr]]  = 1.0

    for freq in freq.values():
        dataEntropy += (-freq/len(data)) * math.log(freq/len(data), 2) 
        
    return dataEntropy


