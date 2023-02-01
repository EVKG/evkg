# EVKG
This is the repository for the paper "EVKG: An Interlinked and Interoperable Electric Vehicle Knowledge Graph for Smart Transportation System", which is submitted to TGIS.
## About this project
In this work, we develop an EV-centric knowledge graph, called EVKG, that serves as an interlinked, cross-domain, scalable, and open data repository to help pace toward more smart EV knowledge management system. Meanwhile, this work will provide an ontology for various EV-related knowledge. which enables rigorous logical interpretation and machine-actionability. With the proposed ontology, EVKG would enable an effective integration of critical spatial and semantic information of electric vehicles including the EV charging infrastructures, the electricity transmission network, and the electric vehicle adoptions at different spatial scales.
## Data Sources 
Our graph is generated based on mainly four repositories: 
* The EV registration records from the Atlas EV Hub:  https://www.atlasevhub.com/materials/state-ev-registration-data/#data
* The electric power transmission network data across the U.S. from the Homeland Infrastructure Foundation Level Database (HIFLD): https://hifld-geoplatform.opendata.arcgis.com/datasets/geoplatform::electric-power-transmission-lines/
* The compatible charger types and connector types from the public repository of EVS pecifications: https://www.evspecifications.com/
* The road network from KnowWhereGraph: https://www.knowwheregraph.org/
* The charging infrastructure: https://afdc.energy.gov/fuels/electricity_locations.html#/find/nearest?fuel=ELEC
## Ontology
<p align="center">
    <img src="https://github.com/EVKG/evkg/blob/main/ontology.png" alt="framework" >
</p>

## Competency Questions and Exemplary Queries
* Q1
```
select DISTINCT ?lev where { 
	?ev a ev-ont:ElectricVehicleProduct.
    	?ev ev-ont:hasMatchableConnectorType evr:connectortype.CHAdeMO.
    	?ev rdfs:label ?lev.
}
```
* Q2
```
select * where { 
	?county a kwg-ont:AdministrativeRegion_3.
    	?county rdfs:label "King".
    	?zipcode a kwg-ont:ZipCodeArea.
    	?zipcode kwg-ont:sfWithin ?county.
    
   	?road a kwg-ont:RoadSegment.
    	?road kwg-ont:sfWithin ?county.
    
    	?transline a ev-ont:TransmissionLine.
    	?transline kwg-ont:sfCrosses ?zipcode.
	
    	?char_station a ev-ont:ChargingStation.
    	?char_station kwg-ont:sfWithin ?zipcode.
    
    	?substation a ev-ont:Substation.
    	?substation kwg-ont:sfWithin ?zipcode.
    
    	?powerplant a ev-ont:PowerPlant.
    	?powerplant kwg-ont:sfWithin ?zipcode.
}

```
* Q3
```
SELECT Distinct ?co ?station ?sWKT
WHERE
{
    {    
        ?zipcode a kwg-ont:ZipCodeArea.
        ?zipcode rdfs:label "zip code 95814".
        ?station a ev-ont:PublicChargingStation.
        ?station kwg-ont:sfWithin ?zipcode.
        ?station ev-ont:hosts ?chargerCollection. 
        ?chargerCollection ev-ont:hasConnectorType ?co.
        ?station ev-ont:hasOperatingHours "24 hours daily  ".
        ?station ev-ont:isUnderChargingNetwork evr:chargingnetwork.ChargePointNetwork.
        ?station geo:hasGeometry ?sGeom .
        ?sGeom geo:asWKT ?sWKT .
        
        ?ev a ev-ont:ElectricVehicleProduct.
        ?ev ev-ont:hasModelType ?model.
        ?ev rdfs:label "Nissan Leaf".
        ?ev ev-ont:hasModelYear "2021"^^xsd:gYear.
        ?ev ev-ont:hasMatchableConnectorType ?co.
        ?co rdfs:label ?co_name.
        VALUES ?co_name{"CHAdeMO" "J1772COMBO" "TESLA"}

    }
}
```
* Q4 The temporal variation of the DCFC-EVSE number
```
select ?co_name ?year (SUM(?evtg_n) AS ?DC_EV_reg_n) where{
select Distinct ?evtg ?evtg_n ?co_name ?year where { 
	?zip a ev-ont:ZipCodeArea.
    	?zip rdfs:label ?lz.
    	?state a ev-ont:State.
    	?state rdfs:label "New Jersey".
    	?state ev-ont:sfContains ?zip.

	?evtg a ev-ont:ElectricVehicleRegistrationCollection.
    	?evtg ev-ont:hasAmount ?evtg_n.
    	?evtg ev-ont:hasTemporalScope ?year.
    	?evtg ev-ont:hasSpatialScope ?zip.
    	?evtg ev-ont:hasProductInfo ?ev.
    	?ev ev-ont:hasMatchableConnectorType ?co.
   	?co rdfs:label ?co_name.
    	VALUES ?co_name{"TESLA" "CHAdeMO" "J1772COMBO"}
}}  Group By ?co_name ?year

```
The temporal variation of the number of EVs with fast charging capability
```
select ?co_name ?year (SUM(?evtg_n) AS ?DC_EV_reg_n) where{
select Distinct ?evtg ?evtg_n ?co_name ?year where { 
	?zip a ev-ont:ZipCodeArea.
    	?zip rdfs:label ?lz.
    	?state a ev-ont:State.
    	?state rdfs:label "New Jersey".
    	?state ev-ont:sfContains ?zip.

	?evtg a ev-ont:ElectricVehicleRegistrationCollection.
    	?evtg ev-ont:hasAmount ?evtg_n.
    	?evtg ev-ont:hasTemporalScope ?year.
    	?evtg ev-ont:hasSpatialScope ?zip.
    	?evtg ev-ont:hasProductInfo ?ev.
    	?ev ev-ont:hasMatchableConnectorType ?co.
    	?co rdfs:label ?co_name.
    	VALUES ?co_name{"TESLA" "CHAdeMO" "J1772COMBO"}
}}  Group By ?co_name ?year
```
* Q5 a)
```
SELECT DISTINCT ?zipcode (SUM(?regNum) AS ?zipRegNum)
WHERE{
        ?zipcode a kwg-ont:ZipCodeArea.
        ?state a kwg-ont:AdministrativeRegion_2.
        ?state rdfs:label "New Jersey".
        ?state kwg-ont:sfContains ?zipcode.
        ?reggroup a ev-ont:ElectricVehicleRegistrationCollection.
        ?reggroup ev-ont:hasSpatialScope ?zipcode.
        ?reggroup ev-ont:hasTemporalScope "2021"^^xsd:gYear.
        ?reggroup ev-ont:hasProductInfo ?ev. 
        ?reggroup ev-ont:hasAmount ?regNum.
        ?ev ev-ont:hasMatchableConnectorType evr:connectortype.J1772COMBO.
	} GROUP BY ?zipcode
}

```
* Q5 b)
```
SELECT ?zipcpde ?zipChargerNum ?zipRegNum (?zipChargerNum/?zipRegNum AS ?ratio)
        WHERE{
		### part 1 the EVSE number at zip code level
            	{SELECT DISTINCT ?zipcode (SUM(?chargerNum) AS ?zipChargerNum)
                 WHERE{
                    ?zipcode a kwg-ont:ZipCodeArea.
                    ?state a kwg-ont:AdministrativeRegion_2.
                    ?state rdfs:label "New Jersey".
                    ?zipcode kwg-ont:sfWithin ?state.
                    ?station a ev-ont:ChargingStation.
                    ?station kwg-ont:sfWithin ?zipcode.
                    ?station ev-ont:hosts ?chargerCollection. 
                    ?chargerCollection ev-ont:hasAmount ?chargerNum.
                    ?chargerCollection ev-ont:hasConnectorType evr:connectortype.J1772COMBO.
                    } GROUP BY ?zipcode
                }
		### part 2 the registration number at zip code level
                {SELECT DISTINCT ?zipcode (SUM(?regNum) AS ?zipRegNum)
                 WHERE{
                       ?zipcode a kwg-ont:ZipCodeArea.
                       ?state a kwg-ont:AdministrativeRegion_2.
                       ?state rdfs:label "New Jersey".
                       ?state kwg-ont:sfContains ?zipcode.
                       ?reggroup a ev-ont:ElectricVehicleRegistrationCollection.
                       ?reggroup ev-ont:hasSpatialScope ?zipcode.
                      ?reggroup ev-ont:hasTemporalScope "2021"^^xsd:gYear.
                       ?reggroup ev-ont:hasProductInfo ?ev. 
                       ?reggroup ev-ont:hasAmount ?regNum.
                       ?ev ev-ont:hasMatchableConnectorType evr:connectortype.J1772COMBO.
                        } GROUP BY ?zipcode
                }
}
```
* Q6
```
** Condition 1: Average charging resource less than 0.1
SELECT ?zipcode ?transline ?ratio 
WHERE{
    {
        FILTER(?ratio < 0.1)
    }

    {
    ... Queries from Q5...
    }
}
```
```
** Condition 2: Electric vehicle registration more than 98
SELECT ?zipcode ?transline 
WHERE{
    {
        FILTER(?zipRegNum>98)
    }

    {
    ... Queries from Q5 part 2...
    }
}
```
# Code usage
Codes in this project can be grouped into two catgeories: 1) codes to generate the RDF graph (code is in python 3)

* To triplify each of the modules, please see the codes in ```./scripts```. 

# License
This repository, and associated codes, are distributed under the MIT License. See LICENSE for more information.

