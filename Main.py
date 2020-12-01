from matplotlib import pyplot as plt
from Chart import Chart
import requests
from CovidDataHandler import CovidDataHandler



r = requests.get("https://api.covidtracking.com/v1/us/daily.json")
state_r = requests.get("https://api.covidtracking.com/v1/states/daily.json")

state_data = state_r.json() 
data = r.json()

#print(data_list[0])







def main():
    
    
    
    stateCovidHandler = CovidDataHandler(state_data)    
    covidHandler = CovidDataHandler(data)

    date_list = covidHandler.get_date_list()
    death_list = covidHandler.get_data_list("deathIncrease")
    currently_hosp_list = covidHandler.get_data_list("hospitalizedCurrently")
    test_list = covidHandler.get_sum_two_lists("positiveIncrease", "negativeIncrease")
    case_list = covidHandler.get_data_list("positiveIncrease")
    on_ventilator = covidHandler.get_data_list("onVentilatorCurrently")

    SC_death_list = stateCovidHandler.get_state_data_list("SC", "deathIncrease")
    SC_date_list = stateCovidHandler.get_state_date_list("SC")
    Chart(SC_date_list, SC_death_list)
    #print(date_list)
    #Chart(date_list, on_ventilator)
    
    '''Chart(date_list, case_list)
    Chart(date_list, test_list)
    Chart(date_list, currently_hosp_list)
    '''
    #Chart(date_list, death_list)

    plt.show()

if __name__ == '__main__':
    main()



