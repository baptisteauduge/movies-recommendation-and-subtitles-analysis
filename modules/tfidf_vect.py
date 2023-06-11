import os
import pickle
from sklearn.metrics.pairwise import euclidean_distances, cosine_distances
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import seaborn as sns

root_path_image = "exports/images/matrix_distance/"

class TfIdfVect():
  
  def __init__(self, min_df, max_df, nb_episodes, type):
    self._vectorizer = TfidfVectorizer(strip_accents='unicode', stop_words='english', max_df=max_df, min_df=min_df)
    self._type = type
    self._min_df = min_df
    self._max_df = max_df
    self.nb_episodes = nb_episodes
    self._path_vectorizer = f"data/pickle/tf-idf_vectorizer_min-df_{self._min_df}_max-df_{self._max_df}-{self.nb_episodes}{type}.pickle"
    self._path_tf_idf_matrix = f"data/pickle/tf-idf_matrix_min-df_{self._min_df}_max-df_{self._max_df}-{self.nb_episodes}{type}.pickle"
    self._path_euclidian_distance_matrix = f"data/pickle/tf-idf_euclidian_distance_matrix_min-df_{self._min_df}_max-df_{self._max_df}-{self.nb_episodes}{type}.pickle"    
    self._path_cosine_distance_matrix = f"data/pickle/tf-idf_cosine_distance_matrix_min-df_{self._min_df}_max-df_{self._max_df}-{self.nb_episodes}{type}.pickle"    
    self._tf_idf_matrix = None
    self._euclidian_distance_matrix = None
    self._cosine_distance_matrix = None

  def get_vectorizer(self):
    return self._vectorizer

  def get_min_df(self):
    return self._min_df

  def get_max_df(self):
    return self._max_df

  def get_vector_size(self):
    return len(self._vectorizer.vocabulary_)

  def save_vectorizer_as_file(self):
    """
    Saves the Tf-Idf vector as a file, at self._path_vectorizer.
    """
      
    os.makedirs(os.path.dirname(self._path_vectorizer), exist_ok=True)
    with open(self._path_vectorizer, 'wb') as file:
      pickle.dump(self._vectorizer, file)

  def save_tf_idf_matrix_as_file(self):
    """
    Save the Tf_Idf matrix as a file at self._path_tf_idf_matrix
    """
    if self._tf_idf_matrix is None:
      raise Exception("Please, fill the matrix before trying to save it")
      
    os.makedirs(os.path.dirname(self._path_tf_idf_matrix), exist_ok=True)
    with open(self._path_tf_idf_matrix, 'wb') as file:
      pickle.dump(self._tf_idf_matrix, file)

  def save_euclidian_distance_matrix_as_file(self):
    """
    Save the euclidian distance matrix as file at self._path_euclidian_distance_matrix
    """

    if self._euclidian_distance_matrix is None:
      raise Exception("Please, fill the euclidian distance matrix before trying to save it")
      
    os.makedirs(os.path.dirname(self._path_euclidian_distance_matrix), exist_ok=True)
    with open(self._path_euclidian_distance_matrix, 'wb') as file:
      pickle.dump(self._euclidian_distance_matrix, file)

  def save_cosine_distance_matrix_as_file(self):
    """
    Save the cosine distance matrix as file at self._path_cosine_distance_matrix
    """

    if self._cosine_distance_matrix is None:
      raise Exception("Please, fill the euclidian distance matrix before trying to save it")
      
    os.makedirs(os.path.dirname(self._path_cosine_distance_matrix), exist_ok=True)
    with open(self._path_cosine_distance_matrix, 'wb') as file:
      pickle.dump(self._cosine_distance_matrix, file)
    

  def _load_vectorizer_from_file(self):
    """
    Loads the Tf-Idf vectorizer, from self._path_vectorizer
    the function will return an error if the file doesn't exists
    """
    with open(self._path_vectorizer, 'rb') as file:
      self._vectorizer = pickle.load(file)

  def _load_tf_idf_matrix_from_file(self):
    """
    Loads the Tf-Idf Matrix, from self._path_tf_idf_matrix
    the function will return an error if the file doesn't exists
    """
    with open(self._path_tf_idf_matrix, 'rb') as file:
      self._tf_idf_matrix = pickle.load(file)

  def _load_euclidian_distance_matrix_from_file(self):
    """
    Loads the Euclidian Distance Matrix, from self._path_euclidian_distance_matrix
    the function will return an error if the file doesn't exists
    """
    with open(self._path_euclidian_distance_matrix, 'rb') as file:
      self._euclidian_distance_matrix = pickle.load(file)

  def _load_cosine_distance_matrix_from_file(self):
    """
    Loads the Cosine Distance Matrix, from self._path_euclidian_distance_matrix
    the function will return an error if the file doesn't exists
    """
    with open(self._path_cosine_distance_matrix, 'rb') as file:
      self._cosine_distance_matrix = pickle.load(file)

  def fit_and_save_or_import(self, text):
    """
    Array[str] -> Int
    Fit the model and save it if there is no save of this model parameters in this computer.
    Otherwise, it loads the model from the file.
    """
  
    try:
      self._load_vectorizer_from_file()
      self._load_tf_idf_matrix_from_file()
    except:
      self._tf_idf_matrix = self._vectorizer.fit_transform(text)
      self.save_vectorizer_as_file()
      self.save_tf_idf_matrix_as_file()

  def get_euclidian_distance_matrix(self):
    """
    Returns the euclidian distance matrix. The function will load it from a file if possible
    """

    if self._euclidian_distance_matrix is None:
      try:
        self._load_euclidian_distance_matrix_from_file()
      except:
        if self._tf_idf_matrix is None:
          raise Exception("Please fill the tf_idf_matrix, before. You can use `fit_and_save_or_import()`")
        self._euclidian_distance_matrix = euclidean_distances(self._tf_idf_matrix, self._tf_idf_matrix)
        self.save_euclidian_distance_matrix_as_file()
        
    return self._euclidian_distance_matrix

  def get_cosine_distance_matrix(self):
    """
    Returns the euclidian distance matrix. The function will load it from a file if possible
    """
    
    if self._cosine_distance_matrix is None:
      try:
        self._load_cosine_distance_matrix_from_file()
      except:
        if self._tf_idf_matrix is None:
          raise Exception("Please fill the tf_idf_matrix, before. You can use `fit_and_save_or_import()`")
        self._cosine_distance_matrix = cosine_distances(self._tf_idf_matrix, self._tf_idf_matrix)
        self.save_cosine_distance_matrix_as_file()

    return self._cosine_distance_matrix


  def show_and_save_euclidian_distance_matrix(self, min_index_ep, max_index_ep):
    plt.figure(figsize=(10, 10), dpi = 600) 
    sns.heatmap(self.get_euclidian_distance_matrix()[min_index_ep:max_index_ep, min_index_ep:max_index_ep])
    os.makedirs(os.path.dirname(root_path_image), exist_ok=True)
    plt.savefig(root_path_image + f"matrix_tf-idf_euclidian_distance_min-df_{self._min_df}_max-df_{self._max_df}_min-index_{min_index_ep}_max-index_{max_index_ep}_type_{self._type}.png")

  def show_and_save_cosine_distance_matrix(self, min_index_ep, max_index_ep):
    plt.figure(figsize=(10, 10), dpi = 600) 
    sns.heatmap(self.get_cosine_distance_matrix()[min_index_ep:max_index_ep, min_index_ep:max_index_ep])
    os.makedirs(os.path.dirname(root_path_image), exist_ok=True)
    plt.savefig(root_path_image + f"matrix_tf-idf_cosine_distance_min-df_{self._min_df}_max-df_{self._max_df}_min-index_{min_index_ep}_max-index_{max_index_ep}_type_{self._type}.png")