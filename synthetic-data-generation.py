import openai
import csv
import os
from dotenv import load_dotenv
import numpy as np

load_dotenv()

os.environ["OPENAI_API_KEY"] = "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"
PROMPT = (
    """
    
    Randomly generate 10 postgraduate level physics and chemistry questions and answers using the following examples.
    Do not include any numbering or double quotes at the beginning of the lines.
    Format each line exactly like this (without double quotes):
    Example:
    [
        {
            'instruction':'Calculate the number of photons emitted by a 100 W yellow lamp in 1.0 s.',
            'input':'The wavelength of yellow light is 560 nm, and 100 percent efficiency is assumed.',
            'output':'Each photon has an energy $h\nu$', so the total number $N$ of photons needed to produce an energy $E$ is $N=\frac{E}{h\nu}$. To use this equation, you need to know the frequency of the radiation (from $\nu=\frac{c}{\lambda}$) and the total energy emitted by the lamp. The latter is given by the product of the power ($P$, in watts) and the time interval, $\deltat$, for which the lamp is turned on: $E=P\deltat$. Substitution of the data gives $2.8\times10^{20}$ photons.
        },
    ]    
    
    """
)
NUM_OF_CALLS = 3

if not "OPENAI_API_KEY":
    raise ValueError("OPENAI_API_KEY environment variable not set")

openai.api_key = os.environ.get("OPENAI_API_KEY")

def generate_text():
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": PROMPT}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def save_to_csv(data, file_name):
    with open(file_name, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for row in data:
            print(row)
            writer.writerow(row)

if __name__ == "__main__":
    data = []

    try:
        for i in range(NUM_OF_CALLS):
            response = generate_text()
            lines = response.split("\n")
            print(lines)
            for line in lines:
                comment = line
                data.append(comment)
                #if line:
                    #try:
                    #    comment, label = line.rsplit(",", 1)
                    #    label_int = int(label.strip())
                    #    data.append((comment.strip(), label_int))
                    #except ValueError:
                    #    print(f"Skipping line due to invalid format: '{line}'")
                print(f"Completed API call {i + 1} of {NUM_OF_CALLS}")


    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Saving partial data to the CSV file...")

    finally:
        
        #save_to_csv(data, "testoutput.csv")
        np.savetxt("questionstest1.txt", data, fmt="%s")
        print("Data saved to 'questionstest1.txt'.")