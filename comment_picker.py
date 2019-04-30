import sys, json, bz2, gzip
from typing import BinaryIO


# stores the hashes of all the comments that have been seen; set rather than list so that an entry can be found faster
_already_seen_comments = set()


def mk_meme_corpus(infile: BinaryIO, outfile: str, min_score: int=100, min_len: int=1, max_len: int=50):
    """writes a """
    with gzip.open(outfile + ".gz", "wt", encoding="utf-8") as outfile:
        for comment in read_corpus(infile, min_score, min_len, max_len):
            if comment:
                outfile.write(comment)

def read_corpus(infile: BinaryIO, min_score, min_len, max_len):
    """iterator that goes through each line of the infile, which are presumed to be json objects, and returns the
        processed json line (see that function for more info), which is a string"""
    i = 0
    for line in infile:
        json_content = json.loads(line)
        # For testing with a smaller amount of the data:
        # i += 1
        # if i > 10000:
        #     return i
        yield process_json(json_content, min_score, min_len, max_len)

def process_json(content, min_score, min_len, max_len):
    """processes a json object content and checks if it passes the required minimal score, length and maximal length.
        returns the string if the requirements are met, and if it has not already been seen, or None if not"""
    comment: str = content["body"]
    score = content["score"]
    if not _already_seen(comment):
        length = len(comment)
        if length <= max_len and length >= min_len and score >= min_score:
            # return the newline with a simple space because the exercise states "one line, exactly one comment"
            return comment.replace("\n", " ") + "\n"
    return None

def _already_seen(comment: str):
    """checks if the string has already been seen via hashes"""
    h = hash(comment)
    if h in _already_seen_comments:
        return True
    # hash has to be added only once and not everytime it occurs, should save some memory
    else:
        _already_seen_comments.add(h)

def main():
    with bz2.open(sys.argv[1], "rb") as file:
       mk_meme_corpus(file, "new_reddit_corpus")

if __name__ == "__main__":
    main()