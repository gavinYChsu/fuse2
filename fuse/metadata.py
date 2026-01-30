METADATA =\
{
	'name': 'Fuse',
	'description': 'Next generation face swapper and enhancer',
	'version': '1.3.1',
	'license': 'MIT',
	'author': 'Henry Ruhs',
	'url': 'https://fuse.io'
}


def get(key : str) -> str:
	return METADATA[key]
