#!/usr/bin/env python3
"""
QAModule:
  Retrieves relevant wiki passages via KnowledgeBase,
  then calls an LLM (OpenAI or local) to generate an answer.
"""

import os
from openai import OpenAI
from knowledge_base import KnowledgeBase

class QAModule:
    def __init__(self, api_key: str = None):
        self.kb = KnowledgeBase()
        self.client = OpenAI(api_key=api_key) if api_key else None

    def answer(self, question: str) -> str:
        # 1) Retrieve contexts
        contexts = self.kb.retrieve(question, top_k=3)
        prompt = "Use these Star Wars facts to answer:\n"
        for ctx in contexts:
            prompt += f"- {ctx['text']}\n"
        prompt += f"\nQ: {question}\nA:"

        # 2) Generate with LLM
        if self.client:
            resp = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role":"user","content":prompt}],
                max_tokens=150
            )
            return resp.choices[0].message.content.strip()
        else:
            return "Error: No LLM configured."
