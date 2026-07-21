#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
KnowledgeGraph definitions.
see copyright/license https://github.com/DerwenAI/xandergraph/README.md
"""

import pathlib

import rdflib

from .ottr import OttrGenerator, OttrInstances


class KnowledgeGraph:
    """
Represents a knowledge graph, with accessors for both the `RDFlib`
semantic graph and the `NetworkX` property graph.
    """
    def __init__ (
        self,
        *,
        ns: dict[ str, str ] = {},
        ) -> None:
        """
Constructor.
        """
        self.graph: rdflib.Graph = rdflib.Graph()

        for prefix, ns_uri in ns.items():
            self.graph.bind(prefix, rdflib.Namespace(ns_uri))

        self.ottr_generator: OttrGenerator = OttrGenerator()


    def load_stottr (
        self,
        stottr_path: pathlib.Path,
        ) -> rdflib.Graph:
        """
Define and load the OTTR templates.
        """
        with open(stottr_path, "r", encoding = "utf-8") as fp:
            stottr_template: str = fp.read().strip()

            self.ottr_generator.load_templates(
                stottr_template,
                format = "stottr",
            )


    def gen_ottr_rdf (
        self,
        rdf_data: str,
        ) -> rdflib.Graph:
        """
Generate RDF triples based on applying the given text data to the
loaded OTTR templates.
        """
        instances: OttrInstances = self.ottr_generator.instanciate(
            rdf_data,
            format = "stottr",
        )

        for s, p, o in instances.execute(as_nt = False):
            self.graph.add((s, p, o))
