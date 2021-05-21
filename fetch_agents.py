
def create_resp_appfl(company_name, subdomain, dataset_gp, dataset_ap, ext_ids_mappings):
    create_response_agent = {
      "type": "Agents::ChattermillResponseAgent",
      "name": f" {company_name} Competitor Appfollow Create Response",
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
    
def appfollow_fetch(company_name, external_id, app_name, from_date, to_date, backdate = True, frequency = "every_1d" ):
    appfollow = {
          "type": "Agents::AppfollowAgent",
          "name": f"{company_name} {app_name} AppFollow Fetch ({external_id})",
          "disabled": False,
          "guid": "",
          "options": {
            "backdate_enabled_radio": True,
            "backdate_enabled": True,
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
          "propagate_immediately": False
        }
    if backdate:
        appfollow['options']['backdate_enabled_radio'] = True
        appfollow['options']['backdate_enabled'] = True
    else:
        appfollow['schedule'] = frequency
        
    return appfollow
 

   
def trustpilot(business_units_ids):
    trustpilot = {
          "type": "Agents::TrustPilotAgent",
          "name": "Trustpilot Fetch Copy",
          "disabled": False,
          "guid": "",
          "options": {
            "backdate_enabled_radio": "false",
            "backdate_enabled": "false",
            "api_key": "YhzbqU4GeR6mQ2bHF97PYKUWCSkaaeG0",
            "api_secret": "Api Secret",
            "business_units_ids": "Business IDs",
            "mode": "on_change",
            "access_token": "",
            "refresh_token": "",
            "expires_at": "",
            "expected_update_period_in_days": "2"
          },
          "schedule": "every_30m",
          "keep_events_for": 2592000
        }
    return trustpilot


