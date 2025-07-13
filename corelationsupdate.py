import networkx as nx
import json
import itertools
import numpy as np
import matplotlib.pyplot as plt
import nltk
import configparser
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
from sklearn.ensemble import IsolationForest
from openai import OpenAI
from datetime import datetime

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('averaged_perceptron_tagger')

# Load configuration
def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['API_KEYS'].get('openai_api_key', None)

class DataCorrelation:
    def __init__(self):
        self.graph = nx.Graph()
        self.anomaly_detector = IsolationForest(contamination=0.1)
        self.openai_api_key = load_config()
        self.openai_client = OpenAI(api_key=self.openai_api_key) if self.openai_api_key else None
    
    def add_data_point(self, entity, data):
        """Add a data point to the graph."""
        self.graph.add_node(entity, **data)
    
    def add_relationship(self, entity1, entity2, relation):
        """Create a relationship between two entities."""
        self.graph.add_edge(entity1, entity2, relation=relation)
    
    def find_patterns(self):
        """Identify patterns in the data using graph algorithms."""
        cliques = list(nx.find_cliques(self.graph))
        communities = list(nx.community.greedy_modularity_communities(self.graph))
        return {
            "cliques": cliques,
            "communities": [list(community) for community in communities]
        }
    
    def detect_anomalies(self):
        """Use AI-based anomaly detection to find outliers in the data."""
        features = []
        entities = list(self.graph.nodes(data=True))
        for _, data in entities:
            features.append([hash(str(value)) % 1000 for value in data.values()])
        
        if len(features) < 2:
            return "Not enough data for anomaly detection."
        
        features = np.array(features)
        self.anomaly_detector.fit(features)
        predictions = self.anomaly_detector.predict(features)
        
        anomalies = [entities[i][0] for i, pred in enumerate(predictions) if pred == -1]
        return anomalies
    
    def correlate_events(self, event_data):
        """Perform timeline-based event correlation."""
        event_data.sort(key=lambda x: x["timestamp"])
        correlations = []
        for i in range(len(event_data) - 1):
            if event_data[i]["actor"] == event_data[i + 1]["actor"]:
                correlations.append((event_data[i], event_data[i + 1]))
        return correlations
    
    def extract_entities(self, text):
        """Extract named entities using NLTK."""
        words = word_tokenize(text)
        pos_tags = pos_tag(words)
        chunks = ne_chunk(pos_tags)
        entities = {}
        for chunk in chunks:
            if isinstance(chunk, Tree):
                entity_name = " ".join(c[0] for c in chunk)
                entity_type = chunk.label()
                entities[entity_name] = entity_type
        return entities
    
    def analyze_text_with_openai(self, text):
        """Use OpenAI API to analyze text for deeper insights."""
        if not self.openai_client:
            return "OpenAI API key not configured."
        
        response = self.openai_client.Completion.create(
            model="text-davinci-003",
            prompt=f"Extract key insights from this text: {text}",
            max_tokens=100
        )
        return response.choices[0].text.strip()
    
    def generate_report(self, filename="correlation_report.txt"):
        """Generate an automated report with detected patterns and anomalies."""
        report_content = f"Data Correlation Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report_content += "\nPatterns Identified:\n" + json.dumps(self.find_patterns(), indent=4)
        report_content += "\nAnomalies Detected:\n" + json.dumps(self.detect_anomalies(), indent=4)
        
        with open(filename, "w") as f:
            f.write(report_content)
        return f"Report saved as {filename}"
    
    def visualize_graph(self):
        """Visualize the data correlation graph using Matplotlib."""
        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10)
        edge_labels = nx.get_edge_attributes(self.graph, 'relation')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)
        plt.title("Data Correlation Graph")
        plt.show()
    
    def export_graph(self, filename="correlation_graph.json"):
        """Export the graph data as JSON."""
        data = nx.node_link_data(self.graph)
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
    
# Example Usage
if __name__ == "__main__":
    correlator = DataCorrelation()
    correlator.add_data_point("User1", {"email": "user1@example.com", "ip": "192.168.1.1"})
    correlator.add_data_point("User2", {"email": "user2@example.com", "ip": "192.168.1.2"})
    correlator.add_relationship("User1", "User2", "shared_network")
    
    print("Patterns Identified:", correlator.find_patterns())
    print("Anomalies Detected:", correlator.detect_anomalies())
    print("Extracted Entities:", correlator.extract_entities("John Doe lives in New York and works at Google."))
    print("AI Analysis:", correlator.analyze_text_with_openai("John Doe has been involved in multiple transactions across different locations."))
    print(correlator.generate_report())
    
    correlator.visualize_graph()
    correlator.export_graph()
