from group_action import __version__, __num_of_cores__
from group_action.library import *

def task(transposition, function, n):
	"""
	Atomic task
	"""
	permutation = convert_transposition_to_permutation(transposition, n)
	new_function = action(permutation, function)
	new_signature = compute_signature(new_function,n)
	return new_signature

def main():
	print_header()

	# Create the parser
	parser = argparse.ArgumentParser(description='Computation of the orbit of a n-input, 1-output Boolean function specified via its signature as a LE integer under the action of the symmetric group Sn via its transpositions.')

	# Add the arguments
	parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
	parser.add_argument('--s', type=int, default=12, help='Signature')
	parser.add_argument('--n', type=int, default=2, help='Number of inputs')
	parser.add_argument('--c', type=int, default=__num_of_cores__, help='Number of cores')

	# Parse the arguments
	args = parser.parse_args()

	# Print arguments summary
	print_arguments_summary(args, parser, __version__)

	# signature
	signature = args.s

	# number of inputs
	n=args.n

	# number of cores
	num_cores=args.c

	# Computing symmetric group
	permutations = generate_transpositions(n)
	permutations += [()]

	# Computing function
	function = generate_function(signature, n)

	# Total number of permutations
	size = len(permutations)

	# Define the number of jobs
	num_jobs = size

	with tqdm_joblib(tqdm(desc="Brut force orbit computing", total=size)) as progress_bar:
		results = Parallel(n_jobs=num_cores)(delayed(task)(permutation, function, n) for permutation in permutations)

	# Get unique elements from results and sort
	orbit = list(set(results))
	orbit.sort()

	# Printing orbit of input function
	print(f"Orbit of {signature} under the action of S{n} on 2^2^{n}")
	for i, element in enumerate(orbit):
		print(f"index: {i:{0}{len(str(len(orbit)))}} element: {element}")
	print(f"{len(orbit)} elements found.")

	print_footer()

if __name__ == '__main__':
	main()
