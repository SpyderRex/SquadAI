"""
This pipeline file includes two different examples to demonstrate the flexibility of squadAI pipelines.

Example 1: Two-Stage Pipeline
-----------------------------
This pipeline consists of two squads:
1. ResearchSquad: Performs research on a given topic.
2. WriteXSquad: Generates an X (Twitter) post based on the research findings.

Key features:
- The ResearchSquad's final task uses output_json to store all research findings in a JSON object.
- This JSON object is then passed to the WriteXSquad, where tasks can access the research findings.

Example 2: Two-Stage Pipeline with Parallel Execution
-------------------------------------------------------
This pipeline consists of three squads:
1. ResearchSquad: Performs research on a given topic.
2. WriteXSquad and WriteLinkedInSquad: Run in parallel, using the research findings to generate posts for X and LinkedIn, respectively.

Key features:
- Demonstrates the ability to run multiple squads in parallel.
- Shows how to structure a pipeline with both sequential and parallel stages.

Usage:
- To switch between examples, comment/uncomment the respective code blocks below.
- Ensure that you have implemented all necessary squad classes (ResearchSquad, WriteXSquad, WriteLinkedInSquad) before running.
"""

# Common imports for both examples
from squadai import Pipeline



# Uncomment the squads you need for your chosen example
from ..squads.research_squad.research_squad import ResearchSquad
from ..squads.write_x_squad.write_x_squad import WriteXSquad
# from .squads.write_linkedin_squad.write_linkedin_squad import WriteLinkedInSquad  # Uncomment for Example 2

# EXAMPLE 1: Two-Stage Pipeline
# -----------------------------
# Uncomment the following code block to use Example 1

class {{pipeline_name}}Pipeline:
    def __init__(self):
        # Initialize squads
        self.research_squad = ResearchSquad().squad()
        self.write_x_squad = WriteXSquad().squad()
    
    def create_pipeline(self):
        return Pipeline(
            stages=[
                self.research_squad,
                self.write_x_squad
            ]
        )
    
    async def kickoff(self, inputs):
        pipeline = self.create_pipeline()
        results = await pipeline.kickoff(inputs)
        return results


# EXAMPLE 2: Two-Stage Pipeline with Parallel Execution
# -------------------------------------------------------
# Uncomment the following code block to use Example 2

# @PipelineBase
# class {{pipeline_name}}Pipeline:
#     def __init__(self):
#         # Initialize squads
#         self.research_squad = ResearchSquad().squad()
#         self.write_x_squad = WriteXSquad().squad()
#         self.write_linkedin_squad = WriteLinkedInSquad().squad()
    
#     @pipeline
#     def create_pipeline(self):
#         return Pipeline(
#             stages=[
#                 self.research_squad,
#                 [self.write_x_squad, self.write_linkedin_squad]  # Parallel execution
#             ]
#         )

#     async def run(self, inputs):
#         pipeline = self.create_pipeline()
#         results = await pipeline.kickoff(inputs)
#         return results