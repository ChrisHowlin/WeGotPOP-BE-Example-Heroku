import collections

class SorterList:
	def __init__(self, sorter_dict):
		''' sorter_dict maps sorter names to functions '''
		self.sorter_dict = sorter_dict
		self.sorter_weights = {}

	def add_weight(self, label, weight):
		self.sorter_weights[weight] = label

	def sort(self, list_to_sort):
		# First sort the list so weakest first

		sorters_ordered = collections.OrderedDict(sorted(relevance_dict.items(),
														 reverse=True))

        for weight, sorter in sorters_ordered.items():
            print('Iterating sorters %s' % weight)
            list_to_sort = sorter_dict[sorter](list_to_sort)