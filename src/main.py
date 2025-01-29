import os
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from .chains import ProfileChain, JobChain, GapChain, LearningChain
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

def analyze_career_path(profile_path: str, job_path: str, output_dir: str) -> None:
    print("\nStarting Career Skills Gap Analysis")
    
    try:
        # Setup and read files
        client = setup_environment()
        profile_text = read_file(profile_path)
        job_text = read_file(job_path)
        
        # Initialize chains
        profile_chain = ProfileChain(client)
        job_chain = JobChain(client)
        gap_chain = GapChain(client)
        learning_chain = LearningChain(client)
        
        # Run profile and job analysis in parallel using threads
        with ThreadPoolExecutor(max_workers=2) as executor:
            profile_future = executor.submit(profile_chain.analyze_profile, profile_text)
            job_future = executor.submit(job_chain.analyze_job, job_text)
            profile_skills = profile_future.result()
            job_requirements = job_future.result()
        
        # Analyze gaps using both results
        gaps = gap_chain.analyze_gaps(profile_skills, job_requirements)
        
        # Generate learning path
        path = learning_chain.generate_path(gaps)
        
        # Create output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Generate timestamp for output files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save detailed JSON results
        json_output_path = os.path.join(output_dir, f"analysis_results_{timestamp}.json")
        print(f"Saving detailed results to {json_output_path}")
        with open(json_output_path, "w") as f:
            results = {
                "profile_skills": profile_skills.model_dump(),
                "job_requirements": job_requirements.model_dump(),
                "gaps": gaps.model_dump(),
                "learning_path": path.model_dump()
            }
            json.dump(results, f, indent=2)
        
        # Save human-readable summary
        txt_output_path = os.path.join(output_dir, f"analysis_summary_{timestamp}.txt")
        print(f"Saving summary to {txt_output_path}")
        with open(txt_output_path, "w") as f:
            f.write("Career Skills Gap Analysis Summary\n")
            f.write("================================\n\n")
            
            f.write("LinkedIn Profile Analysis\n")
            f.write("------------------------\n")
            f.write(profile_text + "\n\n")
            
            f.write("Job Requirements Analysis\n")
            f.write("-----------------------\n")
            f.write(job_text + "\n\n")
            
            f.write("Skills Gap Analysis\n")
            f.write("------------------\n")
            f.write("Missing Skills:\n")
            for skill in gaps.missing_skills:
                f.write(f"- {skill.skill} (Severity: {skill.severity})\n")
            
            f.write("\nSkills Needing Improvement:\n")
            for skill in gaps.upgrade_needed:
                f.write(f"- {skill.skill}: {skill.current_level} -> {skill.required_level} "
                       f"(Severity: {skill.severity})\n")
            
            f.write("\nLearning Recommendations\n")
            f.write("----------------------\n")
            for item in path.learning_path:
                f.write(f"\nSkill: {item.skill}\n")
                f.write(f"Estimated Time: {item.estimated_time}\n")
                f.write("Resources:\n")
                for resource in item.resources:
                    f.write(f"- {resource.name}: {resource.url} ({resource.type})\n")
                if item.prerequisites:
                    f.write("Prerequisites: " + ", ".join(item.prerequisites) + "\n")
                if item.milestones:
                    f.write("Milestones:\n")
                    for milestone in item.milestones:
                        f.write(f"- {milestone}\n")
        
        print(f"\n✨ Analysis complete!")
        print(f"Detailed results saved to '{json_output_path}'")
        print(f"Summary saved to '{txt_output_path}'")
        
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        raise

def main():
    print("=== Career Skills Gap Analyzer ===\n")
    
    # Get input paths with defaults
    profile_path = input("Enter path to LinkedIn profile text file (default: data/profile.txt): ").strip()
    if not profile_path:
        profile_path = "data/profile.txt"
    
    job_path = input("Enter path to job listing text file (default: data/job.txt): ").strip()
    if not job_path:
        job_path = "data/job.txt"
    
    output_dir = input("Enter output directory path (default: output): ").strip()
    if not output_dir:
        output_dir = "output"
    
    try:
        analyze_career_path(profile_path, job_path, output_dir)
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
