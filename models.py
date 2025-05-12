# For now, we don't need database models for this application
# If needed in the future, can be added using SQLAlchemy as per the blueprint

class FoodSafetyKnowledge:
    """
    Static knowledge base for food safety (simplified example)
    In a production environment, this would be stored in a database
    """
    
    # Common medication-food interactions
    INTERACTIONS = {
        "warfarin": ["green leafy vegetables", "cranberries", "grapefruit"],
        "statins": ["grapefruit", "grapefruit juice"],
        "antibiotics": ["dairy", "alcohol", "caffeine"],
        "maoi": ["aged cheese", "cured meats", "draft beer", "sauerkraut", "soy sauce"],
        "ace inhibitors": ["bananas", "potassium supplements", "salt substitutes"],
        "digoxin": ["high-fiber foods", "licorice"],
        "diuretics": ["licorice", "alcohol"],
        "thyroid medication": ["soy", "walnuts", "high-fiber foods"],
    }
    
    # Common dietary restrictions
    ALLERGIES = [
        "peanuts", "tree nuts", "milk", "eggs", "fish", "shellfish", 
        "soy", "wheat", "gluten", "sesame"
    ]
    
    # Medical conditions with dietary restrictions
    CONDITIONS = {
        "diabetes": ["sugar", "high carbs", "honey", "syrup"],
        "hypertension": ["salt", "sodium", "cured meats", "pickles", "canned soups"],
        "high cholesterol": ["saturated fats", "trans fats", "fatty meats"],
        "gout": ["red meat", "organ meats", "seafood", "alcohol", "high-fructose"],
        "kidney disease": ["phosphorus", "potassium", "sodium", "protein"],
        "celiac": ["gluten", "wheat", "barley", "rye"],
        "heart disease": ["saturated fat", "trans fat", "cholesterol", "sodium"],
        "ibs": ["dairy", "wheat", "citrus fruits", "beans", "cabbage"],
    }
    
    @staticmethod
    def get_risky_foods_for_medication(medication_name):
        """Returns foods that might interact with the given medication"""
        medication_name = medication_name.lower()
        for med, foods in FoodSafetyKnowledge.INTERACTIONS.items():
            if med in medication_name or medication_name in med:
                return foods
        return []
    
    @staticmethod
    def get_foods_to_avoid_for_condition(condition):
        """Returns foods to avoid for a given medical condition"""
        condition = condition.lower()
        for cond, foods in FoodSafetyKnowledge.CONDITIONS.items():
            if cond in condition or condition in cond:
                return foods
        return []
