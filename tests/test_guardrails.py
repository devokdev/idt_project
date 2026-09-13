import pytest
from services.guardrails_service import guardrails_service
from services.routing_service import routing_service
from services.hallucination_service import hallucination_service

def test_guardrail_valid_input():
    res = guardrails_service.validate_input("How to structure my project architecture?")
    assert res["is_valid"] is True

def test_guardrail_blocked_input():
    res = guardrails_service.validate_input("How to hack into university database and steal marks?")
    assert res["is_valid"] is False
    assert "Security Guardrail" in res["reason"]

def test_routing_service_logic():
    code_route = routing_service.route_model("Write a python function to parse AST")
    assert code_route["selected_model"] == "openai/gpt-oss-120b"

    arch_route = routing_service.route_model("Explain the complete microservices architecture and system design trade-offs")
    assert arch_route["selected_model"] == "openai/gpt-oss-20b"

    simple_route = routing_service.route_model("What is Git?")
    assert simple_route["selected_model"] == "groq/compound-mini"

def test_hallucination_service():
    context = [{"content": "Technical implementation carries 35 marks out of 100 in the rubric."}]
    answer = "The technical implementation section has a weightage of 35 marks out of 100."
    h_eval = hallucination_service.analyze_hallucination(answer, context)
    
    assert h_eval["groundedness_score"] > 0.6
    assert h_eval["supported_claims_count"] >= 1
