import json

def jsonl_to_xyz(jsonl_file, xyz_file):
    with open(jsonl_file, 'r') as infile, open(xyz_file, 'w') as outfile:
        for line in infile:
            data = json.loads(line)
            atoms = data["atoms"]
            lattice_mat = atoms["lattice_mat"]
            coords = atoms["coords"]
            elements = atoms["elements"]
            forces = data["forces"]
            energy = data["energy"]
            description = data["description"]
            num_atoms = len(elements)

            # Write the number of atoms
            outfile.write(f"{num_atoms}\n")
            
            # Write the properties and lattice information
            lattice_str = " ".join(str(x) for row in lattice_mat for x in row)
            outfile.write(f'Lattice="{lattice_str}" Properties=species:S:1:pos:R:3:forces:R:3 energy={energy} description="{description}" pbc="F F F"\n')

            # Write atom information
            for i in range(num_atoms):
                element = elements[i]
                x, y, z = coords[i]
                fx, fy, fz = forces[i]
                outfile.write(f"{element} {x:.8f} {y:.8f} {z:.8f} {fx:.8f} {fy:.8f} {fz:.8f}\n")


# Example usage
jsonl_file = '/Users/basit-work/Desktop/NIST/NIST_GIAN_MACE-MP-0/data/MoTaNbTi/MoTaNbTi.jsonl'
xyz_file = '/Users/basit-work/Desktop/NIST/NIST_GIAN_MACE-MP-0/data/molecules.xyz'
jsonl_to_xyz(jsonl_file, xyz_file)
print(f"Conversion from {jsonl_file} to {xyz_file} completed successfully.")
