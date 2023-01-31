# EVKG
This is the repository for the paper "EVKG: An Interlinked and Interoperable Electric Vehicle Knowledge Graph for Smart Transportation System", which is submitted to TGIS.
## About this project
In this work, inspired by the challenges faced by EV charging systems and recent advancements in KG, we develop an EV-centric knowledge graph, called EVKG, that serves as an interlinked, cross-domain, scalable, and open data repository to help pace toward more smart EV knowledge management system. Meanwhile, this work will provide an ontology for various EV-related knowledge. which enables rigorous logical interpretation and machine-actionability. With the proposed ontology, EVKG would enable an effective integration of critical spatial and semantic information of electric vehicles including the EV charging infrastructures, the electricity transmission network,
and the electric vehicle adoptions at different spatial scales.
## Data Sources 
Our graph is generated based on mainly four repositories: 
* The EV registration records from the Atlas EV Hub
* The electric power transmission network data across the U.S. from the Homeland Infrastructure Foundation Level Database (HIFLD)
* The compatible charger types and connector types from the public repository of EVS pecifications
* The road network from KnowWhereGraph
## Ontology
<p align="center">
    <img src="https://github.com/EVKG/evkg/blob/main/Ontology.pdf" alt="framework" >
</p>

## Competency Questions and Exemplary Queries
* Q1
```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX kwg-ont: <http://stko-kwg.geog.ucsb.edu/lod/ontology/>
PREFIX ev-ont: <http://stko-kwg.geog.ucsb.edu/lod/ev/ontology/>
PREFIX evr: <http://stko-kwg.geog.ucsb.edu/lod/ev/resource/>
select DISTINCT ?l ?r ?lm ?ev_n where { 
    ?o rdfs:label ?l .
    ?o a kwg-ont:ZipCodeArea.
    ?state rdfs:label ?ls .
    ?state a kwg-ont:AdministrativeRegion_2.
    ?o kwg-ont:sfWithin ?state.
    ?r a ev-ont:ElectricVehicleRegistrationCollection.
    ?r ev-ont:hasAmount ?ev_n.
    ?r ev-ont:hasSpatialScope ?o.
    ?r ev-ont:hasProductInfo ?ev.
    ?ev ev-ont:hasMatchableChargerType ?c.
    ?ev ev-ont:hasMakeType ?make.
    ?make rdfs:label ?lm.
    ?cc ev-ont:hasChargerType ?c.
    ?cc ev-ont:hasAmount ?n.
    VALUES (?c) {(evr:chargertype.DCFastCharger)}
    VALUES (?ls) {("New Jersey")}
    VALUES (?lm) {("BMW")}
	}
```
* Q2
* Q3
* 



