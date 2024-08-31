from squadai import Pipeline
from squadai.project import PipelineBase
from ..squads.classifier_squad.classifier_squad import ClassifierSquad


@PipelineBase
class EmailClassifierPipeline:
    def __init__(self):
        # Initialize squads
        self.classifier_squad = ClassifierSquad().squad()

    def create_pipeline(self):
        return Pipeline(
            stages=[
                self.classifier_squad
            ]
        )
    
    async def kickoff(self, inputs):
        pipeline = self.create_pipeline()
        results = await pipeline.kickoff(inputs)
        return results


