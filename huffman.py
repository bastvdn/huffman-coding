import heapq
import os
from copy import deepcopy

import time
from termcolor import colored, cprint
import msvcrt as m
from pynput import mouse, keyboard

"""
author: Bhrigu Srivastava
website: https:bhrigu.me
"""


# def on_press(key):
#     try:
#         print('alphanumeric key {0} pressed'.format(
#             key.char))
#     except AttributeError:
#         print('special key {0} pressed'.format(
#             key))
#
# def on_release(key):
#     print('{0} released'.format(
#         key))
#     if key == keyboard.Key.esc:
#         Stop listener
# return False
#
# with keyboard.Listener(
#         on_press=on_press,
#         on_release=on_release) as listener:
#     listener.join()


class HuffmanCoding:
    def __init__(self, path):
        self.path = path
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}

    class HeapNode:
        def __init__(self, char, freq):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None

        # defining comparators less_than and equals
        def __lt__(self, other):
            return self.freq < other.freq

        def __eq__(self, other):
            if (other == None):
                return False
            if (not isinstance(other, HeapNode)):
                return False
            return self.freq == other.freq

    # functions for compression:

    def make_frequency_dict(self, text):
        frequency = {}
        for character in text:
            if not character in frequency:
                frequency[character] = 0
            frequency[character] += 1
        return frequency

    def make_frequency_dict_repr(self, text):
        frequency = {}
        i = 0

        # print(colored(displayedText,'red',attrs=['reverse']))
        flag_fast = False
        while i < len(text):
            if i < len(text)-30:
                displayedText = text[i + 1:i + 30] + '...'
            else:
                displayedText = text[i + 1:i + 30]
            if not text[i] in frequency:
                frequency[text[i]] = 0
            frequency[text[i]] += 1
            # y = input("ok")

            os.system('cls')

            frequencyText = sorted(frequency.items(), key=lambda x: x[1], reverse=True)

            letterText = ''
            letterValue = ''

            for n in frequencyText:
                if n[0] != frequencyText[-1][0]:
                    letterText += n[0] + '  '
                    if n[1] < 10:
                        letterValue += str(n[1]) + '  '
                    else:
                        letterValue += str(n[1]) + ' '
                else:
                    letterText += n[0]
                    letterValue += str(n[1])

            print('{: ^100}'.format(letterText))
            print('{: ^100}'.format(letterValue))
            print(colored(text[i], 'red', attrs=['reverse']), end='')
            print(colored(displayedText, 'red'))
            if not flag_fast:
                comm = m.getch()
            else:
                time.sleep(0.05)
            if comm == b'H':
                flag_fast = True

            i += 1
        input("Frequency analysis complete push any button")
        return frequency

    def make_heap(self, frequency):
        for key in frequency:
            node = self.HeapNode(key, frequency[key])
            heapq.heappush(self.heap, node)

    def merge_nodes_repr(self):
        merge_text = []
        for n in self.heap:
            to_visit = [[n],[]]

            line = ''
            while to_visit[0]:
                current = to_visit[0].pop(0)


                if not current.left and not current.right:
                    line += str(current.char) + ':' + str(current.freq) + ' '
                else:
                    line += str(current.freq) + '  '

                if current.left:
                    to_visit[1].append(current.left)

                if current.right:
                    to_visit[1].append(current.right)
                if not to_visit[0]:
                    merge_text.append(line)
                    line=''
                    to_visit[0] = deepcopy(to_visit[1])
                    to_visit[1] = []




        for line in merge_text:
            print('{:^100}'.format(line))
            print()


    def merge_nodes(self):
        while (len(self.heap) > 1):
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            merged = self.HeapNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            heapq.heappush(self.heap, merged)

    def make_codes_helper(self, root, current_code):
        if (root == None):
            return

        if (root.char != None):
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return

        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")

    def make_codes(self):
        root = heapq.heappop(self.heap)
        current_code = ""
        self.make_codes_helper(root, current_code)
        #print(self.codes)

    def get_encoded_text(self, text):
        encoded_text = ""
        for character in text:
            encoded_text += self.codes[character]
        #print(encoded_text)
        return encoded_text

    def get_encoded_text_repr(self, text):
        encoded = ''
        i = 0
        flag_fast = False
        # print(colored(displayedText,'red',attrs=['reverse']))

        while i < len(text):
            if i < len(text)-30:
                displayedText = text[i + 1:i + 30] + '...'
            else:
                displayedText = text[i + 1:i + 30]
            # y = input("ok")

            os.system('cls')

            print(colored(self.codes[text[i]], 'blue', attrs=['reverse']), end='')
            print(colored(encoded, 'blue'))
            encoded += self.codes[text[i]]
            print(colored(text[i], 'red', attrs=['reverse']), end='')
            print(colored(displayedText, 'red'))

            if not flag_fast:
                comm = m.getch()
            else:
                time.sleep(0.05)
            if comm == b'H':
                flag_fast = True

            i += 1
        return None

    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        #print(len(encoded_text) % 8)
        for i in range(extra_padding):
            encoded_text += "0"

        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        #print(encoded_text)

        return encoded_text

    def pad_encoded_text_repr(self, encoded_text):
        os.system('cls')
        print(colored(encoded_text, 'red'))
        m.getch()
        time.sleep(1)
        os.system('cls')
        print(colored(encoded_text, 'red'))

        extra_padding = 8 - len(encoded_text) % 8
        print(colored('Adding pad : {}'.format(extra_padding), 'blue'))
        m.getch()
        time.sleep(1)
        print(colored(encoded_text, 'red'), end='')
        print(colored('0'*extra_padding,'blue',attrs=['reverse']))
        # print(len(encoded_text) % 8)
        for i in range(extra_padding):
            encoded_text += "0"
        m.getch()

        padded_info = "{0:08b}".format(extra_padding)
        print(colored('Adding padded_info : {0:08b}'.format(extra_padding), 'blue'))
        time.sleep(1)
        print(colored(padded_info,'blue',attrs=['reverse']), end='')
        print(colored(encoded_text, 'red'), end='')
        print(colored('0' * extra_padding, 'blue'))
        encoded_text = padded_info + encoded_text
        m.getch()
        os.system('cls')

        return encoded_text

    def get_byte_array(self, padded_encoded_text):
        if (len(padded_encoded_text) % 8 != 0):
            print("Encoded text not padded properly")
            exit(0)

        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i + 8]
            b.append(int(byte, 2))

        return b

    def compress(self):
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + ".bin"

        with open(self.path, 'r+') as file, open(output_path, 'wb') as output:
            text = file.read()
            text = text.rstrip()

            frequency = self.make_frequency_dict(text)
            #self.make_frequency_dict_repr(text)
            self.make_heap(frequency)

            self.merge_nodes()
            #self.merge_nodes_repr()

            self.make_codes()

            #self.get_encoded_text_repr(text)

            encoded_text = self.get_encoded_text(text)
            padded_encoded_text = self.pad_encoded_text(encoded_text)

            #self.pad_encoded_text_repr(encoded_text)

            b = self.get_byte_array(padded_encoded_text)


            output.write(bytes(b))

        print("Compressed")
        return output_path

    """ functions for decompression: """

    def remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)

        padded_encoded_text = padded_encoded_text[8:]
        encoded_text = padded_encoded_text[:-1 * extra_padding]

        return encoded_text

    def decode_text(self, encoded_text):
        current_code = ""
        decoded_text = ""

        for bit in encoded_text:

            current_code += bit
            if (current_code in self.reverse_mapping):
                character = self.reverse_mapping[current_code]
                decoded_text += character
                current_code = ""

        return decoded_text

    def decompress(self, input_path):
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + "_decompressed" + ".txt"

        with open(input_path, 'rb') as file, open(output_path, 'w') as output:
            bit_string = ""

            byte = file.read(1)
            while (len(byte) > 0):
                print(byte)
                byte = ord(byte)
                print(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                print(bits)
                print("--------------")
                bit_string += bits
                byte = file.read(1)

            encoded_text = self.remove_padding(bit_string)

            decompressed_text = self.decode_text(encoded_text)

            output.write(decompressed_text)

        print("Decompressed")
        return output_path


path = "test.txt"

h = HuffmanCoding(path)
h.compress()

class Node(object):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


class BinarySearchTree(object):
    def __init__(self, value):
        self.root = Node(value)

    def insert(self, value):
        current = self.root
        while current:
            if value > current.value:
                if current.right is None:
                    current.right = Node(value)
                    break
                else:
                    current = current.right
            else:
                if current.left is None:
                    current.left = Node(value)
                    break
                else:
                    current = current.left

    def breadth_first_search(self, root=None):
        repre = []
        root = self.root if root is None else root
        to_visit = [root]
        line = ""
        while to_visit:

            current = to_visit.pop(0)

            if current.left:
                to_visit.append(current.left)
                line += str(current.left.value) + ' '
            if current.right:
                to_visit.append(current.right)
                if current.right.right:
                    line += str(current.right.value)
                else:
                    repre.append(line)
                    line = ""

        for n in repre:
            print('{:*^100}'.format(n))


# t = BinarySearchTree(100)
# t.insert(12)
# t.insert(8)
# t.insert(112)
# t.insert(123)
# t.insert(2)
# t.insert(11)
# t.insert(52)
# t.insert(3)
# t.insert(66)
# t.insert(10)
#
# print("Output of Breadth First search is ")
# t.breadth_first_search(t.root)
#