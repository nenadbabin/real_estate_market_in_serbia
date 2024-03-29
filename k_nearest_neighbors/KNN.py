import enum
from typing import List
from pandas import DataFrame
import math
from collections import Counter


class DistanceMetric(enum.Enum):
    euclidean_distance = "euclidean_distance"
    manhattan_distance = "manhattan_distance"


class KNN:
    def __init__(self, input_data: DataFrame, correct_output_class: DataFrame, k: int = None):
        self.__input_data: DataFrame = input_data
        self.__correct_output_values: DataFrame = correct_output_class
        self.__num_of_data: int = input_data.shape[0]
        self.__num_of_features: int = input_data.shape[1]
        if k:
            self.__k: int = k
        else:
            square_root_k: int = int(math.sqrt(self.__num_of_data + 1))
            if square_root_k % 5 == 0:
                square_root_k = square_root_k + 1
            self.__k: int = square_root_k

    def k(self) -> int:
        return self.__k

    def num_of_features(self) -> int:
        return self.__num_of_features

    def classify(self, data: DataFrame, metric: DistanceMetric) -> dict[int, int]:
        if metric == DistanceMetric.euclidean_distance:
            return self.__get_class(self.__euclidean_distance(data))
        elif metric == DistanceMetric.manhattan_distance:
            return self.__get_class(self.__manhattan_distance(data))

    def __euclidean_distance(self, x: DataFrame) -> List[float]:
        distances: List[float] = []
        x_features = x.values.tolist()
        for data_iter in range(0, self.__num_of_data):
            temp_sum: float = 0.0
            single_data = self.__input_data.iloc[data_iter].values.tolist()
            for features_iter in range(0, self.__num_of_features):
                temp_sum += pow(x_features[features_iter] - single_data[features_iter], 2)
            distances.append(math.sqrt(temp_sum))

        return distances

    def __manhattan_distance(self, x: DataFrame) -> List[float]:
        distances: List[float] = []
        x_features = x.values.tolist()
        for data_iter in range(0, self.__num_of_data):
            temp_sum: float = 0.0
            single_data = self.__input_data.iloc[data_iter].values.tolist()
            for features_iter in range(0, self.__num_of_features):
                temp_sum += abs(x_features[features_iter] - single_data[features_iter])
            distances.append(temp_sum)

        return distances

    def __get_class(self, distances: List[float]) -> dict[int, int]:
        indexes: List[int] = list(range(0, self.__num_of_data))
        for i in range(self.__num_of_data):
            for j in range(0, self.__num_of_data - i - 1):
                if distances[j] > distances[j + 1]:
                    distances[j], distances[j + 1] = distances[j + 1], distances[j]
                    indexes[j], indexes[j + 1] = indexes[j + 1], indexes[j]

        classes: List[int] = []
        for i in range(0, self.__k):
            single_class = self.__correct_output_values.iloc[indexes[i]].values.tolist()[0]
            classes.append(single_class)

        counted_classes = Counter(classes)
        return dict(counted_classes)
