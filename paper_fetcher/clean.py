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
            return re.sub(r'\s[^:]*:', '', string)

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
        
            X_copy[col] = X_copy[col].apply(lambda x: self.dropper(x))

            return X_copy
        
        @staticmethod
        def dropper(string:str)->str:

            if string is None: return None
            else: return re.sub(r'\S*\d\S*', '', string)

class RemoveSpaces(BaseEstimator, TransformerMixin):

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
            else: return re.sub(r'\s+', ' ', string)

class StringsRemover(BaseEstimator, TransformerMixin):

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
            "These authors are joint first authors", "These authors contributed equally",
            "These authors contributed equally to this paper", "These authors contributed equally to this work",
            "These authors have contributed equally to this work and share first authorship",
            "These authors share senior authorship", "These four authors contributed equally to this article",
            "These two authors contributed equally to this article as lead authors and supervised the work",
            "G. Bergamini and R. Pepperkok contributed equally to this article as lead authors and supervised the work",
            "Feipeng Cui and Yu Sun contributed equally to this work", "Deceased: Dr. Lumeng died on June"
        ]

        for substring in to_drop: 
            if substring in string:
                return string.replace(substring, '')
            
        return string


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
            "Colorado", "Alabama", "Nashville", "San Diego", "Oregon", "Minnesota", "Mass", "Minn", "Wash",
            "Ill", "Indiana", "Chicago"
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
            "Cleveland OH", "Indianapolis", "Providence RI", "Masschusetts", "Connecticut", "Stanford University",
            "Hawai'i", "Cambridge MA", "U.S.A", "Tulane", "Yale University", "Brigham and Women's Hospital",
            "Northeastern University", "Columbia University", "Duke University", "Yale School of Medicine", 
            "Albert Einstein College of Medicine", "Stanford Medical School", "American Cancer Society",
            "Cedars-Sinai", "Chicago", "District of Columbia", "Icahn School of Medicine", "Cincinnati",
            "Keck USC School of Medicine", "Harvard Medical School", "Calico Life Sciences", "Calico", "Icahn",
            "Minneapolis", "Calif", "Albuquerque", "Moffitt Cancer Center", "Charles Bronfman Institute",
            "SWOG Statistical Center", "Penn-CHOP Lung Biology Institute"
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

        if string is None: return None

        uk_alias = [
            "United Kingdom", "Manchester", "UNITED KINGDOM", "Wales", "the United Kingdom",
            "Northern Ireland", "U.K", "United kingdom", "England", "British"
        ]

        if string in uk_alias: return "UK"

        uk_loc = [
            "UK", "Scotland", "United Kingdom", "U.K", "Glasgow", "Leicester", "Manchester", "Liverpool",
            "London", "Edinburgh", "Sheffield", "Bristol", "Oxford", "Birmingham", "Bath", "Cardiff", 
            "Southampton", "Newcastle", "Northern Ireland", "Leeds", "University of Cambridge", "Coventry",
            "Belfast", "Aberdeen", "John Radcliffe Hospital", "Addenbrooke's Hospital", "Botnar Research Centre",
            "N. Ireland", "Nottingham", "Swansea University", "Barts Health NHS", "Devon Partnership NHS",
            "Loughborough University", "Lancaster University"
        ]

        for loc in uk_loc:
            if loc in string: return "UK"
        
        return string

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

        if string is None: return None

        china_alias = [
            "People's Republic of China", "PR China", "P.R. China", "Hong Kong", "CHINA", "Chinese"
        ]

        if string in china_alias: return "China"

        china_locs = [
            "China", "Guangdong", "Guangxi", "Hong Kong", "Peking", "Chung Shan", "Zhejiang", "Hunan", "Fudan",
            "Shandong", "Shandong", "Tianjin", "Shenzhen", "Guangzhou", "Xiangya", "Wuhan", "Shiyan", "Beijing",
            "Jiaotong", "Shanghai", "Zhengzhou", "Qikang", "Jinan", "Chinese Academy", "Jiangsu", "Hongqiao",
            "Dongguan", "Pengzhou", "Dongfang", "Changping", "Chengdu", "Heilongjiang", "Li Ka Shing Faculty",
            "Liuzhou", "Soochow University", "Suzhou", "Nanchang", "Sun Yat-sen University", "Oujiang"
        ]

        
        for loc in china_locs:
            if loc in string: return "China"
        
        return string

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

        aus_locs = [
            "Australia", "Queensland", "Melbourne", "Curtin University", "Darlinghurst", "Monash University",
            "Perth", "Sydney"
        ]
        
        for loc in aus_locs:
            if loc in string: return "Australia"

        return string

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

        ger_alias = [
            "Deutschland", "German"
        ]

        if string in ger_alias: return "Germany"

        ger_loc = [
            "Helmholtz", "Munich", "Greifswald", "Essen", "Augsburg", "Berlin", "Freiburg", "Max-Planck",
            "Germany", "Heidelberg", "Hamburg", "Neuherberg"
        ]

        for loc in ger_loc:
            if loc in string: return "Germany"
        
        return string

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
            "Canada", "Vancouver", "Montreal", "Québec", "Quebec", "British Columbia", "Ontario", "Toronto",
            "Lady Davis Institute", "McGill University", "Saskatoon", "Sunnybrook Research Institute"
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
            "Lille", "Nantes", "Dijon", "Paris", "France", "Montpellier", "Bordeaux", "Rennes", "Lyon"
        ]

        for loc in fran_locs:
            if loc in string: return "France"

        return string
    
class Switzerland(BaseEstimator, TransformerMixin):

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

        swiss_alias = [
            
        ]

        if string in swiss_alias: return "Switzerland"

        swiss_locs = [
            "Switzerland", "Bern", "Swiss"
        ]

        for loc in swiss_locs:
            if loc in string: return "Switzerland"

        return string

class Norway(BaseEstimator, TransformerMixin):

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

        norway_alias = [
            
        ]

        if string in norway_alias: return "Norway"

        norway_locs = [
            "Norway", "Oslo", "Bergen", "Norwegian"
        ]

        for loc in norway_locs:
            if loc in string: return "Norway"

        return string

class Denmark(BaseEstimator, TransformerMixin):

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

        den_alias = [
            "Danmark", "Greenland"
        ]

        if string in den_alias: return "Denmark"

        den_locs = [
            "Denmark", "Aarhus", "Danish"
        ]

        for loc in den_locs:
            if loc in string: return "Denmark"

        return string

class Japan(BaseEstimator, TransformerMixin):

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

        jap_loc = [
            "Japan", "Hiroshima", "Kanagawa", "Nagoya", "Osaka", "Saga University", "Otsu", "Fukuoka",
            "Tokyo"
        ]
        for loc in jap_loc:
            if loc in string: return "Japan"
        
        return string
    
class Russia(BaseEstimator, TransformerMixin):

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

        rus_loc = [
            "Russia"
        ]
        for loc in rus_loc:
            if loc in string: return "Russia"
        
        return string

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

        fin_alias = [
            "FINLAND", "Finlan"
        ]

        if string in fin_alias: return "Finland"

        fin_loc = [
            "Finland", "Helsinki", "Oulu"
        ]
        for loc in fin_loc:
            if loc in string: return "Finland"
        
        return string
    
class Belgium(BaseEstimator, TransformerMixin):

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

        bel_loc = [
            "Belgium", "Leuven"
        ]
        for loc in bel_loc:
            if loc in string: return "Belgium"
        
        return string

class SouthAfrica(BaseEstimator, TransformerMixin):

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

        saf_loc = [
            "South Africa"
        ]
        for loc in saf_loc:
            if loc in string: return "South Africa"
        
        return string
    
class Taiwan(BaseEstimator, TransformerMixin):

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

        taw_loc = [
            "Taiwan", "Taipei", "Taoyuan", "Taichung City", "National Yang-Ming University"
        ]
        for loc in taw_loc:
            if loc in string: return "Taiwan"
        
        return string
