# built-in modules
import argparse
from collections import defaultdict
import contextlib
import itertools
import json
import math
import sys

# extra modules
import joblib
from joblib import Parallel, delayed
from tqdm import tqdm

sys.set_int_max_str_digits(8192)

from group_action import __version__

def print_arguments_summary(args, parser, version):
	"""
	Print execution summary
	"""
	command_name = sys.argv[0]
	print(f"Command: {command_name}\nVersion: {version}")
	print("Arguments Summary:")
	for arg, value in vars(args).items():
		# Find the corresponding action for this argument to get its help text
		action = next(action for action in parser._actions if action.dest == arg)
		help_text = action.help
		print(f"  {help_text}: {value}")
	print(f"Type {command_name} --h to get more information about this command usage.")

def print_header():
	print(
"""------------------------
Author: Antoine Sirianni
Location: Paris, France
Date: 2024 Sep 10
------------------------""")

	print(
"""-----------------------------------------------------------------------------
MIT License

Copyright (c) 2024 Antoine Sirianni, Paris, France

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
-----------------------------------------------------------------------------""")

def print_footer():
	print("--------------------------------------------------")
	print("Copyright (c) 2024 Antoine Sirianni, Paris, France")
	print("--------------------------------------------------")

def convert_int_to_bits(i, size, style=0):
	"""
	Convert a LE integer into a BE list of bits
	"""
	if (style==0):
		result = [(i >> k) & 1 for k in range(size)]
	elif (style==1):
		result = [(i >> (size-1-k)) & 1 for k in range(size)]
	else:
		raise Exception(f"Unknown style: {style}. 0 -> BE or 1 -> LE expected");

	return result

def convert_bits_to_int(bits):
	"""
	Convert a BE list of bits into a LE integer
	"""
	result_as_an_int=0
	power = 1
	for i in bits:
		result_as_an_int += i*power
		power = power << 1
	return result_as_an_int

def generate_permutations(elements):
	"""
	Generate all the permutations of the elements in the input list.
	"""
	return list(map(list, itertools.permutations(elements)))

def generate_symmetric_group(n):
	"""
	Generate the symmetric group.
	"""
	return generate_permutations([k for k in range(n)])

def apply_permutation(permutation, elements):
	"""
	Apply a permutation to a list of elements.
	"""
	size=len(permutation)
	if (size>len(elements)):
		raise Exception("Permutation length {size} shall not exceed number of elements {elements}.")
	return [elements[permutation[k]] for k in range(size)]

def compute_permutation_inverse(permutation):
	"""
	Compute the inverse of a permutation.
	"""
	# a is an array
	a = {}
	size=len(permutation)
	for i in range(size):
		a[permutation[i]]=i
	
	return [a[k] for k in range(size)]

def action(permutation, f):
	"""
	Compute natural action of permutation on function
	"""
	n=len(permutation)
	inverse = compute_permutation_inverse(permutation)

	# x is an integer	
	def g(x, f=f, inverse=inverse, n=n):
		size=2**n
		# converting x into bits
		bits = convert_int_to_bits(x, n)
		# permuting
		permuted_args = apply_permutation(inverse, bits)
		# converting x back to an int
		new_x = convert_bits_to_int(permuted_args)
		return f(new_x)
	
	return g

def generate_functions(n):
	"""
	Generate Boolean functions according to number of variables
	"""
	size=2**(2**n)
	functions=[]
	for i in range(size):
		def f(x, i=i):
			return (i >> x) & 1
		functions += [f]
	
	return functions

def compute_signature(f,n):
	"""
	Compute signature of Boolean function
	"""
	signature_as_an_int=0
	power = 1
	size=2**n
	for i in range(size):
		signature_as_an_int += f(i)*power
		power = power << 1

	return signature_as_an_int

def generate_function(signature, n):
	"""
	Generate Boolean function according to its signature as a LE integer
	"""
	size=2**(2**n)
	functions=[]
	def f(x, i=signature):
		return (i >> x) & 1

	return f

def compute_minterm_from_position_in_signature(position, variable_names):
	"""
	Compute minterm from position in signature and list of variable names
	"""
	size = len(variable_names)
	minterm_as_a_BE_list = convert_int_to_bits(position, size)
	minterm_as_a_string = ""
	for i in range(size):

		# Print conjunction if any
		if (i>0):
			minterm_as_a_string += " && "
	
		# Print negation is any
		minterm_element = minterm_as_a_BE_list[i]
		if minterm_element==0:
			minterm_as_a_string += "!"
		elif minterm_element==1:
			# do nothing
			pass
		else:
			raise Exception(f"Unknown minterm element {minterm_element}")

		# Print variable name
		minterm_as_a_string += variable_names[i]
		
	return minterm_as_a_string

def convert_signature_as_BE_bits_to_DNF(signature_as_a_BE_bit_list, variable_names):
	"""
	Convert a signature as a BE list of bits into a DNF according to a list of variable names
	"""
	size = len(signature_as_a_BE_bit_list)
	number_of_variables = len(variable_names);
	DNF = ""
	started = False
	for position in range(size):
		if signature_as_a_BE_bit_list[position]==1:
			if started:
				DNF += " || "
			else:
				started = True
			minterm_as_a_string = compute_minterm_from_position_in_signature(position, variable_names)
			DNF += minterm_as_a_string
		elif signature_as_a_BE_bit_list[position]==0:
			# do nothing
			pass
		else:
			raise Exception(f"Unknown element in signature {signature_as_a_BE_bit_list[position]} at position {position}")
	if not started:
		DNF = "0"
	return DNF

def compute_input_vectors(number_of_variables):
	"""
	Compute the list of input vectors according of the number of variables
	"""
	input_vectors = []
	size = 1 << number_of_variables
	for i in range(size):
		input_vector = convert_int_to_bits(i, number_of_variables)
		input_vectors += [input_vector]
	return input_vectors

@contextlib.contextmanager
def tqdm_joblib(tqdm_object):
	"""
	Context manager to patch joblib to report into tqdm progress bar given as argument
	"""
	class TqdmBatchCompletionCallback(joblib.parallel.BatchCompletionCallBack):
		def __call__(self, *args, **kwargs):
			tqdm_object.update(n=self.batch_size)
			return super().__call__(*args, **kwargs)

	old_batch_callback = joblib.parallel.BatchCompletionCallBack
	joblib.parallel.BatchCompletionCallBack = TqdmBatchCompletionCallback
	try:
		yield tqdm_object
	finally:
		joblib.parallel.BatchCompletionCallBack = old_batch_callback
		tqdm_object.close()

def dfs(node, graph, visited, component):
	"""
	Depth First Search
	"""
	stack = [node]
	while stack:
		current = stack.pop()
		if current not in visited:
			visited.add(current)
			component.append(current)
			stack.extend(graph[current])

def find_connected_components(vertices, edges):
	"""
	Find connected components
	"""
	graph = defaultdict(list)
	for u, v in edges:
		graph[u].append(v)
		graph[v].append(u)  # Since the graph is undirected

	visited = set()
	components = []
	for vertex in vertices:
		if vertex not in visited:
			component = []
			dfs(vertex, graph, visited, component)
			components.append(component)
	
	return components

def task(permutation, chunk, n):
	"""
	Atomic task
	"""
	partial_edges = []
	for function in chunk:
		new_function = action(permutation, function)
		partial_edges += [(compute_signature(function,n), compute_signature(new_function,n))]
	return partial_edges

def chunk_list(data, chunk_size):
	"""
	Compute a list of chunks from data
	"""
	return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
