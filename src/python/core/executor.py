"""
AXIMA Execution Coordinator — Replaces isolated routing with cooperative execution.

Decides:
  - Which plugin(s) to use
  - In what order
  - Whether multiple plugins cooperate
  - How results merge

Uses PluginRegistry for discovery-based routing.

Usage:
    from core.executor import ExecutionCoordinator, get_executor

    executor = get_executor()
    result = executor.execute(context)
    # result.answer, result.engine, result.cooperating_engines
"""

import time
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

from core import Plugin, Result, Context, ResultStatus, PluginRegistry


# ═══════════════════════════════════════════════════════════════
# EXECUTION PLAN
# ═══════════════════════════════════════════════════════════════

@dataclass
class ExecutionStep:
    """A single step in an execution plan."""
    plugin_name: str
    confidence: float = 0.0
    reason: str = ""
    is_primary: bool = False
    is_cooperative: bool = False


@dataclass
class ExecutionResult:
    """Result from the execution coordinator."""
    primary_result: Optional[Result] = None
    supplementary_results: List[Result] = field(default_factory=list)
    execution_plan: List[ExecutionStep] = field(default_factory=list)
    total_latency_ms: float = 0.0
    cooperating_engines: List[str] = field(default_factory=list)

    @property
    def answer(self) -> str:
        if self.primary_result:
            return self.primary_result.answer
        return ""

    @property
    def succeeded(self) -> bool:
        return self.primary_result is not None and self.primary_result.succeeded

    def merged_answer(self) -> str:
        """Merge primary and supplementary results."""
        parts = []
        if self.primary_result and self.primary_result.answer:
            parts.append(self.primary_result.answer)
        for r in self.supplementary_results:
            if r.answer and r.answer not in parts:
                parts.append(r.answer)
        return '\n\n'.join(parts)


# ═══════════════════════════════════════════════════════════════
# EXECUTION COORDINATOR
# ═══════════════════════════════════════════════════════════════

class ExecutionCoordinator:
    """Coordinates plugin execution with cooperation and fallback.
    
    Instead of hardcoded if/elif routing, the coordinator:
    1. Asks all plugins "can you handle this?"
    2. Builds an execution plan (primary + cooperative)
    3. Executes in order with fallback
    4. Merges results if multiple plugins contribute
    """

    def __init__(self, registry: Optional[PluginRegistry] = None):
        self._registry = registry or PluginRegistry()
        self._cooperation_threshold = 0.6  # Min confidence for cooperative execution
        self._fallback_threshold = 0.3     # Min confidence for fallback attempt

    def register_plugin(self, plugin: Plugin):
        """Register a plugin for execution."""
        self._registry.register(plugin)

    def execute(self, context: Context) -> ExecutionResult:
        """Execute a query using the best available plugin(s).
        
        The coordinator:
        1. Routes to the most confident plugin
        2. If multiple plugins score high, runs them cooperatively
        3. Falls back through lower-confidence plugins on failure
        """
        start = time.time()
        exec_result = ExecutionResult()

        # Score all plugins
        scored = self._registry.route(context)
        if not scored:
            exec_result.primary_result = Result(
                status=ResultStatus.UNSUPPORTED,
                answer="No plugin available to handle this query.",
                engine="coordinator",
            )
            exec_result.total_latency_ms = (time.time() - start) * 1000
            return exec_result

        # Build execution plan
        plan = self._build_plan(scored)
        exec_result.execution_plan = plan

        # Execute primary
        primary_step = next((s for s in plan if s.is_primary), None)
        if primary_step:
            plugin = self._registry.get(primary_step.plugin_name)
            if plugin:
                result = self._safe_execute(plugin, context)
                if result.succeeded:
                    exec_result.primary_result = result
                    exec_result.cooperating_engines.append(plugin.name)

        # Execute cooperative plugins (if primary succeeded and others can add value)
        if exec_result.succeeded:
            for step in plan:
                if step.is_cooperative and step.plugin_name not in exec_result.cooperating_engines:
                    plugin = self._registry.get(step.plugin_name)
                    if plugin:
                        result = self._safe_execute(plugin, context)
                        if result.succeeded:
                            exec_result.supplementary_results.append(result)
                            exec_result.cooperating_engines.append(plugin.name)

        # Fallback if primary failed
        if not exec_result.succeeded:
            for step in plan:
                if step.plugin_name == (primary_step.plugin_name if primary_step else ""):
                    continue
                plugin = self._registry.get(step.plugin_name)
                if plugin:
                    result = self._safe_execute(plugin, context)
                    if result.succeeded:
                        exec_result.primary_result = result
                        exec_result.cooperating_engines.append(plugin.name)
                        break

        exec_result.total_latency_ms = (time.time() - start) * 1000
        return exec_result

    def execute_specific(self, plugin_name: str, context: Context) -> Result:
        """Execute a specific plugin by name (bypass routing)."""
        plugin = self._registry.get(plugin_name)
        if not plugin:
            return Result(
                status=ResultStatus.ERROR,
                error_message=f"Plugin '{plugin_name}' not registered",
                engine="coordinator",
            )
        return self._safe_execute(plugin, context)

    def available_plugins(self) -> List[Dict[str, Any]]:
        """List all registered plugins with their health status."""
        plugins = []
        for plugin in self._registry.all():
            health = plugin.health()
            plugins.append({
                "name": plugin.name,
                "version": plugin.version,
                "capabilities": list(plugin.capabilities),
                "healthy": health.get("healthy", False),
            })
        return plugins

    # ─── Internal ───

    def _build_plan(self, scored: List[tuple]) -> List[ExecutionStep]:
        """Build execution plan from scored plugins."""
        plan = []
        primary_set = False

        for plugin, confidence in scored:
            step = ExecutionStep(
                plugin_name=plugin.name,
                confidence=confidence,
            )

            if not primary_set and confidence >= self._fallback_threshold:
                step.is_primary = True
                step.reason = f"Highest confidence ({confidence:.2f})"
                primary_set = True
            elif confidence >= self._cooperation_threshold:
                step.is_cooperative = True
                step.reason = f"Can cooperate ({confidence:.2f})"
            else:
                step.reason = f"Fallback option ({confidence:.2f})"

            plan.append(step)

        return plan

    def _safe_execute(self, plugin: Plugin, context: Context) -> Result:
        """Execute a plugin safely (catch all errors)."""
        try:
            start = time.time()
            result = plugin.process(context)
            result.latency_ms = (time.time() - start) * 1000
            result.engine = plugin.name
            return result
        except Exception as e:
            return Result(
                status=ResultStatus.ERROR,
                engine=plugin.name,
                error_type=type(e).__name__,
                error_message=str(e),
                recovery_hint="Plugin raised an exception",
            )


# ═══════════════════════════════════════════════════════════════
# SINGLETON
# ═══════════════════════════════════════════════════════════════

_executor: Optional[ExecutionCoordinator] = None

def get_executor(registry: Optional[PluginRegistry] = None) -> ExecutionCoordinator:
    """Get the global execution coordinator."""
    global _executor
    if _executor is None:
        _executor = ExecutionCoordinator(registry=registry)
    return _executor
