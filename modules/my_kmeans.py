from sklearn.cluster import KMeans
import pandas as pd
import numpy as np

class My_Kmeans:

  def __init__(self, nb_clusters, random_state = 0):
    self.nb_clusters = nb_clusters
    self._kmeans = KMeans(n_clusters=nb_clusters, random_state=100)
    self._kmeans_predicts = None
    self._df_kmeans = None

  def fit_predict(self, tf_idf_matrix):
    self._kmeans_predicts = self._kmeans.fit_predict(tf_idf_matrix)

  def get_result_df(self, df_series):
    """
    Renvoie un Dataframe, associant à chaque série son cluster prédit. 
    Le DataFrame en entrée doit contenir une colonne `serie`. De plus, l'ordre de ces dernières doit être inchangé par rapport à la matrice utilisé pour la fonction `fit_predict`.
    """
    if self._kmeans_predicts is None:
      raise Exception("La matrice de prédictions est vide, veuillez d'abord appeler la méthode `fit_predict`")

    self._df_kmeans = pd.concat([pd.DataFrame({"serie": df_series["serie"]})] + [pd.Series(np.zeros(len(df_series), dtype=np.int8), name=i) for i in range(self.nb_clusters)], axis=1)
      
    for i in range(len(df_series)):
      self._df_kmeans.loc[i, self._kmeans_predicts[i]] = 1

    self._df_kmeans.loc[:, "cluster"] = self._kmeans_predicts
    return self._df_kmeans

  def get_max_size_cluster(self):
    if self._df_kmeans is None:
      raise Exception("Le DataFrame de résultats est vide, veuillez d'abord appeler la méthode `get_result_df`")
    return max(self._df_kmeans.drop("cluster", axis=1).sum(numeric_only=True))

  def get_inertia(self):
    return self._kmeans.inertia_