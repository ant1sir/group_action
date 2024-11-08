from group_action import __version__, __num_of_cores__
from group_action.library import *
import random

def atomic_task(transposition, function, n):
	"""
	Atomic task
	"""
	permutation = convert_transposition_to_permutation(transposition, n)
	new_function = action(permutation, function)
	new_signature = compute_signature(new_function,n)
	return new_signature

def task(permutations, item, n):
	"""
	Task
	"""
	iteration = item[0]
	signature = item[1]
	function = item[2]
	result = []
	for permutation in permutations:
		result += [atomic_task(permutation, function, n)]
	return [iteration, signature, result]

def main():
	print_header()

	# Create the parser
	parser = argparse.ArgumentParser(description='Iterate on brut force computation of random orbit of n-input, 1-output Boolean function specified via its signature as a LE integer under the action of the symmetric group Sn.')

	# Add the arguments
	parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
	parser.add_argument('--i', type=int, default=1, help='iterations')
	parser.add_argument('--n', type=int, default=2, help='Number of inputs')
	parser.add_argument('--c', type=int, default=__num_of_cores__, help='Number of cores')

	# Parse the arguments
	args = parser.parse_args()

	# Print arguments summary
	print_arguments_summary(args, parser, __version__)

	# iterations
	iterations = args.i

	# number of inputs
	n=args.n

	# number of cores
	num_cores=args.c

	# Computing symmetric group
	permutations = generate_transpositions(n)
	permutations += [()]

	# Total number of permutations
	size = len(permutations)

	# Define the number of jobs
	num_jobs = size

	functions = []

	max_format = 0
	for iteration in range(iterations):

		# generate a random signature in the range 0-2^2^n-1
		signature = random.randrange(2**(2**n))

		it = len(str(signature))
		if it > max_format:
			max_format = it
		
		# compute function
		function = generate_function(signature, n)
		
		# Computing functions
		functions += [[iteration+1, signature, function]]

	# execute tasks	
	with tqdm_joblib(tqdm(desc="Iterate on brut force orbit computing", total=iterations)) as progress_bar:
		results = Parallel(n_jobs=num_cores)(delayed(task)(permutations, item, n) for item in functions)

	for result in results:

		# Get unique elements from results and sort
		orbit = list(set(result[2]))
	
		# print result
		print(f"iteration: {result[0]:{0}{len(str(iterations))}} signature: {result[1]:{0}{max_format}} orbit size: {len(orbit):{0}{len(str(size))}}.")

	print_footer()

if __name__ == '__main__':
	main()
