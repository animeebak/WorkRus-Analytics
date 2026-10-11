import requests as rq
import json as js
import os
from dotenv import load_dotenv
import csv
import pandas as pd
import numpy as np


def print_line(output):
    print(f"--------------------------------------------------------------------------------\n{output}\n")

def get_stat(file_csv : str) -> dict:

    vacancy_col = ["id", "category", "job_name", "schedule", "duty", "region", "salary_min", "salary_max", "education", "experience", "skills", "benefit", "company_name", "vac_url"]
    vacancy = pd.read_csv(f"./csv/{file_csv}")
    vacancy.columns = vacancy_col

    # normalize
    vacancy = vacancy.drop_duplicates()

    vacancy = vacancy.drop("benefit", axis=1)

    vacancy = vacancy.dropna()
    vacancy.set_index("id", inplace=True)
    vacancy["salary_min"] = pd.to_numeric(vacancy["salary_min"], errors="coerce")
    vacancy["salary_max"] = pd.to_numeric(vacancy["salary_max"], errors="coerce")
    vacancy["experience"] = pd.to_numeric(vacancy["experience"], errors="coerce")
    # vacancy["category"] = vacancy["category"].str.split(", ")


    total_median_salary = vacancy["salary_min"].median()
    total_mean_salary = vacancy["salary_min"].mean()
    # print_line(f"Total for Min salary:\nmedian: {median_salary}, mean: {mean_salary}")


    vacancy_slice_category = vacancy.groupby("category")["salary_min"].agg(["count", "mean", "median", "min", "max"])
    # print_line(f"Salary slice (categories):\n{vacancy_slice_category}")


    vacancy_slice_region = vacancy.groupby("region")["salary_min"].agg(["count", "mean", "median", "min", "max"])
    # print_line(vacancy_slice_region)

    vacancy_slice_exp = vacancy.groupby("experience")["salary_min"].agg(["count", "mean", "median", "min", "max"])
    # print_line(vacancy_slice_exp)

    vacancy_schedule = vacancy.groupby("schedule")["salary_min"].agg(["count", "mean", "median", "min", "max"])
    # print_line(vacancy_schedule)

    vacancy_reg_ctgr = pd.pivot_table(vacancy, "salary_min", "category", "region", "median", 0)
    # print_line(vacancy_reg_ctgr)

    statistics = {"vacancy":vacancy,
                    "total_median_salary":total_median_salary,
                    "total_mean_salary":total_mean_salary, 
                    "vacancy_slice_category":vacancy_slice_category, 
                    "vacancy_slice_region":vacancy_slice_region, 
                    "vacancy_slice_exp":vacancy_slice_exp, 
                    "vacancy_schedule":vacancy_schedule, 
                    "vacancy_reg_ctgr":vacancy_reg_ctgr,
                    }
    return statistics

get_stat(file_csv="vac.csv")