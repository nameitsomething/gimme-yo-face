import csv

data=[ ]
counter =0
labels = []


with open('test.csv', "r",newline='') as file: #r = read, a=appead(addded to bottom), w=write
    reader = csv.reader(file, delimiter=",") #delimiter = seperates data

    for row in reader:
        if counter ==0: #if on first row, read labels
            for col in row: # does action colums in row
                
                labels.append(col.strip()) # append the col labels into the label list
            


        else : #else, collect to data list 
            data.append(row)

        counter+=1

with open('test.csv', "a", newline='') as file:
    writer = csv.writer(file, delimiter=",")
    writer.writerow([])
    for i in range(0,10): #for loop 10 times
        writer.writerow(["DrX", 50 + i ])
print(labels)
            


    
