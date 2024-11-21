import numpy as np
from collections import defaultdict

# Define probability tables
P_Aptitude = {'yes': 0.8, 'no': 0.2}
P_Coding = {'yes': 0.5, 'no': 0.5}

# Grade conditional probabilities P(G|A,C)
P_Grade = {
    ('yes', 'yes', 'Good'): 0.9,
    ('yes', 'yes', 'OK'): 0.1,
    ('yes', 'no', 'Good'): 0.7,
    ('yes', 'no', 'OK'): 0.3,
    ('no', 'yes', 'Good'): 0.6,
    ('no', 'yes', 'OK'): 0.4,
    ('no', 'no', 'Good'): 0.3,
    ('no', 'no', 'OK'): 0.7
}

# Job conditional probabilities P(J|G)
P_Job = {
    ('Good', 'yes'): 0.8,
    ('Good', 'no'): 0.2,
    ('OK', 'yes'): 0.2,
    ('OK', 'no'): 0.8
}

def sample_node(probabilities):
    """Sample from a probability distribution."""
    r = np.random.rand()
    cumsum = 0
    for outcome, prob in probabilities.items():
        cumsum += prob
        if r < cumsum:
            return outcome

def monte_carlo_simulation(n_samples=10000, evidence_node='A', evidence_value='yes', query_node='J'):
    """Run Monte Carlo simulation to estimate P(query_node=yes|evidence_node=evidence_value)."""
    count_total = 0
    count_query_yes = 0
    
    for _ in range(n_samples):
        # Set evidence
        if evidence_node == 'A':
            aptitude = evidence_value
        else:
            aptitude = sample_node(P_Aptitude)
        
        if evidence_node == 'C':
            coding = evidence_value
        else:
            coding = sample_node(P_Coding)
        
        # Sample Grade
        grade_probs = {
            'Good': P_Grade[(aptitude, coding, 'Good')],
            'OK': P_Grade[(aptitude, coding, 'OK')]
        }
        grade = sample_node(grade_probs)
        
        if evidence_node == 'G':
            grade = evidence_value
        
        # Sample Job
        job_probs = {
            'yes': P_Job[(grade, 'yes')],
            'no': P_Job[(grade, 'no')]
        }
        job = sample_node(job_probs)
        
        # Count results
        count_total += 1
        if job == 'yes':
            count_query_yes += 1
    
    return count_query_yes / count_total

def get_user_input():
    """Get and validate user input for Bayesian network simulation."""
    # Available nodes and their possible values
    nodes = {
        'A': ['yes', 'no'],
        'C': ['yes', 'no'], 
        'G': ['Good', 'OK'],
        'J': ['yes', 'no']
    }
    
    # Get evidence node
    print("\nAvailable nodes: A (Aptitude), C (Coding), G (Grade), J (Job)")
    evidence_node = input("Enter evidence node (A/C/G/J): ").upper()
    while evidence_node not in nodes:
        print("Invalid node. Please try again.")
        evidence_node = input("Enter evidence node (A/C/G/J): ").upper()
    
    # Get evidence value
    evidence_value = input(f"Enter value for {evidence_node} {nodes[evidence_node]}: ").lower()
    while evidence_value not in nodes[evidence_node]:
        print(f"Invalid value. Choose from: {nodes[evidence_node]}")
        evidence_value = input(f"Enter value for {evidence_node}: ").lower()
    
    # Get query node
    query_node = input("Enter query node (A/C/G/J): ").upper()
    while query_node not in nodes or query_node == evidence_node:
        print("Invalid node or same as evidence. Please try again.")
        query_node = input("Enter query node (A/C/G/J): ").upper()
    
    return evidence_node, evidence_value, query_node

# Get user input and run simulation
evidence_node, evidence_value, query_node = get_user_input()
sample_sizes = [1000, 10000, 100000]

for n_samples in sample_sizes:
    prob = monte_carlo_simulation(n_samples, evidence_node, evidence_value, query_node)
    print(f"\nP({query_node}=yes|{evidence_node}={evidence_value}) with {n_samples} samples: {prob:.4f}")

