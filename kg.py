#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test usage of pyOTTR
"""

import pathlib
import sys

from icecream import ic
import xandergraph as xg
import pyshacl
import rdflib


if __name__ == "__main__":
    kg: xg.KnowledgeGraph = xg.KnowledgeGraph(
        ns = {
            "bwyd": "https://github.com/DerwenAI/bwyd/wiki/ns#",
        },
    )

    kg.load_stottr(pathlib.Path("bwyd.stottr"))

    ## generate models from the data
    rdf_data: str = """
@prefix bwyd:     <https://github.com/DerwenAI/bwyd/wiki/ns#> .

bwyd:Recipe(
  <urn:bwyd:pacoid:panna_cotta> ,
  "Panna Cotta"@en ,
  "A light, creamy dessert which pairs with so many fruits"@en ,
  <https://spdx.org/licenses/CC-BY-NC-SA-4.0> ,
  <https://derwen.ai/paco> ,
  "2022-07-16"^^xsd:dateTime ,
) .

bwyd:RecipeImage(
  <urn:bwyd:pacoid:panna_cotta> ,
  <https://www.instagram.com/p/CgGYEZFL7Dx/> ,
) .

bwyd:RecipeSource(
  <urn:bwyd:pacoid:panna_cotta> ,
  <https://www.thekitchn.com/how-to-make-panna-cotta-cooking-lessons-from-the-kitchn-200070> ,
) .

bwyd:RecipeSource(
  <urn:bwyd:pacoid:panna_cotta> ,
  <https://mytastefulrecipes.com/almond-milk-panna-cotta-recipe/> ,
) .

bwyd:RecipeDepends(
  <urn:bwyd:pacoid:panna_cotta> ,
  <urn:bwyd:pacoid:panna_cotta/closure_1> ,
) .

bwyd:RecipeDepends(
  <urn:bwyd:pacoid:panna_cotta> ,
  <urn:bwyd:pacoid:panna_cotta/closure_2> ,
) .

bwyd:Closure(
  <urn:bwyd:pacoid:panna_cotta/closure_1> ,
  "mix the cream"@en ,
  "Prepare the cream filling"@en ,
) .

bwyd:ClosureConsumes(
  <urn:bwyd:pacoid:panna_cotta/closure_1> ,
  <urn:bwyd:ingredient:cream> ,
) .

bwyd:ClosureConsumes(
  <urn:bwyd:pacoid:panna_cotta/closure_1> ,
  <urn:bwyd:ingredient:granulated_sugar> ,
) .

bwyd:ClosureProduces(
  <urn:bwyd:pacoid:panna_cotta/closure_1> ,
  <urn:bwyd:pacoid:panna_cotta/closure_1/product/filling> ,
) .


bwyd:Closure(
  <urn:bwyd:pacoid:panna_cotta/closure_2> ,
  "chill in containers"@en ,
  "Fill the ramekins and chill"@en ,
) .

bwyd:ClosureConsumes(
  <urn:bwyd:pacoid:panna_cotta/closure_2> ,
  <urn:bwyd:pacoid:panna_cotta/closure_1/product/filling> .
) .

bwyd:ClosureProduces(
  <urn:bwyd:pacoid:panna_cotta/closure_2> ,
  <urn:bwyd:pacoid:product:panna_cotta> .
) .
    """.strip()

    kg.gen_ottr_rdf(rdf_data)

#  rdfs:subClassOf <urn:bwyd:subject:dessert> , <urn:bwyd:subject:pudding> ;
#  skos:related <urn:bwyd:keyword:italian> ;


    ## save to a file

    ttl_path: pathlib.Path = pathlib.Path("corpus.ttl")

    with open(ttl_path, "w", encoding = "utf-8") as fp:
        ttl: str = kg.graph.serialize(format = "turtle")
        fp.write(ttl)

    ## SHACL validation
    data_graph = "corpus.ttl"
    shacl_graph = "shapes.ttl"
    ont_graph = "domain.ttl"

    graph: rdflib.Graph = rdflib.Graph()
    graph.parse(data_graph)
    graph.parse(shacl_graph)
    graph.parse(ont_graph)

    #sys.exit(0)

    r = pyshacl.validate(
        data_graph,
        shacl_graph = shacl_graph,
        ont_graph = ont_graph,
        inference = "rdfs",
        abort_on_first = False,
        allow_infos = False,
        allow_warnings = False,
        meta_shacl = False,
        advanced = False,
        js = False,
        debug = False,
    )

    conforms, results_graph, results_text = r
    ic(conforms, results_graph, results_text)
