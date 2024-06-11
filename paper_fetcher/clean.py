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

class ElectronicAddressDropper(BaseEstimator, TransformerMixin):

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
        else:
            return re.sub(r'\.[^:]*:', '', string)

class AffiliationSelector(BaseEstimator, TransformerMixin):

    def __init__(self) -> None:
        super().__init__()

    def get_feature_names_out(self):
        pass

    def fit(self, X:pd.DataFrame, y=None):
        return self
    
    def transform(self, X:pd.DataFrame, y=None)->pd.DataFrame:

        X_copy= X.copy()
        col = X_copy.columns[0]

        X_copy[col] = X_copy[col].apply(lambda x: self.selector(x))

        return X_copy
    
    @staticmethod
    def selector(string:str)->str:

        if string is None: return None
        else:
            return string.split(';')[0]

class ParenthesisDropper(BaseEstimator, TransformerMixin):

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
        else:
            return re.sub(r'\([^)]*\)', '', string)

class CountrySelector(BaseEstimator, TransformerMixin):

    def __init__(self) -> None:
        super().__init__()

    def get_feature_names_out(self):
        pass

    def fit(self, X:pd.DataFrame, y=None):
        return self
    
    def transform(self, X:pd.DataFrame, y=None)->pd.DataFrame:

        X_copy= X.copy()
        col = X_copy.columns[0]

        X_copy["country"] = X_copy[col].apply(lambda x: self.selector(x))

        return X_copy
    
    @staticmethod
    def selector(string:str)->str:

        if string is None: return None
        else:
            res = string.split(',')[-1]
            return res.lstrip()

class USA(BaseEstimator, TransformerMixin):

    def __init__(self) -> None:
        super().__init__()

    def get_feature_names_out(self):
        pass

    def fit(self, X:pd.DataFrame, y=None):
        return self
    
    def transform(self, X:pd.DataFrame, y=None)->pd.DataFrame:

        X_copy= X.copy()
        col = X_copy.columns[0]

        X_copy[col] = X_copy[col].apply(lambda x: self.encoder(x))

        return X_copy
    
    @staticmethod
    def encoder(string:str)->str:

        usa_alias = [
            "US", "United States", "United States of America", "Boston", "Washington", "Tennessee", 
            "PA", "MA", "TN", "San Francisco", "Berkeley", "New Jersey", "California", "NY", "TX",
            "Ann Arbor", "Oakland", "Texas", "Maryland", "Houston", "Minneapolis", "Dallas",
            "LA", "Connecticut", "Austin", "Ohio", "New York", "CA", "Los Angeles", "Arizona",
            "Pennsylvania", "Iowa City", "Missouri", "Seattle", "St Louis", "Iowa", "Louisiana",
            "Chapel Hill", "Utah", "Salt Lake City", "North Carolina", "South Carolina",
            "Kentucky", "Hawaii", "New Hampshire", "Florida", "Virginia", "Philadelphia", "U.S.A",
            "Puerto Rico", "Illinois", "Califirnia", "Tallahassee", "Sacramento", "Miami", "FL",
            "Colorado", "Alabama", "Nashville", "San Diego", "Oregon"
        ]

        if string is None: return None
        elif string in usa_alias or "Mayo Clinic" in string or "Vanderbilt" in string: return "USA"
        elif "Johns Hopkins" in string or "Massachusetts" in string or "California" in string: return "USA"
        elif "USA" in string: return "USA"
        else: return string

class Netherlands(BaseEstimator, TransformerMixin):

    def __init__(self) -> None:
        super().__init__()

    def get_feature_names_out(self):
        pass

    def fit(self, X:pd.DataFrame, y=None):
        return self
    
    def transform(self, X:pd.DataFrame, y=None)->pd.DataFrame:

        X_copy= X.copy()
        col = X_copy.columns[0]

        X_copy[col] = X_copy[col].apply(lambda x: self.encoder(x))

        return X_copy
    
    @staticmethod
    def encoder(string:str)->str:

        netherlands_alias = [
            "the Netherlands", "The Netherlands"
        ]

        if string is None: return None
        elif string in netherlands_alias: return "Netherlands"
        else: return string

class UnitedKingdom(BaseEstimator, TransformerMixin):

    def __init__(self) -> None:
        super().__init__()

    def get_feature_names_out(self):
        pass

    def fit(self, X:pd.DataFrame, y=None):
        return self
    
    def transform(self, X:pd.DataFrame, y=None)->pd.DataFrame:

        X_copy= X.copy()
        col = X_copy.columns[0]

        X_copy[col] = X_copy[col].apply(lambda x: self.encoder(x))

        return X_copy
    
    @staticmethod
    def encoder(string:str)->str:

        uk_alias = [
            "United Kingdom", "Manchester", "UNITED KINGDOM", "Wales", "the United Kingdom",
            "Northern Ireland"
        ]

        if string is None: return None
        elif string in uk_alias: return "UK"
        else: return string

class China(BaseEstimator, TransformerMixin):

    def __init__(self) -> None:
        super().__init__()

    def get_feature_names_out(self):
        pass

    def fit(self, X:pd.DataFrame, y=None):
        return self
    
    def transform(self, X:pd.DataFrame, y=None)->pd.DataFrame:

        X_copy= X.copy()
        col = X_copy.columns[0]

        X_copy[col] = X_copy[col].apply(lambda x: self.encoder(x))

        return X_copy
    
    @staticmethod
    def encoder(string:str)->str:

        china_alias = [
            "People's Republic of China", "PR China", "P.R. China", "Hong Kong", "CHINA"
        ]

        if string is None: return None
        elif string in china_alias or "China" in string: return "China"
        elif "Guangdong" in string: return "China"
        else: return string

class Australia(BaseEstimator, TransformerMixin):

    def __init__(self) -> None:
        super().__init__()

    def get_feature_names_out(self):
        pass

    def fit(self, X:pd.DataFrame, y=None):
        return self
    
    def transform(self, X:pd.DataFrame, y=None)->pd.DataFrame:

        X_copy= X.copy()
        col = X_copy.columns[0]

        X_copy[col] = X_copy[col].apply(lambda x: self.encoder(x))

        return X_copy
    
    @staticmethod
    def encoder(string:str)->str:

        if string is None: return None
        elif "Australia" in string: return "Australia"
        else: return string

class Spain(BaseEstimator, TransformerMixin):

    def __init__(self) -> None:
        super().__init__()

    def get_feature_names_out(self):
        pass

    def fit(self, X:pd.DataFrame, y=None):
        return self
    
    def transform(self, X:pd.DataFrame, y=None)->pd.DataFrame:

        X_copy= X.copy()
        col = X_copy.columns[0]

        X_copy[col] = X_copy[col].apply(lambda x: self.encoder(x))

        return X_copy
    
    @staticmethod
    def encoder(string:str)->str:

        if string is None: return None
        elif "Spain" in string: return "Spain"
        else: return string

class Finland(BaseEstimator, TransformerMixin):

    def __init__(self) -> None:
        super().__init__()

    def get_feature_names_out(self):
        pass

    def fit(self, X:pd.DataFrame, y=None):
        return self
    
    def transform(self, X:pd.DataFrame, y=None)->pd.DataFrame:

        X_copy= X.copy()
        col = X_copy.columns[0]

        X_copy[col] = X_copy[col].apply(lambda x: self.encoder(x))

        return X_copy
    
    @staticmethod
    def encoder(string:str)->str:

        if string is None: return None
        elif "FINLAND" in string: return "Finland"
        else: return string
