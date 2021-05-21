import json
import fetch_agents as agnt

subdomain = 'test_sub'
dataset_gp = 11
dataset_ap = 12
external_id = 'test.io'
from_date = '2021-01-01'
to_date = '2021-02-01'
company_name = 'Company Name'

external_ids = {'app_ext_id':'app_name', 
                'app_ext_id2':'app_name2',
                'app_ext_id3':'app_name3'}

backdat = True 
frequency = "every_1h" # no need to specify frequency if Backdate = True

possible_freq = """every_1m, every_2m, every_5m, every_10m, every_30m, every_1h, every_2h, every_5h, 
                every_12h, every_1d, every_2d, every_7d, midnight, 1am, 2am, 3am, 4am, 5am, 6am, 7am, 8am, 
                9am, 10am, 11am, noon, 1pm, 2pm, 3pm, 4pm, 5pm, 6pm, 7pm, 8pm, 9pm, 10pm, 11pm, every_sunday, 
                every_monday, every_tuesday, every_wednesday, every_thursday, every_friday, every_saturday, 
                every_month, never"""

def main():
    links = create_links(external_ids)
    agents = create_agents(company_name, subdomain, dataset_gp, dataset_ap)
    return compose_scenario(agents, links)  
    
def create_links(external_ids):
    links = [{"source": num+1, "receiver": 0 } for num in range(len(external_ids))]
    return links

def create_agents(company_name, subdomain, dataset_gp, dataset_ap):
    create_resp = agnt.create_resp_appfl(company_name, subdomain, dataset_gp, dataset_ap, external_ids)
    agents = [create_resp]
    
    for key in external_ids: 
        appfollow_agent = agnt.appfollow_fetch(company_name, key, external_ids[key], from_date, to_date )
        agents.append(appfollow_agent)
        
    return agents

def compose_scenario(agents, links):    
    scenario = {
      "schema_version": 1,
      "name": f"123 {company_name} Competitor Appfollow",
      "description": "No description provided",
      "source_url": False,
      "guid": "",
      "tag_fg_color": "#ffffff",
      "tag_bg_color": "#5bc0de",
      "icon": "gear",
      "exported_at": "2021-05-20T12:10:15Z",
      "agents": agents,
      "links": links,
      "control_links": [
      ]
    }
    return scenario

scenario = main()

with open('test.json', 'w') as outfile:
    json.dump(scenario, outfile)




