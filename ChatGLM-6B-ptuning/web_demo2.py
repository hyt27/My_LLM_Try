from transformers import AutoModel, AutoTokenizer, AutoConfig
import streamlit as st
from streamlit_chat import message
import torch
import os

st.set_page_config(
    page_title="ChatGLM-6b 演示",
    page_icon=":robot:"
)
CHECKPOINT_PATH=f'ChatGLM-6B/ptuning/output/adgen-chatglm-6b-pt-128-2e-2/checkpoint-3000'

@st.cache_resource
def get_model():
    global CHECKPOINT_PATH
    tokenizer = AutoTokenizer.from_pretrained("ChatGLM-6B/THUDM/chatglm-6b", trust_remote_code=True)
    config = AutoConfig.from_pretrained("ChatGLM-6B/THUDM/chatglm-6b", trust_remote_code=True, pre_seq_len=128)
    model = AutoModel.from_pretrained("ChatGLM-6B/THUDM/chatglm-6b", config=config, trust_remote_code=True)
    prefix_state_dict = torch.load(os.path.join(CHECKPOINT_PATH, "pytorch_model.bin"))
    new_prefix_state_dict = {}
    for k, v in prefix_state_dict.items():
        if k.startswith("transformer.prefix_encoder."):
            new_prefix_state_dict[k[len("transformer.prefix_encoder."):]] = v
    model.transformer.prefix_encoder.load_state_dict(new_prefix_state_dict)

    model = model.half().cuda()
    model.transformer.prefix_encoder.float()
    model = model.eval()
    return tokenizer, model


MAX_TURNS = 20
MAX_BOXES = MAX_TURNS * 2


def predict(input, max_length, top_p, temperature, history=None):
    tokenizer, model = get_model()
    if history is None:
        history = []

    with container:
        if len(history) > 0:
            for i, (query, response) in enumerate(history):
                message(query, avatar_style="big-smile", key=str(i) + "_user")
                message(response, avatar_style="bottts", key=str(i))

        message(input, avatar_style="big-smile", key=str(len(history)) + "_user")
        st.write("AI正在回复:")
        with st.empty():
            for response, history in model.stream_chat(tokenizer, input, history, max_length=max_length, top_p=top_p,
                                               temperature=temperature):
                query, response = history[-1]
                st.write(response)

    return history


container = st.container()

# create a prompt text for the text generation
prompt_text = st.text_area(label="用户命令输入",
            height = 100,
            placeholder="请在这儿输入您的命令")

max_length = st.sidebar.slider(
    'max_length', 0, 4096, 2048, step=1
)
top_p = st.sidebar.slider(
    'top_p', 0.0, 1.0, 0.6, step=0.01
)
temperature = st.sidebar.slider(
    'temperature', 0.0, 1.0, 0.95, step=0.01
)

if 'state' not in st.session_state:
    st.session_state['state'] = []

if st.button("发送", key="predict"):
    with st.spinner("AI正在思考，请稍等........"):
        # text generation
        st.session_state["state"] = predict(prompt_text, max_length, top_p, temperature, st.session_state["state"])