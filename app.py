import streamlit as st
import pandas as pd
from apyori import apriori

def perform_market_basket_analysis(df):
    transactions = []
    for i in range(0, df.shape[0]):
        transactions.append([str(df.values[i, j]) for j in range(0, df.shape[1])])
    
    rules = apriori(transactions, min_support=0.003, min_confidence=0.2, min_lift=3, min_length=2)
    results = list(rules)
    
    lhs, rhs, support, confidence, lift = [], [], [], [], []
    for result in results:
        lhs.append(tuple(result[2][0][0])[0])
        rhs.append(tuple(result[2][0][1])[0])
        support.append(result[1])
        confidence.append(result[2][0][2])
        lift.append(result[2][0][3])
    
    columns = list(zip(lhs, rhs, support, confidence, lift))
    result_df = pd.DataFrame(columns)
    result_df.columns = ['Item1', 'Item2', 'Support', 'Confidence', 'Lift']
    result_df = result_df.sort_values('Lift', ascending=False)
    
    return result_df

def main():
    st.title("Market Basket Analysis")
    
    # Load data
    df = pd.read_csv("Market_Basket_Optimisation.csv", header=None)
    
    # User input
    product = st.text_input("Enter a product:")
    
    # Perform analysis
    if st.button("Recommend Associated Products"):
        if product:
            filtered_df = df[df.astype(str).values == product]
            result_df = perform_market_basket_analysis(filtered_df)
            
            st.subheader("Associated Products:")
            st.write(result_df)
        else:
            st.warning("Please enter a product.")
            
if __name__ == "__main__":
    main()