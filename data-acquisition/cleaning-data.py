import pandas as pd
from IPython.core.display_functions import display

df = pd.read_csv('immowebepc.csv')

# drop column swimmingpool
df.drop('wellnessEquipment_hasSwimmingPool', axis=1, inplace=True)

# drop duplicate row base on same id
pd.drop_duplicates(subset=['id'], keep='last')









