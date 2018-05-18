# Issue 1:

After a certain point things just explode (revenue / x) leads the wage update to break

```
A: [645.0]
x [0.0223, 0.0475]
revenue [0.003, 0.0918]
----------
A: [645.0]
x [9.0604, 0.1593]
revenue [0.0501, 1.4571]
----------
A: [645.0]
x [2362.9111, 111.2802]
revenue [23.1682, 1246.0108]
----------
A: [645.0]
x [4702.9318, 52314.9887]
revenue [7519.2957, 48178.5528]
```


Code:
```{python}
wages = readWages()

lr = 0.03

# these are fixed
const_lamda, sums, skill_shares = computeLrt(skills)

previous_newWages = wages
for i in range(300):
    # normalize wages BY THE PRICE OF THE AGRICULTURAL GOOD

    wages = priceNormalize(wages)

    # compute the update
    pi = computePi(wages) # (1 by 2 by 645)
    Theta_h, Theta_l = computeTheta(wages) # (645,)
    GDP = computeGDP(skills, wages)
    revenue = (1-param.alpha) * pi * vAt * GDP
    GDP

    #  labor market clearing conditions

    # A
    s_hA = Psi[H,A] * (wages[t,A] / Theta_h)**(param.zeta)
    s_lA = Psi[L,A] * (wages[t,A] / Theta_l)**(param.zeta)
    x_A = myGamma(param.zeta) * (skills[t,H] * s_hA * Theta_h + skills[t,L] * s_lA * Theta_l)

    # NA
    s_hNA = Psi[H,NA] * (wages[t,NA] / Theta_h)**(param.zeta)
    s_lNA = Psi[L,NA] * (wages[t,NA] / Theta_l)**(param.zeta)
    x_NA = myGamma(param.zeta) * (skills[t,H] * s_hNA * Theta_h + skills[t,L] * s_lNA * Theta_l)
    
    newWages = revenue / np.vstack([x_A, x_NA])
    
    if i%2==0:
        print('-' * 10)
        logNorm("A:", s_lA + s_lNA)
        logNorm("x", x_A, x_NA)
        logNorm("revenue", revenue[t,A], revenue[t,NA])

    loss = np.sum((newWages - previous_newWages)**2)
    previous_newWages = newWages
    
    wages = lr * newWages + (1-lr) * wages

    if loss < 1e-7:
        print('w-- #{}: {}'.format(i, loss))
        break

    if i%2 == 0:
        pass
#         print(i, np.sum(newWages), np.sum(wages), loss)
```
# What it was:

I was using the wrong code, computing something totally different than