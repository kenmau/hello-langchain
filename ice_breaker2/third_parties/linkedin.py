import os
import requests

from dotenv import load_dotenv

def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """
    scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile
    :param linkedin_profile_url:
    :param mock:
    :return:
    """

    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/kenmau/0f128075b9ea2561792b2761b4062af8/raw/6e826183bb1c651a00b0ffad60322abfc4a0e66b/eden-marco.json"
        response = requests.get(
            linkedin_profile_url,
            timeout=10
        )
    else:
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        header_dic = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
        response = requests.get(
            api_endpoint,
            params={"url": linkedin_profile_url},
            headers=header_dic,
            timeout=10
        )

    # print(response.status_code)
    # print(response.text)

    data = response.json()

    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
           and k not in ["people_also_viewed", "certifications"]
    }

    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data

if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            linkedin_profile_url="https://www.linkedin.com/in/eden-marco/",
            mock=True
        )
    )