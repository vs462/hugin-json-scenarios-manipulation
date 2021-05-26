import json

subdomain = 'test_sub' # org subdomain

dataset_gp = 1111 # apple
dataset_ap = 1112 # google

from_date = '2021-01-01'
to_date = '2021-02-01'

company_name = 'Company Name' # just to be displayed in the scenario/agents names 

file_save_name = 'competitor_huginn_json_company_X' # name of the json file that'll be saved on your computer

external_ids = {'app_ext_id':'app_name', 
                'app_ext_id2':'app_name2',
                'app_ext_id3':'app_name3'}

backdate = True 

frequency = "every_1h" # no need to specify frequency if Backdate = True

possible_freq = """every_1m, every_2m, every_5m, every_10m, every_30m, every_1h, every_2h, every_5h, 
                every_12h, every_1d, every_2d, every_7d, midnight, 1am, 2am, 3am, 4am, 5am, 6am, 7am, 8am, 
                9am, 10am, 11am, noon, 1pm, 2pm, 3pm, 4pm, 5pm, 6pm, 7pm, 8pm, 9pm, 10pm, 11pm, every_sunday, 
                every_monday, every_tuesday, every_wednesday, every_thursday, every_friday, every_saturday, 
                every_month, never"""
 
    
def main(company_name, subdomain, dataset_gp, dataset_ap, external_ids, backdate, frequency):
    mode = 'BACKDATE' if backdate else "LIVE"
    agents = create_agents(company_name, subdomain, dataset_gp, dataset_ap, mode, backdate, frequency)
    links = create_links(external_ids)
    return compose_scenario(agents, links, mode)  

def create_agents(company_name, subdomain, dataset_gp, dataset_ap, mode, backdate, frequency):
    create_resp = create_resp_appfl(company_name, subdomain, dataset_gp, dataset_ap, external_ids, mode)
    agents = [create_resp]
    
    for key in external_ids: 
        appfollow_agent = appfollow_fetch(company_name, key, external_ids[key], from_date, to_date, backdate, frequency)
        agents.append(appfollow_agent)
       
    return agents     

   
def create_links(external_ids):
    links = [{"source": num+1, "receiver": 0 } for num in range(len(external_ids))]
    return links


def compose_scenario(agents, links, mode):    
    scenario = {
      "schema_version": 1,
      "name": f"{company_name} Competitor Appfollow {mode}",
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

def create_resp_appfl(company_name, subdomain, dataset_gp, dataset_ap, ext_ids_mappings, mode):
    create_response_agent = {
      "type": "Agents::ChattermillResponseAgent",
      "name": f" {company_name} Competitor Appfollow Create Response {mode}",
      "disabled": False,
      "guid": "",
      "options": {
        "organization_subdomain": "subdomain",
        "id": "",
        "comment": "{{ content }}",
        "score": "{{ rating }}",
        "data_type": "",
        "data_source": "",
        "dataset_id": "{{ store | replace: \"gp\"," + f'{dataset_gp} | replace: \"as\", {dataset_ap}' + "}}",
        "created_at": "{{date}} {{time}}",
        "user_meta": {
          "title": {
            "type": "text",
            "name": "Title",
            "value": "{{title}}"
          },
          "response_id": {
            "type": "text",
            "name": "Response ID",
            "value": "{{internal_id}}"
          },
          "author": {
            "type": "text",
            "name": "Author",
            "value": "{{author}}"
          },
          "external_id": {
            "type": "text",
            "name": "External ID",
            "value": "{{external_id}}"
          },
          "review_id": {
            "type": "text",
            "name": "Review ID",
            "value": "{{review_id}}"
          },
          "user_id": {
            "type": "text",
            "name": "User ID",
            "value": "{{user_id}}"
          }
        },
        "segments": {
          "company": {
            "type": "text",
            "name": "Company",
            "value": "{{external_id}}"
          },
          "app_version": {
            "type": "text",
            "name": "App Version",
            "value": "{{app_version}}"
          },
          "iso": {
            "type": "text",
            "name": "ISO",
            "value": "{{country}}"
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
          "segments.company.value": ext_ids_mappings
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
    
def appfollow_fetch(company_name, external_id, app_name, from_date, to_date, backdate = True, frequency = "never" ):
    appfollow = {
          "type": "Agents::AppfollowAgent",
          "name": f"{company_name} {app_name} AppFollow Fetch ({external_id}) {'BACKDATE' if backdate else 'LIVE'}",
          "disabled": False,
          "guid": "",
          "options": {
            "backdate_enabled_radio": backdate,
            "backdate_enabled": backdate,
            "client_id": "25227",
            "api_secret": "QkAB7RfnQ7Uy4mDA2bfs",
            "api_method": "reviews",
            "collection_name": "",
            "external_id": external_id,
            "from_date": from_date,
            "to_date": to_date,
            "page": "1",
            "page_size": "1000",
            "mode": "on_change",
            "expected_update_period_in_days": "1",
            "deduplication_fields": "review_id,content,rating",
            "uniqueness_look_back": "1000"
          },
          "schedule": "never",
          "keep_events_for": 2592000,
          "propagate_immediately": True
        }
    if not backdate:
        appfollow['options']['backdate_enabled_radio'] = False
        appfollow['options']['backdate_enabled'] = False
        appfollow['schedule'] = frequency
        
    return appfollow

scenario = main(company_name, subdomain, dataset_gp, dataset_ap, external_ids, backdate, frequency)


with open(f'{file_save_name}.json', 'w') as outfile:
    json.dump(scenario, outfile)