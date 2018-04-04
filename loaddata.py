from sklearn.preprocessing import LabelEncoder
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import math


feature_dict = {i:label for i,label in zip(
                range(8),
                  ('Medu',
                  'Fedu',
                  'traveltime',
                  'studytime',
                  'freetime',
                  'goout',
                  'health',
                  'absences'))}

ab = pd.ExcelFile('studentupdate.xlsx')
df = ab.parse("Sheet1")

print(ab)
