from sklearn.preprocessing import LabelEncoder
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import math


feature_dict = {i:label for i,label in zip(
                range(9),
                  ('Mjob',
                  'Fjob',
                  'traveltime',
                  'studytime',
                  'freetime',
                  'goout',
                  'health',
                  'absences',
                  'meanscore'))}


ab=pd.ExcelFile("Book2.xlsx")
dd=pd.ExcelFile("Book2.xlsx")
cd=ab.parse("Sheet1")
de=dd.parse("Sheet1")
cd.columns = [l for i,l in sorted(feature_dict.items())] + ['Class']
de.columns=[l for i,l in sorted(feature_dict.items())] + ['Class']
cd.tail()
de.tail()
print(de)