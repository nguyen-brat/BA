import json
import datetime
import random
import pandas as pd
from catboost import CatBoostRegressor, Pool
from fastapi import FastAPI, HTTPException

# Initialize FastAPI
app = FastAPI()

# Load pre-trained model and data mappings
loaded_model = CatBoostRegressor()

with open("dictionary_map.json", "r", encoding='utf-8') as f:
    dictionary_map = json.load(f)

with open("all_categories_dict.json", "r", encoding="utf-8") as f:
    all_categories_dict = json.load(f)

with open('keys_list.json', 'r') as f:
    keys_list = json.load(f)
    keys_list.remove("ExcessDelay")

# Function to prepare data
def prepare_data_for_catboost(street_name):
    if street_name not in dictionary_map:
        raise HTTPException(status_code=404, detail=f"Street name '{street_name}' not found.")

    table_data = dictionary_map[street_name]
    now = datetime.datetime.now()

    sample = {key: [0] for key in keys_list}
    sample["Delay"] = [table_data["Delay"]]
    sample["Id"] = [table_data["Id"]]
    sample["Length"] = [table_data["Length"]]
    sample["TT"] = [table_data["TT"]]
    name_id = [all_categories_dict["Name"][street_name]]
    sample[f"Name_{name_id}"] = [1]
    sample["Speed"] = [random.randint(10, 120)]
    StartEndDescription_id = [all_categories_dict["StartEndDescription"][table_data["StartEndDescription"]]]
    sample[f"StartEndDescription_{StartEndDescription_id}"] = [1]
    sample["Timezone_0"] = [1]
    sample["Year"] = [now.year]
    sample["Month"] = [now.month]
    sample["Day"] = [now.day]
    sample["Hour"] = [now.hour]
    sample["Minute"] = [now.minute]
    sample["Second"] = [now.second]

    return pd.DataFrame.from_dict(sample)

# Prediction endpoint
@app.post("/predict_excess_delay/")
def predict_excess_delay(street_name: str):
    try:
        sample_data = prepare_data_for_catboost(street_name)
        sample_data = Pool(sample_data, cat_features=keys_list)
        
        # Load the model (ensure path is correct)
        loaded_model.load_model("catboost_excess_delay_model.cbm")
        
        y_pred = loaded_model.predict(sample_data)
        return {"street_name": street_name, "excess_delay_prediction": y_pred.tolist()[0]}
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    #print(predict_excess_delay("(Belconnen Wy/Bindubi St) to (London Cct) via Bindubi St, Parkes Wy and Edinburgh Av"))
