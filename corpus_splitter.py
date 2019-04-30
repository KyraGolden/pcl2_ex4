import sys, gzip
from lxml import etree
from typing import BinaryIO
import random


class BufferedWriter:

    _data = []
    _dir = None
    _count = 0
    n = 0

    def __init__(self, outdir, n = 10000):
        self._dir = outdir
        self.n = n

    def write_buffered(self, data):
        self._data.append(data)
        self._count += 1
        # only write if there are more than n entries
        if self._count > self.n:
            with open(self._dir, "a+") as file:
                file.writelines(self._prepared_data())
            self._data = []
            self._count = 0

    def force_write(self):
        """at the end, writing has to happen, whether there are n elements in the list or not"""
        with gzip.open(self._dir, "ab+") as file:
            file.write(self._prepared_data())
        self._data = []
        self._count = 0

    def _prepared_data(self):
        return ('\n'.join(self._data)).encode()


def split_corpus(infile: BinaryIO, targetdir: str, n: int = 1000):
    training_writer = BufferedWriter(targetdir + "/abstracts.txt.training.gz")
    dev, test = assign_to_sets(iter_read_xml_corpus(infile), n, targetdir, training_writer)
    # ensure that the last portion of data is written to the training-set
    training_writer.force_write()
    # should not need a buffered writer as the training-set since it already happens at once
    with gzip.open(targetdir + "/abstracts.txt.development.gz", "wb+") as file:
        file.write('\n'.join(dev).encode())
    with gzip.open(targetdir + "/abstracts.txt.test.gz", "wb+") as file:
        file.write('\n'.join(test).encode())


def assign_to_sets(content, n, targetdir, training_writer):
    """assigns the content (of an abstract, in this case) to either the trainings-, the development- or the test-set
        and finally returns these sets"""
    reservoir = []
    for t, abstract in enumerate(content):
        # the reservoir is 2 times the size of n because a test- and a dev-set have to be created. the reservoir will be
        # split in the end, so that both sets are created
        if t < (n * 2):
            reservoir.append(abstract)
        else:
            m = random.randint(0,t)
            if m < (n * 2):
                # if something drops out of the reservoir (i.e., is replaced), it gets written into the training-set
                abstract, reservoir[m] = reservoir[m], abstract
                training_writer.write_buffered(abstract)
    return split_dev_and_test_set(reservoir, n, n)


def iter_read_xml_corpus(infile: BinaryIO):
    """takes the argument infile (the corpus opened in binary reading mode) and yields the sentences of each document
        as strings concatenated with a space"""
    # for testing with a small amount of the data:
    i = 0
    for event, element in etree.iterparse(infile, tag="document"):
        sentences = []
        for elem in element.findall("section"):
            for sentence in elem.findall("sentence"):
                sentences.append(sentence.text)
            elem.clear()
        element.clear()
        yield ''.join(sentences)
        i += 1
        if i > 400: break


def split_dev_and_test_set(l, *k):
    """
    Splits a list :param l into chunks of size n for all n in :param k
    """
    start = 0
    for size in k:
        yield l[start: start+size]
        start += size

def iter_sentences(infile):
    for line in infile:
        yield line

def main():
    with gzip.open(sys.argv[1], "rb") as infile:
        split_corpus(infile, "./corpus_dir", 4)

if __name__ == '__main__':
    main()