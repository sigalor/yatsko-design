#!/usr/bin/env python3

import math
import svgwrite
import argparse

def pisano(modulus, factor):
	if modulus <= 1:
		return []

	ret = [0, 1]
	while True:
		ret.append((ret[-1] + ret[-2]) % modulus)
		if len(ret) >= 4 and ret[0] == ret[-2] and ret[1] == ret[-1]:
			ret = ret[:-2]
			break
	return [x * factor % modulus for x in ret]

def adjacent_pairs(arr):
	ret = set()
	for i, n in enumerate(arr[:-1]):
		if n == arr[i+1]:
			continue
		ret.add((min(n, arr[i+1]), max(n, arr[i+1])))
	return ret

def get_circle_point(step, modulus, size):
	angle_step = 2.0 * math.pi / modulus
	angle = angle_step * step - math.pi / 2
	return ((math.cos(angle) + 1) * size / 2, (math.sin(angle) + 1) * size / 2)

# draws the design 'modulus' over 'factor' (see https://www.youtube.com/watch?v=o1eLKODSCqw, 12:00 min)
def draw_svg(filename, modulus, factor, size):
	svg = svgwrite.Drawing(filename, profile="tiny", size=(size, size))
	line_pairs = adjacent_pairs(pisano(modulus, factor))

	svg.add(svg.rect((0, 0), (size, size), fill="#f3ff00"))
	svg.add(svg.circle((size/2, size/2), size/2, stroke="black", fill="none"))
	for (frm, to) in line_pairs:
		svg.add(svg.line(get_circle_point(frm, modulus, size), get_circle_point(to, modulus, size), stroke="black"))
	svg.save()



parser = argparse.ArgumentParser()
parser.add_argument("-f", "--factor", help="the factor to multiply Fibonacci sequence items by before taking the modulo, default: 1", type=int, default=1)
parser.add_argument("-s", "--size", help="the dimensions of the square output SVG, default: 500", type=int, default=500)
required_named = parser.add_argument_group("required named arguments")
required_named.add_argument("-m", "--modulus", help="the modulus for taking the remainder of Fibonacci sequence items", type=int, required=True)
required_named.add_argument("-o", "--output", help="the filename of the output SVG", required=True)
args = parser.parse_args();

draw_svg(args.output, args.modulus, args.factor, args.size)





