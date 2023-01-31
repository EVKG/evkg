import pandas as pd
from util import *
from variable import _PREFIX
import re

ev_abbr = "ElectricVehicleProduct"


class EVReg:
    def __init__(self):
        self.kg = init_kg_with_prefix(_PREFIX)

    def add_ontology_triples(self):
        self.kg.add((_PREFIX["ev-ont"]["ElectricVehicleProduct"], RDF["type"], OWL["Class"]))
        self.kg.add((_PREFIX["ev-ont"]["ElectricVehicleProduct"], RDFS["subClassOf"], OWL["Thing"]))
        self.kg.add((_PREFIX["ev-ont"]["ElectricVehicleProduct"], RDFS["label"],
                     Literal("EV Product")))

        self.kg.add((_PREFIX["ev-ont"]["ElectricVehicleRegistrationCollection"], RDF["type"], OWL["Class"]))
        self.kg.add(
            (_PREFIX["ev-ont"]["ElectricVehicleRegistrationCollection"], RDFS["subClassOf"], OWL["Thing"]))
        self.kg.add((_PREFIX["ev-ont"]["ElectricVehicleRegistrationCollection"], RDFS["label"],
                     Literal("EV Registration Collection")))

        self.kg.add((_PREFIX["ev-ont"]["hasProductInfo"], RDF["type"], OWL["ObjectProperty"]))
        self.kg.add((_PREFIX["ev-ont"]["hasProductInfo"], RDFS["domain"],
                     _PREFIX['ev-ont']['ElectricVehicleRegistrationCollection']))
        self.kg.add(
            (_PREFIX["ev-ont"]["hasProductInfo"], RDFS["range"],
             _PREFIX['ev-ont']['ElectricVehicleProduct']))

        self.kg.add((_PREFIX["ev-ont"]["MakeType"], RDF["type"], OWL["Class"]))
        self.kg.add((_PREFIX["ev-ont"]["MakeType"], RDFS["subClassOf"], OWL["Thing"]))
        self.kg.add((_PREFIX["ev-ont"]["MakeType"], RDFS["label"], Literal("Make Type")))

        self.kg.add((_PREFIX["ev-ont"]["ModelType"], RDF["type"], OWL["Class"]))
        self.kg.add((_PREFIX["ev-ont"]["ModelType"], RDFS["subClassOf"], OWL["Thing"]))
        self.kg.add((_PREFIX["ev-ont"]["ModelType"], RDFS["label"], Literal("Model Type")))

        self.kg.add((_PREFIX["ev-ont"]["Technology"], RDF["type"], OWL["Class"]))
        self.kg.add((_PREFIX["ev-ont"]["Technology"], RDFS["subClassOf"], OWL["Thing"]))
        self.kg.add((_PREFIX["ev-ont"]["Technology"], RDFS["label"], Literal("EV Technology")))

        self.kg.add((_PREFIX["ev-ont"]["Manufacturer"], RDF["type"], OWL["Class"]))
        self.kg.add((_PREFIX["ev-ont"]["Manufacturer"], RDFS["subClassOf"], _PREFIX["schema"]["Organization"]))
        self.kg.add((_PREFIX["ev-ont"]["Manufacturer"], RDFS["label"], Literal("Vehicle Manufacturer")))

        self.kg.add((_PREFIX["ev-ont"]["DutyType"], RDF["type"], OWL["Class"]))
        self.kg.add((_PREFIX["ev-ont"]["DutyType"], RDFS["subClassOf"], OWL["Thing"]))
        self.kg.add((_PREFIX["ev-ont"]["DutyType"], RDFS["label"], Literal("Vehicle Duty Type")))

        self.kg.add((_PREFIX["ev-ont"]["WeightLevel"], RDF["type"], OWL["Class"]))
        self.kg.add((_PREFIX["ev-ont"]["WeightLevel"], RDFS["subClassOf"], OWL["Thing"]))
        self.kg.add((_PREFIX["ev-ont"]["WeightLevel"], RDFS["label"], Literal("Vehicle Weight Level")))

        self.kg.add((_PREFIX["ev-ont"]["UseCase"], RDF["type"], OWL["Class"]))
        self.kg.add((_PREFIX["ev-ont"]["UseCase"], RDFS["subClassOf"], OWL["Thing"]))
        self.kg.add((_PREFIX["ev-ont"]["UseCase"], RDFS["label"], Literal("Vehicle Use Case")))

        self.kg.add((_PREFIX["ev-ont"]["hasTemporalScope"], RDF["type"], OWL["DatatypeProperty"]))
        self.kg.add((_PREFIX["ev-ont"]["hasTemporalScope"], RDFS["label"], Literal('Registration Year')))
        self.kg.add((_PREFIX["ev-ont"]["hasTemporalScope"], RDFS["comment"],
                     Literal(f'The year of the EV registration collection')))

        self.kg.add((_PREFIX["ev-ont"]["hasAmount"], RDF["type"], OWL["DatatypeProperty"]))
        self.kg.add((_PREFIX["ev-ont"]["hasAmount"], RDFS["label"], Literal('Vehicle Number')))
        self.kg.add((_PREFIX["ev-ont"]["hasAmount"], RDFS["comment"],
                     Literal(f'The number of EV registrations in this collection')))

        self.kg.add((_PREFIX["ev-ont"]["hasModelType"], RDF["type"], OWL["ObjectProperty"]))
        self.kg.add(
            (
                _PREFIX["ev-ont"]["hasModelType"], RDFS["domain"],
                _PREFIX['ev-ont']['ElectricVehicleProduct']))
        self.kg.add((_PREFIX["ev-ont"]["hasModelType"], RDFS["range"], _PREFIX['ev-ont']['ModelType']))

        self.kg.add((_PREFIX["ev-ont"]["hasSpatialScope"], RDF["type"], OWL["ObjectProperty"]))
        self.kg.add((_PREFIX["ev-ont"]["hasSpatialScope"], RDFS["domain"],
                     _PREFIX['ev-ont']['ElectricVehicleRegistrationCollection']))
        self.kg.add((_PREFIX["ev-ont"]["hasSpatialScope"], RDFS["range"],
                     _PREFIX["kwg-ont"]["AdministrativeRegion_3"]))

        self.kg.add((_PREFIX["ev-ont"]["hasSpatialScope"], RDF["type"], OWL["ObjectProperty"]))
        self.kg.add((_PREFIX["ev-ont"]["hasSpatialScope"], RDFS["domain"],
                     _PREFIX['ev-ont']['ElectricVehicleRegistrationCollection']))
        self.kg.add((_PREFIX["ev-ont"]["hasSpatialScope"], RDFS["range"], _PREFIX["kwg-ont"]["ZipCodeArea"]))

        self.kg.add((_PREFIX["ev-ont"]['isSpatialScopeOf'], RDF["type"], OWL["ObjectProperty"]))
        self.kg.add((_PREFIX["ev-ont"]['isSpatialScopeOf'], RDFS["domain"], _PREFIX["kwg-ont"]["ZipCodeArea"]))
        self.kg.add((_PREFIX["ev-ont"]['isSpatialScopeOf'], RDFS["range"],
                     _PREFIX['ev-ont']['ElectricVehicleRegistrationCollection']))

        self.kg.add((_PREFIX["ev-ont"]['isSpatialScopeOf'], RDF["type"], OWL["ObjectProperty"]))
        self.kg.add(
            (_PREFIX["ev-ont"]['isSpatialScopeOf'], RDFS["domain"],
             _PREFIX["kwg-ont"]["AdministrativeRegion_3"]))
        self.kg.add((_PREFIX["ev-ont"]['isSpatialScopeOf'], RDFS["range"],
                     _PREFIX['ev-ont']['ElectricVehicleRegistrationCollection']))

        self.kg.add((_PREFIX["ev-ont"]["hasMakeType"], RDF["type"], OWL["ObjectProperty"]))
        self.kg.add(
            (_PREFIX["ev-ont"]["hasMakeType"], RDFS["domain"], _PREFIX['ev-ont']['ElectricVehicleProduct']))
        self.kg.add((_PREFIX["ev-ont"]["hasMakeType"], RDFS["range"], _PREFIX['ev-ont']['MakeType']))

        self.kg.add((_PREFIX["ev-ont"]["hasModelYear"], RDF["type"], OWL["DatatypeProperty"]))
        self.kg.add((_PREFIX["ev-ont"]["hasModelYear"], RDFS["label"], Literal('Model Year')))
        self.kg.add((_PREFIX["ev-ont"]["hasModelYear"], RDFS["comment"], Literal(f'Mode year')))

        self.kg.add((_PREFIX["ev-ont"]["hasMatchableConnectorType"], RDF["type"], OWL["ObjectProperty"]))
        self.kg.add((_PREFIX["ev-ont"]["hasMatchableConnectorType"], RDFS["domain"],
                     _PREFIX['ev-ont']['ElectricVehicleProduct']))
        self.kg.add((_PREFIX["ev-ont"]["hasMatchableConnectorType"], RDFS["range"],
                     _PREFIX["ev-ont"]["ConnectorType"]))

        self.kg.add((_PREFIX["ev-ont"]["hasMatchableChargerType"], RDF["type"], OWL["ObjectProperty"]))
        self.kg.add((_PREFIX["ev-ont"]["hasMatchableChargerType"], RDFS["domain"],
                     _PREFIX['ev-ont']['ElectricVehicleProduct']))
        self.kg.add(
            (_PREFIX["ev-ont"]["hasMatchableChargerType"], RDFS["range"], _PREFIX["ev-ont"]["ChargerType"]))

        self.kg.add((_PREFIX["ev-ont"]["hasManufacturer"], RDF["type"], OWL["ObjectProperty"]))
        self.kg.add((_PREFIX["ev-ont"]["hasManufacturer"], RDFS["domain"],
                     _PREFIX['ev-ont']['ElectricVehicleProduct']))
        self.kg.add((_PREFIX["ev-ont"]["hasManufacturer"], RDFS["range"], _PREFIX["ev-ont"]["Manufacturer"]))

        self.kg.add((_PREFIX["ev-ont"]["hasVehicleDutyType"], RDF["type"], OWL["ObjectProperty"]))
        self.kg.add((_PREFIX["ev-ont"]["hasVehicleDutyType"], RDFS["domain"],
                     _PREFIX['ev-ont']['ElectricVehicleProduct']))
        self.kg.add((_PREFIX["ev-ont"]["hasVehicleDutyType"], RDFS["range"], _PREFIX["ev-ont"]["DutyType"]))

        self.kg.add((_PREFIX["ev-ont"]["hasVehicleWeightLevel"], RDF["type"], OWL["ObjectProperty"]))
        self.kg.add((_PREFIX["ev-ont"]["hasVehicleWeightLevel"], RDFS["domain"],
                     _PREFIX['ev-ont']['ElectricVehicleProduct']))
        self.kg.add(
            (_PREFIX["ev-ont"]["hasVehicleWeightLevel"], RDFS["range"], _PREFIX["ev-ont"]["WeightLevel"]))

        self.kg.add((_PREFIX["ev-ont"]["hasFastChargingConnector"], RDF["type"], OWL["ObjectProperty"]))
        self.kg.add((_PREFIX["ev-ont"]["hasFastChargingConnector"], RDFS["domain"],
                     _PREFIX['ev-ont']['ElectricVehicleProduct']))
        self.kg.add((_PREFIX["ev-ont"]["hasFastChargingConnector"], RDFS["range"],
                     _PREFIX["ev-ont"]["ConnectorType"]))

        self.kg.add((_PREFIX["ev-ont"]["hasVehicleUseCase"], RDF["type"], OWL["ObjectProperty"]))
        self.kg.add((_PREFIX["ev-ont"]["hasVehicleUseCase"], RDFS["domain"],
                     _PREFIX['ev-ont']['ElectricVehicleProduct']))
        self.kg.add((_PREFIX["ev-ont"]["hasVehicleUseCase"], RDFS["range"], _PREFIX["ev-ont"]["UseCase"]))

        self.kg.add((_PREFIX["ev-ont"]["isWithTechnology"], RDF["type"], OWL["ObjectProperty"]))
        self.kg.add((_PREFIX["ev-ont"]["isWithTechnology"], RDFS["domain"],
                     _PREFIX['ev-ont']['ElectricVehicleProduct']))
        self.kg.add((_PREFIX["ev-ont"]["isWithTechnology"], RDFS["range"], _PREFIX["ev-ont"]["Technology"]))

        self.kg.add((_PREFIX["ev-ont"]["publishes"], RDF["type"], OWL["ObjectProperty"]))
        self.kg.add((_PREFIX["ev-ont"]["publishes"], RDFS["domain"], _PREFIX['ev-ont']['Manufacturer']))
        self.kg.add((_PREFIX["ev-ont"]["publishes"], RDFS["range"], _PREFIX["ev-ont"]["MakeType"]))

        self.kg.add((_PREFIX["ev-ont"]["produces"], RDF["type"], OWL["ObjectProperty"]))
        self.kg.add((_PREFIX["ev-ont"]["produces"], RDFS["domain"], _PREFIX['ev-ont']['Manufacturer']))
        self.kg.add((_PREFIX["ev-ont"]["produces"], RDFS["range"], _PREFIX["ev-ont"]["ModelType"]))

    def zipcode_link(self, sale_iri, sale_rec):
        zipcode_iri = _PREFIX["kwgr"][f"zipcodearea.{str(int(sale_rec['ZIP']))}"]
        self.kg.add((zipcode_iri, RDF["type"], _PREFIX["kwg-ont"]["ZipCodeArea"]))
        # self.kg.add((zipcode_iri, RDFS["label"], Literal('ZIP Code ' + str(sale_rec['ZIP']))))
        self.kg.add((zipcode_iri, _PREFIX["ev-ont"]['isSpatialScopeOf'], sale_iri))
        self.kg.add((sale_iri, _PREFIX["ev-ont"]['hasSpatialScope'], zipcode_iri))

    def county_link(self, sale_iri, sale_rec):
        county_iri = rdflib.term.URIRef(sale_rec['county'])
        self.kg.add((county_iri, RDF["type"], _PREFIX["kwg-ont"]["AdministrativeRegion_3"]))
        self.kg.add((county_iri, RDFS["label"], Literal(str(sale_rec['countyName']))))
        self.kg.add((county_iri, _PREFIX["ev-ont"]['isSpatialScopeOf'], sale_iri))
        self.kg.add((sale_iri, _PREFIX["ev-ont"]['hasSpatialScope'], county_iri))

    def link_county_zip_state(self, county_zip):
        for idx, itm in county_zip.iterrows():
            zipcode_iri = rdflib.term.URIRef(itm['zipcode'])
            county_iri = rdflib.term.URIRef(itm['county'])
            state_iri = rdflib.term.URIRef(itm['state'])
            self.kg.add((zipcode_iri, RDF["type"], _PREFIX["kwg-ont"]["ZipCodeArea"]))
            self.kg.add((county_iri, RDF["type"], _PREFIX["kwg-ont"]["AdministrativeRegion_3"]))
            self.kg.add((state_iri, RDF["type"], _PREFIX["kwg-ont"]["AdministrativeRegion_2"]))

            self.kg.add((zipcode_iri, RDFS["label"], Literal(f'{itm["lz"]}')))
            self.kg.add((county_iri, RDFS["label"], Literal(f'{itm["lc"]}')))
            self.kg.add((state_iri, RDFS["label"], Literal(f'{itm["ls"]}')))
            self.kg.add((zipcode_iri, _PREFIX["kwg-ont"]['sfWithin'], county_iri))
            self.kg.add((zipcode_iri, _PREFIX["kwg-ont"]['sfWithin'], state_iri))
            self.kg.add((county_iri, _PREFIX["kwg-ont"]['sfWithin'], state_iri))

            self.kg.add((county_iri, _PREFIX["kwg-ont"]['sfContains'], zipcode_iri))
            self.kg.add((state_iri, _PREFIX["kwg-ont"]['sfContains'], zipcode_iri))
            self.kg.add((state_iri, _PREFIX["kwg-ont"]['sfContains'], county_iri))

    def link_zip_state(self, state_zip):
        for idx, itm in state_zip.iterrows():
            zipcode_iri = rdflib.term.URIRef(itm['zipcode'])
            state_iri = rdflib.term.URIRef(itm['state'])
            self.kg.add((zipcode_iri, RDF["type"], _PREFIX["kwg-ont"]["ZipCodeArea"]))
            self.kg.add((state_iri, RDF["type"], _PREFIX["kwg-ont"]["AdministrativeRegion_2"]))

            self.kg.add((zipcode_iri, RDFS["label"], Literal(f'{itm["lz"]}')))
            self.kg.add((state_iri, RDFS["label"], Literal(f'{itm["ls"]}')))

            self.kg.add((zipcode_iri, _PREFIX["kwg-ont"]['sfWithin'], state_iri))
            self.kg.add((state_iri, _PREFIX["kwg-ont"]['sfContains'], zipcode_iri))

    def triplify_evont(self, vin8):
        for idx, ev_itm in vin8.iterrows():
            print(idx)
            ev_iri = _PREFIX['evr'][f'evproduct.{ev_itm["VIN_Key"]}']
            self.kg.add((ev_iri, RDF["type"], _PREFIX['ev-ont'][ev_abbr]))
            self.kg.add((ev_iri, RDFS["label"], Literal(f'{ev_itm["Vehicle Name"]}')))

            fuel_iri = _PREFIX['evr'][f'technology.{ev_itm["Technology"]}']
            self.kg.add((fuel_iri, RDF["type"], _PREFIX['ev-ont']["Technology"]))
            self.kg.add((fuel_iri, RDFS["label"], Literal(f'{ev_itm["Technology"]}')))
            self.kg.add((ev_iri, _PREFIX["ev-ont"]["isWithTechnology"], fuel_iri))

            # add model year
            self.kg.add((ev_iri, _PREFIX["ev-ont"]["hasModelYear"],
                         Literal(ev_itm["Model Year"], datatype=XSD["gYear"])))

            # add make type
            make_iri = _PREFIX['evr'][f'maketype.{ev_itm["Make"].replace(" ", "-")}']
            self.kg.add((make_iri, RDF["type"], _PREFIX['ev-ont']["MakeType"]))
            self.kg.add((make_iri, RDFS["label"], Literal(f'{ev_itm["Make"]}')))
            # add model type
            # model_str = str(ev_itm["Model"]).replace(" ", "-").replace('\'', '')
            model_iri = _PREFIX['evr'][f'modeltype.{str(ev_itm["Model"]).replace(" ", "-")}']
            self.kg.add((model_iri, RDF["type"], _PREFIX['ev-ont']["ModelType"]))
            self.kg.add((model_iri, RDFS["label"], Literal(f'{ev_itm["Model"]}')))

            self.kg.add((ev_iri, _PREFIX["ev-ont"]["hasMakeType"], make_iri))
            self.kg.add((ev_iri, _PREFIX["ev-ont"]["hasModelType"], model_iri))

            # add usecase type
            use_iri = _PREFIX['evr'][f'usecase.{str(ev_itm["Vehicle Use Case"]).replace(" ", "-")}']
            self.kg.add((use_iri, RDF["type"], _PREFIX['ev-ont']["UseCase"]))
            self.kg.add((use_iri, RDFS["label"], Literal(f'{ev_itm["Vehicle Use Case"]}')))
            self.kg.add((ev_iri, _PREFIX["ev-ont"]["hasVehicleUseCase"], use_iri))

            # add duty type
            duty_iri = _PREFIX['evr'][f'dutytype.{ev_itm["Vehicle Category"].split(" ")[0]}']
            self.kg.add((duty_iri, RDF["type"], _PREFIX['ev-ont']["DutyType"]))
            self.kg.add((duty_iri, RDFS["label"], Literal(f'{ev_itm["Vehicle Category"]}')))
            self.kg.add((ev_iri, _PREFIX["ev-ont"]["hasVehicleDutyType"], duty_iri))

            # add weight level
            weight_iri = _PREFIX['evr'][
                f'weightlevel.{ev_itm["Vehicle Class"].split(":")[0].replace(" ", "-")}']
            self.kg.add((weight_iri, RDF["type"], _PREFIX['ev-ont']["WeightLevel"]))
            self.kg.add((weight_iri, RDFS["label"], Literal(f'{ev_itm["Vehicle Class"]}')))
            self.kg.add((ev_iri, _PREFIX["ev-ont"]["hasVehicleWeightLevel"], weight_iri))

            # add manufacturer
            manu_iri = _PREFIX['evr'][
                f'manufacturer.{str(ev_itm["Vehicle Manufacturer"]).replace(" ", "-")}']
            self.kg.add((manu_iri, RDF["type"], _PREFIX['ev-ont']["Manufacturer"]))
            self.kg.add((manu_iri, RDFS["label"], Literal(f'{ev_itm["Vehicle Manufacturer"]}')))
            self.kg.add((ev_iri, _PREFIX["ev-ont"]["hasManufacturer"], manu_iri))

            if assert_existence(ev_itm["DC"]):
                connectortype_iri = _PREFIX["evr"][f"connectortype.{ev_itm['DC']}"]
                self.kg.add((connectortype_iri, RDF["type"], _PREFIX["ev-ont"]['ConnectorType']))
                self.kg.add((connectortype_iri, RDFS["label"], Literal(ev_itm['DC'])))
                self.kg.add((ev_iri, _PREFIX["ev-ont"]["hasMatchableConnectorType"], connectortype_iri))
                chargertype_iri = _PREFIX["evr"]['chargertype.DCFastCharger']
                self.kg.add((ev_iri, _PREFIX["ev-ont"]["hasMatchableChargerType"], chargertype_iri))
            if ev_itm["Model"] != "Roadster":
                l2connector_iri = _PREFIX["evr"][f"connectortype.J1772"]
                l2chargertype_iri = _PREFIX["evr"][f'chargertype.Level2Charger']
                self.kg.add((ev_iri, _PREFIX["ev-ont"]["hasMatchableConnectorType"], l2connector_iri))
                self.kg.add((ev_iri, _PREFIX["ev-ont"]["hasMatchableChargerType"], l2chargertype_iri))

        print('...')

    def triplify_state_regis(self, state_reg_df, state_abbr):
        ev_groups = state_reg_df.groupby(['VIN Prefix', "VIN Model Year", "ZIP Code", "snapshot_year"])
        for ix, ev_group in ev_groups:
            # print(ev_group['snapshot_year'].iloc[0])
            # add zipcode iri
            zipcode = ev_group['ZIP Code'].iloc[0]
            if type(zipcode) is not str:
                zipcode = "%05d" % zipcode

            zipcode_iri = _PREFIX["kwgr"][f"zipcodearea.{str(zipcode)}"]
            self.kg.add((zipcode_iri, RDF["type"], _PREFIX["kwg-ont"]["ZipCodeArea"]))
            self.kg.add((zipcode_iri, RDFS["label"], Literal('zip code ' + str(zipcode))))

            # add ev registration group
            group_uni_str = ev_group["VIN Prefix"].iloc[0] + ev_group["VIN Model Year"].iloc[0] + "-" \
                            + ev_group["snapshot_year"].iloc[0] + "-" + str(zipcode)

            evgroup_iri = _PREFIX['evr'][f'evgroup.{group_uni_str}']
            self.kg.add(
                (evgroup_iri, RDF["type"], _PREFIX['ev-ont']["ElectricVehicleRegistrationCollection"]))

            if ("Make" in ev_group.keys()) and ("Model" in ev_group.keys()):
                vehicle_name = ev_group.iloc[0]["Make"] + " " + ev_group.iloc[0]["Model"]

            elif "Vehicle Name" in ev_group.keys():
                vehicle_name = ev_group.iloc[0]["Vehicle Name"]
            # print(f'{vehicle_name} Registration in {ev_group.iloc[0]["snapshot_year"]}')
            self.kg.add((evgroup_iri, RDFS["label"], Literal(f'{vehicle_name} '
                                                             f'Registration in {state_abbr}-{str(zipcode)}-'
                                                             f'{ev_group.iloc[0]["snapshot_year"]}')))

            # add link to ev product information
            ev_iri = _PREFIX['evr'][
                f'evproduct.{ev_group["VIN Prefix"].iloc[0] + ev_group["VIN Model Year"].iloc[0]}']

            self.kg.add((evgroup_iri, _PREFIX["ev-ont"]["hasProductInfo"], ev_iri))
            self.kg.add((evgroup_iri, _PREFIX["ev-ont"]["hasAmount"], Literal(ev_group.shape[0])))
            self.kg.add((evgroup_iri, _PREFIX["ev-ont"]["hasTemporalScope"],
                         Literal(str(ev_group['snapshot_year'].iloc[0]),
                                 datatype=XSD["gYear"])))
            self.kg.add((evgroup_iri, _PREFIX["ev-ont"]["hasSpatialScope"], zipcode_iri))

            zipcode_ev_iri = _PREFIX["evr"][f"zipcodearea.{str(zipcode)}"]
            self.kg.add((evgroup_iri, _PREFIX["ev-ont"]['hasSpatialScope'], zipcode_ev_iri))


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


def read_file(f_path):
    p1 = re.compile(r'[(](.*?)[)]', re.S)
    if f_path.split('.')[1] == 'csv':
        state_reg = pd.read_csv(f_path)
    else:
        state_reg = pd.read_excel(f_path)

    state_reg['snapshot_date'] = state_reg['DMV Snapshot'].apply(lambda x: re.findall(p1, x)[0])
    state_reg['snapshot_month'] = state_reg['snapshot_date'].apply(
        lambda x: x.split('/')[0])
    state_reg['snapshot_day'] = state_reg['snapshot_date'].apply(
        lambda x: x.split('/')[1])
    state_reg['snapshot_year'] = state_reg['snapshot_date'].apply(
        lambda x: x.split('/')[2])

    state_reg.dropna(subset=['VIN Prefix', "VIN Model Year", "ZIP Code", "snapshot_date"],
                     inplace=True)
    return state_reg


def extract_regis_data(state_reg, state):
    groups = state_reg.groupby(["snapshot_year"])
    valid_date_ls = []
    for ix, group in groups:
        # print(ix)
        count_df = group.groupby('snapshot_date').count().sort_values(by="DMV ID")
        index_ls = count_df.index
        valid_date = index_ls[-1]
        valid_date_ls.append(valid_date)
        # print('...')

    cleaned_reg_df = state_reg[state_reg['snapshot_date'].isin(valid_date_ls)]
    cleaned_reg_df.to_excel(f'EVRegData/cleaned_reg/{state}.xlsx')
    # return cleaned_reg_df


root_path = "C:/Users/yanlin93/Work/to_be_done/QE/KG_Projects/EV/triplify_EV"


def main():
    # files = "EVRegData/state_reg/co_ev_registrations_public.csv"
    # co = pd.read_csv(files)

    vin8 = pd.read_excel(os.path.join(root_path, "EVRegData/vin8.xlsx"))
    county_zip = pd.read_csv("EVRegData/county_zip_state.csv")
    state_zip = pd.read_csv("EVRegData/zip_state.csv")
    evr = EVReg()
    evr.triplify_evont(vin8)

    for root, dirs, files in os.walk(os.path.join(root_path, 'EVRegData/cleaned_reg'), topdown=False):
        for name in files:
            state_file = os.path.join(root, name)
            print(state_file)
            state_reg = read_file(state_file)
            print('...')
            # extract_regis_data(state_reg, name[0:2])
            evr.triplify_state_regis(state_reg, name[0:2])

    evr.link_county_zip_state(county_zip)
    evr.link_zip_state(state_zip)
    evr_ttl = "{}/ev_registration_cleaned.ttl".format('./EVRegData/')
    evr.kg.serialize(evr_ttl, format='turtle')

    # charger = pd.read_excel("C:/Users/yanlin93/Work/to_be_done/QE/KG_Projects/"
    #                         "EV/triplify_EV/EVRegData/nj_ev_registrations_public.xlsx")
    # uni_charger = charger.drop_duplicates(subset=["VIN Prefix"], keep='first')
    # uni_charger = pd.DataFrame(uni_charger, columns=["VIN Prefix", "DC"])
    # vin8 = vin8.merge(uni_charger, how='left', left_on="VIN Prefix", right_on="VIN Prefix")
    # vin8.to_excel("C:/Users/yanlin93/Work/to_be_done/QE/KG_Projects/"
    #               "EV/triplify_EV/EVRegData/vin8.xlsx")

    # evr.triplify_state_regis(nj)
    print('...')


if __name__ == "__main__":
    main()
