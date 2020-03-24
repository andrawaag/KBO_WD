from wikidataintegrator import wdi_core, wdi_login, wdi_property_store
import pandas as pd
import pprint
import sys
from time import strftime, gmtime
import copy


logincreds = wdi_login.WDLogin(user="", pwd="")

df = pd.read_excel("nacebel_2003_7positions_tcm325-246795.xlsx", sheetname='nacebel')

labels = dict()
for index, row in df.iterrows():
    if row["NEDERLANDSE OMSCHRIJVING"] not in labels.keys():
        print(row["NEDERLANDSE OMSCHRIJVING "])
        labels[row["NEDERLANDSE OMSCHRIJVING "]] = dict()
        labels[row["NEDERLANDSE OMSCHRIJVING "]]["FR"] = row["FRANSE OMSCHRIJVING "]
        labels[row["NEDERLANDSE OMSCHRIJVING "]]["DE"] = row["DUITSE OMSCHRIJVING "]
        labels[row["NEDERLANDSE OMSCHRIJVING "]]["codes"] = ["0"+str(row["CODE"])]
    else:
        labels[row["NEDERLANDSE OMSCHRIJVING "]]["codes"].append("0"+str(row["CODE"]))

# Reference
refStatedIn = wdi_core.WDItemID(value="Q16626729", prop_nr='P248', is_reference=True)
timeStringNow = strftime("+%Y-%m-%dT00:00:00Z", gmtime())
refRetrieved = wdi_core.WDTime(timeStringNow, prop_nr='P813', is_reference=True)
refUrl = wdi_core.WDUrl("http://economie.fgov.be/nl/binaries/nacebel_2003_7positions_tcm325-246795.xls", prop_nr='P854', is_reference=True)
kbo_reference = [refStatedIn, refRetrieved, refUrl]

# Qualifiers
qualAuthority = wdi_core.WDItemID(value="Q31", prop_nr='P797', is_qualifier=True)
qualVersie2003 = wdi_core.WDString(value="2003", prop_nr="P348", is_qualifier=True)
qualVersie2008 = wdi_core.WDString(value="2008", prop_nr="P348", is_qualifier=True)
qualifiers_2003 = [qualAuthority, qualVersie2003]
qualifier_2008 = [qualAuthority, qualVersie2008]


wdi_property_store.wd_properties['P4496'] = {
        'datatype': 'string',
        'name': 'NACE code',
        'domain': ['economy'],
        'core_id': False
    }
i = 0
for label in labels.keys():

    prep = dict()
    prep["P31"] = [wdi_core.WDItemID("Q8187769",prop_nr="P31")]
    prep["P361"] = [wdi_core.WDItemID("Q732298", prop_nr="P361")]
    print("i: "+str(i))

    prep["P4496"] = []
    for qid in labels[label]["codes"]:
        prep["P4496"].append(wdi_core.WDString(value=qid, prop_nr="P4496", references=[copy.deepcopy(kbo_reference)], qualifiers=[qualAuthority, qualVersie2003]))

    data2add = []
    for key in prep.keys():
        for statement in prep[key]:
            data2add.append(statement)
            print(statement.prop_nr, statement.value)

    wdPage = wdi_core.WDItemEngine(item_name=label, data=data2add, server="www.wikidata.org",
                                  domain="economy")
    wdPage.set_label(label, lang="nl")
    wdPage.set_label(labels[label]["FR"], lang="fr")
    wdPage.set_label(labels[label]["DE"], lang="de")
    wdPage.set_description("economische activiteit", lang="nl")
    wdPage.set_description("activité économique", lang="fr")
    wd_json_representation = wdPage.get_wd_json_representation()

    pprint.pprint(wd_json_representation)
    wdPage.write(login=logincreds)
    i+=1
    if i == 10:
        sys.exit()




