from func_cointegration import *
import matplotlib.pyplot as plt

import pandas as pd
# Plot prices and trends
def plot_trends(sym1 ,sym2, price_data):
    
    # Extract prices
    prices_1 = extract_close_prices(price_data[sym1])
    prices_2 = extract_close_prices(price_data[sym2])

    # Get spread and zscore
    coint_result = calculate_cointegration(prices_1, prices_2)
    spread = calculate_spread(prices_1, prices_2, coint_result[4])
    zscore = calculate_zscore(spread)

    # Calculate  percentage change
    df = pd.DataFrame(columns=[sym1, sym2])
    df[sym1] = prices_1
    df[sym2] = prices_2
    df[f"{sym1}_pct"] = df[sym1] / prices_1[0]
    df[f"{sym2}_pct"] = df[sym2] / prices_2[0]
    series_1 = df[f"{sym1}_pct"].astype(float).values
    series_2 = df[f"{sym2}_pct"].astype(float).values

    # Save results for backtesting
    df_2 = pd.DataFrame()
    df_2[sym1] = prices_1
    df_2[sym2] = prices_2
    df_2["Spread"] = spread
    df_2["Zscore"] = zscore
    df_2.to_csv("3_backtest_file.csv")
    print("3_backtest_file.csv saved")

    # Plot charts
    fig, axs = plt.subplots(3, figsize=(16,8))
    fig.suptitle(f"Price and Spread - {sym1} vs {sym2}")
    axs[0].plot(series_1)
    axs[0].plot(series_2)
    axs[1].plot(spread)
    axs[2].plot(zscore)
    plt.show()

