import json

subdomain = 'test_sub' # org subdomain

dataset_id = 1111

from_date = '2021-01-01'
to_date = '2021-02-01'

company_name = '123 Company Name' # just to be displayed in the scenario/agents names 

file_save_name = 'competitor_huginn_json_company_X' # name of the json file that'll be saved on your computer

business_ids = {'business_id':'comp_name', 
                'business_id2':'comp_name2',
                'business_id3':'comp_name3'}

backdate = False 

frequency = "every_1h" # no need to specify frequency if Backdate = True

possible_freq = """every_1m, every_2m, every_5m, every_10m, every_30m, every_1h, every_2h, every_5h, 
                every_12h, every_1d, every_2d, every_7d, midnight, 1am, 2am, 3am, 4am, 5am, 6am, 7am, 8am, 
                9am, 10am, 11am, noon, 1pm, 2pm, 3pm, 4pm, 5pm, 6pm, 7pm, 8pm, 9pm, 10pm, 11pm, every_sunday, 
                every_monday, every_tuesday, every_wednesday, every_thursday, every_friday, every_saturday, 
                every_month, never"""
    
def main(company_name, subdomain, dataset_id, external_ids, backdate, frequency):
    mode = 'BACKDATE' if backdate else "LIVE"
    agents = create_agents(company_name, subdomain, dataset_id, mode, backdate, frequency)
    links = create_links(external_ids)
    return compose_scenario(agents, links, mode)  

def create_agents(company_name, subdomain, dataset_id, mode, backdate, frequency):
    create_resp = create_resp_trust(company_name, subdomain, dataset_id, mode)
    agents = [create_resp]
    
    for key in business_ids: 
        trustpilot_agent = trustpilot_fetch(company_name, key, business_ids[key], from_date, to_date, backdate, frequency)
        agents.append(trustpilot_agent)
       
    return agents     

   
def create_links(external_ids):
    links = [{"source": num+1, "receiver": 0 } for num in range(len(external_ids))]
    return links

def compose_scenario(agents, links, mode):    
    scenario = {
      "schema_version": 1,
      "name": f"{company_name} Competitor Trustpilot {mode}",
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

def trustpilot_fetch(company_name, business_id, app_name, from_date, to_date, mode, backdate = True, frequency = "never" ):
    option_mode = "all" if backdate else "on_change"
    trustpilot = {
          "type": "Agents::TrustPilotAgent",
          "name": f"{company_name} {app_name} Trustpilot Fetch ({business_id}) {mode}",
          "disabled": False,
          "guid": "",
          "options": {
            "backdate_enabled_radio": True,
            "backdate_enabled": True,
            "api_key": "{% credential TrustPilotApiKey %}",
            "api_secret": "{% credential TrustPilotApiSecret %}",
            "business_units_ids": business_id,
            "mode": option_mode,
            "access_token": "1",
            "refresh_token": "1",
            "expires_at": "1",
            "expected_update_period_in_days": "2"
          },
          "schedule": "never",
          "keep_events_for": 2592000
        }
    if not backdate:
        trustpilot['options']['backdate_enabled_radio'] = False
        trustpilot['options']['backdate_enabled'] = False
        trustpilot['schedule'] = frequency
        
    return trustpilot

def create_resp_trust(company_name, subdomain, dataset_id, mode):
    create_response_agent = {
      "type": "Agents::ChattermillResponseAgent",
      "name": f" {company_name} Competitor Trustpilot Create Response {mode}",
      "disabled": False,
      "guid": "",
      "options": {
        "organization_subdomain": subdomain,
        "id": "",
        "comment": "{{ comment }}",
        "score": "{{ score }}",
        "data_type": "",
        "data_source": "",
        "dataset_id": dataset_id,        
        "created_at": "{{ created_at }}",
        "user_meta": {
            "response_id": {
              "type": "text",
              "name": "Response ID",
              "value": "{{response_id}}"
            },
            "title": {
              "type": "text",
              "name": "Title",
              "value": "{{title}}"
            }
        },
        "segments": {
          "company": {
            "type": "text",
            "name": "Company",
            "value": "{{ raw_json.business_unit.display_name }}"
          },
          "language": {
            "type": "text",
            "name": "Language",
            "value": "Unknown"
          }
        },
        "extra_fields": {
        },
        "mappings": {
        },
        "bucketing": {
        },
        "emit_events_radio": "true",
        "emit_events": "true",
        "expected_receive_period_in_days": "1",
        "send_batch_events_radio": "false",
        "send_batch_events": "false",
        "max_events_per_batch": "30"
      },
      "schedule": "never",
      "keep_events_for": 2592000,
      "propagate_immediately": False
    }
    return create_response_agent

scenario = main(company_name, subdomain, dataset_id, business_ids, backdate, frequency)

with open(f'{file_save_name}.json', 'w') as outfile:
    json.dump(scenario, outfile)