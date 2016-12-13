import three

if __name__ == "__main__":
	decoded = []

	with open("./data/4.txt", "r") as file:
		for line in file:
			line = line.strip()
			decoding_byte = three.try_decode_single_xor(line)
			decoded.append(three.xor_hexstring_with_one_byte(line, decoding_byte))

	scores = [three.text_score(decoded_line) for decoded_line in decoded]
	print(decoded[scores.index(max(scores))])