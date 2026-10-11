import requests as rq
import json as js
import os
from dotenv import load_dotenv
import csv
import pandas as pd
import numpy as np
import plotly.express as px

from main import get_stat

data = get_stat(file_csv="vac.csv")

region_median = pd.DataFrame(data["vacancy_slice_region"])
region_median = region_median.sort_values("median", ascending=False)
region_median = region_median.reset_index().rename(columns={"index":"region"})
print(region_median)
fig = px.bar(region_median[(region_median.index < 29)], y="region", x="median", orientation="h", labels={"region" : "Регион", "median" : "Медиана ЗП Р."})
fig.update_yaxes(dtick = 1)
fig.update_layout(title="Median for region")
fig.show()


vacancy = pd.DataFrame(data["vacancy"])
fig_1 = px.scatter(vacancy, x=vacancy["experience"], y=vacancy["salary_min"])
fig_1.show()