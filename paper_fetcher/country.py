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

    def __init__(self, country_name:str, aliases:list, affi_col:str = 'Affiliations', country_col:str='Country') -> None:
        super().__init__()
        self.country_name= country_name
        self.aliases = aliases
        self.affi_col = affi_col
        self.country_col = country_col

    def get_feature_names_out(self):
        pass

    def fit(self, X:pd.DataFrame, y=None):
        return self
    
    def transform(self, X:pd.DataFrame, y=None)->pd.DataFrame:

        X_copy= X.copy()

        country_name= self.country_name
        aliases  = self.aliases
        country_col = self.country_col
        affi_col = self.affi_col

        X_copy[country_col] = X_copy.apply(
            lambda x: self.country_encoder(affiliation=x[affi_col], new_country=country_name, topos=aliases, old_country=x[country_col]), axis=1
        )

        return X_copy
    
    @staticmethod
    def country_encoder(affiliation: str, new_country: str, topos: list, old_country:str)-> str:
    
        for topo in topos:
            if topo in affiliation:
                return new_country

        return old_country

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
