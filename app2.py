import streamlit as st
import numpy as np
import plotly.graph_objs as go

# Define the fitness function
def fitness(phenotype, desired_phenotype):
    return np.exp(-0.1 * (phenotype - desired_phenotype)**2)

# Define the phenotype function
def phenotype(alpha, beta):
    return beta / (alpha + beta)

# Define the fitness landscape function
def fitness_landscape(alpha, beta, desired_phenotype):
    phenotype_val = phenotype(alpha, beta)
    return fitness(phenotype_val, desired_phenotype)

# Define the simulation function
def simulate(generations, alpha_range, beta_range, desired_phenotype):
    phenotypes = []
    alphas = []
    betas = []

    for _ in range(generations):
        alpha = np.random.uniform(*alpha_range)
        beta = np.random.uniform(*beta_range)
        phenotypes.append(phenotype(alpha, beta))
        alphas.append(alpha)
        betas.append(beta)

    return alphas, betas, phenotypes

# Streamlit App
st.title("ODE-NAR G2P Map")

# Explanatory text
st.write("""
## Interactive Evolutionary Dynamics Simulator

This app simulates the evolution of a population where an ODE-NAR system controls the G2P map
By adjusting the parameters on the left, you can explore how different factors od the ODE influence the fitness
landscape and the distribution of phenotypes within the population.

### How it works:

- **Desired Phenotype**: The optimal phenotype value that yields the highest fitness.
- **Population Size**: The number of individuals in each generation.
- **Generations**: The number of cycles of selection to simulate.
- **Alpha Range**: The range of alpha values (decay rates) to consider.
- **Beta Range**: The range of beta values (production rates) to consider.

The 3D plot shows the fitness landscape as a surface, with the current population represented by red points.
You can interact with the plot by rotating and zooming to get different perspectives on the data.
""")


# Streamlit sidebar for parameters
desired_phenotype = st.sidebar.slider("Desired Phenotype", 0.0, 90.0, 10.0)
pop_size = st.sidebar.number_input("Population Size", 10, 1000, 50)
generations = st.sidebar.number_input("Generations", 10, 1000, 100)

lower_alpha = st.sidebar.number_input("Lower Alpha", 0.01, 10.0, 0.01)
upper_alpha = st.sidebar.number_input("Upper Alpha", 0.1, 50.0, 1.0)
alpha_range = (lower_alpha, upper_alpha)

lower_beta = st.sidebar.number_input("Lower Beta", 0.1, 50.0, 0.1)
upper_beta = st.sidebar.number_input("Upper Beta", 1.0, 50.0, 10.0)
beta_range = (lower_beta, upper_beta)

# Running simulation
alphas, betas, phenotypes = simulate(generations, alpha_range, beta_range, desired_phenotype)

# Fitness landscape for Plotly
alpha_vals = np.linspace(alpha_range[0], alpha_range[1], 30)
beta_vals = np.linspace(beta_range[0], beta_range[1], 30)
alpha_grid, beta_grid = np.meshgrid(alpha_vals, beta_vals)
fitness_values = fitness_landscape(alpha_grid, beta_grid, desired_phenotype)

# Create Plotly figure
fig = go.Figure(data=[go.Surface(z=fitness_values, x=alpha_grid, y=beta_grid, colorscale='Viridis')])

# Add scatter plot for phenotypes
fig.add_trace(go.Scatter3d(x=alphas, y=betas, z=fitness(np.array(phenotypes), desired_phenotype),
                           mode='markers', marker=dict(size=5, color='green')))

# Update layout for a better look
fig.update_layout(
    title='Evolutionary Simulation',
    autosize=True,
    scene=dict(
        xaxis_title='Alpha',
        yaxis_title='Beta',
        zaxis_title='Fitness',
        aspectratio=dict(x=1, y=1, z=0.7)
    )
)

# Show the figure in the Streamlit app
st.plotly_chart(fig)
