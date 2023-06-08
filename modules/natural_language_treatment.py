import swifter
import spacy
import pickle
from tqdm.auto import tqdm
import os
tqdm.pandas()

# ########################################################
#                    LEMMATIZATION
# ########################################################

def lemmatize_sentence(sentence):
  nlp = spacy.load("en_core_web_sm")
  return [word.lemma_ for word in nlp(sentence)]

def load_transcript_from_path(path):
  with open(path, 'r') as file:
    transcript = file.read()
  return transcript

def get_lemmatized_transcript_from_path(path):
  transcript = load_transcript_from_path(path)
  return lemmatize_sentence(transcript)

def save_array_to_path(array, path):
  # Create directory if not exists
  os.makedirs(os.path.dirname(path), exist_ok=True)
  with open(path, 'wb') as file:
    pickle.dump(array, file)

def lematize_transcript_and_save(path):
  lematized = get_lemmatized_transcript_from_path(path)
  save_array_to_path(lematized, 'data/lemmatized/' + path)
  del lematized

def lematize_df_path_episodes_and_save(df):
  df['path'].swifter.apply(lematize_transcript_and_save)

# ########################################################


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
   df['transcript_lemmanized'] = df['transcript_lemmanized'].progress_apply(lower_case_tab)
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
