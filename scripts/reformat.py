import pandas as pd
import numpy as np
import os


def extract_data(entry):
    return entry


def reformat(df):
    # Extracting and converting data from the dataframe
    id = [entry["$oid"] for entry in df["_id"]]
    split_tag = df["tag"].values
    energy = [float(entry["energy"]["$numberDouble"]) for entry in df["outputs"]]
    forces = [
        [[float(force.get("$numberDouble", 0)) for force in l] for l in entry["forces"]]
        for entry in df["outputs"]
    ]
    stress = [
        [
            float(stress["$numberDouble"])
            if isinstance(stress, dict) and "$numberDouble" in stress
            else 0
            for stress in entry["stress"]
        ]
        for entry in df["outputs"]
    ]
    atoms = [
        {
            "lattice_mat": [
                [float(l["$numberDouble"]) for l in list]
                for list in entry["lattice"]["matrix"]
            ],
            "coords": [
                [float(j["$numberDouble"]) for j in i["xyz"]] for i in entry["sites"]
            ],
            "abc": [
                float(entry["lattice"]["a"]["$numberDouble"]),
                float(entry["lattice"]["b"]["$numberDouble"]),
                float(entry["lattice"]["c"]["$numberDouble"]),
            ],
            "elements": [i["species"][0]["element"] for i in entry["sites"]],
            "angles": [
                float(entry["lattice"]["alpha"]["$numberDouble"]),
                float(entry["lattice"]["beta"]["$numberDouble"]),
                float(entry["lattice"]["gamma"]["$numberDouble"]),
            ],
            "cartesian": False,
            "props": [""],
        }
        for entry in df["structure"]
    ]

    converted_data = dict(
        id=id,
        split_tag=split_tag,
        calc_type=df.group.values,
        description=df.description.values,
        energy=energy,
        forces=forces,
        stress=stress,
        atoms=atoms,
    )
    converted_df = pd.DataFrame(converted_data)
    converted_df["energy"] = converted_df["energy"].astype(float)
    converted_df.to_json("data/MoTaNbTi/MoTaNbTi.jsonl", lines=True, orient="records")
    return converted_df


if __name__ == "__main__":
    # first dump bson data to json-lines
    df = pd.read_json("data/MoTaNbTi/output.json", lines=True)
    df_modified = reformat(df)
