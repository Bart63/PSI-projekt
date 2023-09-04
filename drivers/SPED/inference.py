import numpy as np
import tensorflow as tf
from keras import losses
from keras.utils import custom_object_scope
import os


policy_loss_weight = 1
ticks_left_loss_weight = 0.01
ticks_last_loss_weight = 0.01

def policy_loss_fn(y_true, y_pred):
    return losses.SparseCategoricalCrossentropy()(y_true, y_pred, sample_weight=policy_loss_weight)

def ticks_left_loss_fn(y_true, y_pred):
    return losses.MeanAbsolutePercentageError()(y_true, y_pred, sample_weight=ticks_left_loss_weight)

def ticks_last_loss_fn(y_true, y_pred):
    return losses.MeanAbsolutePercentageError()(y_true, y_pred, sample_weight=ticks_last_loss_weight)


current_directory = os.getcwd()
model_path = os.path.join(current_directory, 'drivers/SPED/model_sped.h5')

with custom_object_scope({
    'policy_loss_fn': policy_loss_fn,
    'ticks_left_loss_fn': ticks_left_loss_fn,
    'ticks_last_loss_fn': ticks_last_loss_fn
}):
    model = tf.keras.models.load_model(model_path, compile=False)




converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()
class predictor:
    def __init__(self, height, width):
        interpreter = tf.lite.Interpreter(model_content=tflite_model)
        self.input_details = interpreter.get_input_details()
        size = max((height, width))
        interpreter.resize_tensor_input(self.input_details[0]['index'], (1, size, size, 29))
        self.output_details = interpreter.get_output_details()
        interpreter.allocate_tensors()
        self.interpreter = interpreter

    def predict(self, map_tensor):
        map_tensor = np.expand_dims(map_tensor, axis=0)
        map_tensor = np.transpose(map_tensor, axes=(0, 2, 3, 1))
        map_tensor = map_tensor.astype(np.float32)
        self.interpreter.set_tensor(self.input_details[0]['index'], map_tensor)
        self.interpreter.invoke()
        pi = self.interpreter.get_tensor(self.output_details[1]['index'])[0]
        last_xroad = self.interpreter.get_tensor(self.output_details[0]['index'])[0][0]
        left = self.interpreter.get_tensor(self.output_details[2]['index'])[0][0]
        left = max((left, 0))
        last_xroad = max((last_xroad, 0))

        return pi, left, last_xroad
