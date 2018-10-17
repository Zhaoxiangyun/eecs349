class Node:
  def __init__(self):
    self.label = None
    self.children = {}
	# you may want to add additional fields here...
    def __init__(self, val, dictionary):
        self.value = val
        if (isinstance(dictionary, dict)):
            self.children = dictionary.keys()
