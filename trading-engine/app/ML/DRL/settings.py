MODEL_STORE_INTERVAL = 10
GRAPH_DRAW_INTERVAL = 10
PRINT_STATUS_INTERVAL = 60

INDICATOR_NUM = 26

N_TRAIN = 300

ACTION_SIZE = 2
HIDDEN_SIZE = 2 ** 9
BATCH_SIZE = 2 ** 8#9
BUFFER_SIZE = 100000

# Define Actions
LONG = 0
SHORT = 1
HOLD = 2
CLOSE = 3

# Done States
LIQUIFIED = 0
DATA_DONE = 1

# Reward Value
DEMOCRATISATION = -1000000

MIN_START_POINT = N_TRAIN * 60 * 4 + 1
MAX_START_POINT_FROM = 30 * 24 * 60

def trade_done(env_self):
    env_self.is_data_done = True
    env_self.finish_episode()

def liquified(env_self):
    env_self.is_liquified = True
    env_self.reward_sum += DEMOCRATISATION
    env_self.train_model(DEMOCRATISATION, True)
    env_self.finish_episode()

def get_device():
    import torch
    if torch.cuda.is_available():
        device = torch.device('cuda')
        print(f"CUDA is available. Using GPU: {torch.cuda.get_device_name(device)}")
    elif torch.backends.mps.is_available():
        device = torch.device('mps')
        print("MPS is available. Using GPU on macOS.")
    else:
        device = torch.device('cpu')
        print("No GPU found. Using CPU.")

    return device