import re
import os
import pandas as pd
import re
import logging
import pickle

def __get_number_serie_with_folder_name(folderName):
  return int(folderName.split("___")[0])

def __get_number_season_with_folder_name(folderName):
  return int(folderName)

def __get_number_episode_with_file_name(folderName):
  return int(folderName.split("__")[0])

def get_df_paths_episodes():
  folderTranscripts = "data/transcripts"
  regexSeriesFolderName = re.compile(r"^[0-9]*___.*")
  regexSeasonsFolderName = re.compile(r"^[0-9]+")
  regexEpisodesFolderName = re.compile(r"^[0-9]*__.*")
  allFolders = os.listdir(folderTranscripts);
  foldersSeries = [f for f in allFolders if regexSeriesFolderName.match(f)]
  foldersSeries = sorted(foldersSeries, key=__get_number_serie_with_folder_name)
  data = []

  for i in range(min(len(foldersSeries), 3)):
    folderSerie = foldersSeries[i]
    serieName = folderSerie.split("___")[1]
    logging.info("[Import] Processing folder", folderSerie, "as serie", serieName ,"...")
    logging.info("[Import] Fetching seasons ...")
    allSubfolders = os.listdir(folderTranscripts + "/" + folderSerie)
    allFoldersSeasons = [f for f in allSubfolders if regexSeasonsFolderName.match(f)]
    allFoldersSeasons = sorted(allFoldersSeasons, key=__get_number_season_with_folder_name)

    for j in range(len(allFoldersSeasons)):
      logging.info("[Import] Processing season", allFoldersSeasons[j], "...")
      folderSeason = allFoldersSeasons[j]
      logging.info("[Import] Fetching episodes ...")
      allSubfolders = os.listdir(folderTranscripts + "/" + folderSerie + "/" + folderSeason)
      allFoldersEpisodes = [f for f in allSubfolders if regexEpisodesFolderName.match(f)]
      allFoldersEpisodes = sorted(allFoldersEpisodes, key=__get_number_episode_with_file_name)

      for k in range(len(allFoldersEpisodes)):
        logging.info("[Import] Processing episode", allFoldersEpisodes[k], "...")
        folderEpisode = allFoldersEpisodes[k]
        dataEpisode = dict()
        dataEpisode["serie"] = serieName
        dataEpisode["season"] = folderSeason
        dataEpisode["episode_number"] = __get_number_episode_with_file_name(folderEpisode)
        dataEpisode["episode_name"] = folderEpisode.split("__")[1].split(".")[0]
        dataEpisode["path"] = folderTranscripts + "/" + folderSerie + "/" + folderSeason + "/" + folderEpisode
        data.append(dataEpisode)

  return pd.DataFrame(data)

def save_array_to_path(array, path):
  # Create directory if not exists
  os.makedirs(os.path.dirname(path), exist_ok=True)
  with open(path, 'wb') as file:
    pickle.dump(array, file)

def get_array_from_path(path):
   with open(path, 'rb') as file:
      return pickle.load(file)