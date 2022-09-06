"""Package containing suggestions for deployment component names."""
import re
from git import Repo, InvalidGitRepositoryError


def _validate_name(name: str) -> bool:
    # Validates a name
    assert re.match(r'[A-Za-z_]+', name).group(0) == name and len(name) > 3,\
        ('The name must be at least 3 characters long and only contain letters'
         'and underscores only.')


def _get_experiment_from_git() -> str:
    # Gets the current experiment from the git branch
    try:
        r = Repo()
    except InvalidGitRepositoryError:
        return ''
    branch = r.active_branch.name
    if branch.startswith('experiment/'):
        return branch.split('experiment/')[1]
    else:
        return ''


def get_experiment_name(project: str, experiment: str = None) -> str:
    """Gets a suggested experiment name from the current git branch.

    If the experiment name is not provided, it is obtained from the current
    git branch. If the current branch starts with 'experiment/', the name of
    the experiment is the part after 'experiment/'. Otherwise, an empty string
    is returned.

    Args:
        project (str): The project name.
        experiment (str): The experiment name. Defaults to None.

    Returns:
        str: The experiment name.
    """
    if experiment is None:
        experiment = _get_experiment_from_git()

    if experiment:
        experiment = f'{project}_{experiment}'
    else:
        experiment = project

    _validate_name(experiment)
    return experiment


def _parse_pipeline_name(pipeline: str) -> tuple:
    # Parses the pipeline name
    if pipeline == '__default__':
        pipeline = 'default'
    return pipeline


def _extract_raw_experiment(project: str, experiment: str) -> str:
    # Extracts the raw experiment name from the pipeline name
    return re.sub(f'^{project}_?', '', experiment)


def get_pipeline_name(
    project: str,
    pipeline: str = '__default__',
    experiment: str = None
) -> str:
    """Gets a suggested pipeline.

    It is the concatenation of the project name, the pipeline name and the
    experiment name. If the experiment name is not provided, it is obtained
    from the current git branch. If the pipeline name is not provided, it is
    set to 'default'.

    Args:
        project (str): The project name.
        pipeline (str): The pipeline name. Defaults to '__default__'.
        experiment (str): The experiment name. Defaults to None.

    Returns:
        str: '<project>_<pipeline>_<experiment>' or '<project>_<pipeline>'.
    """
    pipeline = _parse_pipeline_name(pipeline)
    pipeline = f'_{pipeline}'

    experiment = _extract_raw_experiment(project, experiment)
    if experiment:
        experiment = f'_{experiment}'

    pipeline = f'{project}{pipeline}{experiment}'
    _validate_name(pipeline)
    return pipeline