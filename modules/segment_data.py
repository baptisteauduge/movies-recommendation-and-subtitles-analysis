from tqdm.auto import tqdm
import pandas as pd

def filter_df_freq_episode_freq_between(freq_min, freq_max, dfTranscriptsLemmaWithFreq):
    """
    Function that returns a dataframe with all the episodes 
    but the token returned will have a frequency between freq_min and freq_max
    """
    res_df = []
    pd.DataFrame(columns = ["serie", "season", "episode", "name_episode", "frequencies_ep"])
    for i in tqdm(range(len(dfTranscriptsLemmaWithFreq))):
      new_dict_freq = dict()
      for (token, freq) in dfTranscriptsLemmaWithFreq.iloc[i]["frequencies_ep"].items():
          if freq >= freq_min and freq <= freq_max:
              new_dict_freq[token] = freq
      res_df.append({"serie": dfTranscriptsLemmaWithFreq.iloc[i]["serie"],
                    "season": dfTranscriptsLemmaWithFreq.iloc[i]["season"],
                    "num_episode": dfTranscriptsLemmaWithFreq.iloc[i]["nb_episode"],
                    "name_episode": dfTranscriptsLemmaWithFreq.iloc[i]["name_episode"],
                    "frequencies_ep": new_dict_freq})  

    return pd.DataFrame(res_df)

def create_vector_token_ep(df_freq):
    """
    Function that returns a List of the tokens that will be used
    as a dimension of the vector
    """

    set_token = set()
    for i in tqdm(range(len(df_freq))):
        for token in df_freq.iloc[i]["frequencies_ep"]:
            set_token.add(token)
    return list(set_token)


