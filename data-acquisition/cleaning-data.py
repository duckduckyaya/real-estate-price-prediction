import pandas as pd
from IPython.core.display_functions import display

df = pd.read_csv('immowebepc.csv')

# rename the header
df.columns.tolist()

# drop column swimmingpool
df.drop('wellnessEquipment_hasSwimmingPool', axis=1, inplace=True)

df.columns.tolist()




