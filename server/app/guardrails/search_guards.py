from agents import output_guardrail, GuardrailFunctionOutput, Runner
from app.models.web_search import WebSearchResponse
import logging

logger = logging.getLogger("IRIS-Guardrails")

# can implement a checker () agent , to pass the context (ctx)

@output_guardrail
async def search_guardrail(ctx, agent, message) -> GuardrailFunctionOutput:
    """
    Validates Web Search results for malicious URLs or unsafe content.

    Args:
        ctx: Execution context (contains conversation history, tools, etc.)
        agent: The agent that generated the message (Search Specialist)
        message: The output from the agent (likely a string or WebSearchResponse)
    """
    logger.info("🛡️ Running Web Search Guardrail...")

    try:

        if isinstance(message, WebSearchResponse):
            results = message.results
        else:

            logger.warning(
                "Guardrail received non-WebSearchResponse object. Skipping deep check."
            )
            return GuardrailFunctionOutput(
                is_valid=True, reason="Output format not suitable for deep URL check."
            )

        # 2. Check for Blocked Domains
        blocked_domains = ["malware-site.com", "spam.net", "phishing-example.com"]
        suspicious_urls = [
            r.url for r in results if any(domain in r.url for domain in blocked_domains)
        ]

        if suspicious_urls:
            logger.warning(
                f"🚫 Guardrail Triggered: Blocked domains found: {suspicious_urls}"
            )
            return GuardrailFunctionOutput(
                is_valid=False,
                reason=f"Search results contain blocked domains: {suspicious_urls}",
                corrected_output=None,
                tripwire_triggered=True,  
            )

        logger.info("✅ Search Guardrail Passed")
        return GuardrailFunctionOutput(
            tripwire_triggered=False,
            output_info={"status": "skipped", "reason": "Invalid output type"},
        )

    except Exception as e:
        logger.error(f"❌ Guardrail Execution Failed: {e}")

        return GuardrailFunctionOutput(
            is_valid=True, reason=f"Guardrail error: {str(e)}", tripwire_triggered=False
        )
