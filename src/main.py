import os
from dotenv import load_dotenv
from .orchestrator import ChainOrchestrator
import json
from pathlib import Path
from datetime import datetime
from .logger import setup_logger

def analyze_career_path(profile_path: str, job_path: str, output_dir: str) -> None:
    """
    Analyze career path by comparing LinkedIn profile against job requirements.
    
    Args:
        profile_path: Path to the LinkedIn profile text file
        job_path: Path to the job listing text file
        output_dir: Directory to save output files
    """
    # Set up logging
    logger = setup_logger()
    logger.info("Starting Career Skills Gap Analysis")
    
    # Load OpenAI API key from environment
    logger.info("Loading environment variables...")
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY not found in environment variables")
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    # Read input files
    try:
        logger.info(f"Reading profile from {profile_path}")
        with open(profile_path, 'r') as f:
            profile_text = f.read()
        logger.info(f"Reading job listing from {job_path}")
        with open(job_path, 'r') as f:
            job_text = f.read()
    except FileNotFoundError as e:
        logger.error(f"Input file not found: {str(e)}")
        raise ValueError(f"Input file not found: {str(e)}")
    
    # Initialize orchestrator
    logger.info("Initializing analysis chain...")
    orchestrator = ChainOrchestrator(api_key)
    
    try:
        # Execute analysis chain
        logger.info("Executing analysis chain...")
        results = orchestrator.execute_chain(profile_text, job_text)
        
        # Create output directory if it doesn't exist
        logger.info(f"Creating output directory: {output_dir}")
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Generate timestamp for output files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save detailed JSON results
        json_output_path = os.path.join(output_dir, f"analysis_results_{timestamp}.json")
        logger.info(f"Saving detailed results to {json_output_path}")    
        with open(json_output_path, "w") as f:
            json.dump(results, f, indent=2)
        
        # Save human-readable summary
        txt_output_path = os.path.join(output_dir, f"analysis_summary_{timestamp}.txt")
        logger.info(f"Saving summary to {txt_output_path}")
        with open(txt_output_path, "w") as f:
            f.write("=== Career Path Analysis Results ===\n\n")
            
            f.write("Technical Skills Found:\n")
            for skill in results["profile_analysis"]["technical_skills"]:
                f.write(f"- {skill['name']}: {skill['level']} ({skill['years']} years)\n")
            
            f.write("\nSkill Gaps:\n")
            for gap in results["skill_gaps"]["missing_skills"]:
                f.write(f"- Missing: {gap['skill']} (Severity: {gap['severity']})\n")
            for gap in results["skill_gaps"]["upgrade_needed"]:
                f.write(f"- Upgrade Needed: {gap['skill']} "
                      f"(Current: {gap['current_level']} → Required: {gap['required_level']})\n")
            
            f.write("\nLearning Path:\n")
            for item in results["learning_path"]["learning_path"]:
                f.write(f"\nSkill: {item['skill']}\n")
                f.write(f"Estimated Time: {item['estimated_time']}\n")
                f.write("Resources:\n")
                for resource in item['resources']:
                    f.write(f"- {resource['name']}: {resource['url']}\n")
                f.write("Milestones:\n")
                for milestone in item['milestones']:
                    f.write(f"- {milestone}\n")
        
        # Print results to terminal
        logger.info("\n=== Career Path Analysis Results ===\n")
        
        logger.info("Technical Skills Found:")
        for skill in results["profile_analysis"]["technical_skills"]:
            logger.info(f"- {skill['name']}: {skill['level']} ({skill['years']} years)")
        
        logger.info("\nSkill Gaps:")
        for gap in results["skill_gaps"]["missing_skills"]:
            logger.info(f"- Missing: {gap['skill']} (Severity: {gap['severity']})")
        for gap in results["skill_gaps"]["upgrade_needed"]:
            logger.info(f"- Upgrade Needed: {gap['skill']} "
                  f"(Current: {gap['current_level']} → Required: {gap['required_level']})")
        
        logger.info("\nLearning Path:")
        for item in results["learning_path"]["learning_path"]:
            logger.info(f"\nSkill: {item['skill']}")
            logger.info(f"Estimated Time: {item['estimated_time']}")
            logger.info("Resources:")
            for resource in item['resources']:
                logger.info(f"- {resource['name']}: {resource['url']}")
            logger.info("Milestones:")
            for milestone in item['milestones']:
                logger.info(f"- {milestone}")
        
        logger.info(f"\n✨ Analysis complete!")
        logger.info(f"Detailed results saved to '{json_output_path}'")
        logger.info(f"Summary saved to '{txt_output_path}'")
        
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        raise

def main():
    """
    Main entry point for the career path analyzer.
    """
    print("=== Career Skills Gap Analyzer ===")
    
    # Default paths
    default_profile = "data/profile.txt"
    default_job = "data/job.txt"
    default_output = "output"
    
    # Get input paths from user or use defaults
    profile_path = input(f"\nEnter path to LinkedIn profile text file (default: {default_profile}): ").strip()
    if not profile_path:
        profile_path = default_profile
    
    job_path = input(f"Enter path to job listing text file (default: {default_job}): ").strip()
    if not job_path:
        job_path = default_job
    
    output_dir = input(f"Enter output directory path (default: {default_output}): ").strip()
    if not output_dir:
        output_dir = default_output
    
    # Run analysis
    analyze_career_path(profile_path, job_path, output_dir)

if __name__ == "__main__":
    main()
