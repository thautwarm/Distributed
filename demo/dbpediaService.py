# -*- coding: utf-8 -*-
"""
Created on Sun May 28 23:18:12 2017

@author: thautwarm
"""
def beginWith(Astr,begin):
    return Astr[:len(begin)]==begin

from SPARQLWrapper import SPARQLWrapper,JSON
headerLength=len("http://dbpedia.org/resource/")
class DBPediaSPARQL:
    @staticmethod
    def CountEntitiesOfType(Type:str):
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        body=\
        """
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbr: <http://dbpedia.org/resource/>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT DISTINCT (COUNT(?resource) AS ?count)
        WHERE {{?resource a dbo:{Type} }}
        """.format(Type=Type)
        sparql.setQuery(body)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return int(results["results"]["bindings"][0]["count"]["value"])
    def getAbstract(item,limit=1000):
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        body=\
        """
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbr: <http://dbpedia.org/resource/>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT DISTINCT ?resource ?abstract ?type
        WHERE {{ ?resource a dbo:{item} . ?resource dbo:abstract ?abstract .
               OPTIONAL {{ ?resource a ?type . ?type owl:sameAs? dbo:{item} }}
        FILTER (lang(?abstract) = 'en')
        }} LIMIT {limit} 
        """.format(item=item,limit=limit)
        sparql.setQuery(body)
        sparql.setReturnFormat(JSON)
        
        results = sparql.query().convert()  
        Ret=[]
        for result in results["results"]["bindings"]:
            Ret.append(
            (result["resource"]["value"][headerLength:], result["abstract"]["value"])
                        )
        return Ret


        
            
            

    