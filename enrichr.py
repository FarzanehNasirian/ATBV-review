import pandas as pd
import requests
import json

def enrichr(Input, lib):
    #Input: a dataframe of sets that are of interst for enrichement analysis. columns are "set" and "genes" 
    #lib: gene set lib for enrichement analysis
    #df: dataframe of enrichement results 

    df = [] 
    for i in Input.index:
        lisT = Input.loc[i].tolist()
        ENRICHR_URL = 'http://maayanlab.cloud/Enrichr/addList'
        genes_str = '\n'.join(lisT[1])  
        description = 'None'
        payload = {
            'list': (None, genes_str),
            'description': (None, description)
        }

        response = requests.post(ENRICHR_URL, files=payload)
        if not response.ok:
            raise Exception('Error analyzing gene list')

        ENRICHR_URL = 'http://maayanlab.cloud/Enrichr/enrich'
        query_string = '?userListId=%s&backgroundType=%s'
        user_list_id = json.loads(response.text)['userListId']

        response = requests.get(
            ENRICHR_URL + query_string % (user_list_id, lib)
        )
        if not response.ok:
            raise Exception('Error fetching enrichment results')
            
        data = json.loads(response.text)  
        for value in list(data.values())[0]:
            df.append([lisT[0], value[1], value[6]])

    df = pd.DataFrame(df, columns=['set_A', 'set_B', 'adj_p_value'])
    return(df)