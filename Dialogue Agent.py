#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import nltk
from nltk.tokenize import word_tokenize
from classification import Classification
import re
#%%
    #initialize classification agent, then call prediction when necessary
clf_agent=Classification()
clf_agent.initialize_data()
#clf_agent.OverSampling()
clf_agent.TrainLogisticRegression()
def classification(phrase):
    
    y_pred=clf_agent.predict(phrase)
    return y_pred

# In[1]:


# -- Cesar -- preparation for preference extraction
#preparation 

#imported librairies:
import pandas as pd
from Levenshtein import distance as dt
import nltk
from nltk.corpus import stopwords as s_w
from nltk.tokenize import word_tokenize as w_t

#reading the file
file=pd.read_csv("restaurant_info.csv")

#extracting columns
restaurant_names=list(file['restaurantname'])
price_range=list(file['pricerange'])
area=list(file['area'])
food_types=list(file['food'])
phone=list(file['phone'])
address=list(file['addr'])
post_code=list(file['postcode'])


#function that removes stop words e.g Levenshtein_Distance("the",thai") too little
def stop_words_removal(s):
    tk=w_t(s)
    s=[i for i in tk if not i in (s_w.words('english'))]
    s=" ".join(s)
    s = s.lower()
    #print(s)
    s=s.split(" ")
    #print(s)
    return s



#%%
    
def no_preference(user_ut, p):
    """
    check if user indicated no preference by using keyword matching

    Parameters
    ----------
    user_ut : str
        DESCRIPTION.
    p : list
        list of preferences.

    Returns
    -------
    p : list
        DESCRIPTION.

    """
    keywords=re.findall( "any\s(\w+)", user_ut.lower())
    if ("area" in keywords):
        p[0]='any'
    if ("price" in keywords):
        p[1]='any'
    if ("food" in keywords):
        p[2]='any'
    return p

# In[2]:
# -- Cesar -- preference extraction

def preference_extractor(user_ut):
    p=[0 for i in range(3)] #the preferences are stored in a list of three elements, p[0] for the area, p[1] for the price range and p[2] for the food type
    s=stop_words_removal(user_ut)

    p=no_preference(user_ut, p) #check if user indicated no preference
    
#keyword matching for the area
    for i in s:
        for j in area:
            if i == j:
                p[0] = j
    if(('north' and 'american' in s) and (s.count('north'))>1):
        p[0]=0
    #print(p)
#keyword matching for the price range
    for i in s:
        for j in price_range:
            if i == j:
                p[1] = j
#keyword matching for the food type
    for i in s:
        for j in food_types:
            if i == j:
                p[2] = j
            elif ('asian' and 'oriental' in s):
                p[2]='asian oriental'
            elif ('modern' and 'european' in s):
                p[2]='modern european'
            elif ('north' and 'american' in s):
                p[2]='north american'
                
#In case the area has been mispelt
    if (p[0] == 0):
        d = {}
        l=[]
        z=['south', 'centre', 'west', 'east', 'north']
        for i in s:
            for j in z:
                if (dt(i, j)<=2):   
                    d[j] = dt(i, j)
        #print(d)
        for i in d.values():
            l.append(i)
        if len(l)>0:
            k = min(l)
            key_list = list(d.keys())
            val_list = list(d.values())
            if k<=2:
                p[0] = key_list[val_list.index(k)]

    #In case the price range has been mispelt
    if (p[1] == 0):
        d = {}
        l=[]
        d = {}
        l=[]
        for i in s:
            for j in list(set(price_range)):
                if (dt(i, j)<=3):   
                    d[j] = dt(i, j)
        for i in d.values():
            l.append(i)
        if len(l)>0:
            k = min(l)
            key_list = list(d.keys())
            val_list = list(d.values())
            if k<=2:
                p[1] = key_list[val_list.index(k)]
        for i in s:
            for j in list(set(price_range)):
                if (dt(i, j)<=3):   
                    d[j] = dt(i, j)
        #print(d)
        for i in d.values():
            l.append(i)
        if len(l)>0:
            k = min(l)
            key_list = list(d.keys())
            val_list = list(d.values())
            if k<=2:
                p[1] = key_list[val_list.index(k)]
    #In case the  food type has been mispelt                
    #thresolds for Levenshtein distances might need to be better tuned for each preference
    if (p[2] == 0):
        d = {}
        l=[]
        for i in s:
            for j in list(set(food_types)):
                if (dt(i, j)<=2):   
                    d[j] = dt(i, j)
                elif (dt('asian',i)<=2 or dt('oriental',i)<=2 in s):
                    d['asian oriental']=min([dt('asian',i),dt('oriental',i)])
                elif (dt('modern',i)<=2 or dt('european',i)<=2 in s):
                    d['modern european']=min([dt('modern',i),dt('european',i)])
                elif (dt('north',i)<=2 or dt('american',i)<=2 in s):
                    if('north' and 'american' in s):
                        d['north american']=min([dt('north',i),dt('american',i)])
        #print(d)
        for i in d.values():
            l.append(i)
        if len(l)>0:
            k = min(l)
            key_list = list(d.keys())
            val_list = list(d.values())
            if k<=3:
                p[2] = key_list[val_list.index(k)]    
    return p


# %%
# -- Ivan -- look for matches with preferences in the database

def lookup(data):

    res = list()

    fit_area = set()
    fit_price = set()
    fit_food = set()
    
    if data[0] == "any":
        fit_area = set(range(len(area)))
    else:
        for i,a in enumerate(area):
            if a == data[0]:
                fit_area.add(i)
    if data[1] == "any":
        fit_price = set(range(len(price_range)))
    else:
        for j,p in enumerate(price_range):
            if p == data[1]:
                fit_price.add(j)
    if data[2] == "any":
        fit_food = set(range(len(food_types)))
    else:
        for k,f in enumerate(food_types):
            if f == data[2]:
                fit_food.add(k)
    option_numbers = fit_area.intersection(fit_price, fit_food)
    if option_numbers:
        for i in option_numbers:
            res.append(restaurant_names[i])
            
    return res


# %%
# -- Ivan -- finite-state dialogue agent

global statelog
statelog = list()
res=[]
def agree(userinput):
    
    response = classification(userinput)
    if response in ["ack", "affirm"]:
        return True
    elif response in ["deny", "negate"]:
        return False
    else:
        return response
        

def dialogue(userinput, state, rest_data):
    global res
    userinput = userinput.lower()
    
    statelog.append([userinput,state])
    print("statelog: ",statelog)
    if state == "exit":
        return
    if state in ("init", "hello"):
        rest_data = [0,0,0]
        userinput = input("Hello! I can recommend restaurants for you. To start, please enter your request. You can ask for restaurants by area, price range or food type. ")
        state = classification(userinput)
        dialogue(userinput, state, rest_data)
        return
    
    if state == "inform":
        rest_data_mined = preference_extractor(userinput)
        for i,d in enumerate(rest_data):
            if d == 0:
                rest_data[i] = rest_data_mined[i]
        
        if rest_data[0] == 0:
            userinput = input("In which area would you like to find a restaurant? ")
            
            state = classification(userinput)
            if "area" not in userinput:
                userinput+=" area"
        elif rest_data[1] == 0:
            userinput = input("What is your desired price range? ")
            
            state = classification(userinput)
            if "price" not in userinput:
                userinput+=" price"
        elif rest_data[2] == 0:
            userinput = input("What type of food do you prefer? ")
            
            state = classification(userinput)
            if "food" not in userinput:
                userinput+=" food"
        else:
            userinput = input("You are looking for a restaurant with the following preferences:\nArea: {0} \nPrice range: {1} \nwith {2} Food \nDid I get everything correctly? ".format(rest_data[0],rest_data[1],rest_data[2]))
            accept = agree(userinput)
            if accept is True:
                state = "answer"
            elif accept is False:
                userinput = ""
                rest_data = [0,0,0]
            else:    
                state = "accept"
        print(userinput)
        #print(1,userinput, state, rest_data)
        dialogue(userinput, state, rest_data)
        return 

    if state == "answer": 
        res = lookup(rest_data)
        if res:      
            userinput = input("Okay, here is your recommendation: '{}'. Is it fine? ".format(res[0]))
            state = classification(userinput)
            if state in ["ack", "affirm"]:
                state = "goodbye"
            elif state in ["reqalts", "reqmore", "deny", "negate"]:
                res = res.pop()
                state = "answer"
        else:
            userinput = input("Sorry, no recommendations matching your demands. Try to search for another restaurant ")
            rest_data = [0,0,0]
            state = classification(userinput)
        #print(2,userinput, state, rest_data)
        dialogue(userinput, state, rest_data)
        return
        
    if state in ["thankyou", "goodbye", "reset"]:
        if state == "reset":
            print("Restarting the dialogue agent...")
        else:
            print("Thank you for using our chatbot. Come back! ")
        state = "init"
        dialogue(userinput, state, rest_data)
        return
    
    if state == "repeat":
        try:
            userinput = statelog[len(statelog) - 3][0]
            state = statelog[len(statelog) - 3][1]
        except IndexError:
            print("Nowhere to go back, starting again")
            state = init
        dialogue(userinput, state, rest_data)
        return
        #-1
    
    
    
    #to do
    else:
        userinput = input("Please repeat")#statelog[len(statelog) + 1][0]
        state = statelog[len(statelog) - 2][1]
        dialogue(userinput, state, rest_data)
        return
        

        


# %%


if __name__ == "__main__":
    dialogue("", "init", [0,0,0])


# In[ ]:



