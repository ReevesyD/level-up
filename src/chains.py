from openai import OpenAI
from typing import Dict, Any
import json
import logging
from .models import (
    ProfileSkills, JobRequirements, GapAnalysis, LearningPath
)

logger = logging.getLogger('skills_gap_analyzer')

class BaseChain:
    def __init__(self, client: OpenAI):
        self.client = client
        self.model = "gpt-4-turbo-preview"
    
    def _call_openai(self, prompt: str) -> Dict[str, Any]:
        try:
            logger.info("🤖 Calling OpenAI API...")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            logger.debug("Received response from OpenAI")
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"❌ OpenAI API error: {str(e)}")
            raise Exception(f"OpenAI API error: {str(e)}")

class ProfileChain(BaseChain):
    def analyze_profile(self, profile_text: str) -> ProfileSkills:
        logger.info("📊 Analyzing LinkedIn profile...")
        prompt = """
        Analyze this LinkedIn profile and extract:
        1. Technical skills with experience level (Beginner/Intermediate/Expert)
        2. Soft skills with demonstrated examples
        3. Years of experience in each area

        Profile:
        {profile_text}

        Respond with a JSON object in this exact format:
        {{
            "technical_skills": [
                {{
                    "name": "skill name",
                    "level": "skill level",
                    "years": "years of experience"
                }}
            ],
            "soft_skills": [
                {{
                    "skill": "skill name",
                    "examples": ["example 1", "example 2"]
                }}
            ]
        }}
        """
        try:
            result = self._call_openai(prompt.format(profile_text=profile_text))
            skills = ProfileSkills.model_validate(result)
            logger.info(f"✅ Found {len(skills.technical_skills)} technical skills and {len(skills.soft_skills)} soft skills")
            return skills
        except Exception as e:
            logger.error(f"❌ Profile analysis error: {str(e)}")
            raise Exception(f"Profile analysis error: {str(e)}")

class JobChain(BaseChain):
    def analyze_job(self, job_text: str) -> JobRequirements:
        logger.info("📋 Analyzing job requirements...")
        prompt = """
        Analyze this job listing and extract:
        1. Required technical skills with minimum level
        2. Required soft skills
        3. Must-have vs nice-to-have skills

        Job Listing:
        {job_text}

        Respond with a JSON object in this exact format:
        {{
            "required_skills": [
                {{
                    "name": "skill name",
                    "level": "required level",
                    "must_have": true/false
                }}
            ],
            "min_experience": "minimum years required",
            "soft_skills": ["skill 1", "skill 2"]
        }}
        """
        try:
            result = self._call_openai(prompt.format(job_text=job_text))
            requirements = JobRequirements.model_validate(result)
            logger.info(f"✅ Found {len(requirements.required_skills)} required skills and {len(requirements.soft_skills)} soft skills")
            return requirements
        except Exception as e:
            logger.error(f"❌ Job analysis error: {str(e)}")
            raise Exception(f"Job analysis error: {str(e)}")

class GapChain(BaseChain):
    def analyze_gaps(
        self, profile_skills: ProfileSkills, job_requirements: JobRequirements
    ) -> GapAnalysis:
        logger.info("🔍 Analyzing skill gaps...")
        prompt = """
        Compare these profile skills against job requirements and identify:
        1. Missing required skills
        2. Skills needing level improvement
        3. Gap severity (Critical/Moderate/Minor)

        Profile Skills: {profile_skills_json}
        Job Requirements: {job_requirements_json}

        Respond with a JSON object in this exact format:
        {{
            "missing_skills": [
                {{
                    "skill": "skill name",
                    "severity": "Critical/Moderate/Minor"
                }}
            ],
            "upgrade_needed": [
                {{
                    "skill": "skill name",
                    "current_level": "current level",
                    "required_level": "required level",
                    "severity": "Critical/Moderate/Minor"
                }}
            ]
        }}
        """
        try:
            result = self._call_openai(prompt.format(
                profile_skills_json=profile_skills.model_dump_json(),
                job_requirements_json=job_requirements.model_dump_json()
            ))
            gaps = GapAnalysis.model_validate(result)
            logger.info(f"✅ Found {len(gaps.missing_skills)} missing skills and {len(gaps.upgrade_needed)} skills needing improvement")
            return gaps
        except Exception as e:
            logger.error(f"❌ Gap analysis error: {str(e)}")
            raise Exception(f"Gap analysis error: {str(e)}")

class LearningChain(BaseChain):
    def generate_path(self, gaps: GapAnalysis) -> LearningPath:
        logger.info("📚 Generating learning path...")
        prompt = """
        Create a learning path to address these skill gaps:
        1. Recommended learning resources
        2. Estimated time to achieve each skill
        3. Learning sequence with prerequisites
        4. Progress milestones

        Skill Gaps: {gaps_json}

        Respond with a JSON object in this exact format:
        {{
            "learning_path": [
                {{
                    "skill": "skill name",
                    "resources": [
                        {{
                            "name": "resource name",
                            "url": "resource url",
                            "type": "course/tutorial/documentation"
                        }}
                    ],
                    "estimated_time": "estimated completion time",
                    "prerequisites": ["prerequisite 1", "prerequisite 2"],
                    "milestones": ["milestone 1", "milestone 2"]
                }}
            ]
        }}
        """
        try:
            result = self._call_openai(prompt.format(gaps_json=gaps.model_dump_json()))
            path = LearningPath.model_validate(result)
            logger.info(f"✅ Generated learning path with {len(path.learning_path)} skills to learn")
            return path
        except Exception as e:
            logger.error(f"❌ Learning path generation error: {str(e)}")
            raise Exception(f"Learning path generation error: {str(e)}")
