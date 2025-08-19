import os
from crewai import Task, Crew, Process
from agents import parser_agent, jd_keywords_agent, ats_agent, improve_agent

def run_resume_workflow(resume_text, job_desc, tasks_to_run=None):
    """
    Runs the resume analysis workflow and returns a dictionary of results.
    """

    if tasks_to_run is None:
        tasks_to_run = ["parse", "keywords", "ats_score", "improvements"]

    results = {}

    try:
        crew_tasks = []

        # Task 1: Resume Parsing
        if "parse" in tasks_to_run:
            parse_task = Task(
                description=f"""
                Parse the following resume and job description.
                Return ONLY valid JSON, no explanations, no extra text.

                Resume: ```{resume_text}```
                Job Description: ```{job_desc}```
                """,
                agent=parser_agent,
                expected_output="Valid JSON object with fields: name, contact, education, experience, skills, match_percentage, summary"
            )
            crew_tasks.append(parse_task)

        # Task 2: JD Keywords
        if "keywords" in tasks_to_run:
            jd_task = Task(
                description=f"""
                Analyze this job description and return ONLY valid JSON.
                Do not add any explanation or extra text.

                Job Description: ```{job_desc}```
                """,
                agent=jd_keywords_agent,
                expected_output="Valid JSON object with categories: must_have_skills, good_to_have_skills, certifications, tools"
            )
            crew_tasks.append(jd_task)

        # Task 3: ATS Evaluation
        if "ats_score" in tasks_to_run:
            ats_task = Task(
                description=f"""
                Compare the resume and job description.
                Return ONLY valid JSON with:
                - score (0-100)
                - matched_keywords
                - missing_keywords
                - reasoning

                Resume: ```{resume_text}```
                Job Description: ```{job_desc}```
                """,
                agent=ats_agent,
                expected_output="Valid JSON object with fields: score, matched_keywords, missing_keywords, reasoning"
            )
            crew_tasks.append(ats_task)

        # Task 4: Improvements
        if "improvements" in tasks_to_run:
            improve_task = Task(
                description=f"""
                Based on ATS analysis, suggest improvements.
                Markdown/text output allowed (not JSON required).

                Resume: ```{resume_text}```
                Job Description: ```{job_desc}```
                """,
                agent=improve_agent,
                expected_output="Improvement suggestions in plain text or markdown"
            )
            crew_tasks.append(improve_task)

        # Run crew
        crew = Crew(
            agents=[parser_agent, jd_keywords_agent, ats_agent, improve_agent],
            tasks=crew_tasks,
            process=Process.sequential,
            verbose=True
        )

        final_result = crew.kickoff()

        for task in crew_tasks:
            if hasattr(task, "output") and task.output:
                try:
                    results[task.agent.role.lower().replace(" ", "_") + "_output"] = task.output.value
                except:
                    results[task.agent.role.lower().replace(" ", "_") + "_output"] = str(task.output)
            else:
                results[task.agent.role.lower().replace(" ", "_") + "_output"] = "No output generated."

        results["final_crew_output"] = final_result

    except Exception as e:
        results["error"] = str(e)

    return results
