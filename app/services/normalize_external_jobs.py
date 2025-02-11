from xml.etree import ElementTree

def parse_skills(xml_str: str) -> list:
    try:
        root = ElementTree.fromstringlist(xml_str)
        return [skill.text for skill in root.findall('skill')]
    except ElementTree.ParseError:
        return []

def normalize_external_jobs(external_datas: dict) -> list:
    jobs = []

    for country, job_list in external_datas.items():
        for job_array in job_list:
            jobs.append({ # TODO: check if correct order
                "title" : job_array[0],
                "salary" : job_array[1],
                "country" : country,
                "skills" : parse_skills(job_array[2]),
                "source" : "external" # TODO: necessary?
            })

    return jobs


def merge_jobs(internal_jobs: list, external_jobs: list) -> list:
    seen = set()
    combined_jobs = []
    for job in internal_jobs + external_jobs:
        key = f"{job['title']} - {job['country']} - {job['salary']}"
        if key not in seen:
            seen.add(key)
            combined_jobs.append(job)
    return combined_jobs