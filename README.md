# Folder Tree
```
api
├── all_categories_dict.json
├── api.py
├── catboost_excess_delay_model.cbm
├── dictionary_map.json
├── keys_list.json
├── README.md
└── requirements.txt
```

# Environment setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

# Install pretrained model
If you using linux
```
gdown --id 1OhFBtUsN1tHmP2TJEqdi1m2mz2n7xPWz --output model.zip
unzip model.zip
```

If using window
download the pretrained model from gg drive link: https://drive.google.com/file/d/1OhFBtUsN1tHmP2TJEqdi1m2mz2n7xPWz/view?usp=sharing

# Run api
```
python api.py
```

# Test with post man
```
curl -X POST "http://127.0.0.1:8000/predict_excess_delay/" -H "Content-Type: application/json" -d '{"street_name": "(Belconnen Wy/Bindubi St) to (London Cct) via Bindubi St, Parkes Wy and Edinburgh Av"}'
```