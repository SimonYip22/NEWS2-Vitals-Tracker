# Vitals Tracker CLI - Notes

## Day 1: Input & Data Structure

**Goals**  
- Define which patient vitals to track (BP, HR, Temp, O₂)  
- Implement robust input handling  
- Store patient data efficiently  

**Goals Explanation**  
- Track essential vitals for monitoring patient status  
- Ensure inputs are validated to avoid incorrect data  
- Use data structures that allow easy retrieval and future computation (alerts, trend visualization)  

**Plan / Thoughts**  
- Create a Python dictionary keyed by patient ID for each set of vitals  
- Prompt the user for each vital using `input()`  
- Validate numerical ranges for each vital sign  
- Store each patient entry as a dictionary inside a list to allow multiple patient tracking  

**Reflection**  
- Input validation is critical for reliability in CLI tools  
- Organizing data early simplifies future alerting and visualization features  
- Using dictionaries allows easy access and expansion (timestamps, notes, additional vitals)