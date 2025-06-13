import json
class ObjectSave():
    
    def getDataFromJson(self, fileName) -> str:
        try:
            with open(fileName, "r", encoding="utf-8") as file :
                contenu = file.read().strip()
                if not contenu:
                    return {}
                return json.loads(contenu)
        except FileNotFoundError:
            return {}
    def getElementByID(self, id : int, filename : str) -> dict:
        data = self.getDataFromJson(filename)
        if len(data) <= 0:
            return data
        else:
            for d in data.values():
                if d.get("id") == id:
                    return d
            return {}
    def getElementByName(self, name : str, filename : str) -> dict:
        data = self.getDataFromJson(filename)
        if len(data) <= 0:
            return data
        else:
            for d in data.values():
                if d.get("name") == name:
                    return d
            return {}
    def getRelationBetweenTwoNodes(self, node1 : str, node2 : str, filename : str)->dict:
        data = self.getDataFromJson(filename)
        if data == None or len(data) == 0:
            return {}
        relations : dict[int, dict[int:str]] = {}
        for d in data.values():
            node1 = self.getElementByName(node1,"nodes.json")
            node2 = self.getElementByName(node2,"nodes.json")
            if d.get("node1") == node1.get("id") and d.get("node2") == node2.get("id"):
                relations[int(d.get("id"))] = d
        return relations
    
    def getRelationFromNode(self, node_name : str, type_id : int):
        data = self.getDataFromJson(f"storage/from_{node_name}.json")
        if data == None or len(data) == 0:
            return {}
        if type_id == None:
            return data
        relations : dict[int, dict[int:str]] = {}
        for d in data.get("relations"):
            if int(d.get("type")) == type_id:
                relations[int(d.get("id"))] = d
        return relations
    
    def getRelationsToNode(self, node_name : str, type_id : int):
        data = self.getDataFromJson(f"storage/to_{node_name}.json")
        if data == None or len(data) == 0:
            return {}
        if type_id == None:
            return data
        relations : dict[int, dict[int:str]] = {}
        for d in data.get("relations"):
            if int(d.get("type")) == type_id:
                relations[int(d.get("id"))] = d
        return relations
    def writeDataIntoJson(self, fileName : str ,newData : dict):
        data = self.getDataFromJson(fileName)
        if isinstance(data, dict) and isinstance(newData, dict):
            if newData != data.get(str(newData.get("id"))):
                data.update({newData.get("id") : newData})
        elif isinstance(data, list):
            data.append(newData)
        else:
            data = newData
        with open(fileName,"w") as outfile:
            json.dump(data, outfile, indent=4)
    def dumpData(self, url : str, newData : dict):
        with open("storage/"+url+".json", "w") as f:
            json.dump(newData, f, indent=4)