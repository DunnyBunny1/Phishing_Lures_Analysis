# Source Organization 
# High-Level Approach

# Challenges Faced 
- Dealing with edge cases: distinguishing if this domain has 3 matching target terms or 2 target terms
```python
('gmail.mass.gov', ['gmail', 'mail', '.gov'])
```
- Decided to count both - may increase false positive rates but will reduce false negative rates
Graph: 
- Assumed that each team member has one lead (parent), but any team lead can have multiple team members (children)
# Testing Overview
# Resources Used 
- Python official docs 