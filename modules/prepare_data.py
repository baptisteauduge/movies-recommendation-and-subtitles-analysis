import re
def remove_timecodes_and_number(text):
  """string -> Tuple(string, int, int)
  Function that removes timecodes and numbers from a string and returns the new string, the number of removed timecodes and the number of removed numbers
  """
  regexNumber = re.compile(r"^[0-9]*$", re.MULTILINE)
  # 00:12:26,680 --> 00:12:28,680
  regexTimecode = re.compile(r"^[0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3} --> [0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3}$", re.MULTILINE)
  text, count_removed_timecode = re.subn(regexTimecode, "", text)
  text, count_removed_number = re.subn(regexNumber, "", text)
  return text, count_removed_timecode, count_removed_number

def remove_newline_from_text(text):
  """string ->Tuple(string, int)
  Function that removes the newline from a string and returns a new string plus the number of removed newline
  """
  regexNewline = re.compile(r"\n")
  text, count_removed_newline = re.subn(regexNewline,"",text)
  return text, count_removed_newline

def remove_punctuation_from_text(text):
  """string -> Tuple(string, int)
  Function that removes punctuation from a string and returns a new string plus the number of removed punctuation
  """
  regexPunctuation = re.compile(r"[!\"#\＄%&\'\(\)\*\+,-\./:;<=>\?@\[\\\]\^_`{\|}~]")
  text, count_removed_punctuation = re.subn(regexPunctuation," ",text)
  return text, count_removed_punctuation
