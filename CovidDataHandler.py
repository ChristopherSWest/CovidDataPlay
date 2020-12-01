import datetime

class CovidDataHandler:
    def __init__(self, data):
        self.data_dict = data

    def get_data_list(self, key):
        """
        The purpose of this function is to give a key name and return a list of all data values for that key
        """
        data_list = []
        for item in self.data_dict:
            if item[key] == None:
                data_list.append(0)
            else:
                data_list.append(item[key])
        
        return data_list

    def get_state_data_list(self, state, key):
        """
        The purpose of this function is to give a key name and return a list of all data values for that key for a specific state.
        Requires a list of dictionaries that have state data
        """
        data_list = []
        for item in self.data_dict:
            if item["state"] == state:
                if item[key] == None:
                    data_list.append(0)
                else:
                    data_list.append(item[key]) 
        
        return data_list


    def get_sum_two_lists(self, key1, key2):
        """
        return a list made of the sum of two data points from the covid tracking project data
        """
        data_list = []
        for item in self.data_dict:
            if item[key1] == None:
                item[key1] = 0
            elif item[key2] == None:
                item[key2] = 0
            else:
                data_list.append(item[key1] + item[key2])
        
        return data_list

    def get_state_sum_two_lists(self, state, key1, key2):
        """
        return a list made of the sum of two data points from the covid tracking project data for a particular state
        Requires a list of dictionaries that have state data
        """
        data_list = []
        for item in self.data_dict:
            if item["state"] == state:
                if item[key1] == None:
                    item[key1] = 0
                elif item[key2] == None:
                    item[key2] = 0
                else:
                    data_list.append(item[key1] + item[key2])
        
        return data_list

    def split_date_int(self, date):
        '''
            This function takes the date from the covid tracking project api data and converts it into a form that can be graphed
            with matplotlib
        '''
        month = ""
        day = ""
        year = ""
        date = str(date)
        year = date[0] + date[1] + date[2] + date[3]
        year = int(year)
        month = date[4] + date[5]
        month = int(month)
        day = date[6] + date[7]
        day = int(day)
        return year, month, day

    def get_date_list(self):
        """
        This function returns a usable list of dates for plotting
        """
        date_list = []
        
        for i in self.data_dict:
            date2con = self.split_date_int(i["date"])
            date = datetime.date(date2con[0], date2con[1], date2con[2])
            date_list.append(date)
        return date_list

    def get_state_date_list(self, state):
        """
        This funciton returns a usable list of dats for plotting
        Requires a list of dictionaries that have state data
        """
        date_list = []
        
        for i in self.data_dict:
            if i["state"] == state:
                date2con = self.split_date_int(i["date"])
                date = datetime.date(date2con[0], date2con[1], date2con[2])
                date_list.append(date)
        return date_list