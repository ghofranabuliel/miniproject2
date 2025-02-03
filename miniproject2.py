import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def calc_mean_erp(trial_points, ecog_data):


    #here we load the DATA that the func takes as paramters
    trial= pd.read_csv(trial_points, header=None, names=['start', 'peak', 'finger'])
    ecog = pd.read_csv(ecog_data, header=None).squeeze("columns")
    trial=trial.astype(int)


    #I intlize a matrix with 5 rows and 1201 cols - empty matrix with 0 values in all the cells
    fingers_erp_mean = np.zeros((5, 1201))
    cols=1201
    rows=5
    fingers_erp_mean=np.full((rows,cols), fill_value=0.0)

    #loop to over all the fingers from 1 to 5
    for f in range(1, 6):
        #Get all start times where the finger == the loop index
        starts=trial.loc[trial["finger"]==f,"start"].to_numpy() 
        #Extract ECOG segments
        segments=np.array([
            ecog.iloc[int(s - 200): int(s + 1001)].to_numpy()  
            for s in starts
            if 0<=int(s-200)<len(ecog) 
                if int(s+1001)<len(ecog) or int(s+1001)==len(ecog)   
        ])
        #Compute the mean ERP for the current finger ((if there is enough data))
        if segments.size>0:  
            fingers_erp_mean[f - 1]=np.mean(segments, axis=0)
        else:
            fingers_erp_mean[f - 1]=np.zeros(1201) 
            print(f"THERE IS NO ENOUGH DATA, TRY AGAIN.")
        
    
    #our range time: (-200 ms to +1000 ms)
    rrange=np.arange(-200,-200+fingers_erp_mean.shape[1])  
    plt.figure(figsize=(10, 6))

    #Plot the averaged ERP for all the fingers
    for i in range(5):
        plt.plot(rrange, fingers_erp_mean[i], label=f'Finger {i+1}')


    plt.xlabel('Time-MS')
    plt.ylabel('Brain Signal-µV')
    plt.title('Averaged Brain Response')
    plt.show()

    print (fingers_erp_mean)
    return fingers_erp_mean





trial_points = 'events_file_ordered.csv'
ecog_data = 'brain_data_channel_one.csv'

fingers_erp_mean = calc_mean_erp(trial_points, ecog_data)