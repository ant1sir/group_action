from group_action import __version__, __num_of_cores__
from group_action.library import *

def conjugation(perm1, perm2):
	"""
	Compute conjugation of permutation #1 on permutation #2
	"""
	n=len(perm1)
	inverse = compute_permutation_inverse(perm1)
	conjugate = [perm1[perm2[inverse[k]]] for k in range(n)]
	return conjugate

def task(permutation1, chunk, n):
	"""
	Atomic task
	"""
	partial_edges = []
	for permutation2 in chunk:
		conjugate = conjugation(permutation1, permutation2)
		partial_edges += [(",".join(map(str,permutation2)), ",".join(map(str,conjugate)))]
	return partial_edges

def main():
	print_header()

	# Create the parser
	parser = argparse.ArgumentParser(description='Brut force computation of conjugacy classes of the symmetric group Sn.')

	# Add the arguments
	parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
	parser.add_argument('--n', type=int, default=2, help='Number of elements in S')
	parser.add_argument('--c', type=int, default=__num_of_cores__, help='Number of cores')
	parser.add_argument('--v', action='store_true', help='Output every element of each orbit')
	parser.add_argument('--j', action='store_true', help='Output data.json file')

	# Parse the arguments
	args = parser.parse_args()

	# Print arguments summary
	print_arguments_summary(args, parser, __version__)

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

	# Total number of permutations
	size = math.factorial(n)

	# Define the chunk size
	chunk_size = 2**(math.floor(n/2))

	# Define the number of jobs
	num_jobs = int(size / chunk_size)

	# Split the list into chunks
	chunks = chunk_list(permutations, chunk_size)

	with tqdm_joblib(tqdm(desc="Brut force orbit computing", total=len(permutations)*len(chunks))) as progress_bar:
		results = Parallel(n_jobs=num_cores)(delayed(task)(permutation, chunk, n) for permutation in permutations for chunk in chunks)

	# Generating vertices
	vertices = [",".join(map(str,permutation)) for permutation in permutations]

	# Merging list of lists
	edges = list(itertools.chain.from_iterable(results))

	# Computing orbits
	orbits = find_connected_components(vertices, edges)

	size = len(orbits)

	# data list
	data = []

	# Printing orbits
	print(f"Set of conjugacy classes")
	for i, orbit in enumerate(orbits):
		orbit_size=len(orbit)
		representative = orbit[0]
		if verbose:
			if orbit_size>1:
				elements = [f"{orbit[k]}" for k in range(len(orbit))]
				print(f"index: {i+1}, {len(orbit)} elements: {elements}")
			else:
				print(f"index: {i+1}, 1 representative: {representative}")
		else:
			print(f"index: {i+1}, representative: {representative}")

		if json_data_output:
			data += [{"index": i, "size": orbit_size, "representative": representative}]

	if json_data_output:
		# Specify the filename
		filename = 'data.json'

		# Write the dictionary to a JSON file
		with open(filename, 'w') as file:
			json.dump(data, file, indent=4)  # indent=4 for pretty printing

	print_footer()

if __name__ == '__main__':
	main()
