from collections import defaultdict


class PortfolioRules:

    @staticmethod
    def evaluate(portfolio):
        messages = []

        messages.extend(PortfolioRules.check_concentration(portfolio))
        messages.extend(PortfolioRules.check_diversification(portfolio))
        messages.extend(PortfolioRules.check_sector_exposure(portfolio))
        messages.extend(PortfolioRules.check_country_exposure(portfolio))
        messages.extend(PortfolioRules.check_currency_exposure(portfolio))
        messages.extend(PortfolioRules.check_market_cap_exposure(portfolio))
        messages.extend(PortfolioRules.check_portfolio_beta(portfolio))

        return {
            "messages": messages,
            "summary": {
                "message_count": len(messages),
                "highest_severity": PortfolioRules._highest_severity(messages)
            }
        }

    @staticmethod
    def check_concentration(portfolio):
        messages = []

        risk = portfolio.get("risk", {})
        largest_weight = risk.get("largest_position_weight", 0)

        if largest_weight > 50:
            messages.append({
                "type": "concentration",
                "severity": "high",
                "message": (
                    f"La posizione principale pesa "
                    f"{largest_weight:.2f}% del portafoglio."
                )
            })
        elif largest_weight > 25:
            messages.append({
                "type": "concentration",
                "severity": "medium",
                "message": (
                    f"La posizione principale pesa "
                    f"{largest_weight:.2f}% del portafoglio."
                )
            })

        return messages

    @staticmethod
    def check_diversification(portfolio):
        messages = []

        positions = portfolio.get("positions", [])

        if len(positions) < 3:
            messages.append({
                "type": "diversification",
                "severity": "medium",
                "message": (
                    f"Il portafoglio contiene solo "
                    f"{len(positions)} asset."
                )
            })

        return messages

    @staticmethod
    def check_sector_exposure(portfolio):
        messages = []

        exposures = PortfolioRules._aggregate_by_field(portfolio, "sector")

        for sector, weight in exposures.items():
            if not sector:
                continue

            if weight > 70:
                messages.append({
                    "type": "sector_exposure",
                    "severity": "high",
                    "message": (
                        f"Il settore '{sector}' rappresenta "
                        f"{weight:.2f}% del portafoglio."
                    )
                })
            elif weight > 50:
                messages.append({
                    "type": "sector_exposure",
                    "severity": "medium",
                    "message": (
                        f"Il settore '{sector}' rappresenta "
                        f"{weight:.2f}% del portafoglio."
                    )
                })

        return messages

    @staticmethod
    def check_country_exposure(portfolio):
        messages = []

        exposures = PortfolioRules._aggregate_by_field(portfolio,"country")

        for country, weight in exposures.items():
            if not country:
                continue

            if weight > 80:
                messages.append({
                    "type": "country_exposure",
                    "severity": "medium",
                    "message": (
                        f"Il paese '{country}' rappresenta "
                        f"{weight:.2f}% del portafoglio."
                    )
                })

        return messages

    @staticmethod
    def check_currency_exposure(portfolio):
        messages = []

        exposures = PortfolioRules._aggregate_by_field(portfolio,"currency")

        for currency, weight in exposures.items():
            if not currency:
                continue

            if weight > 80:
                messages.append({
                    "type": "currency_exposure",
                    "severity": "medium",
                    "message": (
                        f"La valuta '{currency}' rappresenta "
                        f"{weight:.2f}% del portafoglio."
                    )
                })

        return messages
    
    @staticmethod
    def check_market_cap_exposure(portfolio):
        messages = []
        small_cap_weight = 0

        for position in portfolio.get("positions", []):
            market_cap = position.get("market_cap")
            value = position.get("market_value_base", 0)

            if market_cap and market_cap < 2_000_000_000:
                small_cap_weight += value

        portfolio_value = portfolio.get("portfolio_value", 0)

        if portfolio_value > 0:
            weight = small_cap_weight / portfolio_value * 100

            if weight > 50:
                messages.append({
                    "type": "small_cap_exposure",
                    "severity": "medium",
                    "message":
                        f"Le small cap rappresentano {weight:.2f}% del portafoglio."
                })

        return messages
    
    @staticmethod
    def check_portfolio_beta(portfolio):
        messages = []
        total_value = portfolio.get("portfolio_value", 0)

        if total_value <= 0:
            return messages

        weighted_beta = 0

        for position in portfolio.get("positions", []):
            beta = position.get("beta")

            if beta is None:
                continue

            weight = (position.get("market_value_base", 0) / total_value)
            weighted_beta += beta * weight

        if weighted_beta > 1.5:
            messages.append({
                "type": "portfolio_beta",
                "severity": "high",
                "message":
                    f"Beta medio del portafoglio elevato ({weighted_beta:.2f})."
            })

        return messages
    
    @staticmethod
    def _highest_severity(messages):
        if not messages:
            return None

        priority = {"info": 1, "medium": 2, "high": 3}
        highest = None

        for message in messages:
            severity = message.get("severity", "info")

            if (highest is None or priority.get(severity, 0) > priority.get(highest, 0)):
                highest = severity

        return highest
    
    @staticmethod
    def _aggregate_by_field(portfolio, field):
        positions = portfolio.get("positions", [])
        portfolio_value = portfolio.get("portfolio_value", 0)

        result = defaultdict(float)

        if portfolio_value <= 0:
            return result

        for position in positions:
            value = position.get("market_value_base", 0) or 0
            key = position.get(field)

            if key is None:
                continue

            result[key] += (value / portfolio_value) * 100

        return dict(result)