def audio_predict(path, wav_file):
    from IPython.display import Audio
    from IPython.display import Image

    import tensorflow as tf
    from tensorflow import keras
    import os
    import numpy as np 
    import librosa as lr
    import librosa.display
    import wave
    import soundfile as sf
    import math

    os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
    
    # modeli trebaju biti u istom folderu gdje se nalazi i funkcija !
    
    instruments = ["cel", "pia", "tru", "vio", "voi"]

    instruments_validation = [ "flu", "org", "sax", "gel", "gac", "cla"]
    
    bound_instruments = {}
    bound_instruments["cel"] = 0.9
    bound_instruments["cla"] = 0.7
    bound_instruments["gac"] = 0.35
    bound_instruments["pia"] = 0.3
    bound_instruments["tru"] = 0.6
    bound_instruments["vio"] = 0.5
    bound_instruments["voi"] = 0.25
    bound_instruments["flu"] = 0.7
    bound_instruments["org"] = 0.8
    bound_instruments["gel"] = 0.5
    bound_instruments["sax"] = 0.5
        
    file_path = os.path.join(path, wav_file)
    
    duration_seconds = librosa.get_duration(filename=file_path)
    
    n_intervals = math.ceil(duration_seconds / 3)
    
    pred_labels_temp = np.zeros(n_intervals)
    
    n_coef = 20
    
    hop_length = 1024
    
    dict_instruments = {}
    
    for instrument_of_interest in instruments:
        
        print(instrument_of_interest)
        
        model_name = instrument_of_interest + "best_model.h5"
                
        model_temp = keras.models.load_model(model_name)

        for j in range(n_intervals-1):

            y, sr = librosa.load(file_path, mono=True, sr=None, offset=j*3.0, duration=3.0)

            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_coef, hop_length=hop_length)

            mfcc = mfcc.reshape(-1,n_coef,130,1)

            pred_labels_temp[j] = model_temp.predict(mfcc,)


        y, sr = librosa.load(file_path, mono=True, sr=None, offset=duration_seconds-3.0, duration=3.0)

        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_coef, hop_length=hop_length)

        mfcc = mfcc.reshape(-1,n_coef,130,1)
        
        pred_labels_temp[n_intervals-1] = model_temp.predict(mfcc,)
        
        print(pred_labels_temp)

        boundary = bound_instruments[instrument_of_interest]

        jedinice = np.count_nonzero(pred_labels_temp >= boundary)
        
        nule = n_intervals - jedinice

        if (jedinice >= nule):
            
            dict_instruments[instrument_of_interest] = 1
            
        else:
            
            dict_instruments[instrument_of_interest] = 0
            
    for instrument_of_interest in instruments_validation:
        
        print(instrument_of_interest)

        
        model_name = instrument_of_interest +'_best_model_vali_test_AUGMENTATED_FINAL_test2.h5' 
        
        model_temp = keras.models.load_model(model_name)

        for j in range(n_intervals-1):

            y, sr = librosa.load(file_path, mono=True, sr=None, offset=j*3.0, duration=3.0)

            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_coef, hop_length=hop_length)

            mfcc = mfcc.reshape(-1,n_coef,130,1)

            pred_labels_temp[j] = model_temp.predict(mfcc,)


        y, sr = librosa.load(file_path, mono=True, sr=None, offset=duration_seconds-3.0, duration=3.0)

        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_coef, hop_length=hop_length)

        mfcc = mfcc.reshape(-1,n_coef,130,1)
        
        pred_labels_temp[n_intervals-1] = model_temp.predict(mfcc,)
        
        print(pred_labels_temp)

        boundary = bound_instruments[instrument_of_interest]

        jedinice = np.count_nonzero(pred_labels_temp >= boundary)
        
        nule = n_intervals - jedinice

        if (jedinice >= nule):
            
            dict_instruments[instrument_of_interest] = 1
            
        else:
            
            dict_instruments[instrument_of_interest] = 0
        

    return dict_instruments
