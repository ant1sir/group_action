from group_action import __version__, __num_of_cores__
from group_action.library import *

def compute_symmetric_functions(n, reduced=0):
	"""
	Compute the list of all the reduced unique symmetric functions with n inputs
	Set reduced to 1 to get all the unique symmetric functions with n inputs
	"""
	symmetric_functions = []
	num_symmetric_functions = 1 << n + (1-reduced)

	# Iterate over all possible symmetric functions
	for i in range(num_symmetric_functions):
		# Create the intermediate function g
		g = [(i >> k) & 1 for k in range(n + 1)]

		# Create the function f from g, binding g at creation
		def f(x, g=g):
			return g[sum(x)]

		# Add f to the list of representatives
		symmetric_functions.append(f)

	return symmetric_functions

def main():
	print_header()

	# Create the parser
	parser = argparse.ArgumentParser(description='Generate each symmetric n-input 1-output Boolean function.')

	# Add the arguments
	parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
	parser.add_argument('--n', type=int, default=2, help='Number of inputs')

	# Parse the arguments
	args = parser.parse_args()

	# Print arguments summary
	print_arguments_summary(args, parser, __version__)

	"""
	Initialize Default value
	"""

	# number of inputs
	n=args.n
	
	# Computing symmetric functions whether reduced or not
	expect = 1 << (n + 1)

	symmetric_functions = compute_symmetric_functions(n)
	
	# Generating input vectors according to number of inputs
	input_vectors = compute_input_vectors(n)

	# Compute 
	variable_names = [f"x{k}" for k in range(n)]

	count=0
	for symmetric_function in symmetric_functions:
		signature_as_a_BE_bit_list = [symmetric_function(input_vector) for input_vector in input_vectors]
		signature_as_an_int = convert_bits_to_int(signature_as_a_BE_bit_list)
		print(f"index: {count}, signature: {signature_as_an_int}")

		# index
		count += 1

	if expect != count:
		raise Exception(f"Inconsistent number of symmetric functions. Got {count}, expected {expect} of them.")

	print_footer()

if __name__ == '__main__':
	main()
