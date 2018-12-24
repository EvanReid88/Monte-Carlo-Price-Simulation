#import necessary packages
import numpy as np
import math
import matplotlib.pyplot as plt
import datetime
from scipy.stats import norm
from pandas_datareader import data

#get variables from user
symbol = input('What is the symbol?: ')
symbol.upper()

startDate = input('What is the start date for price history data? (MM/DD/YYY): ')
endDate = input('What is the end date for price history data? (type none for most recent date) (MM/DD/YYY): ')
yearLaterPrice = None

#TODO if end date is over a year old, then grab price from the year after and compare to results

if str(endDate).upper() == 'NONE':
    endDate = datetime.datetime.now()
else: 
    endDate = datetime.datetime.strptime(endDate, "%m/%d/%Y")
    if (endDate <= datetime.datetime.now() - datetime.timedelta(days=365)): 

        yearLaterPrice = data.DataReader(
            symbol, 'yahoo',
            start=endDate, 
            end= (endDate + datetime.timedelta(days=365))
        )['Adj Close'][-1]

simNum = input('How many simulations would you like to run? (<10,000): ')
simNum = int(simNum)

print ('--------------------------------------------')

#download stock price data into DataFrame
stock = data.DataReader(symbol, 'yahoo',start=startDate, end=endDate)

#TODO print current price information
#TODO compare predicions of previous year to actual
#TODO add user option to select number of days predicted, datareader date range, stock symbol, number of simulations

#Define Variables
S = stock['Adj Close'][-1] #starting stock price (i.e. last available real stock price)
T = 252 #Number of trading days

#calculate the compound annual growth rate (CAGR) which 
#will give us our mean return input (mu) 
days = (stock.index[-1] - stock.index[0]).days
cagr = ((((stock['Adj Close'][-1]) / stock['Adj Close'][1])) ** (365.0/days)) - 1
print ('CAGR =', str(round(cagr,4)*100)+"%")
mu = cagr
 
#create a series of percentage returns and calculate 
#the annual volatility of returns
stock['Returns'] = stock['Adj Close'].pct_change()
vol = stock['Returns'].std()*np.sqrt(252)
print ("Annual Volatility =", str(round(vol*100, 4))+"%")

#set up empty list to hold our ending values for each simulated price series
result = []

#run simulation simNum number of times
for i in range(simNum):
    #create list of daily returns using random normal distribution
    daily_returns=np.random.normal(mu/T,vol/math.sqrt(T),T)+1
    
    #set starting price and create price series generated by above random daily returns
    price_list = [S]
    
    for x in daily_returns:
        price_list.append(price_list[-1]*x)
 
    #plot data from each individual run which we will plot at the end
    plt.plot(price_list)

    #append the ending value of each simulated run to the empty list we created at the beginning
    result.append(price_list[-1])
 
#show the plot of multiple price series created above
plt.show()

#create histogram of ending stock values for our mutliple simulations
plt.hist(result,bins=50)
plt.axvline(np.percentile(result,5), color='r', linestyle='dashed', linewidth=2)
plt.axvline(np.percentile(result,95), color='r', linestyle='dashed', linewidth=2)
plt.axvline(np.percentile(result,15), color='b', linestyle='dashed', linewidth=2)
plt.axvline(np.percentile(result,75), color='b', linestyle='dashed', linewidth=2)
plt.show()

#print last real price
print('Last price on ', endDate.strftime("%m/%d/%Y"), ': ', round(S, 4))

#use numpy mean function to calculate the mean of the result
print("Mean: ", round(np.mean(result), 4))
print("Mean Growth: %", round(((np.mean(result) - S)/S)*100, 4))

print ('--------------------------------------------')

print("5% quantile =", round(np.percentile(result,5), 4))
print("25% quantile =", round(np.percentile(result,25), 4))
print("75% quantile =", round(np.percentile(result,75), 4))
print("95% quantile =", round(np.percentile(result,95), 4))

print ('--------------------------------------------')

# if end date for price history is over a year from last trading day
# add more data values that can be grabbed from given data

#TODO add percentage increase from end date and mean, change all parentheses to singl, add actual growth, dfifernciate he mean from he cagr and say what its frome
if yearLaterPrice != None:
    print('Actual price a year later from ', endDate.strftime("%m/%d/%Y"), round(yearLaterPrice, 4))
    print('Variance between actual price and mean result: ', round((yearLaterPrice - np.mean(result)), 4))
    print('% Variance between actual and mean result: %', round(((yearLaterPrice - np.mean(result))/np.mean(result))*100, 4))
    print ('--------------------------------------------')
#print(result)