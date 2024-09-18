from setuptools import setup, find_packages

setup(
	name="group_action",
	version="0.2.15",
	author="ant1sir",
	author_email="antoine@sirianni.ai",
	description="A Python package for group action.",
	long_description=open('README.md').read(),
	long_description_content_type='text/markdown',
	url="https://github.com/ant1sir/group_action",  # replace with your repo URL if you have one
	packages=find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.10',
	install_requires=[
		'joblib>=1.4.2',
		'tqdm>=4.66.4'
	],
	entry_points={
		'console_scripts': [
			'orbits = group_action.orbits:main',
			'conjugacy_classes = group_action.conjugacy_classes:main',
			'burnside = group_action.burnside:main',
		],
	},

)

