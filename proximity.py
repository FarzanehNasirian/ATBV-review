import pandas as pd
import networkx as nx
from network_utils import calculate_proximity
from proximity.network import Network
import multiprocessing as mp
import json
import sys

if __name__ == '__main__':
    
    G = nx.from_pandas_edgelist(pd.read_csv('../ppi/data/Gene_Gene.csv'), 'source', 'target')
    
    chemTar = pd.read_csv('data/chemical_target.csv')
    chemTar = chemTar[chemTar.GeneId.isin(G.nodes())]
    chemTar = chemTar.groupby('chemName')['GeneId'].apply(set).to_dict()
    
    disease = pd.read_csv('data/cvd_genes.csv')
    disease = disease[disease.GeneId.isin(G.nodes())]
    disease = disease.groupby('efoName')['GeneId'].apply(set).to_dict()
    
    """#networkx    
    data_points = [(G, v1, v2) for _,v1 in chemTar.items() for _,v2 in disease.items()]
    pool = mp.Pool() #all cores
    res = pool.starmap(calculate_proximity, data_points[1:2])"""
    
    #graph_tool
    net = Network(G)
    data_points = [(v1, v2) for _,v1 in chemTar.items() for _,v2 in disease.items()]
    data_lables = [(k1, k2) for k1,_ in chemTar.items() for k2,_ in disease.items()]
    print(len(data_points))
    
    i = int(sys.argv[1])
    j = int(sys.argv[2])
    pool = mp.Pool() #all cores
    res = pool.starmap(net.get_proximity, data_points[i:j])
    res = pd.concat([pd.DataFrame(data_lables[i:j], columns=['chemName', 'efoName']), pd.DataFrame(res)], axis=1) 
    res.to_json('data/out_{}_{}.json'.format(i, j))
    

