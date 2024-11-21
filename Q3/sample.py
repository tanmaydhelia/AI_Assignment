import numpy as np

# Define conditional probabilities
P_Cloudy = 0.5
P_Sprinkler_given_Cloudy = {True: 0.1, False: 0.5}
P_Rain_given_Cloudy = {True: 0.8, False: 0.2}
P_WetGrass_given_Sprinkler_Rain = {
    (True, True): 0.99,
    (True, False): 0.90,
    (False, True): 0.80,
    (False, False): 0.00
}

# Monte Carlo simulation to estimate P(WetGrass=True | Rain=True)
def monte_carlo_simulation(num_samples=10000):
    count_wet_grass_given_rain = 0
    count_rain = 0
    for _ in range(num_samples):
        # Sample Cloudy
        cloudy = np.random.rand() < P_Cloudy
        # Sample Sprinkler given Cloudy
        sprinkler = np.random.rand() < P_Sprinkler_given_Cloudy[cloudy]
        # Sample Rain given Cloudy
        rain = np.random.rand() < P_Rain_given_Cloudy[cloudy]
        # Sample WetGrass given Sprinkler and Rain
        wet_grass = np.random.rand() < P_WetGrass_given_Sprinkler_Rain[(sprinkler, rain)]
        # Check if Rain is True and accumulate counts
        if rain:
            count_rain += 1
        if wet_grass:
            count_wet_grass_given_rain += 1
    # Calculate conditional probability
    if count_rain == 0:
        return 0  # Avoid division by zero
    return count_wet_grass_given_rain / count_rain

# Run simulation
estimated_probability = monte_carlo_simulation()
print(f"Estimated P(WetGrass=True | Rain=True): {estimated_probability}")

