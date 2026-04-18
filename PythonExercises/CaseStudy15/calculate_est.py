def calculate_est(r, theta):
    coeff_ans = r * np.cos(theta)
    A_ans = np.array([[1.00, coeff_ans[0]],
                [1.00, coeff_ans[1]],
                [1.00, coeff_ans[2]],
                [1.00, coeff_ans[3]],
                [1.00, coeff_ans[4]]])

    C_ans = A_ans.T @ A_ans
    z_ans = A_ans.T @ r
    
    return np.linalg.solve(C_ans,z_ans)

def calculate_r_theta(theta, estimate):
    return estimate[0] / (1 - estimate[1] * np.cos(thetas))