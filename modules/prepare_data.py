import re
def remove_timecodes_and_number(text):
  """string -> Tuple(string, int, int)
  Function that removes timecodes and numbers from a string and returns the new string, the number of removed timecodes and the number of removed numbers
  """
  regexNumber = re.compile(r"[0-9]*")
  # 00:12:26,680 --> 00:12:28,680
  regexTimecode = re.compile(r"^[0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3} --> [0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3}$", re.MULTILINE)
  text, count_removed_timecode = re.subn(regexTimecode, "", text)
  text, count_removed_number = re.subn(regexNumber, "", text)
  return text, count_removed_timecode, count_removed_number

def remove_newline(text):
  """string ->Tuple(string, int)
  Function that removes the newline from a string and returns a new string plus the number of removed newline
  """
  regexNewline = re.compile(r"\n")
  text, count_removed_newline = re.subn(regexNewline,"",text)
  return text, count_removed_newline

def remove_punctuation(text):
  """string -> Tuple(string, int)
  Function that removes punctuation from a string and returns a new string plus the number of removed punctuation
  """
  regexPunctuation = re.compile(r"[!\"#\＄%&\'\(\)\*\+,-\./:;<=>\?@\[\\\]\^_`{\|}~]")
  text, count_removed_punctuation = re.subn(regexPunctuation," ",text)
  return text, count_removed_punctuation

def remove_multiple_spaces(text):
  """string -> Tuple(string, int)
  Function that removes multiple spaces from a string and returns a new string plus the number of removed spaces
  """
  regexMultipleSpaces = re.compile(r"\s\s+")
  text, count_removed_spaces = re.subn(regexMultipleSpaces," ",text)
  return text, count_removed_spaces
  
def convert_to_lowercase(text):
  """string -> string
  Function that converts a string to lowercase
  """
  return text.lower()

def prepare_data(text):
  """string -> string
  Function that prepares a string for further processing
  """
  text, _, _ = remove_timecodes_and_number(text)
  text, _ = remove_newline(text)
  text, _ = remove_punctuation(text)
  text, _ = remove_multiple_spaces(text)
  text = convert_to_lowercase(text)
  return text

def prepare_data_in_dataframe(df):
  """Dataframe -> Dataframe
  Function that creates an new colmun on the dataframe with the transcripts pre-prepared for tokenization
  Note : ATTENTION ! Dataframe should contains a column "transcripts"
  """
  newDf = df.copy()
  newDf["transcripts_prepared_for_tokenization"] = newDf["transcript"].apply(prepare_data)

  return newDf