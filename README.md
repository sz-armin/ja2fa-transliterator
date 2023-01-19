# Ja2Fa Transliterator
A simple Japanese to Persian transliteration tool based on KyTea.

## Dependencies:
You need Mykytea-python:

    % pip install kytea
    
## Usage:
 
    % python main.py "国境の長いトンネルを抜けると雪国である。"
    کُکّییُ- نُ ناگا ای تُننِرو اُ نوکِ رو تُ یوکیگونی دِ آ رو .
    
Note that you will need a shell supporting both UTF-8 and bidir text, alternatively you can copy/paste from/to an editor supporting those, such as gedit.

## Under the Hood

The process to go from Kana to the translations includes three steps. Preprocessing which handles cases such as Yō-on, the main process involving generic mapping, and postprocessing to map cases such as vowels and gemination. The order is irrelevant within each main step.

- Diacritics are always represented to avoid ambiguity. “و” is not used to represent /o/, and “ه” is not used to represent /e/ at word endings, again to avoid ambiguity.
- Yō-on is mapped individually in cases of noticeable difference in pronunciation. This step will be a preprocess.
- Gemination is represented by adding “ّ-” to the next grapheme in postprocessing. Although this is not relevant if our segmentation units are morphemes.
- Long vowels are handled by collapsing two similar vowels in postprocessing and adding a dash after applying the special rules defined on vowel mapping below:
  - あ: Is mapped to “آ” at the beginning of a word, and to “ا” in other cases.
  - い: Is mapped to “ای” at the beginning of a word, to “ِ-” after another “ِ-”, and to “ی” in other cases.
  - う: Is mapped to “او” at the beginning of a word, to “ُ-” after another “ُ-”, and to “و” in other cases.
  - え: Is mapped to “ِا” at the beginning of a word, and to “ِ-” in other cases.
  - お: Is mapped to “ُا” at the beginning of a word, and to “ُ-” in other cases.
