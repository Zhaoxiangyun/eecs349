from ID3 import ID3,prune,test,evaluate
#import node
from parse import parse
import pdb
data_dir = 'house_votes_84.data'
data = parse(data_dir)
tree = ID3(data[50:],0)
result = evaluate(tree,data[0])
accuracy = test(tree,data)
new_tree = prune(tree,data[0:50])
pdb.set_trace()
