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
        
class RemoveApos(TransformerMixin, BaseEstimator):

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
            return string.replace("' ", " ")
    
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
            "Feipeng Cui and Yu Sun contributed equally to this work", "Deceased: Dr. Lumeng died on June",
            "Contributed equally and are considered to be joint last author",
            "Contributed equally to this article as lead authors and supervised the work", "Lead contact",
            "Ph.D. Program of Cancer Research and Drug Discovery", "Joint first authors", "Joint senior authors",
            "Both authors contributed equally", "P.O. Box", "PO Box", "was a researcher in law at HeLEX until July",
            "Dr Sotoodehnia is supported by NIH grant by AHA grant and by the Laughlin Family",
            "Equal first/senior", "Group leader of Angiogenesis and Tissue Engineering", "Contributed equally",
            "Mr. De Craen suddenly passed away January", "and are considered to be joint last author"
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
            "Cleveland OH", "Clevel OH", "Indianapolis", "Providence RI", "Masschusetts", "Connecticut", "Stanford University",
            "Hawai'i", "Cambridge MA", "U.S.A", "Tulane", "Yale University", "Brigham and Women's Hospital",
            "Northeastern University", "Columbia University", "Duke University", "Yale School of Medicine", 
            "Albert Einstein College of Medicine", "Stanford Medical School", "American Cancer Society",
            "Cedars-Sinai", "Chicago", "District of Columbia", "Icahn School of Medicine", "Cincinnati",
            "Keck USC School of Medicine", "Harvard Medical School", "Calico Life Sciences", "Calico", "Icahn",
            "Minneapolis", "Calif", "Albuquerque", "Moffitt Cancer Center", "Charles Bronfman Institute",
            "SWOG Statistical Center", "Penn-CHOP Lung Biology Institute", "USC Norris", "Eden Prairie",
            "Emory University", "Washington University", "Stanford", "Charlottesville", "Bethesda MD",
            "Claremont CA", "Collegeville PA", "Columbia SC", "Columbus OH", "Corona CA", "Dallas TX",
            "Danville PA", "Davis CA", "Decatur GA", "Louisville KY", "Brown University", "Virginia Tech",
            "Grove IL", "Duarte CA", "East Lansing MI", "East Lansing", "Englewood CO", "Evanston IL",
            "Farmington CT", "Farmington", "Fort Collins CO", "Fort Worth TX", "Ames IA", "Aurora CO",
            "Amherst MA", "Berkeley CA", "Blood Institute MA", "Boulder CO", "Boulder", "Rhode Isl", "Harvard MA",
            "Bronx NY", "Brookline MA", "Brownsville TX", "Chapel Hill NC", "Charleston SC", "Charlestown MA",
            "Burlington VT", "Charlotte NC", "Chevy Chase MD", "Framingham MA", "Frederick MD", "Fremont CA",
            "Gainesville FL", "Gaithersburg MD", "Glen Echo MD", "Gr Rapids MI", "Hagerstown MD", "Hanover NH",
            "Hartford CT", "Harrison NJ", "Harvard", "Buffalo NY", "Durham NC", "Irvine CA", "Ithaca NY",
            "Jackson MS", "Jacksonville FL", "Kalamazoo MI", "Kansas City KS", "King of Prussia PA", 
            "La Jolla CA", "La Jolla", "Lancaster PA", "Las Vegas NV", "Lewisburg PA", "Lexington KY",
            "Winston Salem NC", "Winston-Salem NC", "Washington DC", "Waco TX", "San Diego", "Washington WA",
            "UAB Lung Imaging Lab", "Torrance CA", "Tarrytown NY", "Tampa FL", "Syracuse NY", "Stony Brook NY",
            "Stamford CT", "St Louis MO", "St. Louis MO", "Sioux Center IA", "Severna Park MD", "Scottsdale AZ",
            "Santa Cruz CA", "San Antonio TX", "Sacramento CA", "Grand Rapids MI", "Maywood IL", "Medford MA",
            "Memphis TN", "Milwaukee WI", "Morristown NJ", "Mountain View CA", "New Brunswick NJ", 
            "New Hyde Park NY", "North Haven CT", "Norwood MA", "Oakland CA", "Portland ME", "Portland OR"
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

        if string is None: return None

        net_alias = [
            "the Netherlands", "The Netherlands", "Nederland"
        ]

        if string in net_alias: return "Netherlands"

        net_locs = [
            "Netherlands", "Amsterdam", "Vrije Universiteit", "EMGO", "Groningen"
        ]

        for loc in net_locs:
            if loc in string: return "Netherlands"

        return string

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
            "Northern Ireland", "U.K", "United kingdom", "England", "British", "United ingdom"
        ]

        if string in uk_alias: return "UK"

        uk_loc = [
            "UK", "Scotland", "United Kingdom", "U.K", "Glasgow", "Leicester", "Manchester", "Liverpool",
            "London", "Edinburgh", "Sheffield", "Bristol", "Oxford", "Birmingham", "Bath", "Cardiff", 
            "Southampton", "Newcastle", "Northern Ireland", "Leeds", "University of Cambridge", "Coventry",
            "Belfast", "Aberdeen", "John Radcliffe Hospital", "Addenbrooke's Hospital", "Botnar Research Centre",
            "N. Ireland", "Nottingham", "Swansea University", "Barts Health NHS", "Devon Partnership NHS",
            "Loughborough University", "Lancaster University", "NHS Trust", "University of Exeter"
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
            "Liuzhou", "Soochow University", "Suzhou", "Nanchang", "Sun Yat-sen University", "Oujiang",
            "Liaoning", "Tongxiang", "Shaanxi", "Zhongshan", "Yichang", "Xi'an", "Wannan", "Harbin",
            "Central South University"
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
            "Perth", "Sydney", "Australi"
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

        esp_alias = [
            "España"
        ]

        if string in esp_alias: return "Spain"

        esp_locs = [
            "Spain", "Oviedo", "Murcia", "Madrid", "Barcelona", "Asturias", "Ramón y Cajal", "Sevilla",
            "Bellvitge Biomedical Research Institute"
        ]
        
        for loc in esp_locs:
            if loc in string: return "Spain"

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
            "Germany", "Heidelberg", "Hamburg", "Neuherberg", "Erlangen"
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

        gre_locs = [
            "Greece", "Athens", "Crete"
        ]
        
        for loc in gre_locs:
            if loc in string: return "Greece"

        return string

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

        ita_alias = [
            "ITALY", "Italia", "Itlay"
        ]

        if string in ita_alias: return "Italy"

        ita_locs = [
            "Roma", "Italian", "Bergamo", "Bologna", "Bolzano", "Italy", "Cagliari", "Ragusa", "Turin",
            "Pavia", "Torino", "Milano", "Milan", "Palermo", "Florence", "Fondazione IRCCS", "Garofolo",
            "Monza", "Naples", "Novara", "Padova", "Parma", "Pisa", "Ravenna", "Rende", "Rieti", "Sardinia",
            "Sassari", "Verona", "Udine", "Padua"
        ]
        
        for loc in ita_locs:
            if loc in string: return "Italy"

        return string

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
            "Lille", "Nantes", "Dijon", "Paris", "France", "Montpellier", "Bordeaux", "Rennes", "Lyon",
            "Créteil", "Inserm Centre de Recherche des Cordeliers", "CNRS", "Toulouse"
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
            "Switzerland", "Bern", "Swiss", "Zurich", "Geneva"
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
            "Denmark", "Aarhus", "Danish", "Rigshospitalet"
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
            "Tokyo", "Chiba University", "Chiba", "Iwate Medical University", "Tokushima", "Tohoku"
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

        saf_alias = [
            
        ]

        if string in saf_alias: return "South Africa"

        saf_loc = [
            "South Africa", "University of  Witwatersrand"
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
            "Taiwan", "Taipei", "Taoyuan", "Taichung", "National Yang-Ming University", "Changhua City",
            "Kaohsiung"
        ]
        for loc in taw_loc:
            if loc in string: return "Taiwan"
        
        return string

class Austria(BaseEstimator, TransformerMixin):

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

        aut_alias = [
            
        ]

        if string in aut_alias: return "Austria"

        aut_locs = [
            "Austria"
        ]

        for loc in aut_locs:
            if loc in string: return "Austria"

        return string

class Iceland(BaseEstimator, TransformerMixin):

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

        ice_alias = [
            
        ]

        if string in ice_alias: return "Iceland"

        ice_locs = [
            "Iceland"
        ]

        for loc in ice_locs:
            if loc in string: return "Iceland"

        return string

class Israel(BaseEstimator, TransformerMixin):

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

        isr_alias = [
            
        ]

        if string in isr_alias: return "Israel"

        isr_locs = [
            "Israel"
        ]

        for loc in isr_locs:
            if loc in string: return "Israel"

        return string

class Poland(BaseEstimator, TransformerMixin):

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

        pol_alias = [
            "Pol"
        ]

        if string in pol_alias: return "Poland"

        pol_locs = [
            "Poland", "Warsaw", "Szczecin", "Łódź", "Lodz"
        ]

        for loc in pol_locs:
            if loc in string: return "Poland"

        return string

class Nigeria(BaseEstimator, TransformerMixin):

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

        nig_alias = [
            
        ]

        if string in nig_alias: return "Nigeria"

        nig_locs = [
            "Nigeria", "Lagos", "Abuja"
        ]

        for loc in nig_locs:
            if loc in string: return "Nigeria"

        return string

class SouthKorea(BaseEstimator, TransformerMixin):

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

        kor_alias = [
            "Republic of Korea", "South of Korea"
        ]

        if string in kor_alias: return "South Korea"

        kor_locs = [
            "South Korea", "Republic of Korea", "Goyang-si", "Gwangju", "Gwangmyung", "Gyeonggi-do", "Suwon",
            "Uijeongbu Eulji", "Ulsan", "Daegu", "Daejeon", "Seoul", "Busan", "Cheongju-si", "Chungnam",
            "Hwasun", "Korea University", "Seongnam", "Korea"
        ]

        for loc in kor_locs:
            if loc in string: return "South Korea"

        return string

class Colombia(BaseEstimator, TransformerMixin):

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

        col_alias = [
            
        ]

        if string in col_alias: return "Colombia"

        col_locs = [
            "Colombia", "Bogotá", "Bogota"
        ]

        for loc in col_locs:
            if loc in string: return "Colombia"

        return string

class Czech(BaseEstimator, TransformerMixin):

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

        cz_alias = [
            "Czech"
        ]

        if string in cz_alias: return "Czech Republic"

        cz_locs = [
            "Czech", "Prague"
        ]

        for loc in cz_locs:
            if loc in string: return "Czech Republic"

        return string

class Mexico(BaseEstimator, TransformerMixin):

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

        mx_alias = [
            "México"
        ]

        if string in mx_alias: return "Mexico"

        mx_locs = [
            "Mexico", "México"
        ]

        for loc in mx_locs:
            if loc in string: return "Mexico"

        return string

class Argentina(BaseEstimator, TransformerMixin):

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

        arg_alias = [
            
        ]

        if string in arg_alias: return "Argentina"

        arg_locs = [
            "Argentina", "Buenos Aires"
        ]

        for loc in arg_locs:
            if loc in string: return "Argentina"

        return string

class India(BaseEstimator, TransformerMixin):

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

        ind_alias = [
            
        ]

        if string in ind_alias: return "India"

        ind_locs = [
            "India"
        ]

        for loc in ind_locs:
            if loc in string: return "India"

        return string
    
class Pakistan(BaseEstimator, TransformerMixin):

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

        pk_alias = [
            
        ]

        if string in pk_alias: return "Pakistan"

        pk_locs = [
            "Pakistan"
        ]

        for loc in pk_locs:
            if loc in string: return "Pakistan"

        return string

class Croatia(BaseEstimator, TransformerMixin):

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

        cro_alias = [
            
        ]

        if string in cro_alias: return "Croatia"

        cro_locs = [
            "Croatia", "Split", "Zagreb"
        ]

        for loc in cro_locs:
            if loc in string: return "Croatia"

        return string

class Turkey(BaseEstimator, TransformerMixin):

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

        tur_alias = [
            
        ]

        if string in tur_alias: return "Turkey"

        tur_locs = [
            "Turkey"
        ]

        for loc in tur_locs:
            if loc in string: return "Turkey"

        return string

class SaudiArabia(BaseEstimator, TransformerMixin):

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

        ksa_alias = [
            
        ]

        if string in ksa_alias: return "Saudi Arabia"

        ksa_locs = [
            "Saudi Arabia"
        ]

        for loc in ksa_locs:
            if loc in string: return "Saudi Arabia"

        return string

class Estonia(BaseEstimator, TransformerMixin):

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

        est_alias = [
            
        ]

        if string in est_alias: return "Estonia"

        est_locs = [
            "Estonia", "Tartu"
        ]

        for loc in est_locs:
            if loc in string: return "Estonia"

        return string

class DominicanRep(BaseEstimator, TransformerMixin):

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

        dom_alias = [
            "República Dominicana"
        ]

        if string in dom_alias: return "Dominican Republic"

        _locs = [
            "Dominican Republic"
        ]

        for loc in _locs:
            if loc in string: return "Dominican Republic"

        return string

class NewZealand(BaseEstimator, TransformerMixin):

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

        nz_alias = [
            
        ]

        if string in nz_alias: return "New Zealand"

        nz_locs = [
            "New Zealand", "Auckland", "Dunedin"
        ]

        for loc in nz_locs:
            if loc in string: return "New Zealand"

        return string

class Malaysia(BaseEstimator, TransformerMixin):

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

        mal_alias = [
            
        ]

        if string in mal_alias: return "Malaysia"

        mal_locs = [
            "Malaysia"
        ]

        for loc in mal_locs:
            if loc in string: return "Malaysia"

        return string
