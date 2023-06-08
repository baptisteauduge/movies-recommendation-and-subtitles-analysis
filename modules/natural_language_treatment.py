import swifter
import spacy
import modules.prepare_data as prepare_data
import modules.import_data as import_data
import pandas as pd
from tqdm import tqdm

# ########################################################
#                    LEMMATIZATION
# ########################################################

nlp = spacy.load("en_core_web_sm", disable=['parser', 'ner', 'textcat', 'tokenizer', 'senter', 'sentencizer'])

def lemmatize_batch(batch):
   res = []
   for doc in nlp.pipe(batch, batch_size=50, n_process=-1):
      res.append([word.lemma_.lower() for word in doc if word.lemma_ != ' ' and word.lemma_[0] != "'" and word.lemma_[0] != '-'])
   return res

def load_transcript_from_path(path):
   with open(path, 'r', encoding='utf-8', errors='ignore') as file:
      transcript = file.read().replace('\ufffd', ' ')
   return transcript

def tokenize_and_lemmatize_df_path_episodes_and_save(df, batch_size=200):

   size = len(df)
   for i in tqdm(range(0, len(df), batch_size)):
      batch_transcripts = pd.Series([load_transcript_from_path(df['path'][j]) for j in range(i, min(i + batch_size, size))])
      batch_tokenized_transcripts = batch_transcripts.swifter.progress_bar(False).apply(prepare_data.prepare_data)
      del batch_transcripts
      batch_lemmatized_transcripts = lemmatize_batch(batch_tokenized_transcripts)
      del batch_tokenized_transcripts
      # Saving the lemmatized transcripts in a file with the same name as the original transcript
      print("Saving batch " + str(i) + " to " + str(min(i + batch_size, size)) + "...")
      for j in range(i, min(i + batch_size, size)):
         print("Saving " + df['path'][j].replace('data/transcripts/', 'data/lemmatized/'))
         import_data.save_array_to_path(batch_lemmatized_transcripts[j - i],  df['path'][j].replace('data/transcripts/', 'data/lemmatized/'))

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
