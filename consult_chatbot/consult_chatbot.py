import gradio as gr

from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS


def initialize_consult_bot(vector_store_dir: str="university_index"):
    db = FAISS.load_local(vector_store_dir, OpenAIEmbeddings(), allow_dangerous_deserialization=True)
    llm = ChatOpenAI(model_name="gpt-4-turbo", temperature=0)
    
    global CONSULT_BOT    
    CONSULT_BOT = RetrievalQA.from_chain_type(llm,
                                           retriever=db.as_retriever(search_type="similarity_score_threshold",
                                                                     search_kwargs={"score_threshold": 0.5}))

    CONSULT_BOT.return_source_documents = True

    return CONSULT_BOT


def consult_chat(message, history, province, score, position):
    print(f"[message]{message}")
    print(f"[history]{history}")
    print(f"[score]{score}")
    print(f"[position]{position}")
    if score == 0 or position == 20000000 or province == "默认":
        return "可以告诉我您在哪个省份，考了多少分以及位次是多少吗？请填写在下方additional_inputs展开界面中"
    if score < 600 or position > 5000:
        return "您好，您今年的分数不太适合填报我校，感谢您对我校的关注！"
        
    res = ""
    consult_result = CONSULT_BOT({"query": message})
    print(consult_result)
    if consult_result["source_documents"]:
        res += consult_result["result"]
    else:
        res += "\n这个问题我也不是很清楚，先记录下来，如果有清楚的答案了再回复你。"
    
    return res
    
    
def launch_gradio():
    province = gr.Dropdown(["默认", "北京", "上海", "江苏","四川","云南","湖北","湖南","新疆"], label="省份", info="生源省份")
    score = gr.Number(value=0, precision=0, minimum=0, maximum=750, label="分数")
    position = gr.Number(value=20000000, precision=0, minimum=1, maximum=20000000, label="位次")

    demo = gr.ChatInterface(
        fn=consult_chat,
        title="某高校高考招生咨询",
        chatbot=gr.Chatbot(height=600),
        additional_inputs=[province, score, position]
    )
    demo.launch(share=True, server_name="0.0.0.0")

if __name__ == "__main__":
    initialize_consult_bot()
    launch_gradio()
