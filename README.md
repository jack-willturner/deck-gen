![alt-text](resources/logo.png)

Generating Anki decks for language learning.
  1. Sentence mining from the subtitles of your favourite TV shows.
  2. Extract the most important words from each chapter of your `epub` book.

## TV shows
Very basic functionality: put the `.xml` subtitle files into the `xml` directory. Run `python generator.py`. Import your newly generated deck into Anki and enjoy :)  

## Books (`.epub`)
You can use `python gen_from_epub.py` to get chapter-wise TF-IDF for an `.epub` book.

First, you need to `unzip <book_name>.epub`. This should split the `epub` into a set of `.htm` files that are numbered from `000` to e.g. `048` if your book had 49 chapters. You need to set the correct `BOOKNAME` variable in `gen_from_epub.py` so that these numbers can be iterated over.

## Future plans
- [ ] Tags by episode
- [ ] Difficulty heuristic
- [ ] Separate vocabulary decks
- [ ] Audio

# Acknowledgements
With all of the thanks to [genanki](https://github.com/kerrickstaley/genanki) for making my life extremely easy.
