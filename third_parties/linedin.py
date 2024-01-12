import os
import requests


def scrape_linkedin_profile(linkedin_frofile_url: str):
    response = requests.get(linkedin_frofile_url)

    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certinfications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")
    return data


print(scrape_linkedin_profile)
