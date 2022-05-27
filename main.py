from flask import Flask, request
import pandas as pd

#establish dataframe
super_data = [
       {"name": "Spiderman", "superpower": "Bitten by spider", "weakness": "big dumb"},
       {"name": "Thor", "superpower": "being a god", "weakness": "unclear"},
       {"name": "Rogue", "superpower": "touch of death", "weakness": "very sad"}
   ]
super_df  = pd.DataFrame(super_data)
super_df.set_index(keys="name", drop=False, inplace=True)

#create flask instance
app = Flask(__name__)
app.config["db"]=super_df

@app.route("/see_stats", methods=["GET"])
def show_stats():
    """
    HTTP GET: Query by name, superpower, or weakness
    """
    #access pandas data frame
    global super_df
    #get parameters
    name = request.args.get("name", default=None)
    superpower = request.args.get("superpower", default=None)
    weakness = request.args.get("weakness", default=None)
    #if statement that allows for search by name, superpower or weakness
    if name is not None:
        result_df = super_df.loc[super_df["name"]==name]
    elif superpower is not None:
        result_df = super_df.loc[super_df["superpower"]==superpower]
    elif weakness is not None:
        result_df = super_df.loc[super_df["weakness"]==weakness]
    #if no parameters are provided, return entire dataframe
    else:
        result_df = super_df
    #create response json and headers
    resp_json = {
        "result": result_df.to_dict(orient="records")
    }
    resp_headers = {
        "content-type": "application/json"
    }
    return resp_json, 200, resp_headers


@app.route("/add_stats", methods=["POST"])
def create_hero():
    """
    HTTP POST: Function to add new superhero data
    """
    #access data frame
    global super_df
    try:
        #empty lists for data to be stores in
        inserted_hero = []
        rejected_hero = []
        #defining out data as the input json
        data = request.json
        #looping through input, setting index for new hero and adding new row
        for hero in data:
            if ("name" in hero) and ("superpower" in hero) and ("weakness" in hero):
                index = hero["name"]
                super_df.loc[hero["name"]] = hero
                #append to accepted list
                inserted_hero.append(hero)
            #if needed data is not present append to rejects list
            else:
                rejected_hero.append(hero)
        #create response json and headers
        resp_json = {
            "records_inserted": len(inserted_hero),
            "result": inserted_hero,
            "rejects": rejected_hero,
        }
        resp_headers = {
            "content-type": "application/json",
        }
        return resp_json, 200, resp_headers
    #return error if above cannot be performed.
    except Exception as err:
        return {"status": "error", "error_msg": str(err)}, 400, {"content-type": "application/json"}

#run function
if __name__ == "__main__":
    app.run('0.0.0.0', 5050)