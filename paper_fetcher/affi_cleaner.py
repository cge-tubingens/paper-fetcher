import re

from sklearn.base import TransformerMixin, BaseEstimator

import pandas as pd

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

            X_copy[col] = X_copy[col].apply(lambda x: None if x=="Unknown" or x=='' else x)

        return X_copy
    
class RemoveTwitter(TransformerMixin, BaseEstimator):

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

            X_copy[col] = X_copy[col].apply(lambda x: self.dropper(x))

        return X_copy
    
    @staticmethod
    def dropper(string:str)->str:

        if string is None: return None
        else:
            return re.sub(r'//.*?\s', '', string)
 
class EmailDropper(BaseEstimator, TransformerMixin):

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
            return re.sub(r'\s[^:]*:', '', string)

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

class FinalSymbolsDropper(BaseEstimator, TransformerMixin):

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
            lambda x: self.dropper(x)
        )

        return X_copy
    
    @staticmethod
    def dropper(string:str)->str:

        if string is None: return string

        no_space = string.rstrip()

        if len(no_space)>0:

            if no_space[-1]=='.':
                return no_space[:-1].rstrip()
            else:
                return no_space
        else:
            return None 

class FirstNonLetter(BaseEstimator, TransformerMixin):

    def __init__(self) -> None:
        super().__init__()

    def get_feature_names_out(self):
        pass

    def fit(self, X:pd.DataFrame, y=None):
        return self
    
    def transform(self, X:pd.DataFrame, y=None)->pd.DataFrame:

        X_copy= X.copy()
        col = X_copy.columns[0]

        X_copy[col] = X_copy[col].apply(lambda x: self.first_dropper(x))

        return X_copy
    
    @staticmethod
    def first_dropper(string:str)->str:

        match = re.search(r'[a-zA-Z]', string)
        if match:
            return string[match.start():]
        else:
            return ''

class ORCIDropper(BaseEstimator, TransformerMixin):

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
            else: return re.sub(r'http.*?\d', '', string)

class EndingReplacer(BaseEstimator, TransformerMixin):

    def __init__(self, old:str, new:str) -> None:
        super().__init__()
        self.old = old
        self.new = new

    def get_feature_names_out(self):
        pass

    def fit(self, X:pd.DataFrame, y=None):
        return self
    
    def transform(self, X:pd.DataFrame, y=None)->pd.DataFrame:

        X_copy= X.copy()
        col = X_copy.columns[0]

        non_null_mask = (~X_copy[col].isnull())

        X_copy.loc[non_null_mask, col] = X_copy.loc[non_null_mask, col].apply(
            lambda x: x.replace(self.old, self.new)
        )

        return X_copy
    
class ExcedingWhite(BaseEstimator, TransformerMixin):

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
            lambda x: self.clean_extra_white(x)
        )

        return X_copy
    
    @staticmethod
    def clean_extra_white(string:str)->str:

        if string is None: return None

        res=''

        splitted = string.split()
        for sub in splitted:
            if sub !="," and sub != '.':
                res+=(sub.strip()+' ')
        
        return res.rstrip()

class StatesFixerUS(TransformerMixin, BaseEstimator):

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

            X_copy[col] = X_copy[col].apply(lambda x: self.fixer(x))

        return X_copy
    
    @staticmethod
    def fixer(string:str)->str:

        if string is None: return None

        states_codes = [
            "AL", "AK", "AZ", "AR", "AS", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "GU", "HI", "ID", "IL", 
            "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", 
            "NJ", "NM", "NY", "NC", "ND", "WY", "OH", "OK", "OR", "PA", "PR", "RI", "SC", "SD", "TN", "TX",
            "UT", "VT", "VA", "WA", "WV", "WI"
        ]

        for code in states_codes:
            if f", {code}" in string:
                return string.replace(f", {code}", f" {code}")
            if f"; {code}" in string:
                return string.replace(f"; {code}", f" {code}")
            elif f",{code}" in string:
                return string.replace(f",{code}", f" {code}")
            elif f";{code}" in string:
                return string.replace(f";{code}", f" {code}")
            
        return string
        
class StatesFixerCA(TransformerMixin, BaseEstimator):

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

            X_copy[col] = X_copy[col].apply(lambda x: self.fixer(x))

        return X_copy
    
    @staticmethod
    def fixer(string:str)->str:

        if string is None: return None

        states_codes = [
            "AB", "BC", "MB", "NB", "NL", "NT", "NS", "NU", "ON", "PE", "QC", "SK", "YT"
        ]

        for code in states_codes:
            if f", {code}" in string:
                return string.replace(f", {code}", f" {code}")
            if f"; {code}" in string:
                return string.replace(f"; {code}", f" {code}")
            elif f",{code}" in string:
                return string.replace(f",{code}", f" {code}")
            elif f";{code}" in string:
                return string.replace(f";{code}", f" {code}")
            
        return string
    
class Initials(TransformerMixin, BaseEstimator):

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

            X_copy[col] = X_copy[col].apply(lambda x: self.shorterner(x))

        return X_copy
    
    @staticmethod
    def shorterner(string:str)->str:
        
        if string is None: return None

        return re.sub(r'([A-Z])\.', r'\1', string)

class Brackets(BaseEstimator, TransformerMixin):

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
            lambda x: None if x is None else re.sub(r'\[\d\]', '', x)
        )

        return X_copy

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
            return re.sub(r'\s[^:]*:', '', string)

class WhiteSpaces(BaseEstimator, TransformerMixin):

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
            lambda x: None if x is None else re.sub(r'\s+', ' ', x)
        )

        return X_copy
    
class StrReplace(BaseEstimator, TransformerMixin):

    def __init__(self, old, new) -> None:
        super().__init__()
        self.old = old
        self.new = new

    def get_feature_names_out(self):
        pass

    def fit(self, X:pd.DataFrame, y=None):
        return self
    
    def transform(self, X:pd.DataFrame, y=None)->pd.DataFrame:

        X_copy= X.copy()
        col = X_copy.columns[0]

        X_copy[col] = X_copy[col].apply(
            lambda x: None if x is None else x.replace(self.old, self.new)
        )

        return X_copy

class WebAddresses(BaseEstimator, TransformerMixin):

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
            lambda x: self.web_formatter(string=x)
        )

        return X_copy
    
    @staticmethod
    def web_formatter(string:str)->str:

        if string is None: return None

        result = ''

        splitted = string.split(' ')

        for subs in splitted:
            if subs.endswith('.'):
                # Remove all periods except the last one
                result += (subs[:-1].replace('.', '') + '. ')
            else:
                # Remove all periods
                result += (subs.replace('.', '') + ' ')
        return result

class ListStrReplace(BaseEstimator, TransformerMixin):

    def __init__(self, old:list, new:list) -> None:
        super().__init__()
        self.old = old
        self.new = new

    def get_feature_names_out(self):
        pass

    def fit(self, X:pd.DataFrame, y=None):
        return self
    
    def transform(self, X:pd.DataFrame, y=None)->pd.DataFrame:

        X_copy= X.copy()
        col = X_copy.columns[0]

        old = self.old
        new = self.new

        for k in range(len(old)):

            X_copy[col] = X_copy[col].apply(
                lambda x: None if x is None else x.replace(old[k], new[k])
            )

        return X_copy
    
    @staticmethod
    def replacer(string:str, old:list, new:list)->str:

        if string is None: return None

        for k in range(len(old)):
            if old[k] in string:
                return string.replace(old[k], new[k])
            
        return string

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

        X_copy['first_affiliation'] = X_copy[col].apply(lambda x: self.selector(x))

        return X_copy
    
    @staticmethod
    def selector(string:str)->str:

        if string is None: return None

        if ";" in string:
            return string.split(';')[0]
        else:
            return string

class NumbersDropper(BaseEstimator, TransformerMixin):

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
                lambda x: None if x is None else re.sub(r'[0-9]', '', x)
            )

            return X_copy

class SecondAffiSelector(BaseEstimator, TransformerMixin):

    def __init__(self) -> None:
        super().__init__()

    def get_feature_names_out(self):
        pass

    def fit(self, X:pd.DataFrame, y=None):
        return self
    
    def transform(self, X:pd.DataFrame, y=None)->pd.DataFrame:

        X_copy= X.copy()
        col = X_copy.columns[0]

        X_copy['ult_affiliation'] = X_copy[col].apply(
            lambda x: None if x is None else x.split('.')[0]
        )

        return X_copy

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

        X_copy['country'] = X_copy[col].apply(
            lambda x: None if x is None else x.split(',')[-1].lstrip()
        )

        return X_copy
