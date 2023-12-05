import os
import random

directory_path = "Datasets/"

def generate_random(length, min_value, max_value):
    return [random.randint(min_value, max_value) for _ in range(length)]

def save(val, wt, size):
    file_name = f"dataset_{size}.txt"
    with open(os.path.join(directory_path, file_name), 'w') as file:
        # for v, w in zip(val, wt):
        #     file.write(f"{v} {w}\n")
        file.write("wt[]: \n")
        for w in wt:
            file.write(f"{w} ")
        file.write("\nval[]: \n")
        for v in val:
            file.write(f"{v} ")
        print(f"Dataset saved to {file_name}")


if __name__ == "__main__":
    sizes = [100, 1000, 10000]

    for size in sizes:
        wt = generate_random(size, 20, 200)
        val = [w + random.randint(1,200) for w in wt]


        print("Values:", val)
        print("Weights:", wt)

        save(val, wt, size)
