import os
import pandas as pd
from operator import itemgetter
from copy import deepcopy

import shapely.geometry.linestring

from util import *
from variable import NAME_SPACE, _PREFIX
from rdflib import TIME
import json
import geopandas as gpd
from shapely import geometry
from functools import reduce
import re
import string
import warnings


def geometry_triples(geometry, stn_iri, _PREFIX, namespace='ev-ont'):
    geometry_set = set()
    if geometry._ndim > 2:
        geometry = remove_third_dimension(geometry)
    geometry_str = stn_iri.replace(_PREFIX[namespace], "")
    if "/" in geometry_str:
        geometry_str = geometry_str.split("/")[-1]
    if type(geometry) == shapely.geometry.multipolygon.MultiPolygon:
        geo_type = "MultiPolygon"
    elif type(geometry) == shapely.geometry.polygon.Polygon:
        geo_type = "Polygon"
    elif type(geometry) == shapely.geometry.polygon.Point:
        geo_type = "Point"
    elif (type(geometry) == shapely.geometry.linestring.LineString) or \
            (type(geometry) == shapely.geometry.multilinestring.MultiLineString):
        geo_type = "Polyline"

    else:
        raise Exception("Geometry datatype not support")

    geometry_str_list = geometry_str.split(".")
    assert len(geometry_str_list) > 1
    geometry_str_list[0] = f"geometry.{geo_type.lower()}"
    geometry_iri = _PREFIX[namespace][".".join(geometry_str_list)]

    geometry_set.add((stn_iri, RDF.type, _PREFIX["geo"]["Feature"]))
    geometry_set.add((stn_iri, _PREFIX["geo"]["hasGeometry"], geometry_iri))
    geometry_set.add((geometry_iri, RDF.type, _PREFIX["geo"]["Geometry"]))
    geometry_set.add((geometry_iri, RDF.type, _PREFIX["sf"][geo_type]))

    geometry_wkt = dumps(geometry, rounding_precision=7)
    geometry_set.add(
        (geometry_iri, _PREFIX["geo"]["asWKT"], Literal(geometry_wkt, datatype=_PREFIX["geo"]["wktLiteral"])))
    return geometry_set


def add_ontology_triples(kg, _PREFIX):
    # Ontology Class
    # -----------charging station
    kg.add((_PREFIX["ev-ont"]["ChargingStation"], RDF["type"], OWL["Class"]))
    kg.add((_PREFIX["ev-ont"]["ChargingStation"], RDFS["subClassOf"], OWL["Thing"]))
    kg.add((_PREFIX["ev-ont"]["ChargingStation"], RDFS["label"], Literal("Charging station")))
    kg.add((_PREFIX["ev-ont"]["ChargingStation"], RDFS["comment"],
            Literal("This is the facility information of charging stations in the U.S.")))

    kg.add((_PREFIX["ev-ont"]["PrivateChargingStation"], RDF["type"], OWL["Class"]))
    kg.add((_PREFIX["ev-ont"]["PrivateChargingStation"], RDFS["subClassOf"], _PREFIX["ev-ont"]["ChargingStation"]))
    kg.add((_PREFIX["ev-ont"]["PrivateChargingStation"], RDFS["label"], Literal("Private charging station")))

    kg.add((_PREFIX["ev-ont"]["PublicChargingStation"], RDF["type"], OWL["Class"]))
    kg.add((_PREFIX["ev-ont"]["PublicChargingStation"], RDFS["subClassOf"], _PREFIX["ev-ont"]["ChargingStation"]))
    kg.add((_PREFIX["ev-ont"]["PublicChargingStation"], RDFS["label"], Literal("Public charging station")))

    kg.add((_PREFIX["ev-ont"]["NetworkedChargingStation"], RDF["type"], OWL["Class"]))
    kg.add((_PREFIX["ev-ont"]["NetworkedChargingStation"], RDFS["subClassOf"], _PREFIX["ev-ont"]["ChargingStation"]))
    kg.add((_PREFIX["ev-ont"]["NetworkedChargingStation"], RDFS["label"], Literal("Networked charging station")))

    kg.add((_PREFIX["ev-ont"]["NonNetworkedChargingStation"], RDF["type"], OWL["Class"]))
    kg.add((_PREFIX["ev-ont"]["NonNetworkedChargingStation"], RDFS["subClassOf"], _PREFIX["ev-ont"]["ChargingStation"]))
    kg.add((_PREFIX["ev-ont"]["NonNetworkedChargingStation"], RDFS["label"], Literal("NonNetworked charging station")))

    # -----------charging network
    kg.add((_PREFIX["ev-ont"]["ChargingNetwork"], RDF["type"], OWL["Class"]))
    kg.add((_PREFIX["ev-ont"]["ChargingNetwork"], RDFS["subClassOf"], OWL["Thing"]))
    kg.add((_PREFIX["ev-ont"]["ChargingNetwork"], RDFS["label"],
            Literal("Charging Network")))

    # -----------charger
    kg.add((_PREFIX["ev-ont"]["ChargerCollection"], RDF["type"], OWL["Class"]))
    kg.add((_PREFIX["ev-ont"]["ChargerCollection"], RDFS["subClassOf"], OWL["Thing"]))
    kg.add((_PREFIX["ev-ont"]["ChargerCollection"], RDFS["label"], Literal("Charger collection")))
    # -----------charger
    kg.add((_PREFIX["ev-ont"]["ChargerType"], RDF["type"], OWL["Class"]))
    kg.add((_PREFIX["ev-ont"]["ChargerType"], RDFS["subClassOf"], OWL["Thing"]))
    kg.add((_PREFIX["ev-ont"]["ChargerType"], RDFS["label"], Literal("Charger type")))

    # -----------connector type
    kg.add((_PREFIX["ev-ont"]["ConnectorType"], RDF["type"], OWL["Class"]))
    kg.add((_PREFIX["ev-ont"]["ConnectorType"], RDFS["subClassOf"], OWL["Thing"]))
    kg.add((_PREFIX["ev-ont"]["ConnectorType"], RDFS["label"], Literal("Connector type")))

    # -----------electricity Supplier
    kg.add((_PREFIX["ev-ont"]["ElectricitySupplier"], RDF["type"], OWL["Class"]))
    kg.add((_PREFIX["ev-ont"]["ElectricitySupplier"], RDFS["subClassOf"], OWL["Thing"]))
    kg.add((_PREFIX["ev-ont"]["ElectricitySupplier"], RDFS["label"], Literal("Electricity supplier")))

    # -----------onsite energy
    kg.add((_PREFIX["ev-ont"]["RenewableEnergy"], RDF["type"], OWL["Class"]))
    kg.add((_PREFIX["ev-ont"]["RenewableEnergy"], RDFS["subClassOf"], OWL["Thing"]))
    kg.add((_PREFIX["ev-ont"]["RenewableEnergy"], RDFS["label"], Literal("On-site energy")))

    # -----------urban PlaceType
    kg.add((_PREFIX["ev-ont"]["PlaceType"], RDF["type"], OWL["Class"]))
    kg.add((_PREFIX["ev-ont"]["PlaceType"], RDFS["subClassOf"], OWL["Thing"]))
    kg.add((_PREFIX["ev-ont"]["PlaceType"], RDFS["label"], Literal("Nearby place")))

    # Datatype property
    # -----------charger number
    kg.add((_PREFIX["ev-ont"]["hasAmount"], RDF["type"], OWL["DatatypeProperty"]))
    kg.add((_PREFIX["ev-ont"]["hasAmount"], RDFS["label"], Literal('charger quantity')))
    kg.add((_PREFIX["ev-ont"]["hasAmount"], RDFS["comment"], Literal(f'The number of chargers in the collection')))

    # -----------has street address
    kg.add((_PREFIX["ev-ont"]["hasStreetAddress"], RDF["type"], OWL["DatatypeProperty"]))
    kg.add((_PREFIX["ev-ont"]["hasStreetAddress"], RDFS["label"], Literal('street address')))
    kg.add(
        (
        _PREFIX["ev-ont"]["hasStreetAddress"], RDFS["comment"], Literal(f'The street address of the charging station')))
    # -----------access type property
    kg.add((_PREFIX["ev-ont"]["hasAccessComments"], RDF["type"], OWL["DatatypeProperty"]))
    kg.add((_PREFIX["ev-ont"]["hasAccessComments"], RDFS["label"], Literal('access types')))
    kg.add((_PREFIX["ev-ont"]["hasAccessComments"], RDFS["comment"], Literal(f'Comments for Access Restrictions')))
    # -----------pricing scheme
    kg.add((_PREFIX["ev-ont"]["hasPricingScheme"], RDF["type"], OWL["DatatypeProperty"]))
    kg.add((_PREFIX["ev-ont"]["hasPricingScheme"], RDFS["label"], Literal('pricing scheme')))
    kg.add((_PREFIX["ev-ont"]["hasPricingScheme"], RDFS["comment"], Literal(f'pricing scheme of charging stations')))
    # -----------operating hours
    kg.add((_PREFIX["ev-ont"]["hasOperatingHours"], RDF["type"], OWL["DatatypeProperty"]))
    kg.add((_PREFIX["ev-ont"]["hasOperatingHours"], RDFS["label"], Literal('hours of operation')))
    kg.add(
        (_PREFIX["ev-ont"]["hasOperatingHours"], RDFS["comment"], Literal(f'operating hours of the charging station')))
    # -----------user group restriction
    kg.add((_PREFIX["ev-ont"]["hasAllowedUser"], RDF["type"], OWL["DatatypeProperty"]))
    kg.add((_PREFIX["ev-ont"]["hasAllowedUser"], RDFS["label"], Literal('allowed user group')))
    kg.add(
        (_PREFIX["ev-ont"]["hasAllowedUser"], RDFS["comment"], Literal(f'allowed user group of the charging station')))
    # -----------parking restriction
    kg.add((_PREFIX["ev-ont"]["hasParkingRestriction"], RDF["type"], OWL["DatatypeProperty"]))
    kg.add((_PREFIX["ev-ont"]["hasParkingRestriction"], RDFS["label"], Literal('parking restriction')))
    kg.add((_PREFIX["ev-ont"]["hasParkingRestriction"], RDFS["comment"],
            Literal(f'parking restriction of the charging station')))

    # -----------charging station<->open time
    kg.add((_PREFIX["ev-ont"]["hasOpenDate"], RDF["type"], OWL["DatatypeProperty"]))
    kg.add((_PREFIX["ev-ont"]["hasOpenDate"], RDFS["label"], Literal('open time')))
    kg.add((_PREFIX["ev-ont"]["hasOpenDate"], RDFS["comment"], Literal(f'the open time of the charging station')))

    # -----------charging station<->open year
    kg.add((_PREFIX["ev-ont"]["hasOpenYear"], RDF["type"], OWL["DatatypeProperty"]))
    kg.add((_PREFIX["ev-ont"]["hasOpenYear"], RDFS["label"], Literal('open year')))
    kg.add((_PREFIX["ev-ont"]["hasOpenYear"], RDFS["comment"], Literal(f'the open year of the charging station')))

    # -----------charger<->charging station
    kg.add((_PREFIX["ev-ont"]["isHostedBy"], RDF["type"], OWL["ObjectProperty"]))
    kg.add((_PREFIX["ev-ont"]["isHostedBy"], RDFS["domain"], _PREFIX['ev-ont']['ChargerCollection']))
    kg.add((_PREFIX["ev-ont"]["isHostedBy"], RDFS["range"], _PREFIX['ev-ont']['ChargingStation']))

    kg.add((_PREFIX["ev-ont"]["hosts"], RDF["type"], OWL["ObjectProperty"]))
    kg.add((_PREFIX["ev-ont"]["hosts"], RDFS["domain"], _PREFIX['ev-ont']['ChargingStation']))
    kg.add((_PREFIX["ev-ont"]["hosts"], RDFS["range"], _PREFIX['ev-ont']['ChargerCollection']))

    # -----------charger<->electricity
    kg.add((_PREFIX["ev-ont"]["hasElectricitySupplier"], RDF["type"], OWL["ObjectProperty"]))
    kg.add((_PREFIX["ev-ont"]["hasElectricitySupplier"], RDFS["domain"], _PREFIX['ev-ont']['ChargerCollection']))
    kg.add((_PREFIX["ev-ont"]["hasElectricitySupplier"], RDFS["range"], _PREFIX['ev-ont']['ElectricitySupplier']))

    # -----------RenewableOnsiteEnergy<->Charging station
    kg.add((_PREFIX["ev-ont"]["hasOnsiteRenewableEnergySource"], RDF["type"], OWL["ObjectProperty"]))
    kg.add((_PREFIX["ev-ont"]["hasOnsiteRenewableEnergySource"], RDFS["domain"], _PREFIX['ev-ont']['ChargingStation']))
    kg.add((_PREFIX["ev-ont"]["hasOnsiteRenewableEnergySource"], RDFS["range"], _PREFIX['ev-ont']['RenewableEnergy']))

    # -----------connector type <-> connector
    kg.add((_PREFIX["ev-ont"]["hasConnectorType"], RDF["type"], OWL["ObjectProperty"]))
    kg.add((_PREFIX["ev-ont"]["hasConnectorType"], RDFS["domain"], _PREFIX['ev-ont']['ChargerCollection']))
    kg.add((_PREFIX["ev-ont"]["hasConnectorType"], RDFS["range"], _PREFIX['ev-ont']['ConnectorType']))
    # -----------charger type <-> charger collection
    kg.add((_PREFIX["ev-ont"]["hasChargerType"], RDF["type"], OWL["ObjectProperty"]))
    kg.add((_PREFIX["ev-ont"]["hasChargerType"], RDFS["domain"], _PREFIX['ev-ont']['ChargerCollection']))
    kg.add((_PREFIX["ev-ont"]["hasChargerType"], RDFS["range"], _PREFIX['ev-ont']['ChargerType']))

    kg.add((_PREFIX["ev-ont"]["hasPotentialInfluenceOn"], RDF["type"], OWL["ObjectProperty"]))
    kg.add((_PREFIX["ev-ont"]["hasPotentialInfluenceOn"], RDFS["domain"], _PREFIX['ev-ont']['TransmissionLine']))
    kg.add((_PREFIX["ev-ont"]["hasPotentialInfluenceOn"], RDFS["range"], _PREFIX['ev-ont']['ChargingStation']))

    kg.add((_PREFIX["ev-ont"]["IsPotentiallyInfluencedBy"], RDF["type"], OWL["ObjectProperty"]))
    kg.add((_PREFIX["ev-ont"]["IsPotentiallyInfluencedBy"], RDFS["domain"], _PREFIX['ev-ont']['ChargingStation']))
    kg.add((_PREFIX["ev-ont"]["IsPotentiallyInfluencedBy"], RDFS["range"], _PREFIX['ev-ont']['TransmissionLine']))

    kg.add((_PREFIX["ev-ont"]["hasNearbyPlaceType"], RDF["type"], OWL["ObjectProperty"]))
    kg.add((_PREFIX["ev-ont"]["hasNearbyPlaceType"], RDFS["domain"], _PREFIX['ev-ont']['ChargingStation']))
    kg.add((_PREFIX["ev-ont"]["hasNearbyPlaceType"], RDFS["range"], _PREFIX['ev-ont']['PlaceType']))

    kg.add((_PREFIX["ev-ont"]["isUnderChargingNetwork"], RDF["type"], OWL["ObjectProperty"]))
    kg.add((_PREFIX["ev-ont"]["isUnderChargingNetwork"], RDFS["domain"], _PREFIX['ev-ont']['ChargingStation']))
    kg.add((_PREFIX["ev-ont"]["isUnderChargingNetwork"], RDFS["range"], _PREFIX['ev-ont']['ChargingNetwork']))

    # -----------Private charging station<-> User group
    # kg.add((_PREFIX["ev-ont"]["hasAllowedUser"], RDF["type"], OWL["ObjectProperty"]))
    # kg.add((_PREFIX["ev-ont"]["hasAllowedUser"], RDFS["domain"], _PREFIX['ev-ont']['PrivateChargingStation']))
    # kg.add((_PREFIX["ev-ont"]["hasAllowedUser"], RDFS["range"], _PREFIX['ev-ont']['ChargingUserGroup']))

    # kg.add((_PREFIX["ev-ont"]["hasAccessTo"], RDF["type"], OWL["ObjectProperty"]))
    # kg.add((_PREFIX["ev-ont"]["hasAccessTo"], RDFS["domain"], _PREFIX['ev-ont']['ChargingUserGroup']))
    # kg.add((_PREFIX["ev-ont"]["hasAccessTo"], RDFS["range"], _PREFIX['ev-ont']['PrivateChargingStation']))

    # -----------charging station<-> Parking restriction
    # kg.add((_PREFIX["ev-ont"]["hasParkingRestriction"], RDF["type"], OWL["ObjectProperty"]))
    # kg.add((_PREFIX["ev-ont"]["hasParkingRestriction"], RDFS["domain"], _PREFIX['ev-ont']['EVChargingStation']))
    # kg.add((_PREFIX["ev-ont"]["hasParkingRestriction"], RDFS["range"], _PREFIX['ev-ont']['ParkingRestriction']))
    # -----------charging station<-> service time
    # kg.add((_PREFIX["ev-ont"]["hasOperatingHours"], RDF["type"], OWL["ObjectProperty"]))
    # kg.add((_PREFIX["ev-ont"]["hasOperatingHours"], RDFS["domain"], _PREFIX['ev-ont']['EVChargingStation']))
    # kg.add((_PREFIX["ev-ont"]["hasOperatingHours"], RDFS["range"], _PREFIX['ev-ont']['HoursOfOperation']))
    # -----------charging station<-> pricing scheme
    # kg.add((_PREFIX["ev-ont"]["hasPricingScheme"], RDF["type"], OWL["ObjectProperty"]))
    # kg.add((_PREFIX["ev-ont"]["hasPricingScheme"], RDFS["domain"], _PREFIX['ev-ont']['EVChargingStation']))
    # kg.add((_PREFIX["ev-ont"]["hasPricingScheme"], RDFS["range"], _PREFIX['ev-ont']['PricingScheme']))

    return kg


def process_str(cm):
    s1 = ''.join([x.capitalize() for x in cm.split('_')])
    s2 = s1.translate(str.maketrans('', '', string.punctuation))

    return s2


def add_facility_classes(stn_df, kg, _PREFIX):
    # -----------urban PlaceType
    cat_df = stn_df.drop_duplicates(subset=['FACILITY_TYPE'], keep='first')

    def triplify_facility_category(faci):
        # add category ontology
        if faci['kg_FACILITY_TYPE'] != ' ' and (type(faci["kg_FACILITY_TYPE"]) is not float):
            kg.add((_PREFIX["ev-ont"][faci['kg_FACILITY_TYPE']], RDF["type"], OWL["Class"]))
            kg.add((_PREFIX["ev-ont"][faci['kg_FACILITY_TYPE']], RDFS["subClassOf"], _PREFIX["ev-ont"]["PlaceType"]))
            kg.add((_PREFIX["ev-ont"][faci['kg_FACILITY_TYPE']], RDFS["label"],
                    Literal(faci['FACILITY_TYPE'].replace("_", " ").capitalize())))

    for idx, x in cat_df.iterrows():
        triplify_facility_category(x)

    return kg


def add_emobility_ontology(kg, stn_iri, stn):
    if assert_existence(stn['EV_NETWORK']):
        if stn['EV_NETWORK'] != "NonNetworked":
            cpo_iri = _PREFIX["evr"][f"chargingnetwork.{str(stn['EV_NETWORK'])}"]
            kg.add((cpo_iri, RDF["type"], _PREFIX["ev-ont"]["ChargingNetwork"]))
            kg.add((cpo_iri, RDFS["label"], Literal(f"{str(stn['EV_NETWORK'])}")))

            if (stn['EV_NETWORK_URL'] is not None) and (stn["EV_NETWORK_URL"] != ' '):
                kg.add((cpo_iri, _PREFIX["ev-ont"]["detailsURL"], Literal(f"{str(stn['EV_NETWORK_URL'])}")))
            kg.add((stn_iri, _PREFIX["ev-ont"]["isUnderChargingNetwork"], cpo_iri))

    return kg


def add_facility_ontology(kg, stn_iri, stn):
    if assert_existence(stn['STATION_NAME']) and assert_existence(stn['kg_FACILITY_TYPE']):
        facility_iri = _PREFIX["evr"][f"placetype.{str(stn['ID'])}"]
        kg.add((facility_iri, RDF["type"], _PREFIX["ev-ont"][stn['kg_FACILITY_TYPE']]))
        kg.add((facility_iri, RDFS["label"], Literal(stn["STATION_NAME"].replace("_", " ").capitalize())))
        kg.add((stn_iri, _PREFIX["ev-ont"]["hasNearbyPlaceType"], facility_iri))

    return kg


def add_energy_ontology(kg, stn_iri, stn):
    if assert_existence(stn['ENERGY_ON_SITE']):
        energy_iri = _PREFIX["evr"][f"energyonsite.{stn['ENERGY_ON_SITE']}"]
        kg.add((energy_iri, RDF["type"], _PREFIX["ev-ont"]['RenewableEnergy']))
        kg.add((energy_iri, RDFS["label"], Literal(['ENERGY_ON_SITE'])))
        kg.add((stn_iri, _PREFIX["ev-ont"]["hasOnsiteRenewableEnergy"], energy_iri))

    return kg


def add_charger_ontology(kg, stn_iri, stn):
    def add_ontology(charger_idx, level_id, charger_num, connector_type):
        if charger_num != 0:
            chargerco_iri = _PREFIX["evr"][f"chargercollection.{str(stn['ID']) + str(charger_idx)}"]
            kg.add((chargerco_iri, RDF["type"], _PREFIX["ev-ont"]['ChargerCollection']))
            kg.add((chargerco_iri, RDFS["label"], Literal(f"Charger Collection {str(charger_idx)}")))

            if (level_id == "L1") or (level_id == "L2"):

                chargertype_iri = _PREFIX["evr"][f'chargertype.Level{level_id[1]}Charger']
                kg.add((chargertype_iri, RDF["type"], _PREFIX["ev-ont"]['ChargerType']))
                kg.add((chargertype_iri, RDFS["label"], Literal(f"Level{level_id[1]} Charger")))
                kg.add((chargerco_iri, _PREFIX["ev-ont"]["hasChargerType"], chargertype_iri))

            elif level_id == "DCFast":

                chargertype_iri = _PREFIX["evr"]['chargertype.DCFastCharger']
                kg.add((chargertype_iri, RDF["type"], _PREFIX["ev-ont"]['ChargerType']))
                kg.add((chargertype_iri, RDFS["label"], Literal("DC Fast Charger")))
                kg.add((chargerco_iri, _PREFIX["ev-ont"]["hasChargerType"], chargertype_iri))
            else:
                return

            kg.add((stn_iri, _PREFIX["ev-ont"]["hosts"], chargerco_iri))
            kg.add((chargerco_iri, _PREFIX["ev-ont"]["isHostedBy"], stn_iri))
            if assert_existence(connector_type):
                connectors = connector_type.split(" ")

                for co in connectors:
                    if assert_existence(co):
                        connectortype_iri = _PREFIX["evr"][f"connectortype.{co}"]
                        kg.add((connectortype_iri, RDF["type"], _PREFIX["ev-ont"]['ConnectorType']))
                        kg.add((connectortype_iri, RDFS["label"], Literal(co)))
                        kg.add((chargerco_iri, _PREFIX["ev-ont"]['hasConnectorType'], connectortype_iri))

                if (stn["EV_NETWORK"] != "ElectrifyAmerica") or (level_id != 'DCFast'):
                    kg.add((chargerco_iri, _PREFIX["ev-ont"]["hasAmount"], Literal(charger_num)))
                else:
                    if (level_id == 'DCFast') and (connector_type == "CHAdeMO J1772COMBO"):
                        # add normal charger with ccs and chademo
                        # add normal charger with ccs for ElectrifyAmerica (only 1)
                        kg.add((chargerco_iri, _PREFIX["ev-ont"]["hasAmount"], Literal(1)))
                        # kg.add((chargerco_iri, _PREFIX["ev-ont"]["hasChargerType"], chargertype_iri))

                        # add charger with ccs only----------------------------------------------
                        charger_idx += 1
                        ccschargerco_iri = _PREFIX["evr"][f"chargercollection.{str(stn['ID']) + str(charger_idx)}"]
                        kg.add((ccschargerco_iri, RDF["type"], _PREFIX["ev-ont"]['ChargerCollection']))
                        kg.add((ccschargerco_iri, RDFS["label"], Literal(f"Charger Collection {str(charger_idx)}")))

                        kg.add((ccschargerco_iri, _PREFIX["ev-ont"]["hasAmount"], Literal(charger_num - 1)))

                        kg.add((ccschargerco_iri, _PREFIX["ev-ont"]["hasChargerType"], chargertype_iri))

                        kg.add((stn_iri, _PREFIX["ev-ont"]["hosts"], ccschargerco_iri))
                        kg.add((ccschargerco_iri, _PREFIX["ev-ont"]["isHostedBy"], stn_iri))

                        ccsconnectortype_iri = _PREFIX["evr"]["connectortype.J1772COMBO"]
                        kg.add((ccsconnectortype_iri, RDF["type"], _PREFIX["ev-ont"]['ConnectorType']))
                        kg.add((ccsconnectortype_iri, RDFS["label"], Literal("J1772COMBO")))
                        kg.add((ccschargerco_iri, _PREFIX["ev-ont"]['hasConnectorType'], ccsconnectortype_iri))

            charger_idx += 1
        return charger_idx

    charger_index = 1
    charger_index = add_ontology(charger_index, "L1", stn["EV_LEVEL1_EVSE_NUM"], stn['L1_CONNECTOR_TYPE'])
    charger_index = add_ontology(charger_index, "L2", stn["EV_LEVEL2_EVSE_NUM"], stn['L2_CONNECTOR_TYPE'])
    charger_index = add_ontology(charger_index, "DCFast", stn["EV_DC_FAST_NUM"], stn['DC_CONNECTOR_TYPE'])
    return kg


def add_charging_permit_ontology(kg, stn_iri, stn):
    restricts = stn["ACCESS_DAY_TIME"].replace(':', ' ')
    restricts = stn["ACCESS_DAY_TIME"].replace('|', ' ')
    # restricts = stn["ACCESS_DAY_TIME"].replace('-', ' ')
    if assert_existence(restricts):
        restricts = restricts.split(';')
        operhours = ''
        for item in restricts:
            word_ls = item.lower().split(' ')
            iri_str = str(reduce(lambda x, y: x + '-' + y, word_ls))
            if ("only" in word_ls) and (stn["ACCESS_CODE"].lower() == "private"):
                kg.add((stn_iri, _PREFIX["ev-ont"]["hasAllowedUser"], Literal(item)))
            elif any(c in word_ls for c in ('hours', 'daily')) or re.findall("\dam", item) or re.findall("\dpm", item):
                operhours += f"{item}  "
                kg.add((stn_iri, _PREFIX["ev-ont"]["hasOperatingHours"], Literal(operhours)))

            elif any(c in word_ls for c in ('parking', 'lot')):
                kg.add((stn_iri, _PREFIX["ev-ont"]["hasParkingRestriction"], Literal(item)))

    if assert_existence(stn["EV_PRICING"]):
        kg.add((stn_iri, _PREFIX["ev-ont"]["hasPricingScheme"], Literal(stn["EV_PRICING"])))

    return kg


def integrate_with_kwgr(kg, stn_iri, stn):
    zipcode_iri = _PREFIX["kwgr"][f"zipcodearea.{str('%05d' % int(stn['ZIP']))}"]
    kg.add((zipcode_iri, RDF["type"], _PREFIX["kwg-ont"]["ZipCodeArea"]))
    kg.add((zipcode_iri, RDFS["label"], Literal('zip code ' + str('%05d' % int(stn['ZIP'])))))
    kg.add((zipcode_iri, _PREFIX["kwg-ont"]['sfContains'], stn_iri))
    kg.add((stn_iri, _PREFIX["kwg-ont"]['sfWithin'], zipcode_iri))

    zipcode_ev_iri = _PREFIX["evr"][f"zipcodearea.{str('%05d' % int(stn['ZIP']))}"]
    kg.add((zipcode_ev_iri, _PREFIX["ev-ont"]['sfContains'], stn_iri))
    kg.add((stn_iri, _PREFIX["ev-ont"]['sfWithin'], zipcode_ev_iri))

    return kg


def triplify_charging_station(kg, stn, _PREFIX):
    print(stn['ID'])
    stn_iri = _PREFIX["evr"][f"chargingstation.{str(int(stn['ID']))}"]
    # add basic property ----------------------------------------------------------------------------------
    # charging station class, label,
    kg.add((stn_iri, RDF["type"], _PREFIX["ev-ont"]["ChargingStation"]))  # charging station class
    kg.add((stn_iri, RDFS["label"], Literal(f"Charging Station at {str(stn['STATION_NAME'])}")))

    # open time
    print('open date')

    if assert_existence(stn["OPEN_DATE"]) and stn["OPEN_DATE"] != 'NaT':
        kg.add(
            (stn_iri, _PREFIX["ev-ont"]["hasOpenYear"],
             Literal(stn["OPEN_DATE"].split(' ')[0].split('-')[0], datatype=XSD["gYear"])))
        kg.add((stn_iri, _PREFIX["ev-ont"]["hasOpenDate"],
                Literal(f'{stn["OPEN_DATE"].split(" ")[0]}T{stn["OPEN_DATE"].split(" ")[1]}',
                        datatype=XSD["dateTime"])))

    # street address
    if assert_existence(stn['STREET_ADDRESS']):
        print('STREET_ADDRESS')
        kg.add((stn_iri, _PREFIX["schema"]["streetAddress"], Literal(stn['STREET_ADDRESS'])))

    # add charging station subtype---------------------------------------------------------------------------
    print('Access')
    if assert_existence(stn['ACCESS_CODE']):
        kg.add((stn_iri, RDF["type"], _PREFIX["ev-ont"][f"{str.capitalize(stn['ACCESS_CODE'])}ChargingStation"]))
        kg.add((stn_iri, RDFS["label"], Literal(f"{str.capitalize(stn['ACCESS_CODE'])} Charging Station")))

    # add charging station properties ---------------------------------------------------------------------------
    print('permit')
    kg = add_charging_permit_ontology(kg, stn_iri, stn)
    # add charging operator --------------------------------------------------------------------
    print('add_emobility_ontology')
    kg = add_emobility_ontology(kg, stn_iri, stn)
    # add charger and connector------------------------------------------------------------------------------------
    print('add_charger_ontology')
    kg = add_charger_ontology(kg, stn_iri, stn)
    print('add_facility_ontology')
    kg = add_facility_ontology(kg, stn_iri, stn)
    print('add_energy_ontology')
    kg = add_energy_ontology(kg, stn_iri, stn)
    # add geometry --------------------------------------------------------------------------------------------------
    # kg.add((stn_iri, RDF.type, _PREFIX["geo"]["Feature"]))
    geo_triples = geometry_triples(stn["geometry"], stn_iri, _PREFIX)
    print('geo_triples')
    for triple in geo_triples:
        kg.add(triple)
    # integrate with knowwheregraph ----------------------------------------------------------------------------------
    print('integrate_with_kwgr')
    kg = integrate_with_kwgr(kg, stn_iri, stn)

    return kg


def load_stn_data(file_path):
    stn_df = pd.read_excel(file_path, index_col=None, header=0)
    stn_df["OPEN_DATE"] = [str(x["OPEN_DATE"]) for idx, x in stn_df.iterrows()]
    return stn_df


def add_transline_stn(kg, shp_path):
    line_stn = gpd.read_file(shp_path)
    for idx, stn in line_stn.iterrows():
        stn_iri = _PREFIX["evr"][f"chargingstation.{str(int(stn['ID']))}"]
        line_iri = _PREFIX["evr"][f'transmissionline.{stn["ID_1"]}']
        kg.add((line_iri, _PREFIX["ev-ont"]["hasPotentialInfluenceOn"], stn_iri))
        kg.add((stn_iri, _PREFIX["ev-ont"]["IsPotentiallyInfluencedBy"], line_iri))
    return kg


def assert_existence(val):
    if val is None:
        return False
    elif type(val) is str:
        if (val == ' ') or (val == ''):
            return False
        else:
            return True
    elif type(val) is float:
        if np.isnan(val):
            return False
        else:
            return True
    else:
        return True


def main():
    fpath = "Federal_cleaned.xlsx"
    join_path = "../data/ets/Transline_Stn_join/stn_line_join.shp"
    # fpath = "data/Federal_formatted_tst.xlsx"
    stn_df = load_stn_data(fpath)

    stn_df["geometry"] = [geometry.Point(x["LON"], x["LAT"]) for idx, x in stn_df.iterrows()]
    stn_df = gpd.GeoDataFrame(stn_df, crs="CRS84")

    new_col = pd.DataFrame(stn_df['FACILITY_TYPE'].apply(lambda x: process_str(x))).add_prefix('kg_')
    stn_df = pd.concat([stn_df, new_col], axis=1)

    # initialize
    kg = init_kg_with_prefix(_PREFIX)
    kg = add_ontology_triples(kg, _PREFIX)
    kg = add_facility_classes(stn_df, kg, _PREFIX)
    # for test
    for idx, row in stn_df.iterrows():
        kg = triplify_charging_station(kg, dict(row), _PREFIX)
        """
        try:
            if idx == 0:
                kg = triplify_charging_station(kg, dict(row), _PREFIX)
                warnings.warn(Warning())
        except Warning:
            print('...')
        """
    # for test
    # kg = add_transline_stn(kg, join_path)

    turtle_file = "ev_stns_01-17.ttl"
    kg.serialize(turtle_file, format='turtle')


if __name__ == "__main__":
    main()
