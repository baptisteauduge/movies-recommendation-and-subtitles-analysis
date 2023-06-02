import os
import pandas as pd
import re
import logging

def __get_number_serie_with_folder_name(folderName):
  return int(folderName.split("___")[0])

def __get_number_season_with_folder_name(folderName):
  return int(folderName)

def __get_number_episode_with_file_name(folderName):
  return int(folderName.split("__")[0])

def import_transcripts(nbSeries):
  """int -> DataFrame
  Function that imports the transcripts of the first nbSeries series
  Note: You should add in a .env file the path to the folder containing the transcripts in the PATH_FOLDER_TRANSCRIPTS variable
  Folders are considered as series if they match the following regex: r"^[0-9]*__.*" (i.e. only numbers with a double underscore)
  Folders are considered as seasons if they match the following regex: r"^[0-9]+" (i.e. only numbers)
  Files are considered as episodes if they match the following regex: r"^[0-9]*__.*" (i.e. only numbers with a double underscore)
  And file structure should be:
  - PATH_FOLDER_TRANSCRIPTS
    - 1___Serie1
      - 1    (Season 1)
        - 1__Episode1.txt
  """
  folderTranscripts = "data/transcripts"
  regexSeriesFolderName = re.compile(r"^[0-9]*___.*")
  regexSeasonsFolderName = re.compile(r"^[0-9]+")
  regexEpisodesFolderName = re.compile(r"^[0-9]*__.*")


  allFolders = os.listdir(folderTranscripts);
  foldersSeries = [f for f in allFolders if regexSeriesFolderName.match(f)]
  foldersSeries = sorted(foldersSeries, key=__get_number_serie_with_folder_name)

  data = []
  for i in range(min(nbSeries, len(foldersSeries))):
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
        dataEpisode["nb_episode"] = __get_number_episode_with_file_name(folderEpisode)
        dataEpisode["name_episode"] = folderEpisode.split("__")[1].split(".")[0]
        dataEpisode["transcript"] = ""
        dataEpisode["path"] = folderTranscripts + "/" + folderSerie + "/" + folderSeason + "/" + folderEpisode
        with open(folderTranscripts + "/" + folderSerie + "/" + folderSeason + "/" + folderEpisode, "r", encoding="latin1") as f:
          dataEpisode["transcript"] = f.read()
        data.append(dataEpisode)
  return pd.DataFrame(data)
