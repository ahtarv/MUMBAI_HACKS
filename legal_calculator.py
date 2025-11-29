import re

class LegalCalculator:
    def __init__(self):
        self.supported_calculations = [
            "late_fees", "percentage", "damages", "interest", "penalties"
        ]
    
    def calculate(self, query: str) -> str:
        """Main calculation router"""
        try:
            if any(term in query.lower() for term in ['late', 'fee', 'rent']):
                return self._calculate_late_fee(query)
            elif any(term in query.lower() for term in ['%', 'percent', 'percentage']):
                return self._calculate_percentage(query)
            elif any(term in query.lower() for term in ['damage', 'compensation', 'award']):
                return self._calculate_damages(query)
            else:
                return self._calculate_general(query)
        except Exception as e:
            return f"❌ Calculation error: {str(e)}"
    
    def _calculate_late_fee(self, query: str) -> str:
        """Calculate late fees for rentals or contracts"""
        # Extract numbers from query
        numbers = [float(x) for x in re.findall(r'\d+\.?\d*', query)]
        
        if len(numbers) >= 2:
            rent = numbers[0]
            days_late = numbers[1] if len(numbers) > 1 else 15
            percent = 5  # default late fee percentage
            
            # Look for percentage in query
            percent_match = re.search(r'(\d+)%', query)
            if percent_match:
                percent = float(percent_match.group(1))
            
            daily_fee = (rent * percent / 100) / 30
            total_fee = daily_fee * days_late
            
            return f"""
🧮 **Late Fee Calculation**:

- Rent Amount: ${rent:,.2f}
- Days Late: {days_late}
- Late Fee Rate: {percent}% monthly
- Daily Late Fee: ${daily_fee:.2f}
- **Total Late Fee: ${total_fee:.2f}**

💡 **Legal Note**: Many jurisdictions cap late fees at 5-10% of monthly rent
"""
        else:
            return "❌ Please specify rent amount and days late for calculation"
    
    def _calculate_percentage(self, query: str) -> str:
        """Calculate percentages"""
        numbers = [float(x) for x in re.findall(r'\d+\.?\d*', query)]
        
        if len(numbers) >= 2:
            percentage = numbers[0]
            amount = numbers[1]
            result = (percentage / 100) * amount
            
            return f"""
🧮 **Percentage Calculation**:

- Percentage: {percentage}%
- Amount: ${amount:,.2f}
- **Result: ${result:,.2f}**

💼 **Common Legal Uses**: Commission, royalties, late fees, discounts
"""
        else:
            return "❌ Please specify percentage and amount (e.g., '15% of 2000')"
    
    def _calculate_damages(self, query: str) -> str:
        """Calculate contract damages"""
        numbers = [float(x) for x in re.findall(r'\d+\.?\d*', query)]
        
        if numbers:
            base_amount = numbers[0]
            # Simple multiplier for damages
            multiplier = 1.5  # Typical for consequential damages
            
            return f"""
⚖️ **Damages Estimation**:

- Base Amount: ${base_amount:,.2f}
- Estimated Damages (1.5x): ${base_amount * multiplier:,.2f}
- **Total Potential Award: ${base_amount * (1 + multiplier):,.2f}**

⚠️ **Legal Disclaimer**: Actual damages depend on contract terms and jurisdiction
"""
        else:
            return "❌ Please specify base amount for damages calculation"
    
    def _calculate_general(self, query: str) -> str:
        """General calculation fallback"""
        numbers = [float(x) for x in re.findall(r'\d+\.?\d*', query)]
        
        if numbers:
            total = sum(numbers)
            return f"""
🧮 **General Calculation**:

- Numbers: {', '.join(map(str, numbers))}
- **Sum: {total:,.2f}**

💡 Use specific terms like 'late fee' or 'percentage' for legal calculations
"""
        else:
            return "❌ Please provide numbers for calculation"