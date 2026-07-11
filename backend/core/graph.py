"""Wires the three specialist agents and the aggregator into a LangGraph
StateGraph: fan out from START to bug/security/quality in parallel, then
join at the aggregator."""

from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from backend.agents import bug_agent, quality_agent, security_agent
from backend.core import aggregator
from backend.core.state import ReviewState


def build_graph():
    graph = StateGraph(ReviewState)

    graph.add_node("bug_agent", bug_agent.run)
    graph.add_node("security_agent", security_agent.run)
    graph.add_node("quality_agent", quality_agent.run)
    graph.add_node("aggregator", aggregator.run)

    graph.add_edge(START, "bug_agent")
    graph.add_edge(START, "security_agent")
    graph.add_edge(START, "quality_agent")

    graph.add_edge("bug_agent", "aggregator")
    graph.add_edge("security_agent", "aggregator")
    graph.add_edge("quality_agent", "aggregator")

    graph.add_edge("aggregator", END)

    return graph.compile()
