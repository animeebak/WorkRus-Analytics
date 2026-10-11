import requests as rq
import json
import os
from dotenv import load_dotenv
import sys

load_dotenv()


headers = {
    "User-Agent" : os.getenv("USER_AGENT"),
}


# запись вакансий в csv
import csv
from pprint import pprint
def write_csv(json_name : str, csv_name : str):
    with open(f"./json/{json_name}", "r", encoding="utf-8", newline="") as file:
        reader = json.load(file)
        with open(f"./csv/{csv_name}", "a", encoding="utf-8", newline="") as vac_csv:
            writer_csv = csv.writer(vac_csv)
            # writer_csv.writerow(["id", "category" "job_name", "schedule", "duty", "region", "salary_min", "salary_max", "education", "experience", "skills", "benefit", "company_name", "vac_url"])
            try:
                for el in reader["results"].get("vacancies"):
                    writer_csv.writerow([el["vacancy"].get("id"), 
                                        el["vacancy"].get("category").get("specialisation"),
                                        el["vacancy"].get("job-name"), 
                                        el["vacancy"].get("schedule"),
                                        el["vacancy"].get("duty"),
                                        el["vacancy"].get("region").get("name"), 
                                        el["vacancy"].get("salary_min"),
                                        el["vacancy"].get("salary_max"), 
                                        el["vacancy"].get("requirement").get("education"),
                                        el["vacancy"].get("requirement").get("experience"),
                                        el["vacancy"].get("skills"),
                                        el["vacancy"].get("benefit"),
                                        el["vacancy"].get("company").get("name"),
                                        el["vacancy"].get("vac_url"),
                                        ])
            except KeyError, TypeError:
                print("The number of pages that meet the query is less than what was requested.")
                sys.exit(1)
                




def send_req(count_pages, url):

    url += f"&offset={count_pages}&limit=100"
    response = rq.get(url, headers=headers)

    with open("./json/vac.json", "w", newline="", encoding="utf-8") as file:
        json.dump(response.json(), file, ensure_ascii=False, indent=" ")

    write_csv(json_name="vac.json", csv_name="vac.csv")



def start_scraping(url : str):
    count_pages = int(input("Count vacancy pages: \n>"))
    clean_csv = input('''
Clean vac.csv?
    0 - Yes
    1 - No
>''')
    if "0" in clean_csv:
        with open("./csv/vac.csv", "w", encoding="utf-8", newline="") as file:
            pass

    i = 0
    while i < count_pages:
        send_req(i, url)
        i+=1


def query_builder():
    params = set(input('''
Select the query parameters:
    0 - all vacancies [text, organized set, providing housing, social protected, experience]
    1 - search for region [text, organized set, providing housing, social protected, experience]
    2 - search for company [text, INN/OGRN, organized set, providing housing, social protected, experience]   
>'''))
    base_url = "http://opendata.trudvsem.ru/api/v1/vacancies"
    build_url = ""

    if "0" in params:
        text = ""
        org_set = ""
        prov_hous = ""
        soc_prot = ""
        exp = ""
        all_filters = set(input('''
Select filters:
    0 - text 
    1 - organized set
    2 - providing housing
    3 - social protected
    4 - experience
    5 - none
>'''))
        build_url += "?"
        if "5" not in all_filters:
            if "0" in all_filters:
                text += "text="
                text += input("Input filter text:\n>")
            if "1" in all_filters:
                org_set += input("Input org set:\n>")
                org_set += "=true"
            if "2" in all_filters:
                prov_hous += "accommodation="
                prov_hous += input("Input prov housing: \n>")
            if "3" in all_filters:
                soc_prot += "social_protected="
                soc_prot += input("Input social protected: \n>")
            if "4" in all_filters:
                exp += "experienceFrom="
                exp += input("Input experience min: \n>")
                exp += "&experienceTo="
                exp += input("Input experience max: \n")
            
            build_url += "&".join([text,org_set,prov_hous,soc_prot,exp])

        start_scraping(url="".join([base_url,build_url]))
        



    elif "1" in params:
        region_code = input("Input region code(format:6400000000000)\n>")
        build_url += f"/region/{region_code}"
        text = ""
        org_set = ""
        prov_hous = ""
        soc_prot = ""
        exp = ""
        reg_filters = set(input('''
Select filters:
    0 - text
    1 - organized set
    2 - providing housing
    3 - social protected
    4 - experience
    5 - none
>'''))
        build_url += "?"
        if "5" not in reg_filters:
            if "0" in reg_filters:
                text += "text="
                text += input("Input filter text:\n>")
            if "1" in reg_filters:
                org_set += input("Input org set:\n>")
                org_set += "=true"
            if "2" in reg_filters:
                prov_hous += "accommodation="
                prov_hous += input("Input prov housing: \n>")
            if "3" in reg_filters:
                soc_prot += "social_protected="
                soc_prot += input("Input social protected: \n>")
            if "4" in reg_filters:
                exp += "experienceFrom="
                exp += input("Input experience min: \n>")
                exp += "&experienceTo="
                exp += input("Input experience max: \n>")
            build_url += "&".join([text,org_set,prov_hous,soc_prot,exp])

        start_scraping(url="".join([base_url,build_url]))
        

    elif "2" in params:

        search_method = set(input('''
Select a search method:
    0 - by company code
    1 - by INN
    2 - by OGRN
>'''))
        if "0" in search_method:
            comp_code = input("Input company code: \n>")
            build_url += f"/company/{comp_code}"
            company_filters = set(input('''
Select filters:
    0 - text
    1 - organized set
    2 - providing housing
    3 - social protected
    4 - experience
    5 - none
>'''))
            build_url += "?"
            if "5" not in company_filters:
                if "0" in company_filters:
                    text += "text="
                    text += input("Input filter text:\n>")
                if "1" in company_filters:
                    org_set += input("Input org set:\n>")
                    org_set += "=true"
                if "2" in company_filters:
                    prov_hous += "accommodation="
                    prov_hous += input("Input prov housing: \n>")
                if "3" in company_filters:
                    soc_prot += "social_protected="
                    soc_prot += input("Input social protected: \n>")
                if "4" in company_filters:
                    exp += "experienceFrom="
                    exp += input("Input experience min: \n>")
                    exp += "&experienceTo="
                    exp += input("Input experience max: \n>")
                build_url += "&".join([text,org_set,prov_hous,soc_prot,exp])

            start_scraping(url="".join([base_url,build_url]))


def main():
    start_param = input('''
Select option:
    0 - Update vacancy list
    1 - view statistics
    2 - paint graph
>''')
    if start_param == "0":
        query_builder()
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()