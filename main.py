from flask import Flask
import pandas as pd

super_data = [
       {"name": "Spiderman", "superpower": "Bitten by spider", "weakness": "big dumb"},
       {"name": "Thor", "superpower": "being a god", "weakness": "unclear"},
       {"name": "Rogue", "superpower": "touch of death", "weakness": "very sad"}
   ]
super_df  = pd.DataFrame(super_data)
super_df.set_index(keys="name", drop=False, inplace=True)

app = Flask(__name__)
app.config["db"]=super_df