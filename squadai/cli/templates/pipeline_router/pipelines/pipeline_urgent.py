from squadai import Pipeline
from squadai.project import PipelineBase
from ..squads.urgent_squad.urgent_squad import UrgentSquad

@PipelineBase
class UrgentPipeline:
    def __init__(self):
        # Initialize squads
        self.urgent_squad = UrgentSquad().squad()
    
    def create_pipeline(self):
        return Pipeline(
            stages=[
                self.urgent_squad
            ]
        )
    
    async def kickoff(self, inputs):
        pipeline = self.create_pipeline()
        results = await pipeline.kickoff(inputs)
        return results


