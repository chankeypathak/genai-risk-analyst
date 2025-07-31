from transformers import pipeline
import mlflow
import time

def answer_with_llm(query, context_chunks):
    mlflow.start_run(run_name="llm_query")
    prompt = f"Context: {' '.join(context_chunks)}\n\nQuestion: {query}\nAnswer:"
    mlflow.log_param("prompt", prompt)
    start = time.time()
    #generator = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct-v0.2")
    generator = pipeline("text2text-generation", model="google/flan-t5-large")
    result = generator(prompt, max_new_tokens=256)[0]["generated_text"]
    latency = time.time() - start
    mlflow.log_metric("latency", latency)
    mlflow.log_param("query", query)
    mlflow.log_param("context_len", len(context_chunks))
    mlflow.log_text(result, "llm_output.txt")
    mlflow.end_run()
    return result
