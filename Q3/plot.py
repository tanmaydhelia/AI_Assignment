import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

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

def monte_carlo_simulation(n_samples=10000):
    """Run Monte Carlo simulation to estimate P(J=yes|A=yes)."""
    count_total = 0
    count_job = 0
    
    for _ in range(n_samples):
        # Evidence: A=yes
        aptitude = 'yes'
        
        # Sample other nodes
        coding = sample_node(P_Coding)
        
        # Sample Grade
        grade_probs = {
            'Good': P_Grade[(aptitude, coding, 'Good')],
            'OK': P_Grade[(aptitude, coding, 'OK')]
        }
        grade = sample_node(grade_probs)
        
        # Sample Job
        job_probs = {
            'yes': P_Job[(grade, 'yes')],
            'no': P_Job[(grade, 'no')]
        }
        job = sample_node(job_probs)
        
        # Count results
        count_total += 1
        if job == 'yes':
            count_job += 1
    
    return count_job / count_total

# Run simulation with different sample sizes
sample_sizes = [1000, 10000, 100000]
for n in sample_sizes:
    prob = monte_carlo_simulation(n)
    print(f"P(J=yes|A=yes) with {n} samples: {prob:.4f}")



def run_multiple_simulations(n_samples, n_runs=30):
    results = []
    for _ in range(n_runs):
        prob = monte_carlo_simulation(n_samples)
        results.append(prob)
    return results

# Modify main code
sample_sizes = [1000, 10000, 100000]
all_results = {n: run_multiple_simulations(n) for n in sample_sizes}

# Create visualization
plt.figure(figsize=(12, 4))

# Plot 1: Convergence
plt.subplot(121)
for n in sample_sizes:
    results = all_results[n]
    mean = np.mean(results)
    ci = stats.norm.interval(0.95, loc=mean, scale=stats.sem(results))
    plt.errorbar(n, mean, yerr=[[mean-ci[0]], [ci[1]-mean]], 
                 fmt='o', capsize=5, label=f'n={n}')

plt.xscale('log')
plt.xlabel('Number of Samples')
plt.ylabel('P(J=yes|A=yes)')
plt.title('Convergence of Probability Estimate')
plt.grid(True)
plt.legend()

# Plot 2: Distribution of estimates
plt.subplot(122)
plt.boxplot([all_results[n] for n in sample_sizes], 
            labels=[f'n={n}' for n in sample_sizes])
plt.ylabel('P(J=yes|A=yes)')
plt.title('Distribution of Probability Estimates')
plt.grid(True)

plt.tight_layout()
plt.show()