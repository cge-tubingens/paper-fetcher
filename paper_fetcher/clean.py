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

        if string is None: return None

        usa_alias = [
            "US", "United States", "United States of America", "Boston", "Washington", "Tennessee", 
            "PA", "MA", "TN", "San Francisco", "Berkeley", "New Jersey", "California", "NY", "TX",
            "Ann Arbor", "Oakland", "Texas", "Maryland", "Houston", "Minneapolis", "Dallas",
            "LA", "Connecticut", "Austin", "Ohio", "New York", "CA", "Los Angeles", "Arizona",
            "Pennsylvania", "Iowa City", "Missouri", "Seattle", "St Louis", "Iowa", "Louisiana",
            "Chapel Hill", "Utah", "Salt Lake City", "North Carolina", "South Carolina",
            "Kentucky", "Hawaii", "New Hampshire", "Florida", "Virginia", "Philadelphia", "U.S.A",
            "Puerto Rico", "Illinois", "Califirnia", "Tallahassee", "Sacramento", "Miami", "FL",
            "Colorado", "Alabama", "Nashville", "San Diego", "Oregon", "Minnesota"
        ]

        if string in usa_alias: return "USA"

        usa_locs = [
            "Mayo Clinic", "Vanderbilt", "Johns Hopkins", "Massachusetts", "California", "USA", "Boston",
            "New York", "Atlanta", "New Haven", "Houston", "Pittsburgh", "Alabama", "Utah", "Miami",
            "Mississippi", "North Carolina", "New Orleans", "Illinois", "San Francisco", "Los Angeles",
            "United States", "Seattle", "Salt Lake City", "Baltimore", "West Virginia", "Philadelphia",
            "Maryland", "Denver", "Iowa", "South Carolina", "Palo Alto", "Florida", "Rhode Island",
            "Colorado", "Michigan", "Tucson", "Phoenix", "Pennsylvania", "Vermont", "Wisconsin", "Oklahoma",
            "New Mexico", "Ann Arbor", "Nashville", "Oregon", "Delaware", "Honolulu", "Texas", "Puerto Rico",
            "Cleveland OH", "Indianapolis", "Providence RI", "Masschusetts", "Connecticut", "Stanford University"
        ]

        for loc in usa_locs:
            if loc in string: return "USA"

        return string

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
            "the Netherlands", "The Netherlands", "Nederland"
        ]

        if string is None: return None
        elif string in netherlands_alias: return "Netherlands"
        elif "Netherlands" in string: return "Netherlands"
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
            "Northern Ireland", "U.K", "United kingdom", "England"
        ]

        if string is None: return None
        elif string in uk_alias: return "UK"
        elif "UK" in string or "Scotland" in string or "United Kingdom" in string: return "UK"
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

class Germany(BaseEstimator, TransformerMixin):

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
        elif "Germany" in string: return "Germany"
        else: return string

class Sweden(BaseEstimator, TransformerMixin):

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
        elif "Sweden" in string: return "Sweden"
        else: return string

class Singapore(BaseEstimator, TransformerMixin):

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
        elif "Singapore" in string: return "Singapore"
        else: return string

class Canada(BaseEstimator, TransformerMixin):

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

        canada_loc = [
            "Canada", "Vancouver", "Montreal", "Québec", "Quebec", "British Columbia", "Ontario", "Toronto"
        ]
        for loc in canada_loc:
            if loc in string: return "Canada"
        
        return string

class Slovakia(BaseEstimator, TransformerMixin):

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
        elif "Slovakia" in string: return "Slovakia"
        else: return string

class Hungary(BaseEstimator, TransformerMixin):

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
        elif "Hungary" in string: return "Hungary"
        else: return string

class Greece(BaseEstimator, TransformerMixin):

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
        elif "Greece" in string: return "Greece"
        else: return string

class Italy(BaseEstimator, TransformerMixin):

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
        elif "Italy" in string: return "Italy"
        else: return string

class France(BaseEstimator, TransformerMixin):

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

        france_alias = [
            "Fance"
        ]

        if string in france_alias: return "France"

        fran_locs = [
            "Lille", "Nantes", "Dijon", "Paris", "France"
        ]

        for loc in fran_locs:
            if loc in string: return "France"

        return string
