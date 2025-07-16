import unittest
from langsmith.evaluation import evaluate
from app.agents.support_agent import SupportAgent

class TestLangSmithIntegration(unittest.TestCase):
    def test_response_quality(self):
        agent = SupportAgent()
        
        def evaluator(inputs, outputs):
            return {"score": 1 if "thank you" in outputs.lower() else 0}
        
        test_cases = [
            {"input": "How do I reset my password?", "expected": "thank you"}
        ]
        
        results = evaluate(
            agent.respond,
            data=test_cases,
            evaluators=[evaluator],
            experiment_prefix="support-bot"
        )
        
        print("Evaluation results:", results)

import unittest
from app.services.support_agent import SupportAgent

class TestLangSmithIntegration(unittest.TestCase):
    def test_response_generation(self):
        agent = SupportAgent()
        response = agent.generate_response("چگونه پسورد خود را ریست کنم؟")
        self.assertIn("پسورد", response)
        self.assertIn("ریست", response)