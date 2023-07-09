import re
from tqdm.auto import tqdm
tqdm.pandas()

def remove_timecodes_and_number(text):
  """string -> Tuple(string, int, int)
  Function that removes timecodes and numbers from a string and returns the new string, the number of removed timecodes and the number of removed numbers
  """
  regexNumber = re.compile("\d+")
  # 00:12:26,680 --> 00:12:28,680
  regexTimecode = re.compile(r"^[0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3} --> [0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3}$", re.MULTILINE)
  text, count_removed_timecode = re.subn(regexTimecode, " ", text)
  text, count_removed_number = re.subn(regexNumber, " ", text)
  return text, count_removed_timecode, count_removed_number

def remove_newline_tab_return(text):
  """string ->Tuple(string, int)
  Function that removes the newline from a string and returns a new string plus the number of removed newline, tab and return
  """
  regexNewline = re.compile(r"\n")
  regexTab = re.compile(r"\t")
  regexReturn = re.compile(r"\r")

  text, count_removed_newline = re.subn(regexNewline," ",text)
  text, count_removed_tab = re.subn(regexTab," ",text)
  text, count_removed_return = re.subn(regexReturn," ",text)

  return text, count_removed_newline + count_removed_tab + count_removed_return

def remove_punctuation(text):
  """string -> Tuple(string, int)
  Function that removes punctuation from a string and returns a new string plus the number of removed punctuation
  """
  regexPunctuation = re.compile(r"[!\"#\＄%&\(\)\*\+,-\./:;<=>\?@\[\\\]\^_{\|}~]")
  text, count_removed_punctuation = re.subn(regexPunctuation," ",text)
  return text, count_removed_punctuation

def remove_multiple_spaces(text):
  """string -> Tuple(string, int)
  Function that removes multiple spaces from a string and returns a new string plus the number of removed spaces
  """
  regexMultipleSpaces = re.compile(r"\s\s+")
  text, count_removed_spaces = re.subn(regexMultipleSpaces," ",text)
  return text, count_removed_spaces
  
def remove_non_ascii(text):
  """string -> string
  Function that removes non-ascii characters from a string and returns a new string
  """
  regexNonAscii = re.compile(r"[^\x00-\x7F]+")
  text = re.sub(regexNonAscii," ",text)
  return text

def prepare_data(text):
  """string -> string
  Function that prepares a string for further processing
  """
  text, _, _ = remove_timecodes_and_number(text)
  text = remove_non_ascii(text)
  text, _ = remove_punctuation(text)
  text, _ = remove_newline_tab_return(text)
  text, _ = remove_multiple_spaces(text)
  return text

def prepare_data_in_dataframe(df):
  """Dataframe -> Dataframe
  Function that creates an new colmun on the dataframe with the transcripts pre-prepared for tokenization
  Note : ATTENTION ! Dataframe should contains a column "transcripts", she will be removed
  """
  df["transcripts_prepared_for_tokenization"] = df["transcript"].progress_apply(prepare_data)
  df.drop(columns=["transcript"], inplace=True)
  return df


