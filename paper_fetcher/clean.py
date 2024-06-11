
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
    
class ChangeUnknown(TransformerMixin, BaseEstimator):

    def __init__(self) -> None:
        super().__init__()

    def get_feature_names_out(self):
        pass

    def fit(self, X:pd.DataFrame, y=None):
        return self
    
    def transform(self, X:pd.DataFrame, y=None)->pd.DataFrame:

        X_copy= X.copy()
        cols = X_copy.columns
        
        for col in cols:

            X_copy[col] = X_copy[col].apply(lambda x: None if x=="Unknown" else x)

        return X_copy
    
class EmailDropper(BaseEstimator, TransformerMixin):

    def __init__(self) -> None:
        super().__init__()

    def get_feature_names_out(self):
        pass

    def fit(self, X:pd.DataFrame, y=None):
        return self
    
    def transform(self, X:pd.DataFrame, y=None)->pd.DataFrame:

        X_copy= X.copy()
        col = X_copy.columns

        X_copy[col[0]] = X_copy[col[0]].apply(
            lambda x: self.drop_emails(x)
        )

        return X_copy
    
    @staticmethod
    def drop_emails(string:str)->str:

        splitted = string.split(' ')

        result = ''

        for elem in splitted:

            if "@" not in elem:
                result += (elem+' ')

        return result

class FinalSymbolsDropper(BaseEstimator, TransformerMixin):

    def __init__(self) -> None:
        super().__init__()

    def get_feature_names_out(self):
        pass

    def fit(self, X:pd.DataFrame, y=None):
        return self
    
    def transform(self, X:pd.DataFrame, y=None)->pd.DataFrame:

        X_copy= X.copy()
        col = X_copy.columns

        X_copy[col[0]] = X_copy[col[0]].apply(
            lambda x: self.drop_emails(x)
        )

        return X_copy
    
    @staticmethod
    def drop_emails(string:str)->str:

        if string is None:
            return string

        no_space = string.rstrip()

        if len(no_space)>0:

            if no_space[-1]=='.':
                return no_space[:-1]
            else:
                return no_space
        else:
            return None 
