import numpy as np

max_iterations = 120
escape_radius = 2000000000000000

def interpolate_colors_vectorized(normalized_counts: np.ndarray) -> np.ndarray:
    t = normalized_counts
    r = (255 * np.sin(2 * np.pi * t * 3) ** 2).astype(np.uint8)  
    g = (255 * np.sin(2 * np.pi * t * 5) ** 2).astype(np.uint8) 
    b = (255 * np.sin(2 * np.pi * t * 7) ** 2).astype(np.uint8)     

    return np.stack((r, g, b), axis=-1)



def compute_fractal(matrix: np.ndarray, width: int, height: int, real_bounds=(-2.5, 1), imag_bounds=(-1.5, 1.5), k=1, j=(0.285, 0.01)):
    real = np.linspace(real_bounds[0], real_bounds[1], width)
    imag = np.linspace(imag_bounds[0], imag_bounds[1], height)
    real_grid, imag_grid = np.meshgrid(real, imag)

    if k == 1:
        c_values = real_grid + 1j * imag_grid  
        z = np.zeros_like(c_values, dtype=np.complex128) 
    elif k == 2:
        c_values = complex(j[0], j[1])  
        z = real_grid + 1j * imag_grid  

    counts = np.zeros(z.shape, dtype=np.float32)
    mask = np.ones(z.shape, dtype=bool)

    for i in range(max_iterations):
        if k == 1:
            z[mask] = z[mask] ** 2 + c_values[mask]  
        elif k == 2:
            z[mask] = z[mask] ** 2 + c_values  

        escaped = np.abs(z) > escape_radius
        new_escape = escaped & mask

        counts[new_escape] = i + 1 - np.log(np.log(np.abs(z[new_escape])) + 1) / np.log(2)
        mask &= ~escaped

        if not mask.any():
            break

    normalized_counts = counts / max_iterations
    matrix[:, :, :] = np.transpose(interpolate_colors_vectorized(normalized_counts),(1,0,2))
