import json
from UnityPy.helpers.TypeTreeGenerator import TypeTreeGenerator
from UnityPy.helpers.TypeTreeNode import TypeTreeNode

class GameTypeTreeGenerator(TypeTreeGenerator):
    def get_nodes_up(self, assembly, fullname):
        key=(assembly,fullname)
        if key in self.cache:return self.cache[key]
        if not assembly.endswith('.dll'):assembly+='.dll'
        nodes=json.loads(self.get_nodes_as_json(assembly,fullname))
        for i,n in enumerate(nodes):
            # Generator 0.0.10 marks string[] as string; UnityPy otherwise
            # interprets its element count as a UTF-8 byte count.
            if n['m_Type']=='string' and i+3<len(nodes):
                child=nodes[i+3]
                if child['m_Name']=='data' and child['m_Type']=='string' and child['m_Level']==n['m_Level']+2:
                    n['m_Type']='vector'
            if n['m_Name']=='m_Enabled' and n['m_Level']==1:
                n['m_MetaFlag']|=16384
        node=TypeTreeNode.from_list([TypeTreeNode(n['m_Level'],n['m_Type'],n['m_Name'],0,0,m_MetaFlag=n['m_MetaFlag']) for n in nodes])
        self.cache[key]=node
        return node

def generator(root):
    g=GameTypeTreeGenerator('2017.4.40f1');g.load_local_game(str(root.parent));return g
