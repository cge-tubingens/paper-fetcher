import re

from sklearn.base import TransformerMixin, BaseEstimator

import pandas as pd
import numpy as np

class Identity(BaseEstimator, TransformerMixin):

    def __init__(self) -> None:
        super().__init__()

    def get_feature_names_out(self):
        pass

    def fit(self, X:pd.DataFrame, y=None):
        return self
    
    def transform(self, X:pd.DataFrame, y=None)->pd.DataFrame:

        X_copy= X.copy()

        return X_copy
    
class CountryRecoder(BaseEstimator, TransformerMixin):

    def __init__(self, country:str, locus:str, alias:str=[]) -> None:
        super().__init__()
        self.country= country
        self.locus  = locus
        self.alias  = alias

    def get_feature_names_out(self):
        pass

    def fit(self, X:pd.DataFrame, y=None):
        return self
    
    def transform(self, X:pd.DataFrame, y=None)->pd.DataFrame:

        X_copy= X.copy()
        col = X_copy.columns[0]

        country= self.country
        locus  = self.locus
        alias  = self.alias

        X_copy[col] = X_copy[col].apply(
            lambda x: self.encoder(string=x, alias=alias, locus=locus, country=country)
        )

        return X_copy
    
    @staticmethod
    def encoder(string:str, alias:list, locus:str, country:str)->str:

        if string is None: return None

        if string in alias: return country

        for loc in locus:
            if loc in string: return country

        return string

class SmallWordsRemover(BaseEstimator, TransformerMixin):

    def __init__(self) -> None:
        super().__init__()

    def get_feature_names_out(self):
        pass

    def fit(self, X:pd.DataFrame, y=None):
        return self
    
    def transform(self, X:pd.DataFrame, y=None)->pd.DataFrame:

        X_copy= X.copy()
        col = X_copy.columns[0]

        X_copy[col] = X_copy[col].apply(lambda x: self.dropper(x))

        return X_copy
    
    @staticmethod
    def dropper(string:str)->str:

        if string is None: return None

        to_drop = [
            "The ", " and ", "the "
        ]

        for substring in to_drop: 
            if substring in string:
                return string.replace(substring, ' ').lstrip()
            
        to_none = [
            'and', ' ', '', 'https:', 'to this paper', 'to this work'
        ]
            
        for word in to_none:
            if string==word: return None
            
        return string

class Apostrophe(BaseEstimator, TransformerMixin):

    def __init__(self) -> None:
        super().__init__()

    def get_feature_names_out(self):
        pass

    def fit(self, X:pd.DataFrame, y=None):
        return self
    
    def transform(self, X:pd.DataFrame, y=None)->pd.DataFrame:

        X_copy= X.copy()
        col = X_copy.columns[0]

        X_copy[col] = X_copy[col].apply(
            lambda x: None if x is None else x.replace("'", "").replace('"','').lstrip()
        )

        return X_copy
