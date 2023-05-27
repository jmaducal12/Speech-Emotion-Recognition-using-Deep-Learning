import streamlit as st
import tensorflow as tf
import librosa
import numpy as np

# Load the pre-trained model
model = tf.keras.models.load_model('ltsm_best_weights1.hdf5')

# Define emotion labels
emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad']

# Function to extract audio features from the uploaded audio file
def extract_features(audio_data):
    audio_bytes = io.BytesIO(audio_data)
    y, sr = librosa.load(audio_bytes, sr=None)
    mfccs = librosa.feature.mfcc(y, sr=sr, n_mfcc=40)
    mfccs_scaled = np.mean(mfccs.T, axis=0)
    return mfccs_scaled

# Main function for creating the Streamlit app
def main():
    st.title('Speech Emotion Recognition')
    st.write('Upload an audio file and check the predicted emotion!')

    audio_file = st.file_uploader('Upload Audio', type=['wav'])

    if audio_file is not None:
        audio_data = audio_file.read()
        st.audio(audio_data, format='audio/wav')

        if st.button('Recognize Emotion'):
            try:
                features = extract_features(audio_data)
                features = np.expand_dims(features, axis=0)
                predicted_probabilities = model.predict(features)[0]
                predicted_emotion = emotion_labels[np.argmax(predicted_probabilities)]
                st.success(f'Predicted Emotion: {predicted_emotion}')
            except Exception as e:
                st.error(f'Error: {e}')

if __name__ == '__main__':
    main()
