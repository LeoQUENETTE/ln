from classes.request.CustomRequestClass import CustomRequestClass
import json

from classes.save.ObjectSaver import ObjectSave
class JDM_API():
    '''
    Classe généralisant toutes les requêtes vers l'API JDM
    Utilise grandement la classe CustomRequestClass, qui elle traite toutes les requêtes
    '''
    def __init__(self):
        '''Récupération de la classe R'''
        self.R : CustomRequestClass = CustomRequestClass()
        self.url : str = "https://jdm-api.demo.lirmm.fr/v0/"
    
    def addAttributes(self, url: str,attributeName : str, value : any, isFirst : bool = False) -> str :
        if (attributeName == None or value == None or attributeName == "" or value == ""):
            return url
        if isFirst:
            url = url + "?"
        else:
            url = url + "&"
        return url + attributeName+"="+str(value)
    
    def getRedirectSchema(self, node_id : int):
        '''
        Fonction renvoyant quelque chose
        '''
        pass
    
    def getNodeById(self, node_id : int) -> dict:
        '''
        Fonction renvoyant un noeud grâce à son id
        Utilise l'id pour rechercher le noeud dans la liste des noeuds enregistrer ou fais une requête à l'api
        '''
        url: str = self.url + "/node_by_id/" +str(node_id)
        return json.loads(self.R.getRequest(url))
    def getNodeByName(self, node_name : str) -> dict:
        '''
        Fonction renvoyant un noeud grâce à son nom
        Utilise le nom pour rechercher le noeud dans la liste des noeuds enregistrer ou fais une requête à l'api
        '''
        url: str = self.url + "/node_by_name/" + node_name
        return json.loads(self.R.getRequest(url))
    def getRelationsBetweenTwoNodes(self, 
        node1_name :str,
        node2_name : str,
        types_ids : int = None,
        not_type_ids : list[int] = None,
        min_weight : int = None,
        max_weight : int = None,
        relation_fields : list[str] = None,
        node_fields : list[str] = None,
        limit : int = None,
        without_nodes : bool = None
        ) -> dict[int : str]:
        '''
        Fonction pour récupérer les relations entre deux noeuds
        Fais une recherche parmi les relations enregistrer, sinon fais une requête
        Obligatoire : 
            node1_name : Nom du noeud d'où part la relation
            node2_name : Nom du noeud qui reçoit la relation
        Renvoie:
            Liste de toutes les relations entre ces noeuds
        '''
        saver = ObjectSave()
        url = self.url + f"/relations/from/{node1_name}/to/{node2_name}"
        url = self.typicalAttributes(url, types_ids, not_type_ids, min_weight, max_weight, relation_fields, node_fields, limit, without_nodes)
        r= self.R.getRequest(url)
        data = json.loads(r)
        saver.dumpData(f"from_{node1_name}_to_{node2_name}", data)
        return data
    def getRelationsFromNode(
        self, 
        node1_name : str,
        types_ids : int = None,
        not_type_ids : list[int] = None ,
        min_weight : int = None,
        max_weight : int = None,
        relation_fields : list[str] = None,
        node_fields : list[str] = None,
        limit : int = None,
        without_nodes : bool = None) -> dict[int : dict]:
        '''
        Fonction permettant de récupérer les relations partant d'un noeud
        Fais une recherche parmi les relations enregistrer, sinon fais une requête
        Renvoie:
            Liste de toutes les relations partant du noeud
        ''' 
        saver = ObjectSave()
        url = self.url + f"/relations/from/{node1_name}"
        url = self.typicalAttributes(url, types_ids, not_type_ids, min_weight, max_weight, relation_fields, node_fields, limit, without_nodes)
        r= self.R.getRequest(url)
        data = json.loads(r)
        saver.dumpData(f"from_{node1_name}", data)
        return data
    def getRelationsToNode(
        self, 
        node2_name : str,
        types_ids : int = None,
        not_type_ids : list[int] = None,
        min_weight : int = None,
        max_weight : int = None,
        relation_fields : list[str] = None,
        node_fields : list[str] = None,
        limit : int = None,
        without_nodes : bool = None) -> list[dict]:
        '''
        Fonction permettant de récupérer les relations allant vers un noeud
        Fais une recherche parmi les relations enregistrer, sinon fais une requête
        Renvoie:
            Liste de toutes les relations allant vers le noeud
        '''
        saver = ObjectSave()
        url = self.url + f"/relations/to/{node2_name}"
        url = self.typicalAttributes(url, types_ids, not_type_ids, min_weight, max_weight, relation_fields, node_fields, limit, without_nodes)
        r= self.R.getRequest(url)
        data = json.loads(r)
        saver.dumpData(f"to_{node2_name}", data)
        return data
    
    def getRelationAnnotation(self, relId : int):
        url = self.url + f"/relations/from/:r{relId}"
        r = self.R.getRequest(url)
        data = json.loads(r)
        annotation = data.get("nodes")
        if annotation != None:
            c = 0
            for d in annotation:
                if d.get("name") == "Relation:" or d.get("name") == f":r{relId}":
                    del annotation[c]
                c = c +1 
            return annotation
        return []
    def splitRequest(self, r : str) -> dict[str : str]:
        '''
        Fonction pas folle pour découper les json
        '''
        r = r.replace("{", "")
        r = r.replace("}", "")
        r = r.replace(f'"',"")
        list_r = r.split(",")
        node_dict = {}
        for char in list_r:
            elem = char.split(":")
            node_dict[elem[0]] = elem[1]
        return node_dict
    def typicalAttributes(self, url,
        types_ids : int,
        not_type_ids : list[int],
        min_weight : int,
        max_weight : int,
        relation_fields : list[str],
        node_fields : list[str],
        limit : int,
        without_nodes : bool)->str:
        nbAttribute : int = 0
        if (types_ids != None):
            url = self.addAttributes(url,"types_ids",types_ids, nbAttribute == 0)
            nbAttribute += 1
        if (not_type_ids != None):
            url = self.addAttributes(url,"not_type_ids",not_type_ids, nbAttribute == 0)
            nbAttribute += 1
        if (relation_fields != None):
            url = self.addAttributes(url,"relation_fields",relation_fields, nbAttribute == 0)
            nbAttribute += 1
        if (node_fields != None):
            url = self.addAttributes(url,"node_fields",node_fields, nbAttribute == 0)
            nbAttribute += 1
        if (min_weight != None):
            url = self.addAttributes(url,"min_weight",min_weight, nbAttribute == 0)
            nbAttribute += 1
        if (max_weight != None):
            url = self.addAttributes(url,"max_weight",max_weight, nbAttribute == 0)
            nbAttribute += 1
        if (limit != None):
            url = self.addAttributes(url,"limit",limit, nbAttribute == 0)
            nbAttribute += 1
        if (without_nodes != None):
            url = self.addAttributes(url,"without_nodes",without_nodes, nbAttribute == 0)
            nbAttribute += 1
            
        return url 