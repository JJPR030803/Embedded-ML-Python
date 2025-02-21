import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def box_plot_datos(datos,printing=True):
    """
    Create a box plot and analyze statistical properties of the input data.
    
    Parameters:
    -----------
    datos : array-like
        Input data for statistical analysis and visualization
    
    Returns:
    --------
    dict
        Dictionary containing statistical metrics
    """
    # Ensure input is a numpy array for consistent handling
    datos = np.array(datos)
    
    # Calculate key statistical metrics
    q1 = np.percentile(datos, 25)
    q2 = np.percentile(datos, 50)
    q3 = np.percentile(datos, 75)
    
    
    iqr = q3 - q1
    
   
    limite_inferior = q1 - 1.5 * iqr
    limite_superior = q3 + 1.5 * iqr
    
    
    outliers = datos[(datos < limite_inferior) | (datos > limite_superior)]
    
    
    plt.figure(figsize=(8, 5))
    sns.boxplot(y=datos, color="skyblue", width=0.5)
    plt.title("Box Plot of Data Distribution")
    plt.ylabel("Values")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    
    if printing:
        print(f"Q1 (25%): {q1}")
        print(f"Q2 (Median, 50%): {q2}")
        print(f"Q3 (75%): {q3}")
        print(f"Lower Boundary: {limite_inferior}")
        print(f"Upper Boundary: {limite_superior}")
        print(f"Interquartile Range (IQR): {iqr}")
        print(f"Outliers: {outliers}")
    
    # Optional: Return statistical metrics for further use
    return {
        'Q1': q1,
        'Median': q2,
        'Q3': q3,
        'Lower_Boundary': limite_inferior,
        'Upper_Boundary': limite_superior,
        'IQR': iqr,
        'Outliers': outliers
    }
def aplicar_interpolacion_lineal(datos, lower_limit, upper_limit):
    """
    Apply linear interpolation to remove outliers from input data.
    
    Parameters:
    -----------
    datos : dict or array-like
        Input data for interpolation
    lower_limit : float
        Lower boundary for non-outlier values
    upper_limit : float
        Upper boundary for non-outlier values
    
    Returns:
    -----------
    numpy.ndarray
        Interpolated data with outliers handled
    """
    # Extract data if input is a dictionary
    if isinstance(datos, dict):
        datos = datos.get('Outliers', datos.get('fitness_history', []))
    
    # Convert to numpy array
    datos = np.array(datos)
    
    # If no valid data, return original input
    if len(datos) == 0:
        return datos
    
    # Create DataFrame
    df = pd.DataFrame(datos, columns=["values"])
    
    # Use percentile-based outlier detection if limits not provided
    if lower_limit is None or upper_limit is None:
        q1 = np.percentile(df["values"].dropna(), 25)
        q3 = np.percentile(df["values"].dropna(), 75)
        iqr = q3 - q1
        lower_limit = q1 - 1.5 * iqr
        upper_limit = q3 + 1.5 * iqr
    
    # Replace outliers with NaN
    df.loc[(df["values"] < lower_limit) | (df["values"] > upper_limit), "values"] = np.nan
    
    # Interpolate
    interpolated_values = df["values"].interpolate(method="linear", limit_direction='both')
    
    # If interpolation fails, fill NaNs with mean or original values
    if interpolated_values.isna().all():
        interpolated_values = df["values"].fillna(df["values"].mean())
    
    return interpolated_values.to_numpy()