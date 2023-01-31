import pandas as pd
from util import *
from variable import _PREFIX
import geopandas as gpd
from triplify_stns import geometry_triples
from pandarallel import pandarallel
import re

pandarallel.initialize()


class Electricity:
    def __init__(self):
        self.kg = init_kg_with_prefix(_PREFIX)
        self.trans_line = None
        self.sub_stn = None
        self.pwr_plant = None
        self.init_electricity()

    def add_ontology_triples(self):
        self.kg.add((_PREFIX["ev-ont"]["Substation"], RDF["type"], OWL["Class"]))
        self.kg.add((_PREFIX["ev-ont"]["Substation"], RDFS["subClassOf"], OWL["Thing"]))
        self.kg.add((_PREFIX["ev-ont"]["Substation"], RDFS["subClassOf"], _PREFIX["geo"]["Feature"]))
        self.kg.add((_PREFIX["ev-ont"]["Substation"], RDFS["label"], Literal("Substation")))

        self.kg.add((_PREFIX["ev-ont"]["TransmissionLine"], RDF["type"], OWL["Class"]))
        self.kg.add((_PREFIX["ev-ont"]["TransmissionLine"], RDFS["subClassOf"], OWL["Thing"]))
        self.kg.add((_PREFIX["ev-ont"]["TransmissionLine"], RDFS["subClassOf"], _PREFIX["geo"]["Feature"]))
        self.kg.add((_PREFIX["ev-ont"]["TransmissionLine"], RDFS["label"], Literal("Transmission Line")))

        self.kg.add((_PREFIX["ev-ont"]["TransmissionLineOwner"], RDF["type"], OWL["Class"]))
        self.kg.add((_PREFIX["ev-ont"]["TransmissionLineOwner"], RDFS["subClassOf"], OWL["Thing"]))
        self.kg.add((_PREFIX["ev-ont"]["TransmissionLineOwner"], RDFS["label"], Literal("Owner of Transmission Line")))

        self.kg.add((_PREFIX["ev-ont"]["PowerPlant"], RDF["type"], OWL["Class"]))
        self.kg.add((_PREFIX["ev-ont"]["PowerPlant"], RDFS["subClassOf"], OWL["Thing"]))
        self.kg.add((_PREFIX["ev-ont"]["PowerPlant"], RDFS["subClassOf"], _PREFIX["geo"]["Feature"]))
        self.kg.add((_PREFIX["ev-ont"]["PowerPlant"], RDFS["label"], Literal("Power Plant")))

        self.kg.add((_PREFIX["ev-ont"]["PlantOperator"], RDF["type"], OWL["Class"]))
        self.kg.add((_PREFIX["ev-ont"]["PlantOperator"], RDFS["subClassOf"], OWL["Thing"]))
        self.kg.add((_PREFIX["ev-ont"]["PlantOperator"], RDFS["label"], Literal("Plant Operator")))

        self.kg.add((_PREFIX["ev-ont"]["LineAttribute"], RDF["type"], OWL["Class"]))
        self.kg.add((_PREFIX["ev-ont"]["LineAttribute"], RDFS["subClassOf"], OWL["Thing"]))
        self.kg.add((_PREFIX["ev-ont"]["LineAttribute"], RDFS["label"], Literal("Transmission Line Attribute")))

        self.kg.add((_PREFIX["ev-ont"]["InstallWay"], RDF["type"], OWL["Class"]))
        self.kg.add((_PREFIX["ev-ont"]["InstallWay"], RDFS["subClassOf"], _PREFIX["ev-ont"]["LineAttribute"]))
        self.kg.add((_PREFIX["ev-ont"]["InstallWay"], RDFS["label"], Literal("Install Way")))

        self.kg.add((_PREFIX["ev-ont"]["CurrentType"], RDF["type"], OWL["Class"]))
        self.kg.add((_PREFIX["ev-ont"]["CurrentType"], RDFS["subClassOf"], _PREFIX["ev-ont"]["LineAttribute"]))
        self.kg.add((_PREFIX["ev-ont"]["CurrentType"], RDFS["label"], Literal("Current Type")))

        self.kg.add((_PREFIX["ev-ont"]["VoltageClass"], RDF["type"], OWL["Class"]))
        self.kg.add((_PREFIX["ev-ont"]["VoltageClass"], RDFS["subClassOf"], _PREFIX["ev-ont"]["LineAttribute"]))
        self.kg.add((_PREFIX["ev-ont"]["VoltageClass"], RDFS["label"], Literal("Voltage Class")))

        self.kg.add((_PREFIX["ev-ont"]["Voltage"], RDF["type"], OWL["Class"]))
        self.kg.add((_PREFIX["ev-ont"]["Voltage"], RDFS["subClassOf"], _PREFIX["ev-ont"]["LineAttribute"]))
        self.kg.add((_PREFIX["ev-ont"]["Voltage"], RDFS["label"], Literal("Voltage")))

        self.kg.add((_PREFIX["ev-ont"]["ServingStatus"], RDF["type"], OWL["Class"]))
        self.kg.add((_PREFIX["ev-ont"]["ServingStatus"], RDFS["subClassOf"], _PREFIX["ev-ont"]["LineAttribute"]))
        self.kg.add((_PREFIX["ev-ont"]["ServingStatus"], RDFS["label"], Literal("Serving Status")))

        # ----------object type
        self.kg.add((_PREFIX["ev-ont"]["connects"], RDF["type"], OWL["ObjectProperty"]))
        self.kg.add((_PREFIX["ev-ont"]["connects"], RDFS["domain"], _PREFIX["ev-ont"]['Substation']))
        self.kg.add((_PREFIX["ev-ont"]["connects"], RDFS["range"], _PREFIX["ev-ont"]['TransmissionLine']))

        self.kg.add((_PREFIX["ev-ont"]["hasSubstation"], RDF["type"], OWL["ObjectProperty"]))
        self.kg.add((_PREFIX["ev-ont"]["hasSubstation"], RDFS["domain"], _PREFIX["ev-ont"]['PowerPlant']))
        self.kg.add((_PREFIX["ev-ont"]["hasSubstation"], RDFS["range"], _PREFIX["ev-ont"]['Substation']))

        self.kg.add((_PREFIX["ev-ont"]["isSubstationOf"], RDF["type"], OWL["ObjectProperty"]))
        self.kg.add((_PREFIX["ev-ont"]["isSubstationOf"], RDFS["domain"], _PREFIX["ev-ont"]['Substation']))
        self.kg.add((_PREFIX["ev-ont"]["isSubstationOf"], RDFS["range"], _PREFIX["ev-ont"]['PowerPlant']))

        self.kg.add((_PREFIX["ev-ont"]["hasCurrentType"], RDF["type"], OWL["ObjectProperty"]))
        self.kg.add((_PREFIX["ev-ont"]["hasCurrentType"], RDFS["domain"], _PREFIX["ev-ont"]['TransmissionLine']))
        self.kg.add((_PREFIX["ev-ont"]["hasCurrentType"], RDFS["range"], _PREFIX["ev-ont"]['CurrentType']))

        self.kg.add((_PREFIX["ev-ont"]["hasInstallWay"], RDF["type"], OWL["ObjectProperty"]))
        self.kg.add((_PREFIX["ev-ont"]["hasInstallWay"], RDFS["domain"], _PREFIX["ev-ont"]['TransmissionLine']))
        self.kg.add((_PREFIX["ev-ont"]["hasInstallWay"], RDFS["range"], _PREFIX["ev-ont"]['InstallWay']))

        self.kg.add((_PREFIX["ev-ont"]["hasVoltageClass"], RDF["type"], OWL["ObjectProperty"]))
        self.kg.add((_PREFIX["ev-ont"]["hasVoltageClass"], RDFS["domain"], _PREFIX["ev-ont"]['TransmissionLine']))
        self.kg.add((_PREFIX["ev-ont"]["hasVoltageClass"], RDFS["range"], _PREFIX["ev-ont"]['VoltageClass']))

        self.kg.add((_PREFIX["ev-ont"]["hasServingStatus"], RDF["type"], OWL["ObjectProperty"]))
        self.kg.add((_PREFIX["ev-ont"]["hasServingStatus"], RDFS["domain"], _PREFIX["ev-ont"]['TransmissionLine']))
        self.kg.add((_PREFIX["ev-ont"]["hasServingStatus"], RDFS["range"], _PREFIX["ev-ont"]['ServingStatus']))

        self.kg.add((_PREFIX["ev-ont"]["hasServingStatus"], RDF["type"], OWL["ObjectProperty"]))
        self.kg.add((_PREFIX["ev-ont"]["hasServingStatus"], RDFS["domain"], _PREFIX["ev-ont"]['Substation']))
        self.kg.add((_PREFIX["ev-ont"]["hasServingStatus"], RDFS["range"], _PREFIX["ev-ont"]['ServingStatus']))

        self.kg.add((_PREFIX["ev-ont"]["hasOperator"], RDF["type"], OWL["ObjectProperty"]))
        self.kg.add((_PREFIX["ev-ont"]["hasOperator"], RDFS["domain"], _PREFIX["ev-ont"]['PowerPlant']))
        self.kg.add((_PREFIX["ev-ont"]["hasOperator"], RDFS["range"], _PREFIX["ev-ont"]['PlantOperator']))

        self.kg.add((_PREFIX["ev-ont"]["hasOwner"], RDF["type"], OWL["ObjectProperty"]))
        self.kg.add((_PREFIX["ev-ont"]["hasOwner"], RDFS["domain"], _PREFIX["ev-ont"]['TransmissionLine']))
        self.kg.add((_PREFIX["ev-ont"]["hasOwner"], RDFS["range"], _PREFIX["ev-ont"]['TransmissionLineOwner']))

        # -----------
        '''
        kg.add((_PREFIX["ev-ont"]["hasCurrentType"], RDF["type"], OWL["DatatypeProperty"]))
        kg.add((_PREFIX["ev-ont"]["hasCurrentType"], RDFS["label"], Literal('Current type')))
        kg.add((_PREFIX["ev-ont"]["hasCurrentType"],  RDFS["comment"], Literal(f'The current type of the transmission line')))
        # -----------
        kg.add((_PREFIX["ev-ont"]["hasInstallWay"], RDF["type"], OWL["DatatypeProperty"]))
        kg.add((_PREFIX["ev-ont"]["hasInstallWay"], RDFS["label"], Literal('Install way')))
        kg.add((_PREFIX["ev-ont"]["hasInstallWay"],  RDFS["comment"], Literal(f'The install type of the transmission line')))

        kg.add((_PREFIX["ev-ont"]["hasVoltageClass"], RDF["type"], OWL["DatatypeProperty"]))
        kg.add((_PREFIX["ev-ont"]["hasVoltageClass"], RDFS["label"], Literal('Voltage Class')))
        kg.add((_PREFIX["ev-ont"]["hasVoltageClass"],  RDFS["comment"], Literal(f'The voltage class of the transmission line')))
        '''
        self.kg.add((_PREFIX["ev-ont"]["hasVoltage"], RDF["type"], OWL["DatatypeProperty"]))
        self.kg.add((_PREFIX["ev-ont"]["hasVoltage"], RDFS["label"], Literal('Voltage')))
        self.kg.add((_PREFIX["ev-ont"]["hasVoltage"], RDFS["comment"], Literal(f'The voltage of a transmission line')))

        self.kg.add((_PREFIX["ev-ont"]["hasSummerCapacity"], RDF["type"], OWL["DatatypeProperty"]))
        self.kg.add((_PREFIX["ev-ont"]["hasSummerCapacity"], RDFS["label"], Literal('Summer Capacity')))
        self.kg.add((_PREFIX["ev-ont"]["hasSummerCapacity"], RDFS["comment"],
                     Literal(f'The summer capacity of a power plant')))

        self.kg.add((_PREFIX["ev-ont"]["hasWinterCapacity"], RDF["type"], OWL["DatatypeProperty"]))
        self.kg.add((_PREFIX["ev-ont"]["hasWinterCapacity"], RDFS["label"], Literal('Summer Capacity')))
        self.kg.add((_PREFIX["ev-ont"]["hasWinterCapacity"], RDFS["comment"],
                     Literal(f'The summer capacity of a power plant')))

        self.kg.add((_PREFIX["ev-ont"]["hasMaxVoltage"], RDF["type"], OWL["DatatypeProperty"]))
        self.kg.add((_PREFIX["ev-ont"]["hasMaxVoltage"], RDFS["label"], Literal('Max Voltage')))
        self.kg.add((_PREFIX["ev-ont"]["hasMaxVoltage"], RDFS["comment"],
                     Literal(f'The Max Voltage of a substation')))

        self.kg.add((_PREFIX["ev-ont"]["hasMinVoltage"], RDF["type"], OWL["DatatypeProperty"]))
        self.kg.add((_PREFIX["ev-ont"]["hasMinVoltage"], RDFS["label"], Literal('Min Voltage')))
        self.kg.add((_PREFIX["ev-ont"]["hasMinVoltage"], RDFS["comment"],
                     Literal(f'The Min Voltage of a substation')))

        self.kg.add((_PREFIX["ev-ont"]["hasOperatingCapacity"], RDF["type"], OWL["DatatypeProperty"]))
        self.kg.add((_PREFIX["ev-ont"]["hasOperatingCapacity"], RDFS["label"], Literal('Operating Capacity')))
        self.kg.add((_PREFIX["ev-ont"]["hasOperatingCapacity"], RDFS["comment"],
                     Literal(f'The operating capacity of a power plant')))

        self.kg.add((_PREFIX["ev-ont"]["hasValue"], RDF["type"], OWL["DatatypeProperty"]))
        self.kg.add((_PREFIX["ev-ont"]["hasValue"], RDFS["label"], Literal('Operating Capacity')))
        self.kg.add((_PREFIX["ev-ont"]["hasValue"], RDFS["comment"],
                     Literal(f'The voltage value of a transmission line')))

    def triplify_transline(self):
        for idx, line in self.trans_line.iterrows():
            print(idx)
            line_iri = _PREFIX["evr"][f'transmissionline.{line["ID"]}']
            self.kg.add((line_iri, RDF["type"], _PREFIX["ev-ont"]["TransmissionLine"]))
            self.kg.add((line_iri, RDFS["label"], Literal(f'Transmission Line {line["ID"]}')))

            serve_iri = _PREFIX["evr"][f'lineattributes.servingstatus.{"-".join(line["STATUS"].lower().split(" "))}']
            self.kg.add((serve_iri, RDF["type"], _PREFIX["ev-ont"]["ServingStatus"]))
            self.kg.add((serve_iri, RDFS["label"], Literal(f'{line["STATUS"]}')))
            self.kg.add((line_iri, _PREFIX["ev-ont"]['hasServingStatus'], serve_iri))

            type_ls = line["TYPE"].split('; ')
            install_id = 0
            if len(type_ls) > 1:
                install_id = 1
                current_iri = _PREFIX["evr"][f'lineattributes.currenttype.{type_ls[0]}']
                self.kg.add((current_iri, RDF["type"], _PREFIX["ev-ont"]["CurrentType"]))
                self.kg.add((current_iri, RDFS["label"], Literal(f'{type_ls[0]}')))
                self.kg.add((line_iri, _PREFIX["ev-ont"]['hasCurrentType'], current_iri))

            install_iri = _PREFIX["evr"][
                f'lineattributes.installway.{"-".join(type_ls[install_id].lower().split(" "))}']
            self.kg.add((install_iri, RDF["type"], _PREFIX["ev-ont"]["InstallWay"]))
            self.kg.add((install_iri, RDFS["label"], Literal(f'{type_ls[install_id]}')))
            self.kg.add((line_iri, _PREFIX["ev-ont"]['hasInstallWay'], install_iri))

            vclass_iri = _PREFIX["evr"][
                f'lineattributes.voltageclass.{"-".join(line["VOLT_CLASS"].lower().split(" "))}']
            self.kg.add((vclass_iri, RDF["type"], _PREFIX["ev-ont"]["VoltageClass"]))
            self.kg.add((vclass_iri, RDFS["label"], Literal(f'{line["VOLT_CLASS"]}')))
            self.kg.add((line_iri, _PREFIX["ev-ont"]['hasVoltageClass'], vclass_iri))
            if assert_existence(line["VOLTAGE"])  and (line["VOLTAGE"] != -999999.0):
                voltage_iri = _PREFIX["evr"][f'lineattributes.voltage.{str(line["VOLTAGE"])}']
                self.kg.add((voltage_iri, RDFS["label"], Literal(line["VOLTAGE"])))
                self.kg.add((line_iri, _PREFIX["ev-ont"]['hasVoltage'], voltage_iri))

            # owner
            if assert_existence(line["OWNER"]):
                owner_iri = _PREFIX["evr"][f'transmissionlineowner.{"-".join(line["OWNER"].lower().split(" "))}']
                self.kg.add((owner_iri, RDF["type"], _PREFIX["ev-ont"]["TransmissionLineOwner"]))
                self.kg.add((owner_iri, RDFS["label"], Literal(f'{line["OWNER"]}')))
                self.kg.add((line_iri, _PREFIX["ev-ont"]['hasOwner'], owner_iri))

            # add geometry
            geo_triples = geometry_triples(line["geometry"], line_iri, _PREFIX, namespace="evr")
            for triple in geo_triples:
                self.kg.add(triple)
            # add touched objects
            print("...")
        print('...')

    def triplify_substn(self):
        for idx, stn in self.sub_stn.iterrows():
            if assert_existence(stn.geometry):
                print('substn:', idx)
                stn_iri = _PREFIX["evr"][f'substation.{stn["ID"]}']
                self.kg.add((stn_iri, RDF["type"], _PREFIX["ev-ont"]["Substation"]))
                self.kg.add((stn_iri, RDFS["label"], Literal(f'Substation {stn["NAME"]}')))
                if assert_existence(stn["STATUS"]):
                    serve_iri = _PREFIX["evr"][f'lineattributes.servingstatus.{"-".join(stn["STATUS"].lower().split(" "))}']
                    self.kg.add((serve_iri, RDF["type"], _PREFIX["ev-ont"]["ServingStatus"]))
                    self.kg.add((serve_iri, RDFS["label"], Literal(f'{stn["STATUS"]}')))
                    self.kg.add((stn_iri, _PREFIX["ev-ont"]['hasServingStatus'], serve_iri))
                    self.integrate_with_kwgr(stn_iri, stn)

                if assert_existence(stn["MAX_VOLT"]) and (stn["MAX_VOLT"] != -999999.0):
                    self.kg.add((stn_iri, _PREFIX["ev-ont"]['hasMaxVoltage'], Literal(f'{stn["MAX_VOLT"]}')))
                if assert_existence(stn["MIN_VOLT"]) and (stn["MIN_VOLT"] != -999999.0):
                    self.kg.add((stn_iri, _PREFIX["ev-ont"]['hasMinVoltage'], Literal(f'{stn["MIN_VOLT"]}')))

                geo_triples = geometry_triples(stn["geometry"], stn_iri, _PREFIX, namespace="evr")
                for triple in geo_triples:
                    self.kg.add(triple)

    def triplify_pwrplant(self):
        for idx, plant in self.pwr_plant.iterrows():
            print(idx)
            plant_iri = _PREFIX["evr"][f'powerplant.{plant["ID"]}']
            self.kg.add((plant_iri, RDF["type"], _PREFIX["ev-ont"]["PowerPlant"]))
            self.kg.add((plant_iri, RDFS["label"], Literal(f'Power Plant {plant["NAME"]}')))

            if assert_existence(plant["SUMMER_CAP"]) and (plant["SUMMER_CAP"] != -999999.0):
                self.kg.add((plant_iri, _PREFIX["ev-ont"]['hasSummerCapacity'], Literal(f'{plant["SUMMER_CAP"]}')))
            if assert_existence(plant["WINTER_CAP"]) and (plant["WINTER_CAP"] != -999999.0):
                self.kg.add((plant_iri, _PREFIX["ev-ont"]['hasWinterCapacity'], Literal(f'{plant["WINTER_CAP"]}')))

            if assert_existence(plant["OPER_CAP"]) and (plant["OPER_CAP"] != -999999.0):
                self.kg.add((plant_iri, _PREFIX["ev-ont"]['hasOperatingCapacity'], Literal(f'{plant["OPER_CAP"]}')))

            if assert_existence(plant["OPERATOR"]):
                oper_str = ''.join(re.split(r'[^A-Za-z]', plant["OPERATOR"]))
                oper_iri = _PREFIX["evr"][f'plantoperator.{oper_str}']
                self.kg.add((oper_iri, RDF["type"], _PREFIX["ev-ont"]["PlantOperator"]))
                self.kg.add((oper_iri, RDFS["label"], Literal(f'Plant Operator {plant["OPERATOR"]}')))
                self.kg.add((plant_iri, _PREFIX["ev-ont"]['hasOperator'], oper_iri))
            geo_triples = geometry_triples(plant["geometry"], plant_iri, _PREFIX, namespace="evr")
            for triple in geo_triples:
                self.kg.add(triple)

            self.integrate_with_kwgr(plant_iri, plant)

    def connect_sub_trans(self, touch_df):
        def add_pair(line_id, stn_id):
            line_iri = _PREFIX["evr"][f'transmissionline.{line_id}']
            stn_iri = _PREFIX["evr"][f'substation.{stn_id}']
            self.kg.add((stn_iri, _PREFIX["ev-ont"]['connects'], line_iri))

        touch_df.apply(lambda x: add_pair(x['ID'], x['ID_1']), axis=1)

    def connect_sub_plant(self):
        sub1_conn = pd.merge(self.pwr_plant, self.sub_stn, left_on='SUB_1', right_on='NAME', how='inner')
        sub2_conn = pd.merge(self.pwr_plant, self.sub_stn, left_on='SUB_2', right_on='NAME', how='inner')

        def add_pair(plant_id, sub_id):
            plant_iri = _PREFIX["evr"][f'powerplant.{plant_id}']
            sub_iri = _PREFIX["evr"][f'substation.{sub_id}']
            self.kg.add((plant_iri, _PREFIX["ev-ont"]['hasSubstation'], sub_iri))
            self.kg.add((sub_iri, _PREFIX["ev-ont"]['isSubstationOf'], plant_iri))

        if sub1_conn.shape[0] != 0:
            sub1_conn.apply(lambda x: add_pair(x['ID_x'], x['ID_y']), axis=1)
        if sub2_conn.shape[0] != 0:
            sub2_conn.apply(lambda x: add_pair(x['ID_x'], x['ID_y']), axis=1)

        print('...')

    def connect_trans(self):
        touch_lines = self.trans_line.parallel_apply(line_touch, args=(self.trans_line,), axis=1)
        self.process_touches(touch_lines)

    def init_electricity(self):
        self.add_ontology_triples()
        self.sub_stn = gpd.read_file("../data/ets/Substation/Substations.shp")
        self.sub_stn = self.sub_stn.to_crs(4326)

        self.trans_line = gpd.read_file(
            "../data/ets/Electric_Power_Transmission_Lines/Electric_Power_Transmission_Lines.shp")
        self.trans_line = self.trans_line.to_crs(4326)

        self.pwr_plant = gpd.read_file("../data/ets/Power_Plants/Power_Plants.shp")
        self.pwr_plant = self.pwr_plant.to_crs(4326)

        self.pwr_plant.rename(columns={'PLANT_CODE': 'ID'}, inplace=True)
        self.trans_line.set_index("ID")
        self.pwr_plant.set_index("ID")
        self.sub_stn.set_index("ID")
        self.triplify_substn()
        self.triplify_pwrplant()
        self.triplify_transline()

    def process_touches(self, touch_df, ets_type='transmissionline'):
        for idx, target_df in enumerate(touch_df):
            print(idx)
            if target_df.shape[0] != 0:
                target_iri = _PREFIX["evr"][f'{ets_type}.{target_df["ID_left"].values[0]}']
                for idx, neighbor in target_df.iterrows():
                    neigh_iri = _PREFIX["evr"][f'{ets_type}.{neighbor["ID_right"]}']
                    self.kg.add((target_iri, _PREFIX["kwg-ont"]['sfTouches'], neigh_iri))

    def integrate_with_kwgr(self, stn_iri, stn):
        if stn['ZIP'] != 'NOT AVAILABLE':

            zipcode_iri = _PREFIX["kwgr"][f"zipcodearea.{str('%05d' % int(stn['ZIP']))}"]
            self.kg.add((zipcode_iri, RDF["type"], _PREFIX["kwg-ont"]["ZipCodeArea"]))
            self.kg.add((zipcode_iri, RDFS["label"], Literal('ZIP code ' + str(stn['ZIP']))))
            self.kg.add((zipcode_iri, _PREFIX["kwg-ont"]['sfContains'], stn_iri))
            self.kg.add((stn_iri, _PREFIX["kwg-ont"]['sfWithin'], zipcode_iri))

    def line_zip_intersect(self, line_zip_df):
        for idx, line in line_zip_df.iterrows():
            print('int:', idx)
            line_iri = _PREFIX["evr"][f'transmissionline.{line["ID"]}']
            zipcode_iri = _PREFIX["kwgr"][f"zipcodearea.{str('%05d' % int(line['ZCTA5CE10']))}"]
            self.kg.add((line_iri, _PREFIX["kwg-ont"]['sfCrosses'], zipcode_iri))

    def line_self_touch(self, line_stouch_df):
        for idx, line in line_stouch_df.iterrows():
            print('line self:', idx)
            if (line["ID"] is not None) and (line["ID_1"] is not None):
                target_iri = _PREFIX["evr"][f'transmissionline.{line["ID"]}']
                neigh_iri = _PREFIX["evr"][f"transmissionline.{line['ID_1']}"]
                self.kg.add((target_iri, _PREFIX["kwg-ont"]['sfTouches'], neigh_iri))


def line_touch(target_obj, right_df):
    import geopandas as gpd
    from shapely.wkt import dumps, loads
    target_obj = gpd.GeoDataFrame(target_obj).T.set_geometry('geometry')
    target_obj = target_obj.set_crs('epsg:3857')
    target_obj = target_obj.to_crs(4326)
    target_obj.geometry = target_obj['geometry']
    touch_df = gpd.sjoin(left_df=target_obj, right_df=right_df, predicate='intersects')
    print("...")
    return touch_df


def assert_existence(val):
    if val is None:
        return False
    elif type(val) is str:
        if (val == ' ') or (val == ''):
            return False
        elif val == 'NOT AVAILABLE':
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
    trans_sub_df = gpd.read_file("../data/ets/line_point_touch/line_sub_touch.shp")
    line_zip_df = gpd.read_file("../data/ets/Transline_ZIP_join/Transline_ZIP_join.shp")
    line_self_df = gpd.read_file("../data/ets/Transline_SelfTouch/Transline_SelfTouch.shp")
    trans_sub_df = trans_sub_df.to_crs(4326)
    line_zip_df = line_zip_df.to_crs(4326)
    line_self_df = line_self_df.to_crs(4326)
    elec_obj = Electricity()
    elec_obj.line_zip_intersect(line_zip_df)
    elec_obj.line_self_touch(line_self_df)
    elec_obj.connect_sub_plant()
    elec_obj.connect_sub_trans(trans_sub_df)
    print('...')
    elec_ttl = "{}/elec_system.ttl".format('./EVRegData')
    elec_obj.kg.serialize(elec_ttl, format='turtle')


if __name__ == "__main__":
    main()
