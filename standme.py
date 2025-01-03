#!.venv/bin/python3
import csv
import jinja2
from collections import defaultdict
import click
import os


@click.command(help='Generate static standings with using shoga logs.')
@click.argument('runs', type=click.File('r'))
@click.option('--autogen', '-a', help='Autogen directory.', default='autogen', type=click.Path(exists=True, dir_okay=True, file_okay=False))
@click.option('--time', '-t', help='Submit time upper bound (seconds).', default=5 * 60 * 60)
def gen(runs, autogen, time):
	env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
	template = env.get_template('standings.html')

	dd = defaultdict(lambda: defaultdict(int))
	d = csv.DictReader(runs, delimiter=';')
	for x in d:
		if x['User_Inv'] == 'I':
			continue
		dd[x['Name']][x['Problem']] = max(dd[x['Name']][x['Problem']], int(x['Score']))

	vals = sorted(dd.items(), key=lambda x: (sum(x[1].values()), x[0]), reverse=True)
	res = template.render(vals=vals, prob=['A', 'B', 'C', 'D'])
	with open(os.path.join(autogen, 'standings.html'), 'w') as f:
		f.write(res)


if __name__ == '__main__':
	gen()