import nltk
import pandas as pd
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

def tokenization(df):
  """Dataframe -> Dataframe
  Function that tokenize transcripts that are prepared for tokenization
  """

  df["transcripts_prepared_for_tokenization"] = df["transcripts_prepared_for_tokenization"].astype(str)
  df["transcript_tokenized"] = df["transcripts_prepared_for_tokenization"].apply(word_tokenize)

  return df
      
def remove_not_english(df):
  """Dataframe -> DataFrame
  Function that removes the series without english 
  Attention: the transcript must be tokenized
  """
  toDelete = set()

  for i in range(len(df)):
    text = df.iloc[i]['transcript_tokenized']

    languages_shared_words = {}
    # tokenization en mots
    for language in stopwords.fileids():
        # stopwords pour chaque langue
        stopwords_liste = stopwords.words(language)
        # on retire les doublons
        text = set(text)
        # les mots communs entre stopwords 
        # d'une langue et les mots de message
        common_elements = text.intersection(stopwords_liste)
        # ajout du couple au dictionnaire
        languages_shared_words[language] = len(common_elements)
    # on retourne la langue avec le max de mots commun
    if (max(languages_shared_words, key = languages_shared_words.get) != 'english'):
      toDelete.add(df.iloc[i]['path'])
  
  for ep in toDelete:
     df.drop(ep, axis = 0)
  
  return df

def tag_word(array_text):
   nltk.pos_tag(array_text)

def __lemmatize_word(token):
    lemma = WordNetLemmatizer().lemmatize(token, pos='v')
    if lemma == token:
        lemma = WordNetLemmatizer().lemmatize(token, pos='n')
    if lemma == token:
        lemma = WordNetLemmatizer().lemmatize(token, pos='a')
    if lemma == token:
        lemma = WordNetLemmatizer().lemmatize(token, pos='r')
    if lemma == token:
        lemma_synsets = wordnet.synsets(token)
        if len(lemma_synsets) > 0:
            lemma = lemma_synsets[0].lemmas()[0].name()
    return lemma

def __lematize_array(array_text):
   """Arraytext -> Arraytext
   Function that lematize an array text
   """
   
   return [__lemmatize_word(text) for text in array_text]

def lemanization(df):
   """DataFrame -> Dataframe
   Function that lemanize the tokens from a dataframe 
   """

   df["transcript_lemanized"] = df["transcript_tokenized"].apply(__lematize_array)

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

   df["occurence_ep"] = df["transcript_lemanized"].apply(get_occurence_from_list_lem)

def get_occurence_from_df_serie(df):
   """Dataframe -> Dataframe
   Function that returns a new dataframe with the dictionary of occurence of the words
   """

   last_serie = df.iloc[0]["serie"]
   list_lem_serie = []
   res = dict()

   for i in range(len(df)):

    if df.iloc[i]['serie'] == last_serie:
      list_lem_serie += df.iloc[i]["transcript_lemanized"]
   
    else:
      res[last_serie] = get_occurence_from_list_lem(list_lem_serie)
      last_serie = df.iloc[i]['serie']
      list_lem_serie = df.iloc[i]['transcript_lemanized']
   
   res[last_serie] = get_occurence_from_list_lem(list_lem_serie)
   return pd.DataFrame(res)
         
