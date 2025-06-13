from classes.request.JDM_API import JDM_API
from classes.save.ObjectSaver import ObjectSave


api = JDM_API()
saver = ObjectSave()
relationFileName = "relations.json"
nodesFileName = "nodes.json"

annotation = {"vrai":1.8,"peu pertinent":0.8,"impossible":0,"toujours vrai":4, "pertinent" : 1.1, "non pertinent" : 0.2, "peu pertinent": 0.4, "discutable": 0.4, "souhaitable":1.7, "non souhaitable" : 0.7, "probable":1.6, "improbable": 0}

def getNodeById(id : int):
    node = saver.getElementByID(id,nodesFileName)
    if node == None or len(node) == 0:
        node = api.getNodeById(id)
        saver.writeDataIntoJson(nodesFileName, node)
        return node
    return node
def getNodeByName(name : str):
    node = saver.getElementByName(name,nodesFileName)
    if node == None or len(node) == 0:
        node = api.getNodeByName(name)
        saver.writeDataIntoJson(nodesFileName, node)
        return node
    return node
def getRelationBetweenTwoNodes(node1 : str, node2 : str):
    relation = saver.getRelationBetweenTwoNodes(node1, node2, relationFileName)
    if relation == None or len(relation) == 0:
        data = api.getRelationsBetweenTwoNodes(node1, node2)
        data_r = {rel['id']: rel for rel in data['relations']}
        data_n = {rel['id']: rel for rel in data['nodes']}
        relations = {}
        for r in data_r.values():
            relations[r.get("id")] = r
            saver.writeDataIntoJson(relationFileName, r)
        for n in data_n.values():
            saver.writeDataIntoJson(nodesFileName, n)
        return relations
    return relation
def getRelationsToNode(node2_name : str,
        types_ids : int = None,
        not_type_ids : list[int] = None,
        min_weight : int = None,
        max_weight : int = None,
        relation_fields : list[str] = None,
        node_fields : list[str] = None,
        limit : int = None,
        without_nodes : bool = None):
    
    data = saver.getRelationsToNode(node2_name, type_id=types_ids)
    if data != None and len(data) != 0:
        return data
    data = api.getRelationsToNode(node2_name, types_ids=types_ids, max_weight=max_weight, min_weight=min_weight,relation_fields=relation_fields,limit=limit)
    data_r = {rel['id']: rel for rel in data['relations']}
    relations = {}
    for r in data_r.values():
        relations[r.get("id")] = r
    return relations

def getRelationFromNode(node_name : str,
        types_ids : int = None,
        not_type_ids : list[int] = None,
        min_weight : int = None,
        max_weight : int = None,
        relation_fields : list[str] = None,
        node_fields : list[str] = None,
        limit : int = None,
        without_nodes : bool = None):
    data = saver.getRelationFromNode(node_name, types_ids)
    if data != None and len(data) != 0:
        return data
    data = api.getRelationsFromNode(node_name, types_ids=types_ids, max_weight=max_weight, min_weight=min_weight,relation_fields=relation_fields,limit=limit)
    data_r = {rel['id']: rel for rel in data['relations']}
    data_n = {rel['id']: rel for rel in data['nodes']}
    relations = {}
    for r in data_r.values():
        relations[r.get("id")] = r
    return relations

def deductionClassique(node1 : str, node2 : str):
    deduction(node1,node2,6,24)

def synonyme(node1 : str, node2 : str):
    deduction(node1, node2, 5, 24)
    
def transitivité(node1 : str, node2 : str, type_id : int):
    deduction(node1, node2, type_id, type_id)

def deduction(node1 : str, node2 : str, first_rel : int,second_rel : int):
    relations = []
    isARelations = getRelationFromNode(node_name=node1, types_ids=first_rel, min_weight=25)
    searchedRelation = getRelationsToNode(node2, types_ids=second_rel, min_weight=25)

    for e in searchedRelation.values():
        for isa in isARelations.values():
            if (isa.get("node2") == e.get("node1")):
                relation = {}
                node1_id = isa.get("node1")
                node2_id = isa.get("node2")
                node3_id = e.get("node2")
                node1 = getNodeById(node1_id)
                node2 = getNodeById(node2_id)
                node3 = getNodeById(node3_id)
            
                second = api.getRelationAnnotation(e.get("id"))
                second_weight = e.get("w")
                for a in second:
                    value = annotation.get(a.get("name"))
                    if value == None:
                        value = 1
                    second_weight = second_weight * value
                
                first = api.getRelationAnnotation(isa.get("id"))
                first_weight = isa.get("w")
                for a in first:
                    value = annotation.get(a.get("name"))
                    if value == None:
                        value = 1
                    first_weight = first_weight * value
                
                relation["node1"] = node1
                relation["node2"] = node2
                relation["node3"] = node3
                relation["isa"] = isa
                relation["searchedRelation"] = e
                relation["e_w"] = second_weight
                relation["isa_w"] = first_weight
                relations.append(relation)
    relations.sort(key=lambda d: d["e_w"] * 0.6 + d["isa_w"] * 0.4, reverse=True)
    for r in relations:
        isa_r = r.get("isa")
        searched_r = r.get("searchedRelation")
        
        n1 = r.get("node1")
        n2 = r.get("node2")
        n3 = r.get("node3")
        a = f"{n1.get("name")} -( {r.get("isa_w")} )> {n2.get("name")} -( {r.get("e_w")} )> {n3.get("name")}"
        print(a)

def readRelationDict(relations : dict):
    for r in relations.values():
        node1_id = r.get("node1")
        node2_id = r.get("node2")
        node1 = getNodeById(node1_id)
        node2 = getNodeById(node2_id)
        a = f"{node1.get("name")} - is a > {node2.get("name")} : {r.get("w")}"
        print(a)
    
if __name__ == "__main__":
    #synonyme("tigre","chasser")
    #deductionClassique("pigeon","voler")
    #transitivité("Tour Eiffel", "France",15)
    transitivité("piston","voiture",10)

    
