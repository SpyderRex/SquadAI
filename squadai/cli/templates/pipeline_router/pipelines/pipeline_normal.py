from squadai import Pipeline
from squadai.project import PipelineBase
from ..squads.normal_squad.normal_squad import NormalSquad


@PipelineBase
class NormalPipeline:
    def __init__(self):
        # Initialize squads
        self.normal_squad = NormalSquad().squad()

    def create_pipeline(self):
        return Pipeline(
            stages=[
                self.normal_squad
            ]
        )
    
    async def kickoff(self, inputs):
        pipeline = self.create_pipeline()
        results = await pipeline.kickoff(inputs)
        return results


