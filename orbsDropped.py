# coding: utf-8

import pandas as pd
import numpy as np
data = pd.read_csv("datafiles/data.csv")
groupedByClass = data.groupby('class')
groupedByClass = data.groupby('characterClass')
groupedByClass
hunters = groupedByClass.get_group("Hunter")
titas = groupedByClass.get_group("Titan")
warlock = groupedByClass.get_group("Warlock")
hunters
len(hunters)
len(titans)
titans = groupedByClass.get_group("Titan")
titas = None
del(titas)
len(titans)
len(hunters)
len(warlocks)
warlocks = groupedByClass.get_group("Warlock")
del(warlock)
len(warlocks)
(hunters.orbsGathered/hunters.orbsDropped).mean()
(hunters.orbsGathered/hunters.orbsDropped).replace([np.inf],0).mean()
(titans.orbsGathered/titans.orbsDropped).replace([np.inf],0).mean()
(hunters.orbsDropped/hunters.orbsGathered).replace([np.inf,np.nan],0).mean()
(titans.orbsDropped/titans.orbsGathered).replace([np.inf,np.nan],0).mean()
(warlocks.orbsDropped/warlocks.orbsGathered).replace([np.inf,np.nan],0).mean()
get_ipython().magic(u'save orbsDropped.py 0-28')
