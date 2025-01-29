import os
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from .chains import (
    SkillExtractor, RequirementAnalyzer,
    SkillGapAnalyzer, PathwayPlanner
)
import sys
import json

def setup_environment() -> OpenAI:
    print("Loading environment variables...")
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    return OpenAI(api_key=api_key)

def read_file(file_path: str) -> str:
    try:
        print(f"Reading file: {file_path}")
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {str(e)}")
        raise

def save_analysis_results(results: dict, output_dir: str) -> str:
    """Save analysis results to a human-readable format."""
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Generate timestamp for output file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_dir, f"analysis_summary_{timestamp}.txt")
    
    print(f"Saving results to {output_path}")
    with open(output_path, "w") as f:
        f.write("Career Skills Gap Analysis Summary\n")
        f.write("================================\n\n")
        
        # Profile Analysis
        f.write("LinkedIn Profile Skills\n")
        f.write("----------------------\n")
        for skill in results["profile_skills"]["technical_skills"]:
            f.write(f"- {skill['name']} ({skill['level']}, {skill['years']} experience)\n")
        f.write("\nSoft Skills:\n")
        for skill in results["profile_skills"]["soft_skills"]:
            f.write(f"- {skill['skill']}\n")
            for example in skill["examples"]:
                f.write(f"  • {example}\n")
        f.write("\n")
        
        # Job Analysis
        f.write("Job Requirements\n")
        f.write("---------------\n")
        f.write(f"Minimum Experience: {results['job_requirements']['min_experience']}\n\n")
        f.write("Required Technical Skills:\n")
        for skill in results["job_requirements"]["required_skills"]:
            must_have = "Required" if skill["must_have"] else "Nice to have"
            f.write(f"- {skill['name']} ({skill['level']}) - {must_have}\n")
        f.write("\nRequired Soft Skills:\n")
        for skill in results["job_requirements"]["soft_skills"]:
            f.write(f"- {skill}\n")
        f.write("\n")
        
        # Gap Analysis
        f.write("Skills Gap Analysis\n")
        f.write("------------------\n")
        f.write("Missing Skills:\n")
        for skill in results["gaps"]["missing_skills"]:
            f.write(f"- {skill['skill']} (Severity: {skill['severity']})\n")
        f.write("\nSkills Needing Improvement:\n")
        for skill in results["gaps"]["upgrade_needed"]:
            f.write(f"- {skill['skill']}: {skill['current_level']} -> {skill['required_level']} "
                   f"(Severity: {skill['severity']})\n")
        f.write("\n")
        
        # Learning Path
        f.write("Learning Recommendations\n")
        f.write("----------------------\n")
        for item in results["learning_path"]["learning_path"]:
            f.write(f"\nSkill: {item['skill']}\n")
            f.write(f"Estimated Time: {item['estimated_time']}\n")
            f.write("Resources:\n")
            for resource in item["resources"]:
                f.write(f"- {resource['name']}: {resource['url']} ({resource['type']})\n")
            if item["prerequisites"]:
                f.write("Prerequisites: " + ", ".join(item["prerequisites"]) + "\n")
            if item["milestones"]:
                f.write("Milestones:\n")
                for milestone in item["milestones"]:
                    f.write(f"- {milestone}\n")
    
    return output_path

def analyze_career_path(profile_path: str, job_path: str, output_dir: str) -> None:
    print("\nStarting Career Skills Gap Analysis")
    
    try:
        # Setup and read files
        client = setup_environment()
        profile_text = read_file(profile_path)
        job_text = read_file(job_path)
        
        # Initialize analyzers
        skill_extractor = SkillExtractor(client)
        requirement_analyzer = RequirementAnalyzer(client)
        gap_analyzer = SkillGapAnalyzer(client)
        pathway_planner = PathwayPlanner(client)
        
        # Run profile and job analysis in parallel using threads
        with ThreadPoolExecutor(max_workers=2) as executor:
            profile_future = executor.submit(skill_extractor.analyze_profile, profile_text)
            job_future = executor.submit(requirement_analyzer.analyze_job, job_text)
            profile_skills = profile_future.result()
            job_requirements = job_future.result()
        
        # Analyze gaps using both results
        gaps = gap_analyzer.analyze_gaps(profile_skills, job_requirements)
        
        # Generate learning path
        path = pathway_planner.generate_path(gaps)
        
        # Save results
        results = {
            "profile_skills": profile_skills.model_dump(),
            "job_requirements": job_requirements.model_dump(),
            "gaps": gaps.model_dump(),
            "learning_path": path.model_dump()
        }
        
        output_path = save_analysis_results(results, output_dir)
        print(f"Analysis complete! Results saved to '{output_path}'")
        
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        raise

def main():
    print("=== Career Skills Gap Analyzer ===\n")
    
    # Get input paths
    profile_path = "data/profile.txt"
    job_path = "data/job.txt"
    output_dir = "output"
    
    try:
        analyze_career_path(profile_path, job_path, output_dir)
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
