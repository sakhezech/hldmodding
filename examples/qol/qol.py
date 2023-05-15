from hldmodding import on
from hldlib import HLDLevelList, HLDObj
import re


patch_list: dict[str, dict[str, list[str]]] = {
    '*': {
        'add': [],
        'remove': [r'obj,SickArea']
    },
    'rm_in_halucinationdeath.lvl': {
        'add': [
            'obj,Teleporter,8991,336,608,0,-999999,++,r=rm_C_DrifterWorkshop,d=8992,t=1,i=0'
        ],
        'remove': []
    },
    'rm_c_drifterworkshop.lvl': {
        'add': [
            'obj,Teleporter,8992,180,160,0,-999999,++,r=<undefined>,d=-999999,t=1,i=0'
        ],
        'remove': []
    },
}

@on.patch.levels.sub
def patch_levels(levels: HLDLevelList):
    
    for level in levels:
        to_remove = []
        for obj in level.objects:
            if any([
                re.search(pattern, obj.to_string()) for pattern in (patch_list.get(level.name.lower(), {'remove': []})['remove'] + patch_list['*']['remove'])
            ]): to_remove.append(obj)
        for trm in to_remove:
            level.objects.remove(trm)
        for add in (patch_list.get(level.name.lower(), {'add': []})['add'] + patch_list['*']['add']):
            level.objects.append(HLDObj.from_string(add))