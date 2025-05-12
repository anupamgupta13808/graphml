"""
Core conversion logic for the Graph ML File Converter.
"""

import networkx as nx
from typing import Dict, Any
import json

class GraphConverter:
    """Handles conversion between different graph file formats."""

    def __init__(self):
        """Initialize the converter."""
        self.supported_input_formats = {
            "graphml": self._read_graphml,
            "gml": self._read_gml,
            "json": self._read_json
        }
        self.supported_output_formats = {
            "python": self._write_python,
            "java": self._write_java
        }

    def convert(self, input_file: str, output_file: str,
                input_format: str, output_format: str) -> None:
        """
        Convert a graph file from one format to another.

        Args:
            input_file: Path to the input file
            output_file: Path to the output file
            input_format: Format of the input file
            output_format: Desired output format
        """
        if input_format not in self.supported_input_formats:
            raise ValueError(f"Unsupported input format: {input_format}")
        if output_format not in self.supported_output_formats:
            raise ValueError(f"Unsupported output format: {output_format}")

        # Read the input file
        graph = self.supported_input_formats[input_format](input_file)

        # Write the output file
        self.supported_output_formats[output_format](graph, output_file)

    def _read_graphml(self, file_path: str) -> nx.Graph:
        """Read a GraphML file."""
        return nx.read_graphml(file_path)

    def _read_gml(self, file_path: str) -> nx.Graph:
        """Read a GML file."""
        return nx.read_gml(file_path)

    def _read_json(self, file_path: str) -> nx.Graph:
        """Read a JSON file."""
        with open(file_path, 'r') as f:
            data = json.load(f)
        return nx.node_link_graph(data)

    def _write_python(self, graph: nx.Graph, file_path: str) -> None:
        """Write a Python file with NetworkX graph code."""
        code = self._generate_python_code(graph)
        with open(file_path, 'w') as f:
            f.write(code)

    def _write_java(self, graph: nx.Graph, file_path: str) -> None:
        """Write a Java file with JGraphT graph code."""
        code = self._generate_java_code(graph)
        with open(file_path, 'w') as f:
            f.write(code)

    def _generate_python_code(self, graph: nx.Graph) -> str:
        """Generate Python code for the graph."""
        code = [
            "import networkx as nx",
            "",
            "# Create a new graph",
            "G = nx.Graph()",
            "",
            "# Add nodes",
        ]

        # Add nodes with attributes
        for node, attrs in graph.nodes(data=True):
            attr_str = ", ".join(f"{k}={repr(v)}" for k, v in attrs.items())
            if attr_str:
                code.append(f"G.add_node({repr(node)}, {attr_str})")
            else:
                code.append(f"G.add_node({repr(node)})")

        code.append("")
        code.append("# Add edges")

        # Add edges with attributes
        for u, v, attrs in graph.edges(data=True):
            attr_str = ", ".join(f"{k}={repr(v)}" for k, v in attrs.items())
            if attr_str:
                code.append(f"G.add_edge({repr(u)}, {repr(v)}, {attr_str})")
            else:
                code.append(f"G.add_edge({repr(u)}, {repr(v)})")

        return "\n".join(code)

    def _generate_java_code(self, graph: nx.Graph) -> str:
        """Generate Java code for the graph."""
        code = [
            "import org.jgrapht.Graph;",
            "import org.jgrapht.graph.DefaultWeightedEdge;",
            "import org.jgrapht.graph.SimpleWeightedGraph;",
            "import java.util.HashMap;",
            "import java.util.Map;",
            "",
            "public class GeneratedGraph {",
            "    public static Graph<String, DefaultWeightedEdge> createGraph() {",
            "        Graph<String, DefaultWeightedEdge> graph = ",
            "            new SimpleWeightedGraph<>(DefaultWeightedEdge.class);",
            "",
            "        // Add nodes",
        ]

        # Add nodes with attributes
        for node, attrs in graph.nodes(data=True):
            code.append(f"        graph.addVertex(\"{node}\");")
            if attrs:
                code.append("        {")
                code.append("            Map<String, Object> attributes = new HashMap<>();")
                for k, v in attrs.items():
                    if isinstance(v, str):
                        code.append(f"            attributes.put(\"{k}\", \"{v}\");")
                    else:
                        code.append(f"            attributes.put(\"{k}\", {v});")
                code.append("            // Store attributes in your preferred way")
                code.append("        }")

        code.append("")
        code.append("        // Add edges")

        # Add edges with attributes
        for u, v, attrs in graph.edges(data=True):
            code.append(f"        DefaultWeightedEdge edge = graph.addEdge(\"{u}\", \"{v}\");")
            if attrs:
                code.append("        {")
                code.append("            Map<String, Object> attributes = new HashMap<>();")
                for k, v in attrs.items():
                    if isinstance(v, str):
                        code.append(f"            attributes.put(\"{k}\", \"{v}\");")
                    else:
                        code.append(f"            attributes.put(\"{k}\", {v});")
                code.append("            // Store attributes in your preferred way")
                code.append("        }")

        code.extend([
            "",
            "        return graph;",
            "    }",
            "}"
        ])

        return "\n".join(code) 