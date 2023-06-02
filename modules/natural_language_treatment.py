import nltk
import pandas as pd
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from tqdm.auto import tqdm
import spacy

tqdm.pandas()
nlp = spacy.load("en_core_web_sm")


# def tokenization(df):
#   """Dataframe -> Dataframe
#   Function that tokenize transcripts that are prepared for tokenization
#   """

#   df["transcripts_prepared_for_tokenization"] = df["transcripts_prepared_for_tokenization"].astype(str)
#   df["transcript_tokenized"] = df["transcripts_prepared_for_tokenization"].apply(word_tokenize)

#   return df

# def __lemmatize_word(token):
#     lemma = WordNetLemmatizer().lemmatize(token, pos='v')
#     print('Token is ' + token + ' lemma is ' + lemma)
#     if lemma == token:
#         lemma = WordNetLemmatizer().lemmatize(token, pos='n')
#     print('Token is ' + token + ' lemma is ' + lemma)
#     if lemma == token:
#         lemma = WordNetLemmatizer().lemmatize(token, pos='a')
#     print('Token is ' + token + ' lemma is ' + lemma)
#     if lemma == token:
#         lemma = WordNetLemmatizer().lemmatize(token, pos='r')
#     print('Token is ' + token + ' lemma is ' + lemma)
#     if lemma == token:
#         lemma_synsets = wordnet.synsets(token)
#         if len(lemma_synsets) > 0:
#             lemma = lemma_synsets[0].lemmas()[0].name()
#     print('Token is ' + token + ' lemma is ' + lemma)
#     return lemma

def __lemmatize_text(text):
  """text -> Arraytext
  Function that lemmatize an array text
  """
  if type(text) != str:
    return []
  
  doc = nlp(text)
  return [token.lemma_ for token in doc if token.lemma_ != ' ' and token.lemma_ != '']

def lemmatize_df(df):
  """DataFrame -> Null
  Function that lemanize the tokens from a dataframe 
  """
  df['transcript_lemmanized'] = df.transcripts_prepared_for_tokenization.progress_apply(__lemmatize_text)
  res = df.drop('transcripts_prepared_for_tokenization', axis=1)

  return res

def lower_case_tab(tab):
   """Array_text -> Array_text
   Function that lower case an array text
   """
   res = []
   for word in tab:
      if type(word) == str:
         res.append(word.lower())
   return res

def lower_case_transcript_lemmanized(df):
   """
   DataFrame -> DataFrame
   Function that lower case the transcript_lemmanized column
   """
   for i in tqdm(range(len(df))):
      df.iloc[i]['transcript_lemmanized'] = lower_case_tab(df.iloc[i]['transcript_lemmanized'])
   return df

def get_occurence_from_list_lem(array_lem):
   """Array_text -> Dict
   Function that returns the occurence from every word
   """
   res = dict()
   for lem in array_lem:
      if lem in res:
         res[lem] += 1
      else:
         res[lem] = 1 
   
   return res

def get_occurence_from_df_ep(df):
   """Dataframe -> Dataframe
   Function that counts the occurence of the words of a dataframe per ep
   """

   df["occurence_ep"] = df["transcript_lemmanized"].progress_apply(get_occurence_from_list_lem)
   return df

def get_frequencies_from_dict(dict_occ):
   """Dict -> Dict
   Function that returns the frequencies of the words of a dict
   """

   total = 0
   res = dict()
   for key in dict_occ:
      total += dict_occ[key]
   for key in dict_occ:
      res[key] = dict_occ[key]/total
   
   return res

def get_frequencies_from_df_ep_occ(df):
   """Dataframe -> Dataframe
   Function that returns the frequencies of the words of a dataframe per ep
   """

   df["frequencies_ep"] = df["occurence_ep"].progress_apply(get_frequencies_from_dict)
   return df

def get_occurence_from_df_serie(df):
   """Dataframe -> Dataframe
   Function that returns a new dataframe with the dictionary of occurence of the words
   """

   last_serie = df.iloc[0]["serie"]
   list_lem_serie = []
   res = dict()

   for i in tqdm(range(len(df))):

    if df.iloc[i]['serie'] == last_serie:
      list_lem_serie += df.iloc[i]["transcript_lemmanized"]
   
    else:
      res[last_serie] = get_occurence_from_list_lem(list_lem_serie)
      last_serie = df.iloc[i]['serie']
      list_lem_serie = df.iloc[i]['transcript_lemmanized']
   
   res[last_serie] = get_occurence_from_list_lem(list_lem_serie)
   return res
