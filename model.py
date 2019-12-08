from matplotlib import pyplot as plt
import numpy as np


def summarize_diagnostics(history):
    # plot loss
    plt.subplot(211)
    plt.title('Cross Entropy Loss')
    plt.plot(history.history['loss'], color='blue', label='train')
    plt.plot(history.history['val_loss'], color='orange', label='val')
    # plot accuracy
    plt.subplot(212)
    plt.title('Classification Accuracy')
    plt.plot(history.history['acc'], color='blue', label='train')
    plt.plot(history.history['val_acc'], color='orange', label='val')
    plt.legend()
    # save plot to file
    plt.show()
    plt.close()

def classification_training(train_data, train_label, validation_data ,model, epochs = 10, batch_size = 32):

    training = model.fit(train_data, train_label, epochs=epochs, batch_size=batch_size, validation_data=validation_data, verbose=0)
    summarize_diagnostics(training)
