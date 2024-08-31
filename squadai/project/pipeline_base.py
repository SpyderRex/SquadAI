from typing import Any, Callable, Dict, List, Type, Union

from squadai.squad import Squad
from squadai.pipeline.pipeline import Pipeline
from squadai.routers.router import Router

PipelineStage = Union[Squad, List[Squad], Router]


# TODO: Could potentially remove.
def PipelineBase(cls: Type[Any]) -> Type[Any]:
    class WrappedClass(cls):
        is_pipeline_class: bool = True  # type: ignore
        stages: List[PipelineStage]

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            super().__init__(*args, **kwargs)
            self.stages = []
            self._map_pipeline_components()

        def _get_all_functions(self) -> Dict[str, Callable[..., Any]]:
            return {
                name: getattr(self, name)
                for name in dir(self)
                if callable(getattr(self, name))
            }

        def _filter_functions(
            self, functions: Dict[str, Callable[..., Any]], attribute: str
        ) -> Dict[str, Callable[..., Any]]:
            return {
                name: func
                for name, func in functions.items()
                if hasattr(func, attribute)
            }

        def _map_pipeline_components(self) -> None:
            all_functions = self._get_all_functions()
            squad_functions = self._filter_functions(all_functions, "is_squad")
            router_functions = self._filter_functions(all_functions, "is_router")

            for stage_attr in dir(self):
                stage = getattr(self, stage_attr)
                if isinstance(stage, (Squad, Router)):
                    self.stages.append(stage)
                elif callable(stage) and hasattr(stage, "is_squad"):
                    self.stages.append(squad_functions[stage_attr]())
                elif callable(stage) and hasattr(stage, "is_router"):
                    self.stages.append(router_functions[stage_attr]())
                elif isinstance(stage, list) and all(
                    isinstance(item, Squad) for item in stage
                ):
                    self.stages.append(stage)

        def build_pipeline(self) -> Pipeline:
            return Pipeline(stages=self.stages)

    return WrappedClass
