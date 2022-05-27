from flask import Flask, request
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

@app.route("/see_stats", methods=["GET"])
def show_stats():
    """
    HTTP GET: Query by name, superpower, or weakness
    """
    #access pandas data frame
    global super_df
    name = request.args.get("name", default=None)
    superpower = request.args.get("superpower", default=None)
    weakness = request.args.get("weakness", default=None)
    if name is not None:
        result_df = super_df.loc[super_df["name"]==name]
    elif superpower is not None:
        result_df = super_df.loc[super_df["superpower"]==superpower]
    elif weakness is not None:
        result_df = super_df.loc[super_df["weakness"]==weakness]
    else:
        result_df = super_df
    resp_json = {
        "result": result_df.to_dict(orient="records")
    }
    resp_headers = {
        "content-type": "application/json"
    }
    return resp_json, 200, resp_headers

@app.route("/add_stats", methods=["POST"])
def create():
    """
    HTTP POST: Function to add new superhero data
    """
    global super_df


if __name__ == "__main__":
    app.run('0.0.0.0', 5050)