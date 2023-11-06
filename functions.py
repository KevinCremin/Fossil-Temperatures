
#Jupyter Notebook created by Kevin Cremin
#email = cremin.kev@gmail.com

import pandas as pd


# function returns peak amplitude and frequency between w1 and w2
def mode_w_amp(data,w1,w2):
    idx1 = abs(data['w']-w1).idxmin()
    idx2 = abs(data['w']-w2).idxmin()
    
    idx_mode = data['amp'][idx1:idx2].idxmax()
    mode_w   = data['w'][idx_mode]
    mode_amp = data['amp'][idx_mode]
    
    return [mode_w,mode_amp]


# function takes FTIR specra data and normalizes to the largest peak and 
#   calculates features from the data. Returns a dataframe of features
# Input Data columns ['w','amp']
def feature_setup(data):
    # define feature df column names
    feature_df = pd.DataFrame(data=[],columns=[
                                            '560 w', '560 amp',
                                            '610 w', '610 amp',
                                            '560/610',
                                            '645 shoulder',
                                            '645/610',
                                            '865 shoulder',
                                            '870 w', '870 amp',
                                            '865/870',
                                            '1040 w',
                                            '1425 w', '1425 amp',
                                            '3400 w', '3400 amp'])
    # Normalize data to peak
    data['amp'] = data['amp']/max(data['amp'])
    # temporary dictionary to store features
    temp_dict = {}
    
    # amplitude and wavenumber at ~560 and ~610
    [temp_dict['560 w'], temp_dict['560 amp']] = mode_w_amp(data,w1=550,w2=580)
    [temp_dict['610 w'], temp_dict['610 amp']] = mode_w_amp(data,w1=600,w2=620)
    
    # ratio of the two peaks
    temp_dict['560/610'] = temp_dict['560 amp']/temp_dict['610 amp']
    
    # amplitude of shoulder ~645
    idx_645 = abs(data['w'] - 645).idxmin()
    temp_dict['645 shoulder'] = data['amp'][idx_645]
    # ratio of shoulder to peak
    temp_dict['645/610'] = temp_dict['645 shoulder']/temp_dict['610 amp']
    
    # amplitude of shoulder ~856
    idx_865 = abs(data['w'] - 865).idxmin()
    temp_dict['865 shoulder'] = data['amp'][idx_865]
    
    # amplitude and wavenumber ~870
    [temp_dict['870 w'], temp_dict['870 amp']] = mode_w_amp(data,w1=860,w2=890)
    temp_dict['865/870'] = temp_dict['865 shoulder']/temp_dict['870 amp']
    
    # wavenumber of largest peak ~1040
    temp_dict['1040 w'] = mode_w_amp(data,w1=900,w2=1200)[0]   # Data is normalized to this peak so amplitude is redundent
    [temp_dict['1425 w'], temp_dict['1425 amp']] = mode_w_amp(data,w1=1400,w2=1450)
    [temp_dict['3400 w'], temp_dict['3400 amp']] = mode_w_amp(data,w1=3200,w2=3600)
    
    # append the dictionary to the feature dataframe and return
    feature_df = feature_df.append(temp_dict,ignore_index=True)
    return feature_df
    
    