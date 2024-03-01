from text_classification import get_classification_ollama
import json
import csv
import os

if __name__ == '__main__':
    
    for filename in sorted(os.listdir("orgs")):
        print(filename)
        with open(os.path.join("orgs", filename), "r", encoding= "utf-8") as f:
            data = json.load(f)
        for org in data:
            try:
                name = org.get("name")
                description = org.get("description")
                university = org.get("university")
                category = get_classification_ollama(description, name)

                with open("categories.csv", "a", newline="") as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow([
                        name, 
                        description, 
                        university,
                        category
                    ])
            except Exception as e:
                with open("log.log", "a") as logfile:
                    logfile.write(', '.join([name, description, university]) + '\n')