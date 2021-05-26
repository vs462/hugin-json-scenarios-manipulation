import fetch_agents as agnt

subdomain = 'test_sub'
dataset_gp = 11
dataset_ap = 12
external_id = 'test.io'
from_date = '2021-01-01'
to_date = '2021-02-01'
company_name = 'Company Name'

file_save_name = 'competitor_huginn_json_company_X'

external_ids = {'app_ext_id':'app_name', 
                'app_ext_id2':'app_name2',
                'app_ext_id3':'app_name3'}

backdate = True 
frequency = "every_1h" # no need to specify frequency if Backdate = True



class Integration:
    def __init__(self, company_name, subdomain, dataset_gp, dataset_ap, external_ids, backdate, frequency,
                 external_id, from_date, to_date):
        self.subdomain = subdomain
        self.dataset_gp = dataset_gp
        self.dataset_ap = dataset_ap
        self.external_id = external_id
        self.from_date = from_date
        self.to_date = to_date
        self.company_name = company_name
        self.external_ids = external_ids
        self.backdate = backdate
        self.frequency = frequency

    def main(self):
        agents = self.create_agents()
        links = self.create_links(self.external_ids)
        return self.compose_scenario(agents, links)  

    def create_agents(self):
        create_resp = agnt.create_resp_appfl()
        agents = [create_resp]
        
        for key in self.external_ids: 
            appfollow_agent = agnt.appfollow_fetch(self.company_name, self.key, self.external_ids[key], self.from_date, self.to_date, self.backdate, self.frequency)
            agents.append(appfollow_agent) 
        return agents     
    
    def create_links(self):
        links = [{"source": num+1, "receiver": 0 } for num in range(len(self.external_ids))]
        return links

    def compose_scenario(self):    
        scenario = {
          "schema_version": 1,
          "name": f"123 {self.company_name} Competitor Appfollow",
          "description": "No description provided",
          "source_url": False,
          "guid": "",
          "tag_fg_color": "#ffffff",
          "tag_bg_color": "#5bc0de",
          "icon": "gear",
          "exported_at": "2021-05-20T12:10:15Z",
          "agents": self.agents,
          "links": self.links,
          "control_links": [
          ]
        }
        return scenario

# obj = Integration(company_name, subdomain, dataset_gp, dataset_ap, external_ids, backdate, frequency,
#                  external_id, from_date, to_date)

class Integration2:
    def __init__(self, info):

        for key in info:
            self.key = info[key]
            print(self.key)

        #self.agents = self.create_agents()
        #self.links = self.create_links(self.external_ids)

    # def create_agents(self):
    #     create_resp = agnt.create_resp_appfl(self.company_name, self.subdomain, self.dataset_gp, self.dataset_ap, self.ext_ids_mappings)
    #     agents = [create_resp]
        
    #     for key in self.external_ids: 
    #         appfollow_agent = agnt.appfollow_fetch(self.company_name, self.key, self.external_ids[key], self.from_date, self.to_date, self.backdate, self.frequency)
    #         agents.append(appfollow_agent) 
    #     return agents     
    
    # def create_links(self):
    #     links = [{"source": num+1, "receiver": 0 } for num in range(len(self.external_ids))]
    #     return links

    # def compose_scenario(self):    
    #     scenario = {
    #       "schema_version": 1,
    #       "name": f"123 {self.company_name} Competitor Appfollow",
    #       "description": "No description provided",
    #       "source_url": False,
    #       "guid": "",
    #       "tag_fg_color": "#ffffff",
    #       "tag_bg_color": "#5bc0de",
    #       "icon": "gear",
    #       "exported_at": "2021-05-20T12:10:15Z",
    #       "agents": self.agents,
    #       "links": self.links,
    #       "control_links": [
    #       ]
    #     }
    #     return scenario
    
 
info ={'subdomain' : 'test_sub',
        'dataset_gp' : 11,
        'dataset_ap' : 12,
        'external_id' : 'test.io',
        'from_date' : '2021-01-01',
        'to_date' : '2021-02-01',
        'company_name' : 'Company Name',
        'file_save_name' : 'competitor_huginn_json_company_X',
        'external_ids' : {
            'app_ext_id':'app_name', 
            'app_ext_id2':'app_name2',
            'app_ext_id3':'app_name3'},
        'backdate' : True ,
        'frequency' : "every_1h" # no need to specify frequency if Backdate = True
       }

obj = Integration2(info)
attrs = vars(obj)

# with open(f'{file_save_name}.json', 'w') as outfile:
#     json.dump(obj, outfile)





