from wikidataintegrator import wdi_core, wdi_login, wdi_property_store
import pandas as pd
import pprint
import sys

df_core = pd.read_csv("data/denomination.csv")
#df_code = pd.read_csv("data/code.csv")
#df_contact = pd.read_csv("data/contact.csv")
#df_established = pd.read_csv("data/establishment.csv")
#df_enterprise = pd.read_csv("data/enterprise.csv")
#df_activity = pd.read_csv("data/activity.csv")
df_address = pd.read_csv("data/address.csv")



companies = dict()
logincreds = wdi_login.WDLogin(server="185.54.113.154:8181", user="", pwd="")

for index, row in df_core.iterrows():
    if row["EntityNumber"] not in companies.keys():
        companies[row["EntityNumber"]] = dict()
        if row["Language"] == "1":
            companies[row["EntityNumber"]]["FR"] = row["Denomination"]
        elif row["Language"] == "2":
            companies[row["EntityNumber"]]["NL"] = row["Denomination"]
        elif row["Language"] == "3":
            companies[row["EntityNumber"]]["DE"] = row["Denomination"]
        else:
            companies[row["EntityNumber"]]["NL"] = row["Denomination"]

for index, row in df_address.iterrows():
    if row["Zipcode"] != "":
        companies[row["EntityNumber"]]["zipcode"] = row["Zipcode"]

print(len(companies.keys()))

for vat in companies.keys():
    prep = dict()
    prep["P3"] = []
    prep["P3"].append(wdi_core.WDString(value=vat, prop_nr="P3"))

    prep["P5"] = [wdi_core.WDString(value=companies[vat]["zipcode"])]

    data2add = []
    for key in prep.keys():
        for statement in prep[key]:
            data2add.append(statement)
            print(statement.prop_nr, statement.value)

    wdPage = wdi_core.WDItemEngine(item_name=companies[vat]["NL"], data=data2add, server="185.54.113.154:8181", domain="economy")
    if "NL" in companies[vat].keys():
        wdPage.set_label(companies[vat]["NL"], lang="nl")
    if "DE" in companies[vat].keys():
        wdPage.set_label(companies[vat]["DE"], lang="de")
    if "FR" in companies[vat].keys():
        wdPage.set_label(companies[vat]["FR"], lang="fr")

    wdPage.write(logincreds)

pprint.pprint(list(df_core.columns.values))
#pprint.pprint(df_contact[df_contact["EntityNumber"]==vat])
#pprint.pprint(df_established[df_established["EnterpriseNumber"]==vat])
#pprint.pprint(df_activity[df_activity["EntityNumber"]==vat])
#pprint.pprint(df_address[df_address["EntityNumber"]==vat])
#pprint.pprint(df_enterprise[df_enterprise["EnterpriseNumber"]==vat])