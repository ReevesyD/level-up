# Career Skills Gap Analyzer - Use Cases

## UC1: Skills Gap Analysis
**Actor:** Job Seeker
**Input:** LinkedIn profile URL, job listing URL
**Process:**
1. Extract skills from LinkedIn profile
2. Parse required skills from job listing
3. Identify gaps and match levels
4. Generate gap report
**Output:** Detailed skills gap analysis

## UC2: Learning Path Generation
**Actor:** Job Seeker
**Input:** Skills gap analysis
**Process:**
1. Prioritize skills to acquire
2. Find relevant learning resources
3. Create structured timeline
4. Set progress milestones
**Output:** Personalized learning plan

## Technical Implementation

### Data Structures
```python
@dataclass
class Skill:
    name: str
    level: str  # beginner, intermediate, expert
    source: str  # profile or job_listing
    priority: int  # 1-5, based on job requirement importance

@dataclass
class SkillGap:
    missing_skill: Skill
    current_level: str
    required_level: str
    learning_time_estimate: str

@dataclass
class LearningPath:
    skill_gaps: List[SkillGap]
    courses: List[str]
    estimated_completion_time: str
    milestones: List[str]
```

### Main Flow
1. Profile Analysis
   - LinkedIn data extraction
   - Skill level assessment
   - Experience categorization

2. Gap Analysis
   - Skill matching
   - Level comparison
   - Priority assignment

3. Learning Path
   - Resource identification
   - Timeline creation
   - Progress tracking setup

### Error Handling
- Profile access validation
- Data extraction verification
- Resource availability checking
- Input format validation