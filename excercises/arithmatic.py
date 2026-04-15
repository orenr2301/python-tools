
def ari_product(int1, int2 : int):
    
    product = int1*int2
    
    if product > 1000:
        return int1+int2
    else:
        return product
    


def cumulative_sum():
    for i in range(10):
        if i == 0:
            string_output =  f"Current Number {i} Previous Number {i} Sum: { i + i }"
        else:
            string_output = f"Current Number {i} Previous Number {(( i - 1))} Sum: { i + (( i - 1))}"
        print(string_output)

def cumulative_sum_new():
    ## Boundries
    Previous_num = 0 
    for i in range(10):
        x_sum = Previous_num + i
        print(f"Current Number {i} Previous Number {Previous_num} Sum: {x_sum}")
        
    Previous_num = i
    
def even_number_index(data: str):
    ## Index is the len -1, strating from pistion 0
    boundry = (( len(data) - 1 ))
    stringList = list(data)
    for i in range(boundry):
        if i % 2 == 0:
            print(stringList[i])
            
    even_chars = data[0::2]
    for char in even_chars:
        print(char)
    
    
    

if __name__ == "__main__":
    # print(ari_product(30, 30))
    # cumulative_sum()
    # cumulative_sum_new()
    even_number_index("pussylicious")