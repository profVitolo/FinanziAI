class AssetRules:

    @staticmethod
    def evaluate(asset_analysis):
        messages = []

        messages.extend(AssetRules.check_rsi(asset_analysis))
        messages.extend(AssetRules.check_volatility(asset_analysis))
        messages.extend(AssetRules.check_trend(asset_analysis))
        messages.extend(AssetRules.check_beta(asset_analysis))

        return {
            "messages": messages,
            "summary": {
                "message_count": len(messages),
                "highest_severity":
                    AssetRules._highest_severity(messages)
            }
        }
	
	@staticmethod
	def check_rsi(asset_analysis):
		messages = []
		rsi = asset_analysis["indicators"].get("rsi")

		if rsi is None:
			return messages

		if rsi > 70:
			messages.append({
				"type": "rsi",
				"severity": "medium",
				"message":
					f"RSI a {rsi:.1f}: possibile ipercomprato."
			})
		elif rsi < 30:
			messages.append({
				"type": "rsi",
				"severity": "medium",
				"message":
					f"RSI a {rsi:.1f}: possibile ipervenduto."
			})

		return messages
		
	@staticmethod
	def check_volatility(asset_analysis):
		messages = []
		level = (asset_analysis["analysis"].get("volatility_level"))

		if level == "high":
			messages.append({
				"type": "volatility",
				"severity": "medium",
				"message":
					"L'asset presenta volatilità elevata."
			})

		return messages
		
	@staticmethod
	def check_trend(asset_analysis):
		messages = []
		trend = (asset_analysis["analysis"].get("trend"))

		if trend == "bullish":
			messages.append({
				"type": "trend",
				"severity": "low",
				"message":
					"Trend positivo."
			})
		elif trend == "bearish":
			messages.append({
				"type": "trend",
				"severity": "medium",
				"message":
					"Trend negativo."
			})

		return messages
		
	@staticmethod
	def check_beta(asset_analysis):
		messages = []
		beta = (asset_analysis["asset"].get("beta"))

		if beta is None:
			return messages

		if beta > 1.5:
			messages.append({
				"type": "beta",
				"severity": "medium",
				"message":
					f"Beta elevato ({beta:.2f})."
			})
		elif beta < 0.7:
			messages.append({
				"type": "beta",
				"severity": "low",
				"message":
					f"Beta contenuto ({beta:.2f})."
			})

		return messages