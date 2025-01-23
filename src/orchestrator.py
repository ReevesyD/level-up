from openai import OpenAI
from typing import Dict, Any
from .chains import ProfileChain, JobChain, GapChain, LearningChain
from .models import ProfileSkills, JobRequirements, GapAnalysis, LearningPath

class ChainOrchestrator:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.profile_chain = ProfileChain(self.client)
        self.job_chain = JobChain(self.client)
        self.gap_chain = GapChain(self.client)
        self.learning_chain = LearningChain(self.client)
    
    def execute_chain(self, profile_text: str, job_text: str) -> Dict[str, Any]:
        """
        Execute the full chain of analysis from profile and job listing to learning path.
        
        Args:
            profile_text: The text content of the LinkedIn profile
            job_text: The text content of the job listing
            
        Returns:
            Dict containing the results of each step of the analysis
        """
        try:
            # Step 1: Analyze profile
            profile_skills = self.profile_chain.analyze_profile(profile_text)
            
            # Step 2: Analyze job requirements
            job_requirements = self.job_chain.analyze_job(job_text)
            
            # Step 3: Analyze skill gaps
            gaps = self.gap_chain.analyze_gaps(profile_skills, job_requirements)
            
            # Step 4: Generate learning path
            learning_path = self.learning_chain.generate_path(gaps)
            
            return {
                "profile_analysis": profile_skills.model_dump(),
                "job_requirements": job_requirements.model_dump(),
                "skill_gaps": gaps.model_dump(),
                "learning_path": learning_path.model_dump()
            }
            
        except Exception as e:
            raise Exception(f"Error in chain execution: {str(e)}")
