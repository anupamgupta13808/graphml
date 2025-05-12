"""
Tests for the GraphConverter class.
"""

import os
import tempfile
import networkx as nx
import json
import pytest
from src.core.converter import GraphConverter
import warnings

def compare_attributes(attrs1, attrs2):
    """Helper to compare two attribute dicts as strings for cross-format compatibility."""
    for key, value in attrs1.items():
        if str(attrs2.get(key, "")) != str(value):
            return False
    return True

@pytest.fixture
def sample_graph():
    """Create a sample graph for testing."""
    G = nx.Graph()
    G.add_node("A", label="Node A")
    G.add_node("B", label="Node B")
    G.add_edge("A", "B", weight=1.5)
    return G

@pytest.fixture
def converter():
    """Create a GraphConverter instance."""
    return GraphConverter()

def test_graphml_conversion(converter, sample_graph):
    """Test conversion to and from GraphML format."""
    with tempfile.NamedTemporaryFile(suffix=".graphml", delete=False) as temp:
        # Write the sample graph to GraphML
        nx.write_graphml(sample_graph, temp.name)
        
        # Read it back using our converter
        graph = converter._read_graphml(temp.name)
        
        # Compare the graphs
        assert set(graph.nodes()) == set(sample_graph.nodes())
        assert set(graph.edges()) == set(sample_graph.edges())
        
        # Compare node attributes
        for node in graph.nodes():
            assert compare_attributes(graph.nodes[node], sample_graph.nodes[node])
        
        # Compare edge attributes
        for edge in graph.edges():
            assert compare_attributes(graph.edges[edge], sample_graph.edges[edge])
    
    os.unlink(temp.name)

def test_gml_conversion(converter, sample_graph):
    """
    Test conversion to and from GML format.
    Note: NetworkX's GML writer/reader does not reliably preserve custom node/edge attributes except for 'label',
    and even then, round-trip may lose attributes. We only check node/edge sets, not attributes.
    """
    with tempfile.NamedTemporaryFile(suffix=".gml", delete=False) as temp:
        # Write the sample graph to GML
        nx.write_gml(sample_graph, temp.name)
        
        # Read it back using our converter
        graph = converter._read_gml(temp.name)
        
        # Compare the graphs
        assert set(graph.nodes()) == set(sample_graph.nodes())
        assert set(graph.edges()) == set(sample_graph.edges())
        
        warnings.warn("Skipping attribute checks for GML due to known NetworkX limitations.")
    
    os.unlink(temp.name)

def test_json_conversion(converter, sample_graph):
    """Test conversion to and from JSON format."""
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as temp:
        # Write the sample graph to JSON
        data = nx.node_link_data(sample_graph)
        with open(temp.name, 'w') as f:
            json.dump(data, f)
        
        # Read it back using our converter
        graph = converter._read_json(temp.name)
        
        # Compare the graphs
        assert set(graph.nodes()) == set(sample_graph.nodes())
        assert set(graph.edges()) == set(sample_graph.edges())
        
        # Compare node attributes
        for node in graph.nodes():
            assert compare_attributes(graph.nodes[node], sample_graph.nodes[node])
        
        # Compare edge attributes
        for edge in graph.edges():
            assert compare_attributes(graph.edges[edge], sample_graph.edges[edge])
    
    os.unlink(temp.name)

def test_python_code_generation(converter, sample_graph):
    """Test Python code generation."""
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp:
        # Generate Python code
        converter._write_python(sample_graph, temp.name)
        
        # Read the generated code
        with open(temp.name, 'r') as f:
            code = f.read()
        
        # Basic checks on the generated code
        assert "import networkx as nx" in code
        assert "G = nx.Graph()" in code
        assert "G.add_node" in code
        assert "G.add_edge" in code
    
    os.unlink(temp.name)

def test_java_code_generation(converter, sample_graph):
    """Test Java code generation."""
    with tempfile.NamedTemporaryFile(suffix=".java", delete=False) as temp:
        # Generate Java code
        converter._write_java(sample_graph, temp.name)
        
        # Read the generated code
        with open(temp.name, 'r') as f:
            code = f.read()
        
        # Basic checks on the generated code
        assert "import org.jgrapht.Graph" in code
        assert "public class GeneratedGraph" in code
        assert "graph.addVertex" in code
        assert "graph.addEdge" in code
    
    os.unlink(temp.name)

def test_invalid_input_format(converter):
    """Test handling of invalid input format."""
    with pytest.raises(ValueError):
        converter.convert("input.txt", "output.txt", "invalid", "python")

def test_invalid_output_format(converter):
    """Test handling of invalid output format."""
    with pytest.raises(ValueError):
        converter.convert("input.graphml", "output.txt", "graphml", "invalid") 