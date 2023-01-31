import pandas as pd
from util import *
from variable import _PREFIX
import re

kg = init_kg_with_prefix(_PREFIX)


def add_ontology_triples(kg):
  kg.add((_PREFIX["ev-ont"]["ZipCodeArea"], RDF["type"], OWL["Class"]))
  kg.add((_PREFIX["ev-ont"]["ZipCodeArea"], RDFS["subClassOf"], OWL["Thing"]))
  kg.add((_PREFIX["ev-ont"]["ZipCodeArea"], RDFS["label"],
          Literal("ZIP Code Area")))

  kg.add((_PREFIX["ev-ont"]["County"], RDF["type"], OWL["Class"]))
  kg.add((_PREFIX["ev-ont"]["County"], RDFS["subClassOf"], OWL["Thing"]))
  kg.add((_PREFIX["ev-ont"]["County"], RDFS["label"],
          Literal("County")))

  kg.add((_PREFIX["ev-ont"]["State"], RDF["type"], OWL["Class"]))
  kg.add((_PREFIX["ev-ont"]["State"], RDFS["subClassOf"], OWL["Thing"]))
  kg.add((_PREFIX["ev-ont"]["State"], RDFS["label"],
          Literal("State")))

  kg.add((_PREFIX["ev-ont"]["sfWithin"], RDF["type"], OWL["ObjectProperty"]))
  kg.add((_PREFIX["ev-ont"]["sfWithin"], RDFS["domain"], _PREFIX['ev-ont']['ZipCodeArea']))
  kg.add((_PREFIX["ev-ont"]["sfWithin"], RDFS["range"], _PREFIX["ev-ont"]["County"]))

  kg.add((_PREFIX["ev-ont"]["sfWithin"], RDF["type"], OWL["ObjectProperty"]))
  kg.add((_PREFIX["ev-ont"]["sfWithin"], RDFS["domain"], _PREFIX['ev-ont']['ZipCodeArea']))
  kg.add((_PREFIX["ev-ont"]["sfWithin"], RDFS["range"], _PREFIX["ev-ont"]["State"]))

  kg.add((_PREFIX["ev-ont"]["sfWithin"], RDF["type"], OWL["ObjectProperty"]))
  kg.add((_PREFIX["ev-ont"]["sfWithin"], RDFS["domain"], _PREFIX['ev-ont']['County']))
  kg.add((_PREFIX["ev-ont"]["sfWithin"], RDFS["range"], _PREFIX["ev-ont"]["State"]))

  kg.add((_PREFIX["ev-ont"]["sfContains"], RDF["type"], OWL["ObjectProperty"]))
  kg.add((_PREFIX["ev-ont"]["sfContains"], RDFS["domain"], _PREFIX['ev-ont']['State']))
  kg.add((_PREFIX["ev-ont"]["sfContains"], RDFS["range"], _PREFIX["ev-ont"]["County"]))

  kg.add((_PREFIX["ev-ont"]["sfContains"], RDF["type"], OWL["ObjectProperty"]))
  kg.add((_PREFIX["ev-ont"]["sfContains"], RDFS["domain"], _PREFIX['ev-ont']['State']))
  kg.add((_PREFIX["ev-ont"]["sfContains"], RDFS["range"], _PREFIX["ev-ont"]["ZipCodeArea"]))

  kg.add((_PREFIX["ev-ont"]["sfContains"], RDF["type"], OWL["ObjectProperty"]))
  kg.add((_PREFIX["ev-ont"]["sfContains"], RDFS["domain"], _PREFIX['ev-ont']['County']))
  kg.add((_PREFIX["ev-ont"]["sfContains"], RDFS["range"], _PREFIX["ev-ont"]["ZipCodeArea"]))


def link_county_zip_state(zip_raw, zip_with_kwg):
  for idx, itm in zip_with_kwg.iterrows():
    print(idx)
    county_iri = None
    state_ev_iri = None

    county_ev_iri = None
    state_iri = None
    # ######################################### zipcode #########################
    zipcode_iri = _PREFIX["kwgr"][f"zipcodearea.{str('%05d' % int(itm['zip']))}"]
    zipcode_ev_iri = _PREFIX["evr"][f"zipcodearea.{str('%05d' % int(itm['zip']))}"]

    kg.add((zipcode_ev_iri, RDF["type"], _PREFIX["kwg-ont"]["ZipCodeArea"]))
    kg.add((zipcode_ev_iri, RDF["type"], _PREFIX["ev-ont"]["ZipCodeArea"]))

    kg.add((zipcode_iri, RDFS["label"], Literal('zip code ' + str('%05d' % int(itm['zip'])))))
    kg.add((zipcode_ev_iri, RDFS["label"], Literal('zip code ' + str('%05d' % int(itm['zip'])))))
    kg.add((zipcode_ev_iri, OWL["sameAs"], zipcode_iri))
    # ######################################### county #########################
    if type(itm['county']) is not float:
      county_ev_iri = _PREFIX["evr"][f"county.{itm['state'].replace(' ', '-')}-{itm['county'].replace(' ', '-')}"]
      kg.add((county_ev_iri, RDF["type"], _PREFIX["ev-ont"]["County"]))
      kg.add((county_ev_iri, RDFS["label"], Literal(itm['county'])))

      if type(itm['county_iri']) is not float:
        county_iri = rdflib.term.URIRef(itm['county_iri'])
        kg.add((county_iri, RDF["type"], _PREFIX["kwg-ont"]["AdministrativeRegion_3"]))
        kg.add((county_iri, RDFS["label"], Literal(itm['county'])))
        kg.add((county_iri, OWL["sameAs"], county_ev_iri))

    # ######################################### state #########################
    if type(itm['state']) is not float:
      state_ev_iri = _PREFIX["evr"][f"state.{itm['state']}"]
      if type(itm['State']) is not float:
        kg.add((state_ev_iri, RDF["type"], _PREFIX["ev-ont"]["State"]))
        kg.add((state_ev_iri, RDFS["label"], Literal(itm['State'])))

      if type(itm['state_iri']) is not float:
        state_iri = rdflib.term.URIRef(itm['state_iri'])
        kg.add((state_iri, RDF["type"], _PREFIX["kwg-ont"]["AdministrativeRegion_2"]))
        kg.add((state_iri, OWL["sameAs"], state_ev_iri))

      if county_iri is not None:
        kg.add((zipcode_iri, _PREFIX["kwg-ont"]['sfWithin'], county_iri))
        kg.add((county_iri, _PREFIX["kwg-ont"]['sfContains'], zipcode_iri))
      if state_iri is not None:
        kg.add((zipcode_iri, _PREFIX["kwg-ont"]['sfWithin'], state_iri))
        kg.add((state_iri, _PREFIX["kwg-ont"]['sfContains'], zipcode_iri))
      if county_iri is not None and (state_iri is not None):
        kg.add((county_iri, _PREFIX["kwg-ont"]['sfWithin'], state_iri))
        kg.add((state_iri, _PREFIX["kwg-ont"]['sfContains'], county_iri))

    if county_ev_iri is not None:
      kg.add((zipcode_ev_iri, _PREFIX["ev-ont"]['sfWithin'], county_ev_iri))
      kg.add((county_ev_iri, _PREFIX["ev-ont"]['sfContains'], zipcode_ev_iri))
    if state_ev_iri is not None:
      kg.add((zipcode_ev_iri, _PREFIX["ev-ont"]['sfWithin'], state_ev_iri))
      kg.add((state_ev_iri, _PREFIX["ev-ont"]['sfContains'], zipcode_ev_iri))
    if county_ev_iri is not None and (state_ev_iri is not None):
      kg.add((county_ev_iri, _PREFIX["ev-ont"]['sfWithin'], state_ev_iri))
      kg.add((state_ev_iri, _PREFIX["ev-ont"]['sfContains'], county_ev_iri))


def main():
  zipcode = pd.read_excel("EVRegData/administrative_info/zip_code_database.xls")
  state = pd.read_excel("EVRegData/administrative_info/States.xlsx")
  # county_kwg = pd.read_csv("EVRegData/administrative_info/kwg_county.csv")
  # state_kwg = pd.read_csv("EVRegData/administrative_info/kwg_state.csv")
  county_state_kwg = pd.read_csv("EVRegData/administrative_info/kwg_county_state.csv")
  zip_raw = zipcode.merge(state, left_on="state", right_on="Abbr", how="left")
  # zip_new1 = zip_new.merge(county_kwg, left_on="county", right_on="county_label", how="left")
  # zip_new2 = zip_new1.merge(state_kwg, left_on="State", right_on="state_label", how="left")
  # zip_new1[[type(x) is float for x in zip_new1['county_iri']]]
  zip_new3 = zip_raw.merge(county_state_kwg, left_on=["State", "county"], right_on=["ls", "lc"], how="left")
  link_county_zip_state(zip_raw, zip_new3)
  adm_ttl = "{}/ev_administrative.ttl".format('./EVRegData/')
  kg.serialize(adm_ttl, format='turtle')


if __name__ == "__main__":
  main()
