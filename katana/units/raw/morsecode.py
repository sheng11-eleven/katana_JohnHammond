# -* coding: utf-8 *-

from katana.unit import BaseUnit
from collections import Counter
import sys
from io import StringIO
import argparse
from pwn import *
import subprocess
from katana.units import raw
from katana import utilities
from katana.units import NotApplicable
from katana import units

class Unit(units.PrintableDataUnit):

	PRIORITY = 30

	def evaluate(self, katana, case):

		international_morse_code_mapping = {
			"di-dah":"A",
			"dah-di-di-dit":"B",
			"dah-di-dah-dit":"C",
			"dah-di-dit":"D",
			"dit":"E",
			"di-di-dah-dit":"F",
			"dah-dah-dit":"G",
			"di-di-di-dit":"H",
			"di-dit":"I",
			"di-dah-dah-dah":"J",
			"dah-di-dah":"K",
			"di-dah-di-dit":"L",
			"dah-dah":"M",
			"dah-dit":"N",
			"dah-dah-dah":"O",
			"di-dah-dah-dit":"P",
			"dah-dah-di-dah":"Q",
			"di-dah-dit":"R",
			"di-di-dit":"S",
			"dah":"T",
			"di-di-dah":"U",
			"di-di-di-dah":"V",
			"di-dah-dah":"W",
			"dah-di-di-dah":"X",
			"dah-di-dah-dah":"Y",
			"dah-dah-di-dit":"Z",
			"dah-dah-dah-dah-dah":"0",
			"di-dah-dah-dah-dah":"1",
			"di-di-dah-dah-dah":"2",
			"di-di-di-dah-dah":"3",
			"di-di-di-di-dah":"4",
			"di-di-di-di-dit":"5",
			"dah-di-di-di-dit":"6",
			"dah-dah-di-di-dit":"7",
			"dah-dah-dah-di-dit":"8",
			"dah-dah-dah-dah-dit":"9",
			"di-dah-di-dah":"ä",
			"di-dah-dah-di-dah":"á",
			"di-dah-dah-di-dah":"å",
			"dah-dah-dah-dah":"Ch",
			"di-di-dah-di-dit":"é",
			"dah-dah-di-dah-dah":"ñ",
			"dah-dah-dah-dit":"ö",
			"di-di-dah-dah":"ü",
			"di-dah-di-di-dit":"&",
			"di-dah-dah-dah-dah-dit":"'",
			"di-dah-dah-di-dah-dit":"@",
			"dah-di-dah-dah-di-dah":")",
			"dah-di-dah-dah-dit":"(",
			"dah-dah-dah-di-di-dit":":",
			"dah-dah-di-di-dah-dah":",",
			"dah-di-di-di-dah":"=",
			"dah-di-dah-di-dah-dah":"!",
			"di-dah-di-dah-di-dah":".",
			"dah-di-di-di-di-dah":"-",
			"di-dah-di-dah-dit":"+",
			"di-dah-di-di-dah-dit":"\"",
			"di-di-dah-dah-di-dit":"?",
			"dah-di-di-dah-dit":"/",
		}

		morse_alphabet = {'A': '.-',              'a': '.-',
		                 'B': '-...',            'b': '-...',
		                 'C': '-.-.',            'c': '-.-.',
		                 'D': '-..',             'd': '-..',
		                 'E': '.',               'e': '.',
		                 'F': '..-.',            'f': '..-.',
		                 'G': '--.',             'g': '--.',
		                 'H': '....',            'h': '....',
		                 'I': '..',              'i': '..',
		                 'J': '.---',            'j': '.---',
		                 'K': '-.-',             'k': '-.-',
		                 'L': '.-..',            'l': '.-..',
		                 'M': '--',              'm': '--',
		                 'N': '-.',              'n': '-.',
		                 'O': '---',             'o': '---',
		                 'P': '.--.',            'p': '.--.',
		                 'Q': '--.-',            'q': '--.-',
		                 'R': '.-.',             'r': '.-.',
		                 'S': '...',             's': '...',
		                 'T': '-',               't': '-',
		                 'U': '..-',             'u': '..-',
		                 'V': '...-',            'v': '...-',
		                 'W': '.--',             'w': '.--',
		                 'X': '-..-',            'x': '-..-',
		                 'Y': '-.--',            'y': '-.--',
		                 'Z': '--..',            'z': '--..',
		                 '0': '-----',           ',': '--..--',
		                 '1': '.----',           '.': '.-.-.-',
		                 '2': '..---',           '?': '..--..',
		                 '3': '...--',           ';': '-.-.-.',
		                 '4': '....-',           ':': '---...',
		                 '5': '.....',           "'": '.----.',
		                 '6': '-....',           '-': '-....-',
		                 '7': '--...',           '/': '-..-.',
		                 '8': '---..',           '(': '-.--.-',
		                 '9': '----.',           ')': '-.--.-',
		                 ' ': '/',               '_': '..--.-',
		                 '/': " ",               '=': '-...-'
		                 }

		final_morse_code = []
		inverse_morse_alphabet = dict((v, k) for (k, v) in morse_alphabet.items())
		token = b''
		whitespace = bytes(string.whitespace, 'utf-8')
		count = 0

		with self.target.stream as stream:
			for c in iter(lambda: stream.read(1), b''):
				if c in whitespace and len(token) > 0:
					if len(token) > 0:
						token = token.decode('utf-8')
						if token in international_morse_code_mapping:
							count += 1
							final_morse_code.append(
								international_morse_code_mapping[token]
							)
						elif token in inverse_morse_alphabet:
							count += 1
							final_morse_code.append(
								inverse_morse_alphabet[token]
							)
						token = b''
				elif c not in whitespace:
					token += c

			if len(token) > 0:
				token = token.decode('utf-8')
				if token in international_morse_code_mapping:
					count += 1
					final_morse_code.append(
						international_morse_code_mapping[token]
					)
				elif token in inverse_morse_alphabet:
					count += 1
					final_morse_code.append(
						inverse_morse_alphabet[token]
					)
				token = b''
		if ( count ):
			final_morse_code = ''.join(final_morse_code).upper().strip()

			# if this results in an emptry string, don't bother...
			if final_morse_code != '':
				# Who knows what this data may be. So scan it again!
				katana.recurse(self, final_morse_code)
				katana.add_results(self, final_morse_code)