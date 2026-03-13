import pandas as pd
import json
import os

def run_task_3_simulation():
    print("🚀 --- Task 3: Nutritional Analysis Simulation ---")
    
    input_file = "data/All_Diets.csv"
    
    if not os.path.exists(input_file):
        print(f"❌ Error: {input_file} not found in current directory!")
        return

    print(f"📥 Loading dataset: {input_file}...")
    df = pd.read_csv(input_file)
    
    print("📊 Processing nutritional data (Serverless Logic)...")
    analysis = df.groupby('Diet_type')[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean()
    
    result_dict = analysis.reset_index().to_dict(orient='records')

    output_dir = 'simulated_nosql'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'results.json')
    
    with open(output_path, 'w') as f:
        json.dump(result_dict, f, indent=4)
        
    print(f"✅ SUCCESS: Analysis results saved to {output_path}")
    print("\n--- Summary of Results (First 3 rows) ---")
    print(analysis.head(3))

if __name__ == "__main__":
    run_task_3_simulation()