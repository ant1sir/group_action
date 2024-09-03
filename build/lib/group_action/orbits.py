from group_action.library import *

def main():
	print_header()

	# Create the parser
	parser = argparse.ArgumentParser(description='Brut force computation of orbits of n-input 1-output Boolean functions under the action of the symmetric group Sn.')

	# Add the arguments
	parser.add_argument('--n', type=int, default=2, help='Number of inputs')
	parser.add_argument('--c', type=int, default=8, help='Number of cores')
	parser.add_argument('--v', action='store_true', help='Output every element of each orbit')
	parser.add_argument('--j', action='store_true', help='Output data.json file')

	# Parse the arguments
	args = parser.parse_args()

	# Print arguments summary
	print_arguments_summary(args, parser)

	"""
	Initialize Default value
	"""

	# number of inputs
	n=args.n

	# number of cores
	num_cores=args.c

	# verbose output
	verbose = args.v

	# json data output
	json_data_output = args.j

	# Computing symmetric group
	permutations = generate_symmetric_group(n)

	# Computing functions
	functions = generate_functions(n)

	# Total number of functions
	size = 2**(2**n)

	# Define the chunk size
	chunk_size = 2**(n+2)

	# Define the number of jobs
	num_jobs = int(math.factorial(n) * size / chunk_size)

	# Split the list into chunks
	chunks = chunk_list(functions, chunk_size)

	with tqdm_joblib(tqdm(desc="Brut force orbit computing", total=len(permutations)*len(chunks))) as progress_bar:
		results = Parallel(n_jobs=num_cores)(delayed(task)(permutation, chunk, n) for permutation in permutations for chunk in chunks)

	# Generating vertices
	vertices = [k for k in range(size)]

	# Merging list of lists
	edges = list(itertools.chain.from_iterable(results))

	# Computing orbits
	orbits = find_connected_components(vertices, edges)

	size = len(orbits)

	# data list
	data = []

	# Printing orbits
	print(f"Set of {n}-input, 1-output Boolean functions orbits")
	for i, orbit in enumerate(orbits):
		orbit_size=len(orbit)
		signatures = [orbit[k] for k in range(len(orbit))]
		representative = signatures[0]
		if verbose:
			print(f"index: {i}, size: {orbit_size}, signatures: {signatures}")
		else:
			print(f"index: {i}, representative: {representative}")

		if json_data_output:
			if verbose:
				data += [{"index": i, "size": orbit_size, "signatures": signatures}]
			else:
				data += [{"index": i, "representative": representative}]

	if json_data_output:
		# Specify the filename
		filename = 'data.json'

		# Write the dictionary to a JSON file
		with open(filename, 'w') as file:
			json.dump(data, file, indent=4)  # indent=4 for pretty printing

	print_footer()

if __name__ == '__main__':
	main()
